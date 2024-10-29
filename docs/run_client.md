# Running a `rain` client

A `rain` client is called by calling the client Command Line Interface (CLI) from within your virtual environment.
The CLI takes a number of arguments, which vary depending on the type of message you want to send.
There are however some arguments that can always be called, no matter the type of message.

There are two compulsory arguments:

- the name of the server to connect to
- `get`, `set` or `sub`: the type of request to make

As well as a number of optional arguments:

- `-a` or `--auth`: is set to `False` when called. This disables a Subscribe client's authentication measures. It must also be disabled on the server's side, or no messages can be received.
- `-c` or `--cfgpath`: the path to the client's main configuration folder. This argument must be called if this folder is not in the default location, otherwise it can be omitted
- `-l` or `--logfile`: the path to a file that will be used to store the client's logs
- `-o` or `--logprint`: is set to `True` when called. This instructs to print the client's logs to `stdout` (to print to the console for example)
- `-v` or `--loglevel`: the lowest logging level of messages past on to the file or print logging handlers
- `-vl` or `--filelevel`: the logging level of the messages saved in the log file
- `-vo` or `--printlevel`: the logging level of the messages passed to `stdout`
- `-s` or `--suppress`: is set to `True` when called. This instructs to stop the printing the received messages to `stdout`

## GET or SET commands

`get` and `set` requests include the following:

- `param`: the names of the parameters to request
- `data`: called with `-d` or `--data`

In the event of a `get` request, the `data` argument can be used as extra information to provide to a server, if they require such extra information.
However this argument remains optional for `get` requests.

For `set` requests, the `data` argument contains the value(s) to set the parameter(s) to.
This argument is compulsory.

In either case, the number of `data` arguments must match the number of parameters requested.

### Examples

For a simple example, with a client requesting a parameter called `herd_size` from a server called "reindeer", with no optional arguments called:
```
rain-client get herd_size
```

For a slightly more complex `set` request, with a client requesting two parameters from "reindeer": `herd_size` and `activity` to be set to `12` and `sleeping` respectively.
No optional arguments.
```
rain-client set herd_size activity -d 12 sleeping
```

For a `set` request of one parameter, with a non-default configuration folder location and setting the printing level to `DEBUG`:
```
rain-client -c ~/path/to/folder -v DEBUG -vo DEBUG set herd_size -d 15
```

## SUB command

A server makes available two types of parameters available to request: timed parameters and trigger parameters.
Timed parameters are parameters whose values are updated regularly, at a frequency set for each parameter.
Trigger parameters represent sporadic events, they are not updated regularly and are their values are only published by the server when they have been triggered.
However, a client can make a distinction among the timed parameters, allowing users to only save messages if a parameter's value has changed.

`sub` requests include the following:

- `-c` or `--changes`: the parameters to subscribe to, where server messages will only be saved if the parameters' values change
- `-f` or `--freq`: the parameters to subscribe to, where all relevant server messages will be saved
- `-t` or `--trigger`: the trigger parameters to subscribe to

### Examples

For an example where a client subscribes to three parameters: `herd_size` (only changes in values), `activity` (all values) and `antlers` (a trigger parameter).
No other optional arguments are called.
```
rain-client sub -c herd_size -f activity -t antlers
```
