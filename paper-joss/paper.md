---
title: 'RAIN: A Python package for sending messages between research infrastructure in the Nordics'
tage:
  - Python
  - Infrastructure
  - Computer network
authors:
  - name: Calum Lonie
    affiliation: "1, 2"
  - name: Daniel Kastinen
    orcid:
    affiliation: 1
affiliations:
  - name: Institutet för Rymdfysik, Kiruna, Sverige
    index: 1
  - name: Luleå Tekniska Universitet, Kiruna, Sverige
    index: 2
date:
bibliography: bibliography.bib
---

# Summary

RAIN (ReseArch Infrastructure Network) is an open-source Python package that allows for servers and clients to exchange messages between each other over a TCP/IP connection.
This message exchange takes place in a decentralised peer-to-peer setting, allowing users greater flexibility in how they interact using RAIN.

This software package is general, meaning that the software installed is identical for every user.
However, server-specific information is still needed to run a server, such as the parameters that are made available to connected clients.
This is accomplished through what is called the plugin system.
This system allows server users to define a series of Python functions (placed in a configurable location).
These functions form a bridge between the information requested by RAIN to form a message and the server's systems where this information is held.

Two interaction models have been defined:
- Request/Response: a client sends a request to a server, which replies with a response
- Publish/Subscribe: a server publish updates relating to parameters, which clients can subscribe to. Parameters can have their value updated regularly or sporadically as a trigger. An analogy could be a weather station where weather data is updated reguarly, at a set frequency, and weather alerts are published sporadically

Clients can send three types of messages:
- GET: request the current value of a parameter
- SET: request to change the value of a parameter
- SUB: subscribe to updates of a parameter

Information is exchanged between a client and a server through JSON messages, which have a set structure
These messages are also validated before transmission and on reception, using validation schemas.
These schemas check the structure of the messages, ensuring they have the correct fields.
They don't check the content of the messages, though this is something that could be implemented in a server's plugins.
- Add example message

Security was considered when developing this package.
There are two main security features:
- Public-private keypairs, implemented from PyZMQ, based off libsodium. The principle is very similar to SSH
- For server (optional): a list of the IP addresses of the clients that are allowed to connect. Configurable by the server user

RAIN was originally developed to be used to connect ground-based research infrastructure in the Arctic region of the Nordics, but it can be used in any situation that requires this kind of server-client interaction.

- PyZMQ used extensively
- Configs

# Statement of Need

Need something usable and worth implementing

# Mathematics

# Citations

# Figures

# Acknowledgements

# References
