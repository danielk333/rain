# Examples README

The `examples` folder contains a series of files designed to help illustrate how a `rain` server and client should be set up, as well as how the configurations look.
An example instrument has been registered, called `reindeer`.
The instrument's public key has been placed in both the `authorised_keys` and `known_hosts` folders, meaning that `reindeer`'s server and client can communicate with each other, sharing a private key.
The `rain` servers' hostnames have been set to `localhost`, but on different ports.

This README shall serve as a guide on how to run a `rain` server and client, sending client requests, receiving server responses, as well as subscribing to a Publish server.

It is important to remember that for this example, the instrument's configuration folder is not in the default location, meaning the path to this folder will need to be added to every command.
This applies to trying to run the server and the client.

The examples also do not change any of the logging configurations.
A description of these configurations can be found in the guide.

## Configurations

The registration of an instrument to `rain` leads to configuration files being generated for both a server and a client, regardless of which will eventually be used by the user.
These files have been pre-filled with the necessary sections, and default values have been added where necessary.
The first task when wanting to run `rain` is to adjust these configurations.

### Server configurations

Starting with the server configurations, `server.cfg`, with only the `Allowed` section having been altered.
This section tells the server to reject any attempted communications made using addresses that aren't in this section.
This is optional however, and can be left empty.
An addition was made here however, to illustrate how this section is to be filled out.

The client's IP address was added as follows:
```
reindeer = 127.0.0.1
```
In a real-world implementation, this section must either be completely empty, or contain the IP addresses of all clients that are allowed to connect.

### Client configurations

More modifications were made to the client's configurations however, in `hosts.cfg`.
This file must contain the connection details of each server the client can connect to.
A section needs to be created for each server, with the section name being made up of the server's name and type (response or publish).
This section then needs to contain the server's hostname (IP address) and port.
```
[reindeer-response]
hostname = 127.0.0.1
port = 1234
```
If the client is going to connect to both server types of an instrument, then two separate sections need to be filled out, as shown in `hosts.cfg`.

## Starting a Response server

Starting the Response server can be done with the following command:
```
rain-server -c ./examples/reindeer rep
```

## Sending a request to the server

All servers come with a built-in command, called `api`, that when called returns a list of all the parameters made available by the server.
The parameters are listed for each type of request: `get`, `set` or `sub`.
Some parameters will appear in several lists.

The first client command can be to request this `api` parameter:
```
rain-client -c ./examples/reindeer reindeer get api
```

A `GET` request can be made using the following command (in this case requesting `herd_size`):
```
rain-client -c ./examples/reindeer reindeer get herd_size
```

A `SET` request is called in a very similar manner, but requires an extra `data` parameter:
```
rain-client -c ./examples/reindeer reindeer set herd_size -d 12
```

A `GET` request can be then called again to show that the `SET` request worked.

## Starting a Publish server

Starting a Publish server requires a near-identical command as for starting a Response server:
```
rain-server -c ./examples/reindeer pub
```

## Subscribing to a Publish server

There are three types of parameters that a client can subscribe to:

- Timed parameters (with `-f`), whose values are published at regular intervals by the server
- Changes in parameter values (with `-c`), whose values are published at regular intervals, but are only saved by the client if the parameter value has changed
- Trigger parameters (with `-t`), which represent sporadic events, with their values updated infrequently

The example server provides two parameters (`herd_size` and `activity`) for whom a client can subscribe to all values or only to changes.
The server also provides a trigger parameter (`antlers`) that a client can subscribe to.

A client can subscribe to all values of `activity`, only changes in `herd_size` and to the `antlers` trigger by calling the following command:
```
rain-client -c ./examples/reindeer reindeer sub -c herd_size -f activity -t antlers
```

When this command has been entered, the user should see the current value of `activity` appear every 4 seconds, but the `herd_size` parameter should only appear once, as its value isn't changing.
A `SET` command can be sent to the Response server, changing the value of `herd_size` (as in the example above).
The new value of `herd_size` should then appear when this parameter's value is published again by the server.

The trigger parameter won't yet show up, as it needs to be triggered on the server side.
This will be shown in the next section.

## Triggering a trigger parameter

Trigger parameters are triggered on the server side by entering a command contianing the parameter's name and a data value associated with this value.
In this example, the `antlers` parameters informs the client that a reindeer's antlers have fallen off.
This sends a message to the Publish server's internal trigger server, allowing for an update to be sent.
The command to trigger the `antlers` parameter is the following:
```
rain-trigger -c ./examples/reindeer antlers "a reindeer's antlers have fallen off"
```

The subscribed client should now see the value of the `antlers` parameter.

## Shutting things down

Shutting down a server or a subscribed client can be done through the use of a keyboard interrupt:
```
Ctrl + C
```
