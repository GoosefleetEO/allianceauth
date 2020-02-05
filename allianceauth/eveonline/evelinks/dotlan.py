# this module generates profile URLs for dotlan

from urllib.parse import urljoin, quote

from . import *

BASE_URL = 'http://evemaps.dotlan.net'


def _build_url(category: str, name: str) -> str:
    """return url to profile page for an eve entity"""
    
    if category == ESI_CATEGORY_ALLIANCE:        
        partial = 'alliance'

    elif category == ESI_CATEGORY_CORPORATION:        
        partial = 'corp'

    elif category == ESI_CATEGORY_REGION:
        partial = 'map'
    
    elif category == ESI_CATEGORY_SOLARSYSTEM:
        partial = 'system'
    
    else:
        raise NotImplementedError(
            "Not implemented yet for category:" + category
        )
        
    url = urljoin(
        BASE_URL,
        '{}/{}'.format(partial, quote(str(name).replace(" ", "_")))
        
    )
    return url


def alliance_url(name: str) -> str:
    """url for page about given alliance on dotlan"""
    return _build_url(ESI_CATEGORY_ALLIANCE, name)

def corporation_url(name: str) -> str:
    """url for page about given corporation on dotlan"""
    return _build_url(ESI_CATEGORY_CORPORATION, name)

def region_url(name: str) -> str:
    """url for page about given region on dotlan"""
    return _build_url(ESI_CATEGORY_REGION, name)

def solar_system_url(name: str) -> str:
    """url for page about given solar system on dotlan"""
    return _build_url(ESI_CATEGORY_SOLARSYSTEM, name)