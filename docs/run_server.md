# Running a `rain` server

A `rain` server is started by calling the server Command Line Interface (CLI) from within your virtual environment.
This CLI takes a number of arguments.
There is one compulsory argument:

- `rep` or `pub`: depending on whether the server to start is a Response or a Subscribe server respectively

Additionally, there are several optional arguments:

- `-a` or `--auth`: is set to `False` when called. This disables a Publish server's authentication measures. It must also be disabled on the client's side, or no messages can be received.
- `-c` or `--cfgpath`: the path to the server's main configuration folder. This argument must be called if this folder is not in the default location, otherwise it can be omitted
- `-l` or `--logfile`: the path to a file that will be used to store the server's logs
- `-o` or `--logprint`: is set to `True` when called. This sets whether to print the server's logs to `stdout` (to print to the console for example)
- `-v` or `--loglevel`: the lowest logging level of messages past on to the file or print logging handlers
- `-vl` or `--filelevel`: the logging level of the messages saved in the log file
- `-vo` or `--printlevel`: the logging level of the messages passed to `stdout`

If the logging arguments are not called, the related configurations will be used, else pre-set defaults will be enacted.

## Simplest example

The simplest example is one where the server's configuration folder is in the default location and no other optional arguments are called.
Assume the user wants to start a Response server:
```
rain-server rep
```
This short command is enough to start a `rain` server, with `rain` extracting all the information it needs from the server's configurations.

## More complicated example

In this example, assume the server's logging configurations have been left at their default values (no file logging, print logging enabled, all logging levels set at INFO).
The server's configuration folder has been placed in a non-default location and the user wants to log DEBUG messages in a file.
Assume the user wants to start a Publish server:
```
rain-server pub -c ~/path/to/folder -l ~/path/to/logs/file.log -v DEBUG -vl DEBUG
```
