# Registration Guide

Once `rain` has been installed, users need to "register" an instrument before they can start connecting to others.

## Registration initialisation

The registration process is simple to initiate, and is done by calling the registration CLI (Command Line Interface).
It only needs to be done once per instrument, whether you are wanting to run it as a server or as a client.
The registration process involves setting up the instrument's configurations and generating the instrument's public-private keypair.
The CLI source code can be found in `src/rain/cli.py`.
This CLI has one required argument:

- The name of the instrument

And two optional arguments:

- The path to the folder containing the instrument's configurations. If this is not provided, the default location will be used: `~/home/.config/rain`
- The path to the keypairs folder which will hold the instrument's public and private keys. If this is not provided, the default location will be used, which is inside the configuration folder

## The configuration folder

The configuration folder contains the following items:

- `server.cfg`: the file containing the server's configurations
- `hosts.cfg`: the file containing the client's configurations
- `authorised_keys`: the folder used to store the public keys of clients that are allowed to connect to the server. This folder starts empty
- `known_hosts`: the folder used to store the public keys of the server that the client is authorised to connect to. This folder starts empty
- `plugins`: the folder used to store the server's plugins
- `keypairs`: the folder containing the instrument's public and private keys (if the path to this folder has been left at the default location)

Verify these files and folders have been generated and are in the right location(s).
Once you have done this, you can move on to setting up your instrument's server, client or both.
<!-- Add links to relevant files -->
