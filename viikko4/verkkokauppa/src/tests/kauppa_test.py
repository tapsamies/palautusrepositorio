import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):

    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())

        # palautetaan aina arvo 42

        self.varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "käpylehmä", 3)
            if tuote_id == 3:
                return Tuote(3, "golf-osake", 200000)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(
            self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock
        )

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

    def test_laitetaan_kaksi_eri_riittoisaa_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("antsa", "54321")

        self.pankki_mock.tilisiirto.assert_called_with(
            "antsa", ANY, "54321", "33333-44455", 8
        )

    def test_laitetaan_kaksi_samaa_riittoisaa_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("jarppa", "33333")
        self.pankki_mock.tilisiirto.assert_called_with(
            "jarppa", ANY, "33333", "33333-44455", 10
        )

    def test_ostetaan_olevaa_ja_olematonta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("juhani", "123123")
        self.pankki_mock.tilisiirto.assert_called_with(
            "juhani", ANY, "123123", "33333-44455", 5
        )

    def test_aloita_asiointi_toimii(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("juhani", "123123")
        self.pankki_mock.tilisiirto.assert_called_with(ANY, ANY, ANY, ANY, 0)

    def test_viite_toimii(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("juhani", "123123")
        self.pankki_mock.tilisiirto.assert_called_with(
            "juhani", ANY, "123123", "33333-44455", 5
        )
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("jani", "123123")
        self.pankki_mock.tilisiirto.assert_called_with(
            "jani", 3, "123123", "33333-44455", 5
        )
