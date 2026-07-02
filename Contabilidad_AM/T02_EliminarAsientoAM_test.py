import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    validar_mensaje_snackbar
)

class TestAsientosManuales(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_eliminar_asiento_manual(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 CLICK BOTON INGRESAR")

        find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Asientos manuales"))
        print("🔵 INGRESO AL MODULO ASIENTOS MANUALES")

        find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative']//button[@type='button']"))
        print("🔵 CLICK EN FILTRO DE BUSQUEDA")

        find_and_send_keys(driver, (By.XPATH, "(//input[@id='concepto'])[2]"), "prueba automatizada")
        print("🔵 INGRESO CONCEPTO EN FILTRO DE BUSQUEDA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BOTON BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Prueba Automatizada']"))
        print("🔵 SELECCION DEL ASIENTO MANUAL CREADO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Eliminar']"))
        print("🔵 CLICK EN ELIMINAR")

        find_and_click(driver, (By.XPATH, "//button[@class='col-5 btn-danger-its']"))
        print("🔵 CONFIRMACION DE ELIMINACION")
        validar_mensaje_snackbar(driver, "Asiento contable manual eliminado exitosamente")

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
    unittest.main(argv=['first-arg-is-ignored'], exit=False)