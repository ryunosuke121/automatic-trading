import unittest

import numpy as np
from learning.num_ml import PreprocessingService


class PreprosessingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.preprocessingService = PreprocessingService("test/test.csv", 10, 3)

    def test_split_xy_data(self):
        data = np.array([[i] for i in range(100)])
        x, y = self.preprocessingService.split_xy_data(data, 10, 3)
        print(x)
        print(y)


if __name__ == "__main__":
    unittest.main()
