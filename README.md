# RAIN

ReseArch Infrastructure Network (RAIN) is a Python package that allows users to exchange messages between each other. This package was created with the purpose of sending status information between research infrastructure in the Arctic regions of the Nordics. However RAIN's scope is not limited to this specific use case.
The communication network is set up in a decentralised peer-to-peer configuration, allowing users to run servers and clients. The communication takes place in the form of JSON messages over a TCP/IP connection.

RAIN can be installed in your virtual environment:
- From PyPI:
```pip install rain```
- From this repository:
```
git clone https://github.com/danielk333/rain
pip install .
```
An installation guide can be found in `docs/installation.md`

The software package has two external dependencies:
- [PyZMQ](https://github.com/zeromq/pyzmq): used for creating the connection socket, the transport of messages and also for the authentication of the connection
- [JSON Schema](https://github.com/python-jsonschema/jsonschema): used for validating messages, both before transmission and after reception
