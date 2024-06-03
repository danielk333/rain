from .generate import gen_paths, gen_keys, gen_server_cfg, gen_client_cfg


def rain_register(args):
    ''' The top-level function handling the registration of new instruments to
        RAIN

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    path_conf, path_auth, path_host, path_pair, path_plug = gen_paths(args.cfgpath, args.keypath)
    gen_keys(args.name, path_conf, path_pair)

    gen_server_cfg(args.name, path_conf, path_auth, path_pair, path_plug)
    gen_client_cfg(args.name, path_conf, path_host, path_pair)

    return
