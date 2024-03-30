def generate_static(path, name, key, gen_time):
    with open(f'{path}/{name}.info', 'w') as static:
        static.write(f'#   {name.upper()}\n\n')
        static.write('#   Contact Name:\n')
        static.write('#   Contact Address:\n')
        static.write('#   Coordinates:\n')

        static.write('\n' + '-------------------\n\n')

        static.write('#   Type: ZeroMQ CURVE Public Certificate\n')
        static.write(f'#   Generated: {gen_time[0]}/{gen_time[1]:02}/{gen_time[2]:02} ' +
                     f'at {gen_time[3]:02}:{gen_time[4]:02}:{gen_time[5]:02} UTC\n\n')
        static.write('curve\n')
        static.write(f'    public-key = "{key}"\n')

        static.write('\n' + '-------------------\n\n')

    return
