# Tips and tricks

## Using the api command

A very common pattern when exploring the available commands is to `get api` and then parse the resulting json, i.e. 

```bash
rain-client server get api | jq  -r ".data[0]" | jq -r ".get"
```

to nicely print all the `get` commands available for the server called `server`. 