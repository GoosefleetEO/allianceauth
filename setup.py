import os
from setuptools import setup
import allianceauth

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'mysqlclient>=2.1.0',
    'dnspython',
    'passlib',
    'requests>=2.9.1,<3.0.0',
    'bcrypt',
    'python-slugify>=1.2',
    'requests-oauthlib',
    'semantic_version',
    'packaging>=21.0,<22',
    'beautifulsoup4',

    'redis>=4.0.0,<5.0.0',
    'celery>=5.2.0,<6.0.0',
    'celery_once>=3.0.1',

    'django>=4.0.2,<5.0.0',
    'django-bootstrap-form',
    'django-registration>=3.2',
    'django-sortedm2m',
    'django-redis>=5.2.0<6.0.0',
    'django-celery-beat @ git+https://github.com/celery/django-celery-beat.git@0806ab3c65e1615e9b617146779c21f49749067a',

    'openfire-restapi',
    'slixmpp',
    'pydiscourse',

    'django-esi>=4.0.0a1'
]

testing_extras = [
    'coverage>=4.3.1',
    'requests-mock>=1.2.0',
    'django-webtest',
]

setup(
    name='allianceauth',
    version=allianceauth.__version__,
    author='Alliance Auth',
    author_email='adarnof@gmail.com',
    description=(
        'An auth system for EVE Online to help in-game organizations '
        'manage online service access.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras
    },
    python_requires='~=3.8',
    license='GPLv2',
    packages=['allianceauth'],
    url=allianceauth.__url__,
    zip_safe=False,
    include_package_data=True,
    entry_points="""
            [console_scripts]
            allianceauth=allianceauth.bin.allianceauth:main
    """,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        'Documentation': 'https://allianceauth.readthedocs.io/',
    },
)
