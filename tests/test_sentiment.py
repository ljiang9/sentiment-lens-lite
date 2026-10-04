import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentiment import analyze, scan_hits


class TestPositive(unittest.TestCase):
    def test_simple_positive_zh(self):
        r = analyze("这家餐厅菜很好吃，服务也很棒")
        self.assertEqual(r["label"], "正面")
        self.assertGreater(r["score"], 0)

    def test_simple_positive_en(self):
        r = analyze("The food here is great and the service is nice")
        self.assertEqual(r["label"], "正面")


class TestNegative(unittest.TestCase):
    def test_simple_negative_zh(self):
        r = analyze("这家店太难吃了，服务很差")
        self.assertEqual(r["label"], "负面")
        self.assertLess(r["score"], 0)

    def test_simple_negative_en(self):
        r = analyze("The service was terrible and the food is bad")
        self.assertEqual(r["label"], "负面")


class TestNegation(unittest.TestCase):
    def test_negation_flips(self):
        r = analyze("这家店不好")
        self.assertEqual(r["label"], "负面")

    def test_double_negation(self):
        r = analyze("这家店不是不好")
        self.assertEqual(r["label"], "正面")


class TestIntensifier(unittest.TestCase):
    def test_intensifier_magnifies(self):
        base = analyze("很好")["score"]
        strong = analyze("非常好")["score"]
        self.assertGreater(strong, base)
        self.assertGreater(analyze("极其好")["score"], strong)

    def test_intensifier_positive(self):
        r = analyze("非常满意")
        self.assertEqual(r["label"], "正面")


class TestNeutral(unittest.TestCase):
    def test_neutral_plain(self):
        r = analyze("今天星期二，我去超市买东西")
        self.assertEqual(r["label"], "中性")

    def test_empty(self):
        r = analyze("")
        self.assertEqual(r["label"], "中性")
        self.assertEqual(r["score"], 0.0)


class TestScan(unittest.TestCase):
    def test_hits_found(self):
        hits = scan_hits("非常好")
        kinds = {h[1] for h in hits}
        self.assertIn("intensifier", kinds)
        self.assertIn("pos", kinds)

    def test_en_word_match(self):
        hits = scan_hits("I really love it")
        terms = {h[2] for h in hits}
        self.assertIn("love", terms)
        self.assertIn("really", terms)


if __name__ == "__main__":
    unittest.main()
