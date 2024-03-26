import shutil
import zmq.auth
import os

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

def new_keypair(infra_name):
    # Public and private keys are generated in two separate files
    file_pub, file_prv = zmq.auth.create_certificates(home, infra_name)

    # Put the keypair files into separate directories
    # shutil.move(os.path.join(home, file_pub), os.path.join(dir_pub, '.'))
    # shutil.move(os.path.join(home, file_prv), os.path.join(dir_prv, '.'))

    return file_pub, file_prv
