import zmq.auth
import time

def new_keypair(path, name):
    # Public and private keys are generated in two separate files
    file_pub, file_prv = zmq.auth.create_certificates(path, name)
    gen_time = time.gmtime()

    return file_pub, file_prv, gen_time

def key_detect(key_file):
    with open(key_file, 'r') as in_file:
        row_found = False
        while not row_found:
            line = in_file.readline()
            if line[0:5] == 'curve':
                row_found = True
                key = []
                for item in range(2):
                    line = in_file.readline()
                    pos = []
                    for iter in range(len(line)):
                        if line[iter] == '"':
                            pos.append(iter)
                    key.append(line[pos[0]+1: pos[1]])
                    item =+ 1

    return key[0], key[1]
