# RAIN TODOs

Big TODOs:
- [x] T1: Implement the request parameter process into the server-client model
- [x] T2: Implement commands to change parameters
- [x] T3: Split client and server actions into separate files
- [ ] ~~T4: Convert clients and servers into classes~~
- [x] T5: Split the code into the established layers
- [ ] T6: Separate the server and the client from the network
- [x] T7: Make a package out of the software
- [ ] T8: Implement a Redis database
- [x] T9: Write a CLI to replace the user input
- [ ] T10: Upload to PyPI

Smaller TODOs:
- [ ] ~~TODO 1: Check there is no existing instrument with this name, and no existing keypair~~
- [x] TODO 2: Add the time the keypair was generated
- [x] TODO 3: Delete the automatically generated files
- [x] TODO 4: Add the new info file to a directory with other info files
- [x] TODO 5: Replace os library with Pathlib
- [x] TODO 6: Replace feedback printing with pprint
- [x] TODO 7: Add server details to the info file
- [x] TODO 8: Ask user what server to interact with
- [x] TODO 9: Also find the end of the parameters
- [x] TODO 10: Add the request and command status to the pprint
- [x] TODO 11: Make a list of each type of command and separate the responses to these in separate functions
- [x] TODO 12: Be able to handle changing values of multiple parameters
- [x] TODO 13: Fix how commands are received
- [x] TODO 14: Convert the key from bytes to string
- [x] TODO 15: Fix the request and command status checks
- [x] TODO 16: Load server details from info file
- [ ] TODO 17: Generate the data file
- [x] TODO 18: Be able to handle finding values of multiple parameters
- [ ] ~~TODO 19: Accept numerical inputs~~
- [ ] ~~TODO 20: Move the shutdown command to the server side~~
- [x] TODO 21: Setup a client/server config file
- [x] TODO 22: Rename message file to packaging
- [x] TODO 23: Move user input functions into their own file
- [x] TODO 24: Move the response functions into a packaging file
- [x] TODO 25: Combine the data and actions functions into one file
- [x] TODO 26: Create a decompose file
- [x] TODO 27: Rename the packaging functions
- [x] TODO 28: Move the paths into a separate function
- [x] TODO 29: Split the function calls into separate files
- [x] TODO 30: Merge the setup functions
- [ ] TODO 31: Send subscription updates when changes occur
- [x] TODO 32: Rename function parameters so they no longer match runtime variables
- [x] TODO 33: Write proper headers for each file
- [x] TODO 34: Combine the client, server, publish and subscribe run functions into one file
- [x] TODO 35: Add timestamps to responses
- [x] TODO 36: Move the load_groups and subscribable_params functions into a different file
- [ ] ~~TODO 37: For each request type only show the suitable parameters~~
- [x] TODO 38: Write a CLI for the new user code
- [ ] TODO 39: Add logging messages
- [x] TODO 40: Remove groups
- [ ] TODO 41: Implement a way for a server to nicely shut itself down
- [x] TODO 42: Rework the request_components function
- [x] TODO 43: Rework the pub_split function
- [ ] TODO 44: Improve the layout of the --help command
- [ ] TODO 45: Move the argument handling into functions
- [ ] TODO 46: Move the config handling into functions
- [ ] TODO 47: Load parameters from somewhere other than an info file
- [ ] TODO 48: Change the name of the private key file to include 'curve'

Exception Handling:
