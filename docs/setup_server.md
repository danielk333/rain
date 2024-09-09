# Setting up a `rain` server

This guide will describe what steps to take to set up a server, once an instrument has been registered.

## Server configurations

As was explained in registration.md, a file called `server.cfg` was automatically generated when your instrument was registered.
This file will be located at the location set when registering the instrument, or in `~/home/user/.config/rain` if this was not set.
This file was pre-filled with the relevant items, which were assigned default values.
These items will need to be adjusted to suit your needs.

### Configured paths

There are a number of paths that need to be configured, these are located in the `[Security]` and `[Plugins]` sections of `server.cfg`.

- `public-keys`: the path to the `authorised_keys` folder, which will be used to store the public keys of the clients that will be authorised to connect to your server. By default this path leads to a folder within the configuration folder
- `private-keys`: the path to the `keypairs` folder, which stores the instrument's public and private keys. If a path was entered when registering the instrument, this path will be the one linked, otherwise the path will lead to a folder inside the configuration folder
- `plugins`: the path to the `plugins` folder, which will be used to store the server's plugins. These will be described in more detail later

These paths can be left at their default values but they can also be changed to offer more flexibility to users.
As long as the paths link to the correct folders then the software will function normally.

### Logging

`rain` offers logging support, allowing users to select how to visualise logging messages as well as set logging levels as a filter.
A number of configurations have been given to users:

- `level`: the top-level logging level. The default level is DEBUG
- `filepath`: the path to a file that will store logging messages passed to it by a file handler. This is disabled by default
- `file-level`: the level of messages that are stored in the logging file. The default value is INFO
- `print`: determines whether a stream handler is used, allowing for logging messages to be passed on to `stdout`. This is set to `True` by default
- `print-level`: the level of messages that are passed on to the stream handler. The default value is INFO

The following logging levels are implemented: `NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
Logging is desscribed in more detail in the `Logging` section of the documentation.

The above logging configurations can also be called when starting the server.
In this case, the values entered when starting the server take precedence over the configured values, without overwriting them in `server.cfg`.

### Server details

The server's details, namely hostnames and ports, need to be configured to allow others to connect.
There are three sets of details to configure, depending on what the server wants to allow.

- Server details for a Response server, processing client requests and replying with a response
- Server details for a Publish server, providing updates of parameter values to clients that have subscribed to the server
- Server details for a Trigger server. This in internal to the server, and is used by a server to call its own trigger parameters.

When `server.cfg` was generated, these details were set to `localhost` (127.0.0.1) with random ports.
These will need to be adjusted to your setup, depending on what functionality you want to provide.

### The `Allowed` section

This section is an optional security feature, that can be combined with the public-private cryptography `rain` employs.
The hostnames of the clients that are allowed to connect to the server can be added here.
This list is then used by `rain` to reject any connection attempt using IP addresses that aren't in this list.
However this list can be left empty without affecting how `rain` functions.

### Example

An example server configuration file can be found in `examples/config/server.cfg`.

## Public key exchanges

`rain` uses public-private cryptography as its main security feature.
This works through the use of public and private keys, unique to each user, as in `SSH`, but using `CURVE` authentication.
This means that clients will need to provide their public key to the server, if they wish to connect.
The client public keys must be stored in the `authorised_keys` folder.
Conversely, a server also needs to provide its public key to any client that wishes to connect.

The public-private keypairs are automatically generated when registering an instrument, and it is these keys that are used by `rain`.
Keys in another format are not supported.
More information regarding this can be found in `PyZMQ`'s [documentation](https://pyzmq.readthedocs.io/en/latest/api/zmq.auth.html) and [source code](https://github.com/zeromq/pyzmq).

It is always important to remember that private keys should always remain in the sole possession of the key's owner.
A private key should **never** be shared with anyone else.
