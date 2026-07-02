import unittest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class TestEliminarCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_eliminar_cuenta_vista(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.LINK_TEXT, "Gestión"))
        print("🔵 INGRESO AL MODULO CUENTA A LA VISTA GESTION")

        find_and_click(driver, (By.XPATH, "//button[@class='btn btn-outline-primary lupa']"))
        print("🔵 CLICK EN LUPITA BUSCAR CUENTA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='apellido_nombre']"), "antonio")
        print("🔵 INGRESO NOMBRE CUENTA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='estado_id']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Pendiente")
        print("🔵 SELECCION ESTADO PENDIENTE")

        find_and_click(driver, (By.XPATH, "//button[@type='submit']"))
        print("🔵 CLICK EN BOTON BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Luna, Antonio']"))
        print("🔵 SELECCION CUENTA A LA VISTA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Eliminar']"))
        print("🔵 CLICK EN BOTON ELIMINAR")

        find_and_click(driver, (By.XPATH, "//button[@class='col-5 btn-danger-its']"))
        print("🔵 CONFIRMAR ELIMINACION")

        validar_mensaje_snackbar(driver, "Cuenta a la vista eliminada con éxito.")

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