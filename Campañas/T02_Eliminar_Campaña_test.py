import unittest
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys_with_clear,
    find_and_click,
    find_and_click_via_js,
    validar_mensaje_snackbar
)

class TestCampaña(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_eliminar_campaña(self):
        driver = self.driver

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO DE LA CLAVE")
        find_and_click_via_js(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Campañas"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        print("🔵 INGRESO A LA PARAMETRIA")

        find_and_click_via_js(driver, (By.XPATH, "//button[@class='lupa btn-primary']//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='searchNombreModal']"), "CAMPAÑA PRUEBA TEST")
        print("🔵 BUSQUEDA DE LA LINEA")

        find_and_click_via_js(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")

        find_and_click_via_js(driver, (By.XPATH, "//td[normalize-space()='CAMPAÑA PRUEBA TEST']"))
        print("🔵 SELECCION DE LINEA")

        find_and_click_via_js(driver, (By.XPATH, "//button[normalize-space()='Eliminar']"))
        print("🔵 CLICK EN ELIMINAR")

        boton_eliminar_final = (By.XPATH, "//app-dialog-simple//button[contains(text(), 'Eliminar')]")
        find_and_click_via_js(driver, boton_eliminar_final)

        validar_mensaje_snackbar(driver, "Campaña eliminada correctamente.")

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
            
            nombre_archivo = f"{nombre_test}.png"
            ruta_completa = os.path.join(carpeta_screenshots, nombre_archivo)
            
            self.driver.save_screenshot(ruta_completa)
            print(f"\n📸 ERROR DETECTADO: Captura de pantalla guardada en -> {ruta_completa}")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)