import unittest
from feature_01 import ReceiptProcessor

class TestReceiptProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ReceiptProcessor()

    def test_standard_mapping(self):
        """TC-01: Standard Mapping """
        data = {"item": "Milk", "qty": 2, "price": 1.50}
        result = self.processor.process(data)
        self.assertEqual(result["total"], 3.00)

    def test_zero_quantity(self):
        """TC-02: Zero Quantity """
        data = {"item": "Bread", "qty": 0, "price": 2.00}
        result = self.processor.process(data)
        self.assertEqual(result["total"], 0.00)

    def test_missing_field(self):
        """TC-03: Missing Field [cite: 33, 38]"""
        data = {"item": "Apple", "qty": 5}
        with self.assertRaises(KeyError):
            self.processor.process(data)

    def test_negative_price(self):
        """TC-04: Negative Price [cite: 33, 37, 46]"""
        data = {"item": "Invalid", "qty": 1, "price": -10}
        with self.assertRaises(ValueError):
            self.processor.process(data)

    def test_invalid_input_type(self):
        """Logic Blueprint: Type Safety [cite: 36, 43]"""
        with self.assertRaises(TypeError):
            self.processor.process({"item": "Milk", "qty": "two", "price": 1.50})

if __name__ == '__main__':
    unittest.main()
