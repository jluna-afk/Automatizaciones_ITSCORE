import unittest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click
)

class TestLoginValido(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_login_valido(self):
        driver = self.driver
        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            print("🔵 INGRESO USUARIO")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            print("🔵 INGRESO CLAVE")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
            print("🔵 CLICK BOTON INGRESAR")
            time.sleep(2)

            expected_home_url = "https://qa.itscore.its.com.ar/#/home"
      
            WebDriverWait(driver, 20).until(EC.url_to_be(expected_home_url))
            print(f"✅ Login exitoso: La URL es '{expected_home_url}'.")
        except TimeoutException:
            current_url = driver.current_url
            print(f"❌ Login fallido: La URL esperada era '{expected_home_url}', pero la actual es '{current_url}'.")
            self.fail(f"La URL no cambió a la página de inicio después del login. URL actual: {current_url}")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado durante la validación de la URL: {e}")
            self.fail(f"Error inesperado: {e}")

    def tearDown(self):
        test_fallo = False
            
        if hasattr(self._outcome, 'result'):
            errores_y_fallos = self._outcome.result.errors + self._outcome.result.failures
            for test, traceback in errores_y_fallos:
                if test == self:
                    test_fallo = True
                    break
        elif hasattr(self._outcome, 'errors'):
            for method, error in self._outcome.errors:
                if error:
                    test_fallo = True
                    break

        if test_fallo:
            nombre_test = self._testMethodName
            carpeta_screenshots = "screenshots_errores"
            
            if not os.path.exists(carpeta_screenshots):
                os.makedirs(carpeta_screenshots)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{nombre_test}_{timestamp}.png"
            ruta_completa = os.path.join(carpeta_screenshots, nombre_archivo)
            
            self.driver.save_screenshot(ruta_completa)
            print(f"\n📸 ERROR DETECTADO: Captura de pantalla guardada en -> {ruta_completa}")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()