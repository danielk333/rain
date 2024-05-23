from setuptools import setup

setup(
    name='rain',
    version='0.2',
    license='GNU GPLv3',
    author='Calum Lonie',
    maintainer='Daniel Kastinen',
    install_requires=[
        'zmq'
    ],
    entry_points={
        'console_scripts': [
            'rain-client = rain.cli:client_cli',
            'rain-server = rain.cli:server_cli',
            'rain-register = rain.cli:new_user_cli'
        ]
    }
)
