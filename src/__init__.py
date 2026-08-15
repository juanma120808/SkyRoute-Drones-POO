# -*- coding: utf-8 -*-
"""
Paquete Principal SkyRoute (POO UDEM 2026-2)

Exporta las clases de dominio, utilidades geodésicas y excepciones.
"""

from .exceptions import (
    TelemetriaError,
    BateriaInvalidaError,
    AltitudInvalidaError,
    EstadoMotorInvalidoError,
    CoordenadaInvalidaError,
)
from .utils.geodesia import CalculadorGeodesico
from .telemetria import TelemetriaDrone

__all__ = [
    "TelemetriaDrone",
    "CalculadorGeodesico",
    "TelemetriaError",
    "BateriaInvalidaError",
    "AltitudInvalidaError",
    "EstadoMotorInvalidoError",
    "CoordenadaInvalidaError",
]
