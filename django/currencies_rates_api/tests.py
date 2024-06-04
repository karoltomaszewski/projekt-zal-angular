import unittest
from datetime import date
from currencies_rates_api.models import CurrencyRate

class CurrencyRateModelTestCase(unittest.TestCase):
    def test_currency_rate_creation(self):
        currency_rate = CurrencyRate.objects.create(
            currency_symbol='USD',
            rate=1.2345,
            date=date.today()
        )
        self.assertEqual(currency_rate.currency_symbol, 'USD')
        self.assertAlmostEqual(currency_rate.rate, 1.2345, places=4)
        self.assertEqual(currency_rate.date, date.today())

if __name__ == '__main__':
    unittest.main()
