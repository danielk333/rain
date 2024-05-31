import subprocess

from rain import register_plugin


@register_plugin(
    action="get",
    name="temp",
    data_description="CPU core temperature"
)
def get_temp():
    cmd = "sensors coretemp-isa-0000"
    temp = subprocess.run(cmd, capture_output=True)

    return str(temp)
