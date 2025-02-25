import unittest

from main import top3, cleans_task2, solve


class MyTestCase(unittest.TestCase):
    def test_right_task(self):
        right_result = 'Александр: 10 раз(а), Евгений: 5 раз(а), Максим: 4 раз(а)'
        funct = top3()

        self.assertMultiLineEqual(funct, right_result)

    # def test_non_empty_output(self):
    #     self.assertNotEqual(top3(), "")

    def test_right_task2(self):
        right_result = (
            "Python-разработчик с нуля - 12 месяцев\n"
            "Java-разработчик с нуля - 14 месяцев\n"
            "Fullstack-разработчик на Python - 20 месяцев\n"
            "Frontend-разработчик с нуля - 20 месяцев\n"# \n этого не должно быть
        )
        funct = cleans_task2()

        self.assertMultiLineEqual(funct, right_result)

    def test_palidroms(self):
        phrases = [
            "aba",  # палиндром
            "abc",  # не палиндром
            "a ba",  # палиндром (пробел игнорируется)
            "ab ca",  # не палиндром
            "abba"  # палиндром
        ]
        expected = ["aba", "a ba", "abba"]
        self.assertEqual(solve(phrases), expected)

if __name__ == '__main__':
    unittest.main()
