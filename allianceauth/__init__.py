# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

__version__ = '2.9.3'
__title__ = 'Alliance Auth'
__url__ = 'https://gitlab.com/allianceauth/allianceauth'
NAME = f'{__title__} v{__version__}'
default_app_config = 'allianceauth.apps.AllianceAuthConfig'
