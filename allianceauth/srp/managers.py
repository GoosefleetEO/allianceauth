from allianceauth import NAME
from esi.clients import esi_client_factory
import requests
import logging
import os

logger = logging.getLogger(__name__)
SWAGGER_SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')
"""
Swagger Operations:
get_killmails_killmail_id_killmail_hash
"""


class SRPManager:
    def __init__(self):
        pass

    @staticmethod
    def get_kill_id(killboard_link):
        num_set = '0123456789'
        kill_id = ''.join([c for c in killboard_link if c in num_set])
        return kill_id

    @staticmethod
    def get_kill_data(kill_id):
        url = ("https://zkillboard.com/api/killID/%s/" % kill_id)
        headers = {
            'User-Agent': NAME,
            'Content-Type': 'application/json',
        }
        r = requests.get(url, headers=headers)
        result = r.json()[0]
        if result:
            killmail_id = result['killmail_id']
            killmail_hash = result['zkb']['hash']
            c = esi_client_factory(spec_file=SWAGGER_SPEC_PATH)
            km = c.Killmails.get_killmails_killmail_id_killmail_hash(killmail_id=killmail_id,
                                                                     killmail_hash=killmail_hash).result()
        else:
            raise ValueError("Invalid Kill ID")
        if km:
            ship_type = km['victim']['ship_type_id']
            logger.debug("Ship type for kill ID %s is %s" % (kill_id, ship_type))
            ship_value = result['zkb']['totalValue']
            logger.debug("Total loss value for kill id %s is %s" % (kill_id, ship_value))
            victim_id = km['victim']['character_id']
            return ship_type, ship_value, victim_id
        else:
            raise ValueError("Invalid Kill ID or Hash.")

