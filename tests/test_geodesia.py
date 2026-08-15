# -*- coding: utf-8 -*-
"""
Pruebas Unitarias para el Módulo de Geodesia y Cálculo Haversine (SkyRoute)
"""

import unittest
from src.utils.geodesia import CalculadorGeodesico
from src.exceptions import CoordenadaInvalidaError


class TestCalculadorGeodesico(unittest.TestCase):
    """Casos de prueba para validación de coordenadas y cálculo de distancias."""

    def test_coordenada_valida(self):
        """Verifica la normalización correcta de coordenadas válidas."""
        coord = CalculadorGeodesico.validar_coordenada((6.2518, -75.5636))
        self.assertEqual(coord, (6.2518, -75.5636))

    def test_coordenada_tipo_invalido(self):
        """Rechaza tipos de datos no tupla o con longitud distinta de 2."""
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada([6.25, -75.56]) # type: ignore
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((6.25,)) # type: ignore

    def test_coordenada_rechazo_booleano(self):
        """Previene que valores booleanos pasen como números reales."""
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((True, -75.56)) # type: ignore
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((6.25, False)) # type: ignore

    def test_coordenada_fuera_de_rango(self):
        """Rechaza latitudes fuera de [-90, 90] y longitudes fuera de [-180, 180]."""
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((95.0, -75.0))
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((-95.0, -75.0))
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((6.0, 185.0))
        with self.assertRaises(CoordenadaInvalidaError):
            CalculadorGeodesico.validar_coordenada((6.0, -185.0))

    def test_calculo_haversine_medellin_bogota(self):
        """Verifica la precisión de Haversine para Medellín -> Bogotá (~238 km)."""
        medellin = (6.2518, -75.5636)
        bogota = (4.7110, -74.0721)
        distancia = CalculadorGeodesico.calcular_haversine(medellin, bogota)
        # La distancia real ortodrómica es de ~237.9 km
        self.assertAlmostEqual(distancia, 237.9, delta=5.0)

    def test_calculo_haversine_mismo_punto(self):
        """La distancia entre un punto y sí mismo debe ser 0.0 km."""
        punto = (6.2518, -75.5636)
        distancia = CalculadorGeodesico.calcular_haversine(punto, punto)
        self.assertAlmostEqual(distancia, 0.0, places=4)


if __name__ == "__main__":
    unittest.main()
