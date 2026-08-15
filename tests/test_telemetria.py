# -*- coding: utf-8 -*-
"""
Pruebas Unitarias para el Core de Telemetría (SkyRoute)
"""

import unittest
from src.telemetria import TelemetriaDrone
from src.exceptions import (
    BateriaInvalidaError,
    AltitudInvalidaError,
    EstadoMotorInvalidoError,
    CoordenadaInvalidaError,
)


class TestTelemetriaDrone(unittest.TestCase):
    """Casos de prueba para validaciones de negocio de TelemetriaDrone."""

    def setUp(self):
        """Instancia base válida de dron en vuelo."""
        self.dron_vuelo = TelemetriaDrone(
            id_dron="DRN-TEST-1",
            bateria=85.0,
            altitud=40.0,
            estado_motores="EN_VUELO",
            coordenadas=(6.2518, -75.5636)
        )

        self.dron_tierra = TelemetriaDrone(
            id_dron="DRN-TEST-2",
            bateria=100.0,
            altitud=0.0,
            estado_motores="STANDBY",
            coordenadas=(6.2518, -75.5636)
        )

    # --------------------------------------------------------------------------
    # 1. Validaciones de Identificador
    # --------------------------------------------------------------------------
    def test_id_dron_valido(self):
        self.assertEqual(self.dron_vuelo.id_dron, "DRN-TEST-1")

    def test_id_dron_invalido_cadena_vacia(self):
        with self.assertRaises(ValueError):
            TelemetriaDrone("", 50.0, 0.0, "STANDBY", (6.0, -75.0))
        with self.assertRaises(ValueError):
            TelemetriaDrone("   ", 50.0, 0.0, "STANDBY", (6.0, -75.0))

    # --------------------------------------------------------------------------
    # 2. Validaciones de Batería
    # --------------------------------------------------------------------------
    def test_bateria_limites_validos(self):
        dron_min = TelemetriaDrone("D-MIN", 0.0, 0.0, "APAGADOS", (6.0, -75.0))
        dron_max = TelemetriaDrone("D-MAX", 100.0, 0.0, "APAGADOS", (6.0, -75.0))
        self.assertEqual(dron_min.bateria, 0.0)
        self.assertEqual(dron_max.bateria, 100.0)

    def test_bateria_fuera_de_rango(self):
        with self.assertRaises(BateriaInvalidaError):
            TelemetriaDrone("D-ERR", -0.1, 0.0, "APAGADOS", (6.0, -75.0))
        with self.assertRaises(BateriaInvalidaError):
            TelemetriaDrone("D-ERR", 100.1, 0.0, "APAGADOS", (6.0, -75.0))

    def test_bateria_rechazo_booleano(self):
        with self.assertRaises(BateriaInvalidaError):
            TelemetriaDrone("D-ERR", True, 0.0, "APAGADOS", (6.0, -75.0)) # type: ignore

    # --------------------------------------------------------------------------
    # 3. Validaciones de Altitud
    # --------------------------------------------------------------------------
    def test_altitud_limites_validos(self):
        dron_tierra = TelemetriaDrone("D-GND", 50.0, 0.0, "STANDBY", (6.0, -75.0))
        dron_techo = TelemetriaDrone("D-MAX", 50.0, 120.0, "EN_VUELO", (6.0, -75.0))
        self.assertEqual(dron_tierra.altitud, 0.0)
        self.assertEqual(dron_techo.altitud, 120.0)

    def test_altitud_fuera_de_rango(self):
        with self.assertRaises(AltitudInvalidaError):
            TelemetriaDrone("D-ERR", 50.0, -1.0, "STANDBY", (6.0, -75.0))
        with self.assertRaises(AltitudInvalidaError):
            TelemetriaDrone("D-ERR", 50.0, 120.1, "EN_VUELO", (6.0, -75.0))

    def test_altitud_rechazo_booleano(self):
        with self.assertRaises(AltitudInvalidaError):
            TelemetriaDrone("D-ERR", 50.0, False, "STANDBY", (6.0, -75.0)) # type: ignore

    # --------------------------------------------------------------------------
    # 4. Coherencia Operacional Cruzada (Altitud vs Motores)
    # --------------------------------------------------------------------------
    def test_incoherencia_inicial_altitud_positiva_con_motores_no_vuelo(self):
        """Si altitud > 0, los motores NO pueden ser APAGADOS ni STANDBY."""
        with self.assertRaises(EstadoMotorInvalidoError):
            TelemetriaDrone("D-ERR", 50.0, 20.0, "STANDBY", (6.0, -75.0))
        with self.assertRaises(EstadoMotorInvalidoError):
            TelemetriaDrone("D-ERR", 50.0, 20.0, "APAGADOS", (6.0, -75.0))

    def test_incoherencia_inicial_altitud_cero_con_motores_en_vuelo(self):
        """Si altitud == 0, los motores NO pueden ser EN_VUELO."""
        with self.assertRaises(EstadoMotorInvalidoError):
            TelemetriaDrone("D-ERR", 50.0, 0.0, "EN_VUELO", (6.0, -75.0))

    def test_blindaje_mutacion_posterior_altitud(self):
        """Mutar la altitud a > 0 cuando los motores están en STANDBY debe fallar."""
        with self.assertRaises(EstadoMotorInvalidoError):
            self.dron_tierra.altitud = 30.0

    def test_blindaje_mutacion_posterior_motores(self):
        """Mutar motores a APAGADOS cuando la altitud es 40m debe fallar."""
        with self.assertRaises(EstadoMotorInvalidoError):
            self.dron_vuelo.estado_motores = "APAGADOS"

    # --------------------------------------------------------------------------
    # 5. Métodos Dunder y Delegación
    # --------------------------------------------------------------------------
    def test_representacion_str_y_repr(self):
        str_out = str(self.dron_vuelo)
        repr_out = repr(self.dron_vuelo)
        self.assertIn("DRN-TEST-1", str_out)
        self.assertIn("EN_VUELO", str_out)
        self.assertIn("TelemetriaDrone", repr_out)

    def test_delegacion_calculo_distancia(self):
        bogota = (4.7110, -74.0721)
        dist = self.dron_vuelo.calcular_distancia_a_punto(bogota)
        self.assertAlmostEqual(dist, 237.9, delta=5.0)


if __name__ == "__main__":
    unittest.main()
