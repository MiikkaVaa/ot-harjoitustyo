import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)
        self.kortti2 = Maksukortti(100)

    def test_uudessa_paatteessa_oikea_maara_rahaa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_uudessa_paatteessa_oikea_maara_edullisia_lounaita(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_uudessa_paatteessa_oikea_maara_maukkaita_lounaita(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kateisosto_edullinen_kasvattaa_kassaa_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
    
    def test_kateisosto_maukas_kasvattaa_kassaa_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
    
    def test_kateisosto_edullinen_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)
    
    def test_kateisosto_maukas_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
    
    def test_kateisosto_edullinen_rahat_ei_riita_rahat_palautuu(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)
    
    def test_kateisosto_maukas_rahat_ei_riita_rahat_palautuu(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
    
    def test_kateisosto_edullinen_rahat_ei_riita_kassassa_ei_muutosta(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kateisosto_maukas_rahat_ei_riita_kassassa_ei_muutosta(self):
        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kateisosto_edullinen_kasvattaa_edullisten_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_kateisosto_maukas_kasvattaa_maukkaiden_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_korttiosto_edullinen_veloittaa_summan_oikein(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.  kortti.saldo, 760)
    
    def test_korttiosto_maukas_veloittaa_summan_oikein(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 600)
    
    def test_korttiosto_edullinen_onnistuu_kun_rahaa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)
    
    def test_korttiosto_maukas_onnistuu_kun_rahaa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)
    
    def test_korttiosto_edullinen_kasvattaa_edullisten_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_korttiosto_maukas_kasvattaa_maukkaiden_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_korttiosto_edullinen_ei_onnistu_kun_raha_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti2), False)

    def test_korttiosto_maukas_ei_onnistu_kun_raha_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti2), False)
    
    def test_korttiosto_edullinen_ei_muuta_kortin_rahamaaraa_jos_ei_onnistu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti2)
        self.assertEqual(self.kortti2.saldo, 100)
    
    def test_korttiosto_maukas_ei_muuta_kortin_rahamaaraa_jos_ei_onnistu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti2)
        self.assertEqual(self.kortti2.saldo, 100)
    
    def test_korttiosto_edullinen_ei_muuta_lounaiden_maaraa_jos_ei_onnistu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti2)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_korttiosto_maukas_ei_muuta_lounaiden_marraa_jos_ei_onnistu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti2)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kassassa_oleva_rahamaara_ei_muutu_kortilla_maksaessa_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kassassa_oleva_rahamaara_ei_muutu_kortilla_maksaessa_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortille_rahaa_ladattaessa_kortin_saldo_muuttuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
    
    def test_kassan_rahamaara_kasvaa_kortille_rahaa_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_kortille_negatiivinen_maara_rahaa_ei_muuta_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 1000)

    def test_kassan_rahamaara_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)



    

    
