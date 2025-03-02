import time
import unittest
import configparser
import requests

from main import top3, cleans_task2, solve



class MyTestCase(unittest.TestCase):
    def test_right_task(self):
        # тут больше и не придумаешь нормальных, когда должен быть конкретный ответ
        right_result = 'Александр: 10 раз(а), Евгений: 5 раз(а), Максим: 4 раз(а)'
        funct = top3()

        self.assertMultiLineEqual(funct, right_result)

    # def test_non_empty_output(self):
    #     self.assertNotEqual(top3(), "")

    def test_right_task2(self):
        # и тут тоже
        right_result = (
            "Python-разработчик с нуля - 12 месяцев\n"
            "Java-разработчик с нуля - 14 месяцев\n"
            "Fullstack-разработчик на Python - 20 месяцев\n"
            "Frontend-разработчик с нуля - 20 месяцев\n"# \n этого не должно быть
        )
        funct = cleans_task2()

        self.assertMultiLineEqual(funct, right_result)

    def test_palidroms(self):
        # тут конечно чучуть интереснее
        phrases = [
            "aba",  # палиндром
            "abc",  # не палиндром
            "a ba",  # палиндром (пробел игнорируется)
            "ab ca",  # не палиндром
            "abba"  # палиндром
        ]
        expected = ["aba", "a ba", "abba"]
        self.assertEqual(solve(phrases), expected)
class TestYandexDiskPath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = configparser.ConfigParser()
        config.read('setting.ini')
        cls.token = config['TOKEN']['yandex_token']
        cls.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        cls.headers = {"Authorization": f"OAuth {cls.token}"}

    def setUp(self):
        # Генерируем уникальное имя папки для каждого теста
        self.folder_name = "test_folder_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.params = {'path': self.folder_name}

    def tearDown(self):
        # Удаляем папку после теста, если она существует
        requests.delete(self.base_url, headers=self.headers, params=self.params)
        time.sleep(1)

    def test_create_path(self):
        """Тест создания папки"""
        response = requests.put(self.base_url, headers=self.headers, params=self.params)
        self.assertIn(response.status_code, [200, 201],
                      f"При успешном создании папки ожидается код 200 или 201, получен {response.status_code}")

        # Проверяем, что папка появилась в списке
        response_get = requests.get(self.base_url, headers=self.headers, params=self.params)
        self.assertEqual(response_get.status_code, 200,
                         "После создания папки она должна присутствовать в списке (код 200)")

    def test_double_create(self):
        """Тест повторного создания уже существующей папки"""
        # Первое создание
        response1 = requests.put(self.base_url, headers=self.headers, params=self.params)
        self.assertIn(response1.status_code, [200, 201],
                      f"Первичное создание папки должно вернуть 200 или 201, получен {response1.status_code}")

        # Второе создание (ожидаем ошибку 409)
        response2 = requests.put(self.base_url, headers=self.headers, params=self.params)
        self.assertEqual(response2.status_code, 409,
                         f"Повторное создание папки должно вернуть 409, получен {response2.status_code}")

    def test_delete_path(self):
        """Тест удаления существующей папки"""
        # Сначала создаём папку
        response_create = requests.put(self.base_url, headers=self.headers, params=self.params)
        self.assertIn(response_create.status_code, [200, 201],
                      f"Создание папки должно вернуть 200 или 201, получен {response_create.status_code}")

        # Проверяем, что папка существует
        response_get = requests.get(self.base_url, headers=self.headers, params=self.params)
        self.assertEqual(response_get.status_code, 200,
                         "Созданная папка должна присутствовать в списке (код 200)")

        # Удаляем папку
        response_del = requests.delete(self.base_url, headers=self.headers, params=self.params)
        self.assertIn(response_del.status_code, [200, 202, 204],
                      f"Удаление папки должно вернуть 200, 202 или 204, получен {response_del.status_code}")

        # Небольшая задержка для асинхронного удаления
        time.sleep(1)
        response_get_after = requests.get(self.base_url, headers=self.headers, params=self.params)
        self.assertNotEqual(response_get_after.status_code, 200,
                            "После удаления папка не должна присутствовать в списке (код 200)")

if __name__ == '__main__':
    unittest.main()
