import logging

from celery import shared_task
from .models import EveAllianceInfo
from .models import EveCharacter
from .models import EveCorporationInfo

logger = logging.getLogger(__name__)

TASK_PRIORITY = 7

@shared_task
def update_corp(corp_id):
    EveCorporationInfo.objects.update_corporation(corp_id)


@shared_task
def update_alliance(alliance_id):
    EveAllianceInfo.objects.update_alliance(alliance_id).populate_alliance()


@shared_task
def update_character(character_id):
    EveCharacter.objects.update_character(character_id)


@shared_task
def run_model_update():
    # update existing corp models
    for corp in EveCorporationInfo.objects.all().values('corporation_id'):
        update_corp.apply_async(args=[corp['corporation_id']], priority=TASK_PRIORITY)

    # update existing alliance models
    for alliance in EveAllianceInfo.objects.all().values('alliance_id'):
        update_alliance.apply_async(args=[alliance['alliance_id']], priority=TASK_PRIORITY)

    #update existing character models
    for character in EveCharacter.objects.all().values('character_id'):
        update_character.apply_async(args=[character['character_id']], priority=TASK_PRIORITY)
