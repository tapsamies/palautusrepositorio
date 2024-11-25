import unittest
from varasto import Varasto
from tuote import Tuote


class TestVarasto(unittest.TestCase):

    def setUp(self):
        self.varasto = Varasto()
        self.tuote = Tuote(1, "Koff", 3)

    def test_varaston_tuotteet_haetaan(self):
        self.assertEqual(self.varasto.hae_tuote(1), Tuote(1, "Koff", 3))

    def test_varastossa_olematon_tuote_palauttaa_none(self):
        self.assertIs(self.varasto.hae_tuote(22), None)

    def test_saldo_toimii_kuten_luokka_ohjaa(self):
        self.assertEqual(self.varasto.saldo(1), 100)

    def test_varastosta_ottaminen_miinustaa(self):
        self.varasto.ota_varastosta(self.varasto.hae_tuote(1))
        self.assertEqual(self.varasto.saldo(1), 99)

    def test_varastoon_voi_palauttaa(self):
        self.varasto.ota_varastosta(self.varasto.hae_tuote(1))
        self.assertEqual(self.varasto.saldo(1), 99)
        self.varasto.palauta_varastoon(self.varasto.hae_tuote(1))
        self.assertEqual(self.varasto.saldo(1), 100)
