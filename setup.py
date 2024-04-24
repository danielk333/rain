from setuptools import setup

setup(
    name='rain',
    version='0.1',
    license='GNU GPLv3',
    author='Calum Lonie',
    maintainer='Daniel Kastinen',
    install_requires=[
        'os',
        'time',
        'json',
        'pprint',
        'zmq'
    ],
    entry_points={
        'console_scripts': [
            'run-server = rain:run_server',
            'run-client = rain:run_client'
        ]
    }
)
