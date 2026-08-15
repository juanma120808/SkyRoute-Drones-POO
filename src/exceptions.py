# -*- coding: utf-8 -*-
"""
Módulo de Excepciones de Dominio (SkyRoute)

Define la jerarquía de errores de negocio para el subsistema de telemetría
y navegación de drones. Heredan de ValueError para integrarse naturalmente
con los estándares de validación de Python.
"""

class TelemetriaError(ValueError):
    """Excepción base de dominio para errores operacionales y de telemetría."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class BateriaInvalidaError(TelemetriaError):
    """Lanzada cuando el nivel de batería no es un número real o está fuera del rango [0.0, 100.0]%."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AltitudInvalidaError(TelemetriaError):
    """Lanzada cuando la altitud no es numérica o supera el techo operacional permitido [0.0, 120.0]m."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EstadoMotorInvalidoError(TelemetriaError):
    """Lanzada cuando el estado de motores es desconocido o físicamente inconsistente con la altitud."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CoordenadaInvalidaError(TelemetriaError):
    """Lanzada cuando un par de coordenadas geográficas posee formato o rangos inválidos."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
