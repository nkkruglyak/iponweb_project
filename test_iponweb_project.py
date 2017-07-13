import unittest
from models import Creative
from iponweb_project import get_maximums, simple_auction_0
from collections import Counter


class SimpleAuctionTest(unittest.TestCase):
    def test_one_group_with_id_of_advertiser(self):
        """
        каждый участник (объект класса Сreative) имеет один и тот же id_of_advertiser
        get_maximums вернет список из одного списка
        внутренний список состоит из двух участников

        один победитель из участников будет иметь максимальную цену из цен участников
        ноль победителей - это пустой список
        """
        creatives = [Creative(0, 10, 0), Creative(1, 5, 0), Creative(2, 10, 0, "GB")]

        max_of_groups = get_maximums(creatives)

        self.assertEqual(len(max_of_groups), len(set(i.id_of_advertiser for i in creatives)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 2],
                             'equal id elements')
        winners = simple_auction_0(creatives, 1)

        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                             'equal price')
        empty_winners = simple_auction_0(creatives, 0)

        self.assertListEqual([i.id for i in empty_winners], [],
                             'equal id elements')

    def test_two_group_with_id_of_advertiser(self):
        """
        среди участников (объект класса Сreative) есть 2 разных id_of_advertiser
        get_maximums вернет список из 2х списков
        первый будет содержать 2 элемента с максимальной ценой в своей группе
        второй список содержит только один максимум

        три победителя нельзя найти в этом списке участников - это пустой список
        два победителя имеют в сумме цену, равную сумме цен максимумов групп
        """
        creatives = [Creative(0, 10, 0), Creative(1, 12, 1), Creative(2, 10, 0, "GB"), Creative(3, 9, 1, "FR")]

        max_of_groups = get_maximums(creatives)

        self.assertEqual(len(max_of_groups), len(set(i.id_of_advertiser for i in creatives)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 2],
                             'equal id elements in first')

        self.assertListEqual([i.id for i in max_of_groups[1]], [1],
                             'equal id elements in first')
        too_much_winners = simple_auction_0(creatives, 3)
        self.assertListEqual(too_much_winners, [],
                             'equal id elements')
        winners = simple_auction_0(creatives, 2)
        self.assertEqual(sum([i.price for i in winners]), sum([i[0].price for i in max_of_groups]),
                         'equal id elements')

    def test_many_groups(self):
        """
        почти все группы участников по id_of_advertiser
        состоят из одного элемента
        """
        creatives = [Creative(0, 10, 0),
                     Creative(1, 12, 1),
                     Creative(2, 10, 0, "GB"),
                     Creative(3, 11, 1, "FR"),
                     Creative(4, 13, 1),
                     Creative(5, 13, 2),
                     Creative(6, 14, 3),
                     Creative(7, 15, 4),
                     Creative(8, 10, 4),
                     Creative(9, 3, 4)
                     ]
        max_of_groups = get_maximums(creatives)
        self.assertEqual(len(max_of_groups), len(set(i.id_of_advertiser for i in creatives)),
                         'correct len of group list')

        max_of_groups.sort(key=lambda x: -x[0].price)
        winners = simple_auction_0(creatives, 2)
        self.assertEqual(sum([i.price for i in winners]),
                         sum([i[0].price for i in max_of_groups][:2]),
                         'equal sum price')

    def test_equiprobable_in_groups(self):
        """
        все элементы из разных группы
        найдем 100 раз победителей и посчитаем суммарное число вхождений каждого участника
        """
        count_system_test = 1000
        creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 2),
            Creative(2, 10, 3, "GB"),
            Creative(3, 10, 4, "FR"),
            Creative(4, 10, 5),
            Creative(5, 10, 6),
            Creative(6, 10, 7),
            Creative(7, 10, 8),
            Creative(8, 10, 9),
            Creative(9, 10, 10)
        ]
        count = 5
        all_winners_id = []
        for i in range(count_system_test):
            winners = simple_auction_0(creatives, count)
            all_winners_id.extend([j.id for j in winners])

        counter = Counter(all_winners_id)
        print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < count_system_test / len(creatives),
                        "abs delta max and min  mean")

    def test_equiprobable_in_different_and_same_groups(self):
        """
        есть элементы из одной группы
        найдем count раз победителей и посчитаем суммарное число вхождений каждого участника
        
        этот тест не проходит
        разброс значений при таких входных данных не получается равномерным
        пример значения counter - словарь {id: число раз был в победителях}
        """
        count_system_test = 1000
        creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 2),
            Creative(2, 10, 3, "GB"),
            Creative(3, 10, 4, "FR"),
            Creative(4, 10, 5),
            Creative(5, 10, 6),
            Creative(6, 10, 7),
            Creative(7, 10, 8),
            Creative(8, 10, 9),
            Creative(9, 10, 10),
            Creative(10, 10, 1),
            Creative(11, 10, 1),
            Creative(12, 10, 1),
            Creative(13, 10, 7),
            Creative(14, 10, 7),
            Creative(15, 10, 7),
        ]
        count = 7
        all_winners_id = []
        for i in range(count_system_test):
            winners = simple_auction_0(creatives, count)
            all_winners_id.extend([j.id for j in winners])

        counter = Counter(all_winners_id)
        print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < count_system_test / len(creatives),
                        "abs delta max and min  mean")


