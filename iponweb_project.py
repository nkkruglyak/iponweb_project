import random
from itertools import chain


def auction(creatives, num_of_winners, country=""):
    pass

def simple_auction_0(creatives, num_of_winners, country=""):
    winners = []
    max_of_groups = get_maximums(creatives, country)
    if len(max_of_groups) < num_of_winners:
        return []
    max_of_groups.sort(key=lambda x: -x[0].price)

    while len(winners) < num_of_winners:
        lost_winners = num_of_winners - len(winners)
        bigger_groups = []
        ind_group = 0
        bigger_price = max_of_groups[ind_group][0].price

        while ind_group < len(max_of_groups) and max_of_groups[ind_group][0].price == bigger_price:
            bigger_groups.append(max_of_groups[ind_group])
            ind_group += 1

        if ind_group > lost_winners:
            # случайно дергаем lost_winners индексов от 0 до ind_group
            # в каждой из этой группы  дергаем элемент

            # если так делать, то будет очень большая дисперсия
            # for k in range(lost_winners):
            #     ind = random.randint(0, ind_group - 1 - k)
            #     winners.append(random.choice(max_of_groups.pop(ind)))

            chained_list = list(chain(*max_of_groups))
            while len(winners) < num_of_winners:
                print(chained_list)
                all_ind = len(chained_list)
                choice_ind = random.randint(0, all_ind - 1)
                begin_ind = choice_ind
                end_ind = choice_ind

                while chained_list[begin_ind].id_of_advertiser == chained_list[choice_ind].id_of_advertiser:
                    begin_ind -= 1
                    if begin_ind < 0:
                        break
                while chained_list[end_ind].id_of_advertiser == chained_list[choice_ind].id_of_advertiser:
                    end_ind += 1
                    if end_ind > all_ind - 1:
                        break
                print(begin_ind, choice_ind,end_ind)
                winners.append(chained_list[choice_ind])
                chained_list = chained_list[:begin_ind + 1] + chained_list[end_ind:]


            break
        else:
            # из каждой группы случайно дернем элемент
            for ind in range(ind_group):
                winners.append(random.choice(max_of_groups.pop(ind)))
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

