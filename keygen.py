import zmq.auth
import time

def new_keypair(path, name):
    # Public and private keys are generated in two separate files
    file_pub, file_prv = zmq.auth.create_certificates(path, name)
    gen_time = time.gmtime()

    return file_pub, file_prv, gen_time
