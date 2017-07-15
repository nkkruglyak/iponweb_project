import random
from itertools import chain


def auction(creatives, num_of_winners, country=""):
    pass

def simple_auction_0(creatives, count_winners, country=""):
    winners = []
    max_of_groups = get_maximums(creatives, country)
    count_of_groups = len(max_of_groups)
    if count_of_groups < count_winners:
        return []
    max_of_groups.sort(key=lambda x: -x[0].price)

    while len(winners) < count_winners:
        lost_winners = count_winners - len(winners)
        bigger_groups = []
        bigger_price = max_of_groups[0][0].price

        # группы с максимальной ценой
        #  переложим в bigger_groups
        while len(max_of_groups) > 0 and max_of_groups[0][0].price == bigger_price:
            bigger_groups.append(max_of_groups.pop(0))
        # print("bigger_groups", bigger_groups)
        # print("max_of_groups", max_of_groups)

        num_bigger_groups = len(bigger_groups)
        if num_bigger_groups > lost_winners:
            # случайно дергаем lost_winners индексов от 0 до ind_group
            # в каждой из этой группы  дергаем элемент

            # если так делать, то будет очень большая дисперсия
            # for k in range(lost_winners):
            #     ind = random.randint(0, ind_group - 1 - k)
            #     winners.append(random.choice(max_of_groups.pop(ind)))
            new_winners = get_winners_from_bigger_groups(bigger_groups, lost_winners)
            winners.extend(new_winners)
            break
        else:
            # из каждой группы случайно дернем элемент
            # плохая дисперсия
            # for ind in range(num_bigger_groups):
            #     winners.append(random.choice(bigger_groups.pop(0)))
            new_winners = get_winners_from_bigger_groups(bigger_groups, num_bigger_groups)
            winners.extend(new_winners)
    return winners

def get_maximums(creatives, country=""):
    groups_by_id = dict()

    for el in creatives:
        if country and el.country and country!=el.country:
            continue
        if not groups_by_id.get(el.id_of_advertiser):
            groups_by_id[el.id_of_advertiser] = [el]
        else:
            if el.price < groups_by_id[el.id_of_advertiser][0].price:
                continue
            elif el.price == groups_by_id[el.id_of_advertiser][0].price:
                groups_by_id[el.id_of_advertiser].append(el)
            else:
                groups_by_id[el.id_of_advertiser] = [el]

    return list(groups_by_id.values())

def get_winners_from_bigger_groups(bigger_groups, count_winners):
    """
    :param bigger_groups: [[Creative, ..], ..] все элементы имеют одну цену,
    count_winners: число победителей
    :return: winners, len(winners) == count_winners
    """
    winners = []
    chained_list = list(chain(*bigger_groups))

    shift_by_group_dict = {
        now_el[0].id_of_advertiser:
            (
                sum(len(el) for i, el in enumerate(bigger_groups) if i < j),
                sum(len(el) for i, el in enumerate(bigger_groups) if i > j)

            )
        for j, now_el in enumerate(bigger_groups)
    }

    while len(winners) < count_winners:
        # print("chained list", chained_list)
        # print("shifts", shift_by_group_dict)
        choice_el = random.choice(chained_list)
        winners.append(choice_el)
        begin_ind, end_ind = shift_by_group_dict[choice_el.id_of_advertiser]
        choice_group_size = len(chained_list) - begin_ind - end_ind
        # print(choice_el.id, begin_ind, end_ind, choice_group_size)
        if end_ind == 0:
            chained_list[begin_ind:] = []
        else:
            chained_list[begin_ind: -end_ind] = []
        shift_by_group_dict = {
            key:
                (
                    el[0] - choice_group_size * (begin_ind < el[0]),
                    el[1] - choice_group_size * (end_ind < el[1])
                )
            for key, el in shift_by_group_dict.items() if el[0] != begin_ind
        }
    return winners