import csv

from rain import register_response, register_publish, register_trigger


def find_value(name):
    file_name = "./examples/reindeer/plugins/reindeer_data.csv"
    fields = ["name", "value"]
    with open(file_name, "r") as f:
        reader = csv.DictReader(f, fieldnames=fields)
        for row in reader:
            if row["name"] == name:
                value = row["value"]
                break

    return value


def change_value(name, value):
    file_name = "./examples/reindeer/plugins/reindeer_data.csv"
    fields = ["name", "value"]
    rows = []
    with open(file_name, "r") as database:
        reader = csv.DictReader(database, fieldnames=fields)
        for row in reader:
            if row["name"] != name:
                keep = f'{row["name"]},{row["value"]}'
                rows.append(keep)
            else:
                keep = f'{row["name"]},{value}'
                rows.append(keep)
    with open(file_name, "w") as database:
        for row in range(len(rows)):
            database.write(rows[row])
            database.write("\n")


@register_response(
    action="get",
    name="herd_size",
    data_description="Number of reindeer in the herd, Type: int, Values: any int"
)
def get_herd_size(message):
    if message["name"] == "herd_size":
        value = find_value("Number")

    return value


@register_response(
    action="get",
    name="activity",
    data_description="What the herd of reindeer are up to, Type: string, Values: grazing, asleep"
)
def get_activity(message):
    if message["name"] == "activity":
        value = find_value("Activity")

    return value


@register_response(
    action="set",
    name="herd_size",
    data_description="Number of reindeer in the herd, Type: int, Values: any int"
)
def set_herd_size(message):
    if message["name"] == "herd_size":
        change_value("Number", message["data"])
        new_value = find_value("Number")

    return new_value


@register_response(
    action="set",
    name="activity",
    data_description="What the herd of reindeer are up to, Type: string, Values: grazing, asleep"
)
def set_activity(message):
    if message["name"] == "activity":
        change_value("Activity", message["data"])
        new_value = find_value("Activity")

    return new_value


@register_publish(
    action="sub",
    name="herd_size",
    interval=4,
    data_description="Number of reindeer in the herd, Type: int, Values: any int"
)
def sub_herd_size(param_name):
    if param_name == "herd_size":
        value = find_value("Number")

    return value


@register_publish(
    action="sub",
    name="activity",
    interval=4,
    data_description="What the herd of reindeer are up to, Type: string, Values: grazing, asleep"
)
def sub_activity(param_name):
    if param_name == "activity":
        value = find_value("Activity")

    return value


register_trigger(
    name="trigger",
    data_description="enter parameter description here"
)
