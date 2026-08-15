# -*- coding: utf-8 -*-
"""
Módulo de Utilidades Geodésicas (SkyRoute)

Proporciona funciones y métodos estáticos para validación de coordenadas
y cálculo de distancias ortodrómicas utilizando la fórmula de Haversine.
"""

import math
from typing import Tuple
from src.exceptions import CoordenadaInvalidaError


class CalculadorGeodesico:
    """
    Calculador matemático para navegación y trigonometría esférica.
    """
    RADIO_TIERRA_KM: float = 6371.0
    RANGOS_LATITUD: Tuple[float, float] = (-90.0, 90.0)
    RANGOS_LONGITUD: Tuple[float, float] = (-180.0, 180.0)

    @classmethod
    def validar_coordenada(cls, coordenada: Tuple[float, float]) -> Tuple[float, float]:
        """
        Valida que una coordenada sea una tupla de dos flotantes dentro de los rangos legales.
        
        Retorna:
            Tuple[float, float]: Coordenada normalizada en flotantes.
            
        Lanza:
            CoordenadaInvalidaError: Si el tipo, formato o rango es incorrecto.
        """
        if not isinstance(coordenada, tuple) or len(coordenada) != 2:
            raise CoordenadaInvalidaError(
                f"La coordenada debe ser una tupla de exactamente 2 elementos (latitud, longitud). Recibido: {coordenada}"
            )

        lat, lon = coordenada
        if isinstance(lat, bool) or isinstance(lon, bool) or \
           not isinstance(lat, (float, int)) or not isinstance(lon, (float, int)):
            raise CoordenadaInvalidaError(
                f"Latitud y longitud deben ser números reales (float o int). Recibido: {coordenada}"
            )

        lat_float, lon_float = float(lat), float(lon)
        if not (cls.RANGOS_LATITUD[0] <= lat_float <= cls.RANGOS_LATITUD[1]):
            raise CoordenadaInvalidaError(
                f"Latitud {lat_float} fuera de rango permitido [{cls.RANGOS_LATITUD[0]}, {cls.RANGOS_LATITUD[1]}]."
            )
        if not (cls.RANGOS_LONGITUD[0] <= lon_float <= cls.RANGOS_LONGITUD[1]):
            raise CoordenadaInvalidaError(
                f"Longitud {lon_float} fuera de rango permitido [{cls.RANGOS_LONGITUD[0]}, {cls.RANGOS_LONGITUD[1]}]."
            )

        return (lat_float, lon_float)

    @classmethod
    def calcular_haversine(
        cls,
        origen: Tuple[float, float],
        destino: Tuple[float, float]
    ) -> float:
        """
        Calcula la distancia geodésica en kilómetros entre dos pares de coordenadas
        utilizando la fórmula de Haversine.
        """
        lat1, lon1 = cls.validar_coordenada(origen)
        lat2, lon2 = cls.validar_coordenada(destino)

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2.0) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2.0) ** 2
        )
        c = 2.0 * math.asin(math.sqrt(a))
        return cls.RADIO_TIERRA_KM * c
