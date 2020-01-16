from django.db import models
from typing import Union

from .managers import EveCharacterManager, EveCharacterProviderManager
from .managers import EveCorporationManager, EveCorporationProviderManager
from .managers import EveAllianceManager, EveAllianceProviderManager
from . import providers


EVE_IMAGE_SERVER_URL = 'https://images.evetech.net'


def _eve_entity_image_url(    
    category: str,     
    id: int, 
    size: int = 32, 
    variant: str = None,
    tenant: str = None,
) -> str:
    """returns image URL for an Eve Online ID.
    Supported categories: `alliance`, `corporation`, `character`
    
    Arguments:
    - category: category of the ID
    - id: Eve ID of the entity
    - size: (optional) render size of the image.must be between 32 (default) and 1024
    - variant: (optional) image variant for category. currently not relevant.
    - tentant: (optional) Eve Server, either `tranquility`(default) or `singularity`

    Returns:
    - URL string for the requested image on the Eve image server

    Exceptions:
    - Throws ValueError on invalid input
    """
    
    # input validations
    categories = {
        'alliance': {
            'endpoint': 'alliances',
            'variants': [
                'logo'
            ]
        },
        'corporation': {
            'endpoint': 'corporations',
            'variants': [
                'logo'
            ]
        },
        'character': {
            'endpoint': 'characters',
            'variants': [
                'portrait'
            ]
        }
    }
    tenants = ['tranquility', 'singularity']
   
    if size < 32 or size > 1024 or (size & (size - 1) != 0):
        raise ValueError('Invalid size: {}'.format(size))
   
    if category not in categories:
        raise ValueError('Invalid category {}'.format(category))
    else:
        endpoint = categories[category]['endpoint']

    if variant:
        if variant not in categories[category]['variants']:
            raise ValueError('Invalid variant {} for category {}'.format(
                variant,
                category
            ))
    else:
        variant = categories[category]['variants'][0]

    if tenant and tenant not in tenants:
            raise ValueError('Invalid tentant {}'.format(tenant))
        
    # compose result URL
    result = '{}/{}/{}/{}?size={}'.format(
        EVE_IMAGE_SERVER_URL,
        endpoint,
        id,
        variant,
        size
    )
    if tenant:
        result += '&tenant={}'.format(tenant)
    
    return result


class EveAllianceInfo(models.Model):
    alliance_id = models.CharField(max_length=254, unique=True)
    alliance_name = models.CharField(max_length=254, unique=True)
    alliance_ticker = models.CharField(max_length=254)
    executor_corp_id = models.CharField(max_length=254)

    objects = EveAllianceManager()
    provider = EveAllianceProviderManager()

    def populate_alliance(self):
        alliance = self.provider.get_alliance(self.alliance_id)
        for corp_id in alliance.corp_ids:
            if not EveCorporationInfo.objects.filter(corporation_id=corp_id).exists():
                EveCorporationInfo.objects.create_corporation(corp_id)
        EveCorporationInfo.objects.filter(corporation_id__in=alliance.corp_ids).update(alliance=self)
        EveCorporationInfo.objects.filter(alliance=self).exclude(corporation_id__in=alliance.corp_ids).update(
            alliance=None)

    def update_alliance(self, alliance: providers.Alliance = None):
        if alliance is None:
            alliance = self.provider.get_alliance(self.alliance_id)
        self.executor_corp_id = alliance.executor_corp_id
        self.save()
        return self

    def __str__(self):
        return self.alliance_name

    @staticmethod
    def generic_logo_url(alliance_id: int, size: int = 32) -> str:
        """image URL for the given alliance ID"""
        return _eve_entity_image_url('alliance', alliance_id, size)
    
    def logo_url(self, size:int = 32) -> str:
        """image URL of this alliance"""
        return self.generic_logo_url(self.alliance_id, size)

    @property
    def logo_url_32(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(32)

    @property
    def logo_url_64(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(64)

    @property
    def logo_url_128(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(128)

    @property
    def logo_url_256(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(256)


class EveCorporationInfo(models.Model):
    corporation_id = models.CharField(max_length=254, unique=True)
    corporation_name = models.CharField(max_length=254, unique=True)
    corporation_ticker = models.CharField(max_length=254)
    member_count = models.IntegerField()
    alliance = models.ForeignKey(EveAllianceInfo, blank=True, null=True, on_delete=models.SET_NULL)

    objects = EveCorporationManager()
    provider = EveCorporationProviderManager()

    def update_corporation(self, corp: providers.Corporation = None):
        if corp is None:
            corp = self.provider.get_corporation(self.corporation_id)
        self.member_count = corp.members
        try:
            self.alliance = EveAllianceInfo.objects.get(alliance_id=corp.alliance_id)
        except EveAllianceInfo.DoesNotExist:
            self.alliance = None
        self.save()
        return self

    def __str__(self):
        return self.corporation_name

    @staticmethod
    def generic_logo_url(corporation_id: int, size: int = 32) -> str:
        """image URL for the given corporation ID"""
        return _eve_entity_image_url('corporation', corporation_id, size)

    def logo_url(self, size:int = 32) -> str:
        """image URL for this corporation"""
        return self.generic_logo_url(self.corporation_id, size)

    @property
    def logo_url_32(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(32)

    @property
    def logo_url_64(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(64)

    @property
    def logo_url_128(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(128)

    @property
    def logo_url_256(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(256)


class EveCharacter(models.Model):
    character_id = models.CharField(max_length=254, unique=True)
    character_name = models.CharField(max_length=254, unique=True)
    corporation_id = models.CharField(max_length=254)
    corporation_name = models.CharField(max_length=254)
    corporation_ticker = models.CharField(max_length=5)
    alliance_id = models.CharField(max_length=254, blank=True, null=True, default='')
    alliance_name = models.CharField(max_length=254, blank=True, null=True, default='')
    alliance_ticker = models.CharField(max_length=5, blank=True, null=True, default='')

    objects = EveCharacterManager()
    provider = EveCharacterProviderManager()

    @property
    def alliance(self) -> Union[EveAllianceInfo, None]:
        """
        Pseudo foreign key from alliance_id to EveAllianceInfo
        :raises: EveAllianceInfo.DoesNotExist
        :return: EveAllianceInfo or None
        """
        if self.alliance_id is None:
            return None
        return EveAllianceInfo.objects.get(alliance_id=self.alliance_id)

    @property
    def corporation(self) -> EveCorporationInfo:
        """
        Pseudo foreign key from corporation_id to EveCorporationInfo
        :raises: EveCorporationInfo.DoesNotExist
        :return: EveCorporationInfo
        """
        return EveCorporationInfo.objects.get(corporation_id=self.corporation_id)

    def update_character(self, character: providers.Character = None):
        if character is None:
            character = self.provider.get_character(self.character_id)
        self.character_name = character.name
        self.corporation_id = character.corp.id
        self.corporation_name = character.corp.name
        self.corporation_ticker = character.corp.ticker
        self.alliance_id = character.alliance.id
        self.alliance_name = character.alliance.name
        self.alliance_ticker = getattr(character.alliance, 'ticker', None)
        self.save()
        return self

    def __str__(self):
        return self.character_name

    @staticmethod
    def generic_portrait_url(character_id: int, size: int = 32) -> str:
        """image URL for the given character ID"""
        return _eve_entity_image_url('character', character_id, size)

    def portrait_url(self, size = 32) -> str:
        """image URL for this character"""
        return self.generic_portrait_url(self.character_id, size)

    @property
    def portrait_url_32(self) -> str:
        """image URL for this character"""
        return self.portrait_url(32)

    @property
    def portrait_url_64(self) -> str:
        """image URL for this character"""
        return self.portrait_url(64)

    @property
    def portrait_url_128(self) -> str:
        """image URL for this character"""
        return self.portrait_url(128)
    
    @property
    def portrait_url_256(self) -> str:
        """image URL for this character"""
        return self.portrait_url(256)

    def corporation_logo_url(self, size = 32) -> str:
        """image URL for corporation of this character"""
        return EveCorporationInfo.generic_logo_url(self.corporation_id, size)

    @property
    def corporation_logo_url_32(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(32)

    @property
    def corporation_logo_url_64(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(64)

    @property
    def corporation_logo_url_128(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(128)

    @property
    def corporation_logo_url_256(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(256)

    def alliance_logo_url(self, size = 32) -> str:
        """image URL for alliance of this character or empty string"""
        if self.alliance_id:
            return EveAllianceInfo.generic_logo_url(self.alliance_id, size)
        else:
            return ''

    @property
    def alliance_logo_url_32(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(32)

    @property
    def alliance_logo_url_64(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(64)

    @property
    def alliance_logo_url_128(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(128)
    
    @property
    def alliance_logo_url_256(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(256)
