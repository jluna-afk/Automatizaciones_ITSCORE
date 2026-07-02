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

class TestCuentaVistaGestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_cuenta_vista(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.LINK_TEXT, "Gestión"))
        print("🔵 INGRESO AL MODULO DE CUENTA A LA VISTA GESTION")

        find_and_click(driver, (By.XPATH, "(//input[@type='text'])[1]"))
        seleccionar_opcion_ng_select_js(driver, "PROV AGUA")
        print("🔵 SELECCION DE LINEA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='tipoPersona']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Proveedor")
        print("🔵 SELECCION TIPO PERSONA")

        find_and_click(driver, (By.XPATH, "//input[@id='persona']"))
        print("🔵 CLICK EN LUPITA BUSCAR PERSONA")
        
        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_apellido_nombre']"), "Antonio")
        print("🔵 INGRESO NOMBRE PERSONA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BOTON BUSCAR")

        find_and_click(driver, (By.XPATH, "//tr[@class='clickable']"))
        print("🔵 SELECCION DE PERSONA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN BOTON CREAR")

        find_and_click(driver, (By.XPATH, "//button[@class='col-5 btn-primary-its']"))
        print("🔵 CONFIRMAR CREACION")
        
        validar_mensaje_snackbar(driver, "Cuenta a la vista creada con exito.")

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