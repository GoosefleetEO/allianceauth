from unittest.mock import patch

from django.test import TestCase

from ..models import EveCharacter, EveCorporationInfo, EveAllianceInfo
from ..tasks import (
    update_alliance, 
    update_corp, 
    update_character, 
    run_model_update
)


class TestTasks(TestCase):

    @patch('allianceauth.eveonline.tasks.EveCorporationInfo')
    def test_update_corp(self, mock_EveCorporationInfo):
        update_corp(42)
        self.assertEqual(
            mock_EveCorporationInfo.objects.update_corporation.call_count, 1
        )
        self.assertEqual(
            mock_EveCorporationInfo.objects.update_corporation.call_args[0][0], 42
        )
            
    @patch('allianceauth.eveonline.tasks.EveAllianceInfo')
    def test_update_alliance(self, mock_EveAllianceInfo):
        update_alliance(42)
        self.assertEqual(
            mock_EveAllianceInfo.objects.update_alliance.call_args[0][0], 42
        )
        self.assertEqual(
            mock_EveAllianceInfo.objects
            .update_alliance.return_value.populate_alliance.call_count, 1
        )

    @patch('allianceauth.eveonline.tasks.EveCharacter')
    def test_update_character(self, mock_EveCharacter):
        update_character(42)
        self.assertEqual(
            mock_EveCharacter.objects.update_character.call_count, 1
        )
        self.assertEqual(
            mock_EveCharacter.objects.update_character.call_args[0][0], 42
        )

    @patch('allianceauth.eveonline.tasks.update_character')
    @patch('allianceauth.eveonline.tasks.update_alliance')
    @patch('allianceauth.eveonline.tasks.update_corp')
    def test_run_model_update(
        self,
        mock_update_corp,
        mock_update_alliance,
        mock_update_character,
    ):
        EveCorporationInfo.objects.all().delete()
        EveAllianceInfo.objects.all().delete()
        EveCharacter.objects.all().delete()

        EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name='corp.name',
            corporation_ticker='corp.ticker',
            member_count=10,
            alliance=None,
        )
        EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name='alliance.name',
            alliance_ticker='alliance.ticker',
            executor_corp_id='78910',
        )
        EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='c.c.t',  # max 5 chars 
            alliance_id=3456,
            alliance_name='character.alliance.name',
        )

        run_model_update()

        self.assertEqual(mock_update_corp.apply_async.call_count, 1)
        self.assertEqual(
            int(mock_update_corp.apply_async.call_args[1]['args'][0]), 2345
        )
        
        self.assertEqual(mock_update_alliance.apply_async.call_count, 1)
        self.assertEqual(
            int(mock_update_alliance.apply_async.call_args[1]['args'][0]), 3456
        )
        
        self.assertEqual(mock_update_character.apply_async.call_count, 1)
        self.assertEqual(
            int(mock_update_character.apply_async.call_args[1]['args'][0]), 1234
        )
