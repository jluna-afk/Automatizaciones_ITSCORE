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
    seleccionar_opcion_ng_select,
    validar_mensaje_snackbar
)

class TestCaja_Mov_Suma(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_ingresar_movimiento_suma_caja(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO USUARIO Y CLAVE")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 CLICK BOTON INGRESAR")

        find_and_click(driver, (By.LINK_TEXT, "Caja"))
        find_and_click(driver, (By.LINK_TEXT, "Puesto"))
        print("🔵 INGRESO MODULO CAJA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='cajaAsignada']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Caja 3")
        print("🔵 SELECCION DE CAJA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='operacion']"), "1500")
        print("🔵 INGRESO CODIGO DE OPERACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='tipoPersona']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Proveedor")
        print("🔵 SELECCION TIPO DE PERSONA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='persona']"), "41656139")
        print("🔵 INGRESO NUMERO DE DOCUMENTO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='moneda']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Pesos")
        print("🔵 SELECCION DE MONEDA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Agregar']"))
        print("🔵 CLICK BOTON AGREGAR")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='importe0']"), "1000")
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK BOTON ACEPTAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ejecutar']"))
        print("🔵 CLICK BOTON EJECUTAR")
        
        validar_mensaje_snackbar(driver, "Operaciones ejecutadas exitosamente")

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