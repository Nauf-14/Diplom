import requests, json


class WebsiteTester:
    def __init__(self, url: str = "https://google.com"):
        
        # Ссылка на сатй
        self.url = url  
        
        # Цветовая политра
        self.color_code = {
            "RESET": "\033[0m",      # Сброс цвета [Стиль]
            "GREEN": "\033[32m",     # Зеленый 
            "YELLOW": "\033[93m",    # Желтый
            "RED": "\033[31m",       # Красный
            "CYAN": "\033[36m",      # Светло голубой
            "BOLD": "\033[01m"}      # Жирный [Стиль]

    def target(self):
        """Выводит цель для тестирования"""
        print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Цель тестирования:               {self.color_code["RESET"]}{self.color_code["GREEN"]}{self.url}')


    def test_load_speed(self):
        """Измеряем скорость загрузки страницы"""
        try:
            response = requests.get(self.url)
            load_time = response.elapsed.total_seconds()
            print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Скорость загрузки страницы:     {self.color_code["RESET"]}{self.color_code["GREEN"]} {load_time} сек.')
        
        except requests.exceptions.RequestException as e:
            print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка при загрузке страницы: {self.color_code["RESET"]}{self.color_code["RED"]}{e}')

    def test_accessibility(self):
        """Проверяем доступность сайта"""

        try:
            response = requests.head(self.url)
            if response.status_code == 200:
                print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Сайт:                            {self.color_code["RESET"]}{self.color_code["GREEN"]}Доступен')
            else:
                print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Сайт недоступен. Код состояния:  {self.color_code["RESET"]}{self.color_code["RED"]}{response.status_code}')
        
        except requests.exceptions.RequestException as e:
            print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка при проверке доступности сайта: {self.color_code["RESET"]}{self.color_code["RED"]}{e}')

    def test_xss(self):
        """Проверка уязвимости XSS на сайте отправки email"""
        print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}XSS-Уязвимсоти в URL:')

        xss_payloads = [
        '<script>alert("XSS1")</script>',
        '<img src="x" onerror="alert(\'XSS2\')">',
        '"><script>alert("XSS3")</script>',
        '<svg onload=alert("XSS4")>',
        '"><img src=x onerror=alert(\'XSS5\')>']

        for payload in xss_payloads:
            try:
                response = requests.get(self.url, params={'q': payload})
                if payload in response.text:
                    print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Возможно XSS уязвимость:                            {self.color_code["RESET"]}{self.color_code["GREEN"]}{payload}')
                
                else:
                    print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Полезная нагрузка не выполнена:  {self.color_code["RESET"]}{self.color_code["RED"]}{payload}')
            
            except requests.exceptions.RequestException as e:
                print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка при проверки XSS-Уязвимости: {self.color_code["RESET"]}{self.color_code["RED"]}{e}')

    def test_sql_injection(self):
        """Проверка уязвимости SQL в форме отправки email"""

        try:
            response = requests.post(self.url + "/email", json={"email": "SELECT * FROM base"}).json()
            with open("result_SQL.json", "w") as result_file: result_file.write(json.dumps(response["message"]))
            print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}SQL-Инъекция в email:            {self.color_code["RESET"]}{self.color_code["GREEN"]}Доступна, результат был сохранен в {self.color_code["RESET"]}"result_SQL.json"')
            
        except requests.exceptions.RequestException as e:
            print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка при проверки SQL-Инъекции: {self.color_code["RESET"]}{self.color_code["RED"]}{e}')

    def test_functionality(self):
        """Проверка работы формы обратной связи"""
        
        try:
            response = requests.post(self.url + "/contact", data={"name": "John", "email": "john@example.com", "message": "Test message"})
            if response.status_code == 200:
                print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Форма обратной связи:            {self.color_code["RESET"]}{self.color_code["GREEN"]}Работает корректно')
        
            else:
                print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка:                          {self.color_code["RESET"]}{self.color_code["RED"]}Форма обратной связи не работает или работает не корректно')
        
        except requests.exceptions.RequestException as e:
            print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка:                          {self.color_code["RESET"]}{self.color_code["RED"]}Форма обратной связи не работает')

    def test_seo(self):
        """Проверка правильности использования метатегов"""
        try:
            response = requests.get(self.url)
            if "<title>" in response.text:
                print(F'{self.color_code["CYAN"]}{self.color_code["BOLD"]}Метатег <title>:                 {self.color_code["RESET"]}{self.color_code["GREEN"]}Присутствует на главной странице')
            
            else:
                print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка:                       {self.color_code["RESET"]}{self.color_code["RED"]}Отсутствует метатег <title> на главной странице')

        except requests.exceptions.RequestException as e:
            print(F'{self.color_code["YELLOW"]}{self.color_code["BOLD"]}Ошибка:                       {self.color_code["RESET"]}{self.color_code["RED"]}Отсутствует метатег <title> на главной странице')


if __name__ == "__main__":
    tester = WebsiteTester("http://denista-center.online")
    tester.target()
    tester.test_load_speed()
    tester.test_accessibility()
    tester.test_functionality()
    tester.test_seo()
    tester.test_sql_injection()
    tester.test_xss()
