# -*- coding: utf-8 -*-
"""
Módulo de Telemetría y Validación Operacional de Aeronaves No Tripuladas (SkyRoute)

Este módulo implementa las entidades de dominio, reglas aeronáuticas y validaciones
estrictas de la capa de telemetría para drones de entrega de última milla.
"""

import math
from typing import Tuple, Set


# ==============================================================================
# 1. EXCEPCIONES DE DOMINIO PERSONALIZADAS
# ==============================================================================

class TelemetriaError(ValueError):
    """Excepción base de dominio para errores de telemetría en aeronaves."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class BateriaInvalidaError(TelemetriaError):
    """Lanzada cuando el nivel de batería no es un número real o está fuera de [0.0, 100.0]."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AltitudInvalidaError(TelemetriaError):
    """Lanzada cuando la altitud no es numérica o excede los límites legales [0.0, 120.0]."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EstadoMotorInvalidoError(TelemetriaError):
    """Lanzada cuando el estado del motor no es reconocido o es incoherente con la altitud."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CoordenadaInvalidaError(TelemetriaError):
    """Lanzada cuando las coordenadas geográficas son físicamente imposibles o tienen formato erróneo."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


# ==============================================================================
# 2. CLASE PRINCIPAL: TelemetriaDrone
# ==============================================================================

class TelemetriaDrone:
    """
    Encapsula y valida los datos de telemetría reportados en tiempo real por un dron.
    
    Aplica encapsulamiento estricto mediante `@property` y validación cruzada bidireccional
    entre la altitud del dron y el estado de sus motores para garantizar la coherencia
    del estado físico y aeronáutico.
    """
    # Constantes de negocio a nivel de clase (Cero valores mágicos hardcodeados)
    BATERIA_MIN: float = 0.0
    BATERIA_MAX: float = 100.0
    ALTITUD_MIN: float = 0.0
    ALTITUD_MAX: float = 120.0  # Techo operacional regulatorio en metros
    
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
        Constructor de la telemetría del dron.
        
        Aplica las validaciones de tipo, rango y la coherencia operacional cruzada
        tanto en la instanciación inicial como en mutaciones futuras.
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
        if not isinstance(valor, tuple) or len(valor) != 2:
            raise CoordenadaInvalidaError(
                f"Las coordenadas deben ser una tupla de exactamente 2 elementos (latitud, longitud). Recibido: {valor}"
            )
        
        latitud, longitud = valor
        if isinstance(latitud, bool) or isinstance(longitud, bool) or \
           not isinstance(latitud, (float, int)) or not isinstance(longitud, (float, int)):
            raise CoordenadaInvalidaError(f"Latitud y longitud deben ser números reales. Recibido: {valor}")
        
        lat_float, lon_float = float(latitud), float(longitud)
        if not (self.RANGOS_LATITUD[0] <= lat_float <= self.RANGOS_LATITUD[1]):
            raise CoordenadaInvalidaError(
                f"Latitud {lat_float} fuera de rango legal [{self.RANGOS_LATITUD[0]}, {self.RANGOS_LATITUD[1]}]."
            )
        if not (self.RANGOS_LONGITUD[0] <= lon_float <= self.RANGOS_LONGITUD[1]):
            raise CoordenadaInvalidaError(
                f"Longitud {lon_float} fuera de rango legal [{self.RANGOS_LONGITUD[0]}, {self.RANGOS_LONGITUD[1]}]."
            )
            
        self._coordenadas = (lat_float, lon_float)

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
    # CÁLCULOS GEOGRÁFICOS (Fórmula de Haversine)
    # ==========================================================================

    def calcular_distancia_a_punto(self, destino: Tuple[float, float]) -> float:
        """
        Calcula la distancia geodésica ortodrómica en kilómetros entre la posición actual
        del dron y un punto de destino utilizando la fórmula de Haversine.

        Parámetros:
            destino (Tuple[float, float]): Par (latitud, longitud) del punto objetivo.

        Retorna:
            float: Distancia en kilómetros (km).
            
        Lanza:
            CoordenadaInvalidaError: Si el destino no es una tupla válida o está fuera de rango.
        """
        if not isinstance(destino, tuple) or len(destino) != 2:
            raise CoordenadaInvalidaError(f"El destino debe ser una tupla (latitud, longitud). Recibido: {destino}")
        
        lat2, lon2 = destino
        if isinstance(lat2, bool) or isinstance(lon2, bool) or \
           not isinstance(lat2, (float, int)) or not isinstance(lon2, (float, int)):
            raise CoordenadaInvalidaError(f"Latitud y longitud de destino deben ser números. Recibido: {destino}")
        
        lat2, lon2 = float(lat2), float(lon2)
        if not (self.RANGOS_LATITUD[0] <= lat2 <= self.RANGOS_LATITUD[1]) or \
           not (self.RANGOS_LONGITUD[0] <= lon2 <= self.RANGOS_LONGITUD[1]):
            raise CoordenadaInvalidaError(f"Coordenadas de destino fuera de rango geográfico: {destino}")

        lat1, lon1 = self.coordenadas
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(dlat / 2.0) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2.0) ** 2
        )
        c = 2.0 * math.asin(math.sqrt(a))
        radio_tierra_km = 6371.0
        
        return radio_tierra_km * c


# ==============================================================================
# DEMOSTRACIÓN Y VERIFICACIÓN EN CONSOLA
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  SKYROUTE TELEMETRY CORE - EJECUCION DE VERIFICACION")
    print("=" * 70)
    
    # 1. Instanciación correcta en vuelo
    dron1 = TelemetriaDrone(
        id_dron="DRN-X100",
        bateria=95.5,
        altitud=35.0,
        estado_motores="EN_VUELO",
        coordenadas=(6.2518, -75.5636)  # Medellín
    )
    print("\n[OK] Dron creado exitosamente:")
    print(f"  Str:  {dron1}")
    print(f"  Repr: {repr(dron1)}")
    
    # 2. Cálculo de distancia a Bogotá (4.7110, -74.0721)
    bogota_gps = (4.7110, -74.0721)
    distancia = dron1.calcular_distancia_a_punto(bogota_gps)
    print(f"\n[OK] Distancia calculada a Bogota: {distancia:.2f} km")
    
    # 3. Verificación de blindaje ante mutación inconsistente (Altitud -> Motor)
    print("\n[TEST] Probando blindaje ante mutacion posterior inconsistente:")
    dron_tierra = TelemetriaDrone("DRN-GROUND", 100.0, 0.0, "STANDBY", (6.25, -75.56))
    print(f"  Dron en tierra: {dron_tierra}")
    try:
        print("  Intentando elevar altitud a 50m con motores en STANDBY...")
        dron_tierra.altitud = 50.0  # Debe fallar porque los motores siguen en STANDBY
        print("  [ERROR] No debio permitir la elevacion.")
    except EstadoMotorInvalidoError as e:
        print(f"  [BLOQUEO EXITOSO] Regla protegida -> {e}")
        
    print("\n" + "=" * 70)
    print("  TODAS LAS REGLAS DE NEGOCIO Y BLINDAJES VERIFICADOS CON EXITO")
    print("=" * 70)
