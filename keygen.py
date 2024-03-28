import zmq.auth
import os
import time

home = os.path.dirname(__file__)

def new_keypair(infra_name):
    # Public and private keys are generated in two separate files
    file_pub, file_prv = zmq.auth.create_certificates(home, infra_name)
    gen_time = time.gmtime()

    return file_pub, file_prv, gen_time
