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
    find_and_send_keys_with_clear,
    find_and_click,
    seleccionar_opcion_ng_select,
    validar_mensaje_snackbar
)

class TestContabilidadMovimiento(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_ingre_movimiento_resta(self):
        driver = self.driver

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
        find_and_click(driver, (By.LINK_TEXT, "Movimientos"))
        print("🔵 INGRESO A CONTABILIDAD MOVIMIENTOS")

        find_and_click(driver, (By.XPATH, "(//input[@type='text'])[2]"))
        seleccionar_opcion_ng_select(driver, "Pesos")
        print("🔵 SELECCION MONEDA PESOS")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='operacion']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "496")
        print("🔵 SELECCION OPERACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipo_persona']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Proveedor")
        print("🔵 SELECCION TIPO PERSONA PROVEEDOR")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='persona']"), "41656139")
        print("🔵 SELECCION PERSONA")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='concepto']"), "Prueba Test")
        print("🔵 INGRESO CONCEPTO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='importe0']"), "2000")
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK BOTON ACEPTAR")
        
        validar_mensaje_snackbar(driver, "Movimiento ejecutado correctamente")

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