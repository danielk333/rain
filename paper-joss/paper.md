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
- Publish/Subscribe: a server publishes updates relating to parameters, which clients can subscribe to. Parameters can have their value updated regularly or sporadically as a trigger. An analogy could be a weather station where weather data is updated reguarly, at a set frequency, and weather alerts are published sporadically

Clients can send three types of messages:
- GET: request the current value of a parameter
- SET: request to change the value of a parameter
- SUB: subscribe to updates of a parameter

Information is exchanged between a client and a server through JSON messages, which have a set structure, containing an identification of the message's sender, the time the message was formed as well as the message's content.

```
{
    "sender-name": "reindeer",
    "sender-key": "N?</IPRcpG.aNx()nLiAMEO0LWzwWfb<0H?d{IVE",
    "datetime": "2024-10-29T22:25:09.633010+01:00",
    "action": "get",
    "name": [
        "herd_size"
    ],
    "data": [
        "10"
    ]
}

```

To ensure nominal operations, each message is validated using validation schemas both before transmission and after reception.
These validation schemas are features from the JSON Schema package, and are used to check the structure of the JSON message, ensuring they contain all the correct fields in the right format.
They, however, do not check the content of these messages.

RAIN was developed with security in mind, boasting a few security features.
The main feature is the use of public-private keypairs, which encrypts the communication between a server and a client while allowing only them to decrypt these messages.
This was implemented using functionality from the PyZMQ library, which uses an implementation of the libsodium library.
It has a similar behaviour to SSH.
There is also an optional security feature for servers, which can define a list of the IP addresses of the clients that are allowed to connect to this server.
This allows for communication attempts from unwanted IP addresses to be immediately rejected.
Additional measures have also been taken to avoid spoofing.

A significant portion of RAIN's source code implements functionality provided by the PyZMQ package, the Python version of the ZeroMQ library.
PyZMQ was used notably for establishing connections, handling the security aspects and transporting the messages over these secured connections.
PyZMQ and JSON Schema are the only two external dependencies RAIN depends on, making this package easier to install and maintain.
A number of configuration options have also been made available to users, providing them with the opportunity to tailor their interactions when using RAIN.

RAIN was originally developed to be used to connect ground-based research infrastructure in the Arctic region of the Nordics, but it can be used in any situation that requires this kind of server-client interaction.

# Statement of Need

The Arctic regions of the Nordic countries are, ironically, a hotbed of scientific research of geo-
physics.
It is home to a number of scientific research institutes thatobserve a number of geophysical phenomena such as the aurora borealis, polar vortices, Polar Stratospheric Clouds (PSCs), meteors, Polar Mesospheric Summer Echoes (PMSEs) and Polar Mesospheric Winter Echoes (PMWEs), climate change and many more.
The level of research has gone beyond simple characterisation of these phenomena, with the research performed going deeper into the details, with the creation and refining of high-resolution models and simulations.
These are based off of detailed observations, which often require more than one instrument, meaning combined multi-instrument observations are becoming increasingly common, involving coordination across multiple sites in multiple countries.

The aim of this package is to increase the connectivity between these ground-based research instruments by providing researchers with the means of easily exchanging information (but not data).
This package is to be created using established standards and terminology in order for the system to be as user-friendly as possible.
RAIN is meant to be a tool to enable researchers to carry out their work more efficiently, therefore it should be straightforward and intuitive to use.
Finally, this package will be made open source, both for transparency and to make it easier for others to replicate this kind of network in their own area.

# Citations

# Figures

# Acknowledgements

# References
