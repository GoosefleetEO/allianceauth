from django.test import TestCase

from ...models import EveCharacter, EveCorporationInfo, EveAllianceInfo
from .. import dotlan, zkillboard, evewho
from ...templatetags import evelinks


class TestEveWho(TestCase):

    def test_alliance_url(self):
        self.assertEqual(
            evewho.alliance_url(12345678),
            'https://evewho.com/alliance/12345678'
        )
    
    def test_corporation_url(self):
        self.assertEqual(
            evewho.corporation_url(12345678),
            'https://evewho.com/corporation/12345678'
        )  

    def test_character_url(self):
        self.assertEqual(
            evewho.character_url(12345678),
            'https://evewho.com/character/12345678'
        )


class TestDotlan(TestCase):

    def test_alliance_url(self):
        self.assertEqual(
            dotlan.alliance_url('Wayne Enterprices'),
            'http://evemaps.dotlan.net/alliance/Wayne_Enterprices'
        )

    def test_corporation_url(self):
        self.assertEqual(
            dotlan.corporation_url('Wayne Technology'),
            'http://evemaps.dotlan.net/corp/Wayne_Technology'
        )
        self.assertEqual(
            dotlan.corporation_url('Crédit Agricole'),
            'http://evemaps.dotlan.net/corp/Cr%C3%A9dit_Agricole'
        )

    def test_region_url(self):
        self.assertEqual(
            dotlan.region_url('Black Rise'),
            'http://evemaps.dotlan.net/map/Black_Rise'
        )
    
    def test_solar_system_url(self):
        self.assertEqual(
            dotlan.solar_system_url('Jita'),
            'http://evemaps.dotlan.net/system/Jita'
        )


class TestZkillboard(TestCase):

    def test_alliance_url(self):
        self.assertEqual(
            zkillboard.alliance_url(12345678),
            'https://zkillboard.com/alliance/12345678/'
        )

    def test_corporation_url(self):
        self.assertEqual(
            zkillboard.corporation_url(12345678),
            'https://zkillboard.com/corporation/12345678/'
        )        

    def test_character_url(self):
        self.assertEqual(
            zkillboard.character_url(12345678),
            'https://zkillboard.com/character/12345678/'
        )
    

    def test_region_url(self):
        self.assertEqual(
            zkillboard.region_url(12345678),
            'https://zkillboard.com/region/12345678/'
        )

    def test_solar_system_url(self):
        self.assertEqual(
            zkillboard.solar_system_url(12345678),
            'https://zkillboard.com/system/12345678/'
        )

