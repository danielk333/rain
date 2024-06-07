import zmq


def rain_trigger(args):
    name = args.name
    value = args.value
    message = {
        "name": name,
        "data": value
    }

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:1793")
    socket.send_json(message, 0)
