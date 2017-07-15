import unittest
from models import Creative
from iponweb_project import get_maximums, \
    simple_auction_0, \
    get_winners_from_price_equal_groups_by_elments, \
    get_winners_from_price_equal_groups_by_groups, \
    get_winners_from_price_equal_groups_step_by_step
from collections import Counter


class SingleGroupTest(unittest.TestCase):
    def setUp(self):
        """
            каждый участник (объект класса Сreative) имеет один и тот же id_of_advertiser
        """

        self.creatives = [
            Creative(0, 10, 0),
            Creative(1, 5, 0),
            Creative(2, 10, 0, "GB")
        ]

    def test_get_maximums(self):
        """
            get_maximums вернет список из одного списка
            внутренний список состоит из двух участников
        """
        max_of_groups = get_maximums(self.creatives)
        self.assertEqual(len(max_of_groups), len(set(i.id_of_advertiser for i in self.creatives)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 2],
                             'equal id elements')

    def test_get_winners_from_bigger_groups(self):
        """
        :return: 
        """
        max_of_groups = get_maximums(self.creatives)
        max_of_groups.sort(key=lambda x: -x[0].price)
        bigger_groups = [max_of_groups[0]]
        winners = get_winners_from_price_equal_groups_step_by_step(bigger_groups, 1)
        self.assertEqual(sum([i.price for i in winners]), bigger_groups[0][0].price,
                         'equal price')

    def test_auction(self):
        """
            один победитель из участников будет иметь максимальную цену из цен участников
            ноль победителей - это пустой список
        """
        max_of_groups = get_maximums(self.creatives)

        winners = simple_auction_0(self.creatives, 1)
        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')

        empty_winners = simple_auction_0(self.creatives, 0)

        self.assertListEqual([i.id for i in empty_winners], [],
                             'equal id elements')


class TwoGroupsTest(unittest.TestCase):
    def setUp(self):
        self.creatives = [
            Creative(0, 10, 0),
            Creative(1, 12, 1),
            Creative(2, 10, 0, "GB"),
            Creative(3, 9, 1, "FR")
        ]


class SimpleAuctionTest(unittest.TestCase):

    def test_two_group_with_id_of_advertiser(self):
        """
        среди участников (объект класса Сreative) есть 2 разных id_of_advertiser
        get_maximums вернет список из 2х списков
        первый будет содержать 2 элемента с максимальной ценой в своей группе
        второй список содержит только один максимум

        три победителя нельзя найти в этом списке участников - это пустой список
        два победителя имеют в сумме цену, равную сумме цен максимумов групп
        """
        creatives = [
            Creative(0, 10, 0),
            Creative(1, 12, 1),
            Creative(2, 10, 0, "GB"),
            Creative(3, 9, 1, "FR")
        ]

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

    def test_some_small_groups_with_one_price(self):
        """
        many groups

        """
        creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 2),
            Creative(2, 10, 3, "GB"),
            Creative(3, 10, 4, "FR"),
            Creative(4, 10, 5),
        ]
        count = 3
        winners = simple_auction_0(creatives, count)

    def test_some_different_groups_with_one_price(self):
        """
        many groups
        
        """
        creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 1),
            Creative(2, 10, 3, "GB"),
            Creative(3, 10, 4, "FR"),
            Creative(4, 10, 4, "FR"),
            Creative(5, 10, 5),
            Creative(6, 10, 5),
            Creative(7, 10, 5),

        ]
        count = 3
        winners = simple_auction_0(creatives, count)


class ProbableAuctionTest(unittest.TestCase):
    def test_equiprobable_in_groups(self):
        """
        все элементы из разных группы
        найдем 1000 раз победителей и посчитаем суммарное число вхождений каждого участника
        тест порйдет для любой из get_winners
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
            winners = simple_auction_0(creatives, count, get_winners_from_price_equal_groups_by_groups)
            all_winners_id.extend([j.id for j in winners])

        counter = Counter(all_winners_id)
        print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < count_system_test / len(creatives),
                        "abs delta max and min  mean")

    def test_equiprobable_in_two_groups(self):
        """
                элементы из 2х группы
                найдем 1000 раз победителей и посчитаем суммарное число вхождений каждого участника
                тест не пройдет для любой из get_winners_from_price_equal_groups_by_groups
                и пройдет для всех других
                """
        count_system_test = 1000
        creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 1),
            Creative(2, 10, 1, "GB"),
            Creative(3, 10, 1, "FR"),
            Creative(4, 10, 1),
            Creative(5, 10, 8),
            Creative(6, 10, 8),
            Creative(7, 10, 8),
        ]
        count = 1

        all_winners_id = []
        for i in range(count_system_test):
            winners = simple_auction_0(creatives, count, get_winners_from_price_equal_groups_step_by_step)
            all_winners_id.extend([j.id for j in winners])

        counter = Counter(all_winners_id)
        print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < count_system_test / len(creatives),
                        "abs delta max and min  mean")

    # @unittest.skip("choice equiprobable by group, not by creatives")
    def test_equiprobable_in_different_and_same_groups(self):
        """
        есть несколько групп они содержат разное число элемнетов
        найдем count раз победителей и посчитаем суммарное число вхождений каждого участника
        пройдет только для get_winners_from_price_equal_groups_by_elments
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

        count = 3
        all_winners_id_sets = []

        # winners = simple_auction_0(creatives, count)

        for i in range(count_system_test):
            winners = simple_auction_0(creatives, count)
            sorted_id = tuple(sorted([j.id for j in winners]))
            all_winners_id_sets.append(sorted_id)

        counter = Counter(all_winners_id_sets)
        print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) / 2 < count_system_test / len(creatives),
                        "abs delta max and min  mean")


class CountryAuctionTest(unittest.TestCase):
    def test_one_group_with_id_of_advertiser(self):
        """
        если третий аргумент "FR", возможных победителей 2: с айди 1 и 2
        если третий аргумент "GB", возможных победителей 2: с айди 0 и 4
        """

        creatives = [
            Creative(0, 10, 0, "GB"),
            Creative(1, 5, 0, "FR"),
            Creative(2, 5, 0),
            Creative(3, 7, 0, "GB"),
            Creative(4, 10, 0, "GB")
        ]

        max_of_groups = get_maximums(creatives, "FR")

        self.assertEqual(len(max_of_groups),
                         len(set(i.id_of_advertiser for i in creatives if i.country == "FR" or not i.country)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [1, 2],
                             'equal id elements')
        winners = simple_auction_0(creatives, 1, "FR")

        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')

        # тоже самое на другой стране
        max_of_groups = get_maximums(creatives, "GB")

        self.assertEqual(len(max_of_groups),
                         len(set(i.id_of_advertiser for i in creatives if i.country == "GB" or not i.country)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 4],
                             'equal id elements')
        winners = simple_auction_0(creatives, 1, "GB")

        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')

    def test_two_group_with_id_of_advertiser(self):
        """
        среди участников (объект класса Сreative) есть 2 разных id_of_advertiser
        get_maximums вернет список из 2х списков
        первый будет содержать 2 элемента с максимальной ценой в своей группе
        второй список содержит только один максимум

        три победителя нельзя найти в этом списке участников - это пустой список
        два победителя имеют в сумме цену, равную сумме цен максимумов групп
        """
        creatives = [
            Creative(0, 10, 0),
            Creative(1, 12, 1),
            Creative(2, 24, 0, "GB"),
            Creative(3, 9, 1, "FR"),
            Creative(4, 10, 0)

        ]

        max_of_groups = get_maximums(creatives, "FR")

        self.assertEqual(len(max_of_groups),
                         len(set(i.id_of_advertiser for i in creatives if i.country == "FR" or not i.country)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 4],
                             'equal id elements in first')

        self.assertListEqual([i.id for i in max_of_groups[1]], [1],
                             'equal id elements in first')

        winners = simple_auction_0(creatives, 2, "FR")
        self.assertEqual(sum([i.price for i in winners]),
                         sum([i[0].price for i in max_of_groups]),
                         'equal id elements')

        #  тоже самое для другой страны

        max_of_groups = get_maximums(creatives, "GB")

        self.assertEqual(len(max_of_groups),
                         len(set(i.id_of_advertiser for i in creatives if i.country == "GB" or not i.country)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [2],
                             'equal id elements in first')

        self.assertListEqual([i.id for i in max_of_groups[1]], [1],
                             'equal id elements in first')

        winners = simple_auction_0(creatives, 2, "GB")
        self.assertEqual(sum([i.price for i in winners]),
                         sum([i[0].price for i in max_of_groups]),
                         'equal id elements')
