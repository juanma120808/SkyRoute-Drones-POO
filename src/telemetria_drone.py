# -*- coding: utf-8 -*-
"""
Módulo de Telemetría y Validación Operacional de Aeronaves No Tripuladas (SkyRoute)

Este módulo implementa las entidades de dominio y validaciones de la capa de 
telemetría para dispositivos aéreos no tripulados.
"""

import math 
from typing import Tuple, Set

# ==============================================================================
# EXCEPCIONES DE DOMINIO PERSONALIZADAS
# ==============================================================================

class TelemetriaError(ValueError):
    """Excepción base para errores de telemetría en aeronaves."""
    def __init__(self, message: str) -> None: 
        super().__init__(message)
        
class BateriaInvalidaError(TelemetriaError):
    """Lanzada cuando el nivel de batería está fuera del rango permitido [0.0, 100.0]."""
    def __init__(self, message: str) -> None:
        super().__init__(message)

class AltitudInvalidaError(TelemetriaError):
    """Lanzada cuando la altitud excede los límites regulatorios [0.0, 120.0]."""
    def __init__(self, message: str) -> None:
        super().__init__(message)

class EstadoMotorInvalidoError(TelemetriaError):
    """Lanzada cuando se asigna un estado de motor no reconocido o inconsistente con la altitud."""
    def __init__(self, message: str) -> None:
        super().__init__(message)

class CoordenadaInvalidaError(TelemetriaError):
    """Lanzada cuando las coordenadas geográficas son físicamente imposibles o tienen formatos incorrectos."""
    def __init__(self, message: str) -> None:
        super().__init__(message)

# ==============================================================================
# CLASE PRINCIPAL: TelemetriaDrone
# ==============================================================================

class TelemetriaDrone:
    """
    Encapsula y valida los datos de telemetría reportados en tiempo real por un dron.
    """
    # CONSTANTES DE NEGOCIO (Evita valores mágicos)
    BATERIA_MIN: float = 0.0
    BATERIA_MAX: float = 100.0
    ALTITUD_MIN: float = 0.0
    ALTITUD_MAX: float = 120.0
    
    ESTADOS_VALIDOS: Set[str] = {"APAGADOS", "STANDBY", "EN_VUELO", "EMERGENCIA"}
    
    RANGOS_LATITUD: Tuple[float, float] = (-90.0, 90.0)
    RANGOS_LONGITUD: Tuple[float, float] = (-180.0, 180.0)

    def __init__(
        self,
        id_dron: str,
        bateria: float,
        altitud: float,
        estado_motores: str,
        coordenadas: Tuple[float, float]
    ) -> None:
        """
        Inicializador de la telemetría del dron.
        Aplica las validaciones de negocio mediante setters en la instanciación.
        """
        self.id_dron = id_dron
        self.bateria = bateria
        self.altitud = altitud
        self.estado_motores = estado_motores
        self.coordenadas = coordenadas

    # ==========================================================================
    # PROPERTIES Y SETTERS (Encapsulamiento estricto)
    # ==========================================================================

    @property
    def id_dron(self) -> str:
        return self._id_dron

    @id_dron.setter
    def id_dron(self, valor: str) -> None: 
        if not valor.strip():
            raise ValueError("El ID del dron debe ser una cadena no vacía.")
        self._id_dron = valor

    @property
    def bateria(self) -> float:
        return self._bateria

    @bateria.setter
    def bateria(self, valor: object) -> None:
        if not isinstance(valor, (float, int)):
            raise BateriaInvalidaError(f"El valor de batería debe ser un número. Recibido: {valor}")
        if not (self.BATERIA_MIN <= valor <= self.BATERIA_MAX):
            raise BateriaInvalidaError(f"El valor de batería debe estar entre {self.BATERIA_MIN} y {self.BATERIA_MAX}. Recibido: {valor}")
        self._bateria = float(valor) 

    @property
    def altitud(self) -> float:
        return self._altitud

    @altitud.setter
    def altitud(self, valor: object) -> None:
        if not isinstance(valor, (float, int)):
            raise AltitudInvalidaError(f"La altitud debe ser un número. Recibido: {valor}")
        if not (self.ALTITUD_MIN <= valor <= self.ALTITUD_MAX):
            raise AltitudInvalidaError(f"La altitud debe estar entre {self.ALTITUD_MIN} y {self.ALTITUD_MAX}. Recibido: {valor}")
        self._altitud = float(valor)

    @property
    def estado_motores(self) -> str:
        return self._estado_motores

    @estado_motores.setter
    def estado_motores(self, valor: str) -> None:
        valor_upper = valor.upper()
        if valor_upper not in self.ESTADOS_VALIDOS:
            raise EstadoMotorInvalidoError(f"Estado de motores inválido: {valor}. Debe ser uno de {self.ESTADOS_VALIDOS}.")
        if self.altitud > 0.0 and valor_upper != "EN_VUELO":
            raise EstadoMotorInvalidoError(f"Con altitud {self.altitud}m, el estado de motores debe ser 'EN_VUELO'. Recibido: {valor_upper}.")
        if self.altitud == 0.0 and valor_upper == "EN_VUELO":
            raise EstadoMotorInvalidoError(f"Con altitud {self.altitud}m, el estado de motores no puede ser 'EN_VUELO'.")
        self._estado_motores = valor_upper

    @property
    def coordenadas(self) -> Tuple[float, float]:
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor: Tuple[float, float]) -> None: 
        if not isinstance(valor, tuple) or len(valor) != 2:
            raise CoordenadaInvalidaError(f"Las coordenadas deben ser una tupla de dos elementos (latitud, longitud). Recibido: {valor}")
        latitud, longitud = valor 
        if not (isinstance(latitud, (float, int)) and isinstance(longitud, (float, int))):
            raise CoordenadaInvalidaError(f"Latitud y longitud deben ser números. Recibido: {valor}")
        if not (self.RANGOS_LATITUD[0] <= latitud <= self.RANGOS_LATITUD[1]):
            raise CoordenadaInvalidaError(f"La latitud debe estar entre {self.RANGOS_LATITUD[0]} y {self.RANGOS_LATITUD[1]}. Recibido: {latitud}")
        if not (self.RANGOS_LONGITUD[0] <= longitud <= self.RANGOS_LONGITUD[1]):
            raise CoordenadaInvalidaError(f"La longitud debe estar entre {self.RANGOS_LONGITUD[0]} y {self.RANGOS_LONGITUD[1]}. Recibido: {longitud}")
        self._coordenadas = (float(latitud), float(longitud))

    # ==========================================================================
    # MÉTODOS MÁGICOS (Dunder Methods)
    # ==========================================================================

    def __str__(self) -> str:
        return f"Dron[{self.id_dron}] - Bat: {self.bateria:.1f}% | Alt: {self.altitud:.1f}m | Motores: {self.estado_motores}"

    def __repr__(self) -> str:
        return f"TelemetriaDrone('{self.id_dron}', {self.bateria:.1f}, {self.altitud:.1f}, '{self.estado_motores}', {self.coordenadas})"

    # ==========================================================================
    # CÁLCULOS GEOGRÁFICOS (Fórmula de Haversine)
    # ==========================================================================

    def calcular_distancia_a_punto(self, destino: Tuple[float, float]) -> float:
        """
        Calcula la distancia geodésica en kilómetros entre las coordenadas del dron
        y unas coordenadas de destino utilizando la fórmula de Haversine.
        """
        if not isinstance(destino, tuple) or len(destino) != 2:
            raise CoordenadaInvalidaError(f"El destino debe ser una tupla de dos elementos (latitud, longitud). Recibido: {destino}")
        latitud_destino, longitud_destino = destino
        if not (isinstance(latitud_destino, (float, int)) and isinstance(longitud_destino, (float, int))):
            raise CoordenadaInvalidaError(f"Latitud y longitud del destino deben ser números. Recibido: {destino}")

        lat1, lon1 = self.coordenadas
        lat2, lon2 = latitud_destino, longitud_destino

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0  # Radio de la Tierra en kilómetros
        return r * c


# ==============================================================================
# VERIFICACIÓN DE FUNCIONALIDAD
# ==============================================================================

if __name__ == "__main__":
    print("Ejecutando verificaciones del modulo de telemetria...")
    
    try:
        dron = TelemetriaDrone(
            id_dron="DRN-X100",
            bateria=95.4,
            altitud=15.5,
            estado_motores="EN_VUELO",
            coordenadas=(4.7110, -74.0721)
        )
        print(f"[OK] Instanciacion correcta: {dron}")
        
        coordenadas_medellin = (6.2518, -75.5636)
        dist = dron.calcular_distancia_a_punto(coordenadas_medellin)
        print(f"[OK] Distancia a Medellin: {dist:.2f} km")
    except Exception as e:
        print(f"[ERROR] Durante verificacion: {e}")

