import os
from esi.clients import EsiClientProvider

from allianceauth import __version__

SWAGGER_SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

esi = EsiClientProvider(
    spec_file=SWAGGER_SPEC,
    app_info_text=("allianceauth v" + __version__)
)
