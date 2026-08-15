# -*- coding: utf-8 -*-
"""
Módulo de Telemetría (SkyRoute)

Implementa la clase `TelemetriaDrone` con encapsulamiento estricto,
validaciones cruzadas de estado y delegación de cálculos geodésicos.
"""

from typing import Tuple, Set

from src.exceptions import (
    TelemetriaError,
    BateriaInvalidaError,
    AltitudInvalidaError,
    EstadoMotorInvalidoError,
    CoordenadaInvalidaError,
)
from src.utils.geodesia import CalculadorGeodesico


class TelemetriaDrone:
    """
    Encapsula y valida los datos de telemetría reportados en tiempo real por un dron.
    
    Aplica encapsulamiento estricto mediante `@property` y validación cruzada bidireccional
    entre la altitud del dron y el estado de sus motores.
    """
    BATERIA_MIN: float = 0.0
    BATERIA_MAX: float = 100.0
    ALTITUD_MIN: float = 0.0
    ALTITUD_MAX: float = 120.0  # Techo legal en metros
    
    ESTADOS_VALIDOS: Set[str] = {"APAGADOS", "STANDBY", "EN_VUELO", "EMERGENCIA"}

    def __init__(
        self,
        id_dron: str,
        bateria: float,
        altitud: float,
        estado_motores: str,
        coordenadas: Tuple[float, float]
    ) -> None:
        """
        Constructor de la telemetría del dron.
        Ejecuta la validación de rango y la validación cruzada de estado.
        """
        self._initialized: bool = False
        
        self.id_dron = id_dron
        self.bateria = bateria
        self._set_altitud_raw(altitud)
        self._set_estado_motores_raw(estado_motores)
        
        # Validación conjunta de coherencia operacional
        self._validar_coherencia_operacional(self._altitud, self._estado_motores)
        
        self.coordenadas = coordenadas
        self._initialized = True

    # ==========================================================================
    # VALIDACIONES AUXILIARES ATÓMICAS (Clean Code)
    # ==========================================================================

    @classmethod
    def _validar_coherencia_operacional(cls, altitud: float, estado_motores: str) -> None:
        """Valida la coherencia física entre la altitud y el estado del motor."""
        if altitud > 0.0 and estado_motores != "EN_VUELO":
            raise EstadoMotorInvalidoError(
                f"Incoherencia operacional: Con altitud {altitud}m > 0, "
                f"los motores DEBEN estar en 'EN_VUELO'. Recibido: '{estado_motores}'."
            )
        if altitud == 0.0 and estado_motores == "EN_VUELO":
            raise EstadoMotorInvalidoError(
                "Incoherencia operacional: Con altitud 0.0m (en tierra), "
                "los motores NO pueden estar 'EN_VUELO' (Use 'APAGADOS', 'STANDBY' o 'EMERGENCIA')."
            )

    def _set_altitud_raw(self, valor: object) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (float, int)):
            raise AltitudInvalidaError(f"La altitud debe ser un número real en metros. Recibido: {type(valor).__name__} ({valor})")
        valor_float = float(valor)
        if not (self.ALTITUD_MIN <= valor_float <= self.ALTITUD_MAX):
            raise AltitudInvalidaError(
                f"Altitud fuera de límites legales [{self.ALTITUD_MIN}m, {self.ALTITUD_MAX}m]. Recibido: {valor_float}m"
            )
        self._altitud = valor_float

    def _set_estado_motores_raw(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise EstadoMotorInvalidoError(f"El estado de motores debe ser texto. Recibido: {type(valor).__name__}")
        valor_upper = valor.strip().upper()
        if valor_upper not in self.ESTADOS_VALIDOS:
            raise EstadoMotorInvalidoError(
                f"Estado de motores no reconocido: '{valor}'. Estados válidos: {sorted(list(self.ESTADOS_VALIDOS))}"
            )
        self._estado_motores = valor_upper

    # ==========================================================================
    # PROPERTIES Y SETTERS (Encapsulamiento estricto y validación de mutación)
    # ==========================================================================

    @property
    def id_dron(self) -> str:
        """Identificador único alfanumérico del dron."""
        return self._id_dron

    @id_dron.setter
    def id_dron(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El ID del dron debe ser una cadena no vacía. Recibido: {repr(valor)}")
        self._id_dron = valor.strip()

    @property
    def bateria(self) -> float:
        """Nivel porcentual de batería [0.0 - 100.0]."""
        return self._bateria

    @bateria.setter
    def bateria(self, valor: object) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (float, int)):
            raise BateriaInvalidaError(f"El valor de batería debe ser un número real. Recibido: {type(valor).__name__} ({valor})")
        
        valor_float = float(valor)
        if not (self.BATERIA_MIN <= valor_float <= self.BATERIA_MAX):
            raise BateriaInvalidaError(
                f"Batería fuera de rango [{self.BATERIA_MIN}%, {self.BATERIA_MAX}%]. Recibido: {valor_float}%"
            )
        self._bateria = valor_float

    @property
    def altitud(self) -> float:
        """Altitud en metros sobre el nivel del suelo [0.0 - 120.0]."""
        return self._altitud

    @altitud.setter
    def altitud(self, valor: object) -> None:
        self._set_altitud_raw(valor)
        if getattr(self, "_initialized", False):
            self._validar_coherencia_operacional(self._altitud, self._estado_motores)

    @property
    def estado_motores(self) -> str:
        """Estado operativo de la planta motriz {'APAGADOS', 'STANDBY', 'EN_VUELO', 'EMERGENCIA'}."""
        return self._estado_motores

    @estado_motores.setter
    def estado_motores(self, valor: str) -> None:
        self._set_estado_motores_raw(valor)
        if getattr(self, "_initialized", False):
            self._validar_coherencia_operacional(self._altitud, self._estado_motores)

    @property
    def coordenadas(self) -> Tuple[float, float]:
        """Posición geográfica del dron como tupla (latitud, longitud)."""
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor: Tuple[float, float]) -> None:
        # Delega la validación completa en el módulo especializado de geodesia
        self._coordenadas = CalculadorGeodesico.validar_coordenada(valor)

    # ==========================================================================
    # MÉTODOS MÁGICOS (Dunder Methods)
    # ==========================================================================

    def __str__(self) -> str:
        """Representación visual amigable para la consola del operador de vuelo."""
        return (
            f"Dron[{self.id_dron}] - Bat: {self.bateria:.1f}% | "
            f"Alt: {self.altitud:.1f}m | Motores: {self.estado_motores} | "
            f"GPS: ({self.coordenadas[0]:.4f}, {self.coordenadas[1]:.4f})"
        )

    def __repr__(self) -> str:
        """Representación técnica sin ambigüedades para depuración y serialización."""
        return (
            f"TelemetriaDrone(id_dron='{self.id_dron}', bateria={self.bateria}, "
            f"altitud={self.altitud}, estado_motores='{self.estado_motores}', "
            f"coordenadas={self.coordenadas})"
        )

    # ==========================================================================
    # CÁLCULOS GEOGRÁFICOS (Delegación en CalculadorGeodesico)
    # ==========================================================================

    def calcular_distancia_a_punto(self, destino: Tuple[float, float]) -> float:
        """
        Calcula la distancia geodésica ortodrómica en kilómetros hacia un punto destino.
        Delega el cálculo al componente CalculadorGeodesico (Fórmula de Haversine).
        """
        return CalculadorGeodesico.calcular_haversine(self.coordenadas, destino)
