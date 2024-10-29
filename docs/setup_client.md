# Setting up a `rain` client

This guide will describe what steps to take to set up a client, once an instrument has been registered.

## Client configurations

As was explained in the Registration Guide, a file called `hosts.cfg` was automatically generated when your instrument was registered.
This file will be located at the location set when registering the instrument, or in `~/home/.config/rain` if this was not set.
This file was pre-filled with the relevant items, which were assigned default values.
These items will need to be adjusted to suit your needs.

### Configured paths

There are a number of paths that need to be configured, these are located in the `[Security]` section of `hosts.cfg`.

- `public-keys`: the path to the `known_hosts` folder, which will be used to store the public keys of the servers that the client is authorised to connect to. By default this path leads to a folder within the configuration folder
- `private-keys`: the path to the `keypairs` folder, which stores the instrument's public and private keys. If a path was entered when registering the instrument, this path will be the one linked, otherwise the path will lead to a folder inside the configuration folder

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

The above logging configurations can also be called when starting the client.
In this case, the values entered when starting the client take precedence over the configured values, without overwriting them in `hosts.cfg`.

### Connection timeouts

Two timeouts have been implemented, in order to ensure that a server or client will not hang, potentially blocking interactions.

- `receive`: the connection timeout if a request message isn't being received by a Response server
- `subscribe`: the connection timeout if a message isn't being received by a Publish server

In both cases, the configured values need to be given in milliseconds, with the defaults being set at 10000ms (10s) for the `receive` timeout, and -1 (infinite) for the `subscribe` timeout.
The `subscribe` timeout is set to infinite to avoid a Subscribe client disconnecting from a Publish server with long update frequencies.

### Server details

Before connecting to a server, its connection details will need to be entered in `hosts.cfg`.
The following example is given to show how this should look, assuming we are wanting to connect to a Response server called "reindeer":

```
[reindeer-response]
hostname = 123.4.5.6
port = 7890
```

If we want to connect to the server's Publish server, we would need to enter the server's details in a section called `[reindeer-publish]`.
This distinction is important, as an instrument will run a Publish and a Request server on different ports, and potentially with different IP addresses.

### Example

An example client configuration file can be found in `examples/config/hosts.cfg`.

## Public key exchanges

`rain` uses public-private cryptography as its main security feature.
This works through the use of public and private keys, unique to each user, as in `SSH`, but using `CURVE` authentication.
This means that server will need to provide their public key to the clients that wish to connect.
The server public keys must be stored in the `known_hosts` folder.
Conversely, a client also needs to provide its public key to any server it wishes to connect to.

The public-private keypairs are automatically generated when registering an instrument, and it is these keys that are used by `rain`.
Keys in another format are not supported.
More information regarding this can be found in `PyZMQ`'s [documentation](https://pyzmq.readthedocs.io/en/latest/api/zmq.auth.html) and [source code](https://github.com/zeromq/pyzmq).

It is always important to remember that private keys should always remain in the sole possession of the key's owner.
A private key should **never** be shared with anyone else.
