import random
from itertools import chain


def get_maximums(creatives, country=""):
    """
    :param creatives: [Creative(), ..] 
    :param country: string, если укзана, то только элементы с совпадающей country или неуказанной попадут в ответ
    :return: [[Creative(), ..],...], элементы внутреннего спискаимеют один id_of_advertiser 
    и имеют максимальную цену среди таких же элементов
    """
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


def get_winners_from_price_equal_groups_step_by_step(groups, count_winners):
    """
    :param groups: [[Creative(), ..],...], элементы внутреннего списка имеют один id_of_advertiser,все имеют одну price
    :param count_winners: int, число победителей
    :return: [Creative(), ..], принимает решение о выборе один-за-другим,
     поэтому выбор множества победителей выходит не равновероятным
    """
    winners = []
    chained_list = list(chain(*groups))

    shift_by_group_dict = {
        now_el[0].id_of_advertiser:
            (
                sum(len(el) for i, el in enumerate(groups) if i < j),
                sum(len(el) for i, el in enumerate(groups) if i > j)

            )
        for j, now_el in enumerate(groups)
    }

    while len(winners) < count_winners:
        choice_el = random.choice(chained_list)
        winners.append(choice_el)
        begin_ind, end_ind = shift_by_group_dict[choice_el.id_of_advertiser]
        choice_group_size = len(chained_list) - begin_ind - end_ind
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


def get_winners_from_price_equal_groups_by_groups(groups, count_winners):
    """
    :param groups: [[Creative(), ..],...], элементы внутреннего списка имеют один id_of_advertiser,все имеют одну price
    :param count_winners: int, число победителей
    :return: [Creative(), ..], принимает решение о выборе сначала группы, потом элемента в группе
    """
    winners = []
    num_group = len(groups)
    for k in range(count_winners):
        ind = random.randint(0, num_group - 1 - k)
        winners.append(random.choice(groups.pop(ind)))


def get_winners_from_price_equal_groups_by_elements(groups, count_winners):
    """
    :param groups: [[Creative(), ..],...], элементы внутреннего списка имеют один id_of_advertiser,все имеют одну price
    :param count_winners: int, число победителей
    :return: [Creative(), ..], принимает решение о выборе сразу всех победителей
    """

    chained_list = list(chain(*groups))

    while True:
        possible_winners = random.sample(chained_list, count_winners)
        if len(set(i.id_of_advertiser for i in possible_winners)) == count_winners:
            return possible_winners


def auction(creatives, count_winners, country="", get_winners=get_winners_from_price_equal_groups_by_elements):
    """
    
    :param creatives: [Creative(), ..] участиники аукциона - экземпляры модели Creative 
    :param count_winners: int, необходимое число победителей
    :param country: string, страна победителей
    :param get_winners: func, функция выбора победителей из группы равноправных
    :return: [Creative(), ..] список победителей из creatives
    """
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

        num_bigger_groups = len(bigger_groups)
        if num_bigger_groups > lost_winners:
            new_winners = get_winners(bigger_groups, lost_winners)
            winners.extend(new_winners)
            break
        else:
            new_winners = get_winners(bigger_groups, num_bigger_groups)
            winners.extend(new_winners)
    return winners
