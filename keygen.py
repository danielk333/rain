import zmq.auth
import os

home = os.path.dirname(__file__)

def new_keypair(infra_name):
    # Public and private keys are generated in two separate files
    file_pub, file_prv = zmq.auth.create_certificates(home, infra_name)

    return file_pub, file_prv
