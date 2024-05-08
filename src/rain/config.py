from pathlib import Path


# TODO 21: Setup a client/server config file
def config():
    home = Path.cwd()
    dir_pub = home / "public_keys"
    dir_prv = home / "private_keys"
    dir_info = home / "infra_info"
    dir_data = home / "data"

    return dir_pub, dir_prv, dir_info, dir_data
