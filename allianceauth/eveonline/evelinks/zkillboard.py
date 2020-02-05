# this module generates profile URLs for zKillboard

from urllib.parse import urljoin, quote

from . import *

BASE_URL = 'https://zkillboard.com'


def _build_url(category: str, eve_id: int) -> str:
    """return url to profile page for an eve entity"""
    
    if category == ESI_CATEGORY_ALLIANCE:        
        partial = 'alliance'

    elif category == ESI_CATEGORY_CORPORATION:        
        partial = 'corporation'

    elif category == ESI_CATEGORY_CHARACTER:
        partial = 'character'

    elif category == ESI_CATEGORY_REGION:
        partial = 'region'

    elif category == ESI_CATEGORY_SOLARSYSTEM:
        partial = 'system'
    
    else:
        raise NotImplementedError(
            "Not implemented yet for category:" + category
        )
    
    url = urljoin(
        BASE_URL,
        '{}/{}/'.format(partial, int(eve_id))
    )
    return url


def alliance_url(eve_id: int) -> str:
    """url for page about given alliance on zKillboard"""
    return _build_url(ESI_CATEGORY_ALLIANCE, eve_id)

def character_url(eve_id: int) -> str:
    """url for page about given character on zKillboard"""
    return _build_url(ESI_CATEGORY_CHARACTER, eve_id)

def corporation_url(eve_id: int) -> str:
    """url for page about given corporation on zKillboard"""
    return _build_url(ESI_CATEGORY_CORPORATION, eve_id)

def region_url(eve_id: int) -> str:
    """url for page about given region on zKillboard"""
    return _build_url(ESI_CATEGORY_REGION, eve_id)

def solar_system_url(eve_id: int) -> str:
    return _build_url(ESI_CATEGORY_SOLARSYSTEM, eve_id)