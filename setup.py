from setuptools import setup

setup(
    name='rain',
    version='0.1',
    license='GNU GPLv3',
    author='Calum Lonie',
    maintainer='Daniel Kastinen',
    install_requires=[
        'zmq'
    ],
    entry_points={
        'console_scripts': [
            # 'run-server = rain.server:run_server',
            # 'run-client = rain.client:run_client',
            # 'run-publish = rain.publish:run_publish',
            # 'run-subscribe = rain.subscribe:run_subscribe',
            'rain-client = rain.client:client',
            # 'run-response = rain.server:run_response'
            'rain-server = rain.server:server'
        ]
    }
)
