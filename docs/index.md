# `rain`

ReseArch Infrastructure Network (`rain`) is a Python package that allows users to exchange messages between each other. This package was created with the purpose of sending status information between research infrastructure in the Arctic regions of the Nordics. However `rain`'s scope is not limited to this specific use case.

## Description

The `rain` software package allows users to run `rain` servers and clients.
Servers and clients can communicate with each other in a decentralised peer-to-peer network over a TCP/IP connection.
Users are authenticated through the use of public-private keypairs (`CURVE` algorithm), which also encrypt the transmitted messages.
These messages are in a JSON format, and their structure is validated using validation schemas before transmission and after reception.
`rain` offers configurations for both servers and clients in configuration files, some of which can also be set when starting the server or client.

`rain` has two external dependencies:

- [PyZMQ](https://zeromq.org/languages/python/): used to create the connection socket, encrypt and transport messages and authenticate users
- [JSON Schema](https://json-schema.org/): used to validate messages

Supporting documentation is provided in the form of:

- Online documentation
- Examples, containing a ready-to-use instrument called `reindeer`, and a README as a guide
- Tests

## Develop

### Internal development

Please refer to the style and contribution guidelines documented in the
[IRF Software Contribution Guide](https://danielk.developer.irf.se/software_contribution_guide/).

### External code-contributions

Generally external code-contributions are made trough a "Fork-and-pull"
workflow towards the `main` branch.
