import os


# TODO 21: Setup a client/server config file
def config():
    home = os.path.dirname(__file__)
    home = home.removesuffix("/src/rain")
    dir_pub = os.path.join(home, "public_keys")
    dir_prv = os.path.join(home, "private_keys")
    dir_info = os.path.join(home, "infra_info")
    dir_data = os.path.join(home, "data")

    return dir_pub, dir_prv, dir_info, dir_data
