import setuptools

setuptools.setup(
    name="rain",
    version="0.4",
    license="GNU GPLv3",
    author="Calum Lonie",
    maintainer="Daniel Kastinen",
    package_dir={
        "": "src"
    },
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "pyzmq",
        "jsonschema",
    ],
    entry_points={
        "console_scripts": [
            "rain-client = rain.cli:client_cli",
            "rain-register = rain.cli:register_cli",
            "rain-server = rain.cli:server_cli",
            "rain-trigger = rain.cli:trigger_cli"
        ]
    }
)
