import unittest
from models import Creative
from main import get_maximums, \
    auction, \
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

        winners = auction(self.creatives, 1)
        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')

        empty_winners = auction(self.creatives, 0)

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
        self.assertListEqual([i.id for i in max_of_groups[1]], [1],
                             'equal id elements')

    def test_auction(self):
        max_of_groups = get_maximums(self.creatives)
        max_of_groups.sort(key=lambda x: -x[0].price)
        winners = auction(self.creatives, 1)
        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')


class SomeTwoGroupsOnePrice(unittest.TestCase):
    def setUp(self):
        self.creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 1),
            Creative(2, 10, 1, "GB"),
            Creative(3, 10, 1, "FR"),
            Creative(4, 10, 1),
            Creative(5, 10, 8),
            Creative(6, 10, 8),
            Creative(7, 10, 8),
        ]
        self.count_system_test = 1000
        self.count = 1

    @unittest.skip("choice equiprobable by group, not by creatives")
    def test_equiprobable_one_winner_by_grouops(self):
        """
            этот тест не проходит так как функция get_winners_from_price_equal_groups_by_groups
            гарантирует равновероятный выбор между группами,
            а не между элементами
        """
        all_winners_id = []
        for i in range(self.count_system_test):
            winners = auction(self.creatives, self.count, get_winners_from_price_equal_groups_by_groups)
            all_winners_id.extend([j.id for j in winners])
        counter = Counter(all_winners_id)
        # print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < self.count_system_test / len(self.creatives),
                        "abs delta max and min  mean")

    def test_equiprobable_one_winner_step_by_step(self):
        """
            get_winners_from_price_equal_groups_step_by_step
            гарантирует на каждом шаге равновероятный выбор 
            поэтому тест с выбором одного победителя проходит
        """

        all_winners_id = []
        for i in range(self.count_system_test):
            winners = auction(self.creatives, self.count, get_winners_from_price_equal_groups_step_by_step)
            all_winners_id.extend([j.id for j in winners])
        counter = Counter(all_winners_id)
        # print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < self.count_system_test / len(self.creatives),
                        "abs delta max and min  mean")

    def test_equiprobable_one_winner_by_elements(self):
        """
            get_winners_from_price_equal_groups_by_elments идет по умолчани в auction
            она гарантирует равновероятный выбор всех победителей
            из множества возможных
        """
        all_winners_id_sets = []
        for i in range(self.count_system_test):
            winners = auction(self.creatives, self.count)
            all_winners_id_sets.append(tuple([j.id for j in winners]))
        counter = Counter(all_winners_id_sets)
        # print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < self.count_system_test / len(self.creatives),
                        "abs delta max and min  mean")


class ManyGroupsOnePrice(unittest.TestCase):
    def setUp(self):
        self.creatives = [
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
        self.count = 3
        self.count_system_test = 1000

    def test_equiprobable_one_winner_by_elements(self):
        """
            get_winners_from_price_equal_groups_by_elments идет по умолчани в auction
            она гарантирует равновероятный выбор всех победителей
            из множества возможных
            при другом значении аргумента get_winners
            функция auction этот тест не пройдет
        """

        all_winners_id_sets = []
        for i in range(self.count_system_test):
            winners = auction(self.creatives, self.count)
            all_winners_id_sets.append(tuple([j.id for j in winners]))
        counter = Counter(all_winners_id_sets)
        # print("counter", counter)
        values_counter = list(counter.values())
        max_counter = max(values_counter)
        min_counter = min(values_counter)
        self.assertTrue(abs(max_counter - min_counter) < self.count_system_test / len(self.creatives),
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
        winners = auction(creatives, 1, "FR")

        self.assertEqual(sum([i.price for i in winners]), max_of_groups[0][0].price,
                         'equal price')

        # тоже самое на другой стране
        max_of_groups = get_maximums(creatives, "GB")

        self.assertEqual(len(max_of_groups),
                         len(set(i.id_of_advertiser for i in creatives if i.country == "GB" or not i.country)),
                         'correct len of group list')

        self.assertListEqual([i.id for i in max_of_groups[0]], [0, 4],
                             'equal id elements')
        winners = auction(creatives, 1, "GB")

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

        winners = auction(creatives, 2, "FR")
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

        winners = auction(creatives, 2, "GB")
        self.assertEqual(sum([i.price for i in winners]),
                         sum([i[0].price for i in max_of_groups]),
                         'equal id elements')


class ManyGroupsManyPrice(unittest.TestCase):
    def setUp(self):
        self.creatives = [
            Creative(0, 10, 1),
            Creative(1, 10, 2),
            Creative(2, 10, 3, "GB"),
            Creative(3, 12, 4, "FR"),
            Creative(4, 10, 5),
            Creative(5, 10, 6),
            Creative(6, 14, 7),
            Creative(7, 10, 8),
            Creative(8, 11, 9),
            Creative(9, 10, 10),
            Creative(10, 10, 1),
            Creative(11, 10, 1),
            Creative(12, 10, 1),
            Creative(13, 14, 7),
            Creative(14, 14, 7),
            Creative(15, 14, 7),
        ]
        self.count = 4

    def test_auction(self):
        max_of_groups = get_maximums(self.creatives)
        max_of_groups.sort(key=lambda x: -x[0].price)
        winners = auction(self.creatives, self.count)
        #  этот тест пройдет так как
        #  группы победителей определяются однозначно
        self.assertEqual(sum([i.price for i in winners]),
                         sum([i[0].price for i in max_of_groups[:self.count]]),
                         'equal price')