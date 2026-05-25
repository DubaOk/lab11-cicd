import subprocess
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:8000/index.html"
SERVER_PROCESS = None


def start_server():
    global SERVER_PROCESS
    SERVER_PROCESS = subprocess.Popen(
        ["python", "-m", "http.server", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)


def stop_server():
    global SERVER_PROCESS
    if SERVER_PROCESS:
        SERVER_PROCESS.terminate()
        SERVER_PROCESS.wait(timeout=5)
        SERVER_PROCESS = None


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


class ContactFormUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_server()

    @classmethod
    def tearDownClass(cls):
        stop_server()

    def setUp(self):
        self.driver = create_driver()
        self.driver.get(BASE_URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_page_title_and_heading(self):
        """Страница загружается с правильным заголовком."""
        self.assertEqual(self.driver.title, "Форма обратной связи")

        heading = self.wait.until(
            EC.visibility_of_element_located((By.ID, "page-title"))
        )
        self.assertEqual(heading.text, "Форма обратной связи")

    def test_form_fields_exist(self):
        """На странице присутствуют все поля формы."""
        self.assertTrue(self.driver.find_element(By.ID, "name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-btn").is_displayed())

    def test_submit_button_text(self):
        """Кнопка отправки содержит ожидаемый текст."""
        button = self.driver.find_element(By.ID, "submit-btn")
        self.assertEqual(button.text, "Отправить")

    def test_successful_form_submission(self):
        """При корректном заполнении формы показывается сообщение об успехе."""
        self.driver.find_element(By.ID, "name").send_keys("Иван")
        self.driver.find_element(By.ID, "email").send_keys("ivan@example.com")
        self.driver.find_element(By.ID, "message").send_keys("Тестовое сообщение")
        self.driver.find_element(By.ID, "submit-btn").click()

        result = self.wait.until(
            EC.visibility_of_element_located((By.ID, "result-message"))
        )
        self.assertEqual(
            result.text,
            "Спасибо! Ваше сообщение успешно отправлено.",
        )
        self.assertIn("success", result.get_attribute("class"))


if __name__ == "__main__":
    unittest.main()
