# events/setup.py
from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

setup(
    name='dripp_events',
    version='0.1.0',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'dripp-api=events.main:main',  # API
            'dripp-core-listener=events.core_event_listener:main',  # Core Event Listener
            'dripp-parquet-writer=events.event_parquet_writer:main',  # Event Parquet Writer
        ],
    },
)
