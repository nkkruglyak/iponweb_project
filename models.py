from collections import namedtuple

Creative_ = namedtuple('Creative', ['id', 'price', 'id_of_advertiser', 'country'])


def Creative(id, price, id_of_advertiser, country=''):
    return Creative_(id, price, id_of_advertiser, country)

