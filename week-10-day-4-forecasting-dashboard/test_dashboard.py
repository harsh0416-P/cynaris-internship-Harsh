import unittest
import numpy as np
from data_loader import load_data


class TestForecastDashboard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.listings, cls.monthly, cls.forecast, cls.evaluation = load_data()

    def test_listing_dataset(self):
        self.assertEqual(len(self.listings), 600)
        self.assertFalse(self.listings.isnull().any().any())

    def test_monthly_history(self):
        self.assertEqual(len(self.monthly), 24)
        self.assertTrue(self.monthly["month"].is_monotonic_increasing)

    def test_forecast_data(self):
        self.assertGreaterEqual(len(self.forecast), 27)
        self.assertTrue(
            {"ds", "yhat", "yhat_lower", "yhat_upper"}
            .issubset(self.forecast.columns)
        )
        self.assertTrue(
            (self.forecast["yhat_lower"] <= self.forecast["yhat_upper"]).all()
        )

    def test_evaluation_data(self):
        self.assertEqual(len(self.evaluation), 3)

    def test_evaluation_metrics(self):
        actual = self.evaluation["Actual Price (Lakh)"].to_numpy()
        predicted = self.evaluation["Predicted Price (Lakh)"].to_numpy()

        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        self.assertAlmostEqual(mae, 20.276, places=2)
        self.assertAlmostEqual(rmse, 26.324, places=2)
        self.assertAlmostEqual(mape, 10.75, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
