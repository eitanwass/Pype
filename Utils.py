def parse_addr(addr):
    return str(addr).split(':')


def get_addrs_from_file(file):
    addrs = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if not any(line[0] is item for item in ['/', '\n']):
               addrs.append(parse_addr(line))
    return addrs