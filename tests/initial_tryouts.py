import time
import os
import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import json
import os

## Tests of the time module
while True:
    # print(time.time())
    # local_time = time.localtime()
    # print(local_time)
    # utc_time = time.gmtime()
    # print(utc_time)
    # print(f'UTC Time: {utc_time[3]:02}:{utc_time[4]:02}:{utc_time[5]:02} on {utc_time[2]:02}/{utc_time[1]:02}/{utc_time[0]}')
    # print('%03i' % utc_time[1])
    # print(f'{utc_time[1]:02}')
    # print(local_time[3:6])
    # current_time = f'{local_time[3]}:{local_time[4]}:{local_time[5]}'
    # print(current_time)

    # command = 'shutdown'
    # response = 'Shutting down the server'
    # local_time = time.localtime()
    # current_time = f'{local_time[3]}:{local_time[4]}:{local_time[5]}'
    # feedback = {"command": command,
    #             "response": response,
    #             "time": current_time}
    #
    # print(feedback)
    # for item in feedback:
    #     print(item)
    #     print(feedback[item])
    # print(feedback["command"])
    #
    # print('{')
    # for item in feedback:
    #     print(f'    {item}: {feedback[item]}')
    # print('}')
    break

## Test of the path method
while True:
    # home = os.path.dirname(__file__)
    # print(home)
    # dir_pub = os.path.join(home, 'public_keys')
    # dir_prv = os.path.join(home, 'private_keys')
    # print(dir_pub)
    # print(dir_prv)
    break

## Copy of the ironhouse code
while True:
    # base_dir = os.path.dirname(__file__)
    # keys_dir = os.path.join(base_dir, 'certificates')
    # public_keys_dir = os.path.join(base_dir, 'public_keys')
    # secret_keys_dir = os.path.join(base_dir, 'private_keys')
    #
    # ctx = zmq.Context.instance()
    #
    # # Start an authenticator for this context.
    # auth = ThreadAuthenticator(ctx)
    # auth.start()
    # auth.allow('127.0.0.1')
    # # Tell authenticator to use the certificate in a directory
    # auth.configure_curve(domain='*', location=public_keys_dir)
    #
    # server = ctx.socket(zmq.PUSH)
    #
    # server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
    # server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
    # server.curve_secretkey = server_secret
    # server.curve_publickey = server_public
    # server.curve_server = True  # must come before bind
    # server.bind('tcp://*:10000')
    #
    # client = ctx.socket(zmq.PULL)
    #
    # # We need two certificates, one for the client and one for
    # # the server. The client must know the server's public key
    # # to make a CURVE connection.
    # client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
    # client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
    # client.curve_secretkey = client_secret
    # client.curve_publickey = client_public
    #
    # server_public_file = os.path.join(public_keys_dir, "server.key")
    # server_public, _ = zmq.auth.load_certificate(server_public_file)
    # # The client must know the server's public key to make a CURVE connection.
    # client.curve_serverkey = server_public
    # client.connect('tcp://127.0.0.1:10000')
    #
    # server.send(b"Hello")
    #
    # print(client.recv())
    #
    # # stop auth thread
    # auth.stop()
    break

## Tests of the json module
while True:
    # object = {'4': 5, '6': 7}
    # # test = json.dumps({'4': 5, '6': 7}, sort_keys=False, indent=4)
    # test = json.dumps(object)
    # print(test)
    # print(type(test))
    #
    # output = json.loads(test)
    # print(output)
    # print(type(output))
    break

## Tests of removing files from a directory
while True:
    # open('test.txt', 'w')
    # os.remove('test.txt')
    break

## Tests of loading the certificates
while True:
    home = os.path.dirname(__file__)
    dir_secret = os.path.join(home, 'infra_secret')
    private_file = os.path.join(dir_secret, "test.private")
    print(private_file)
    key_pub, key_prv = zmq.auth.load_certificate(private_file)
    print(key_pub)
    print(key_prv)
    break
