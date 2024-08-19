from setuptools import setup

setup(
    name='rain',
    version='0.4',
    license='GNU GPLv3',
    author='Calum Lonie',
    maintainer='Daniel Kastinen',
    install_requires=[
        'pyzmq',
        'jsonschema',
    ],
    entry_points={
        'console_scripts': [
            'rain-client = rain.cli:client_cli',
            'rain-register = rain.cli:register_cli',
            'rain-server = rain.cli:server_cli',
            'rain-trigger = rain.cli:trigger_cli'
        ]
    }
)
