
import pathlib
from rain import register_response, get_keys

HERE = pathlib.Path(__file__).parent
IDENTITIES = get_keys(HERE.parent / "authorised_keys")


@register_response(
    action="get",
    name="greeting",
    data_description=""
)
def get_herd_size(message):
    sender = IDENTITIES[message["sender-key"]]
    if sender == "mike":
        value = "go touch grass"
    elif sender == "reindeer":
        value = "cuddels"
    else:
        value = "WHO ARE YOU"
    return value
