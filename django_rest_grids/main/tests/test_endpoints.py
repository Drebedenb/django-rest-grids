from django.test import SimpleTestCase, TransactionTestCase, TestCase


class UnitTestOfEndpoints(TestCase):
    def test_valid_count(self):
        url = '/count'
        response = self.client.get(url)
        self.assertEqual(response.data['count']['count'], 686) #TODO: how to make in more beaty way?

    def test_valid_min_price(self):
        url = '/min_price'
        response = self.client.get(url)
        self.assertEqual(response.data['min_price']['min_price'], 1270) #TODO: how to make in more beaty way?

    def test_valid_max_price(self):
        url = '/max_price'
        response = self.client.get(url)
        self.assertEqual(response.data['max_price']['max_price'], 686) #TODO: how to make in more beaty way?


