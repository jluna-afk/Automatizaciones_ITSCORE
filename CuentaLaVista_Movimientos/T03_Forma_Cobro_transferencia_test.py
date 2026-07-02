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

class TestMovimientosCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_CV_forma_cobro_transferencia(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO DE CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.LINK_TEXT, "Movimientos"))
        print("🔵 INGRESO A MOVIMIENTOS DE CUENTA A LA VISTA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='linea']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "CUENTAS COMERCIALES")
        print("🔵 SELECCION DE LINEA")

        find_and_click(driver, (By.XPATH, "(//button[@type='button'])[1]"))
        print("🔵 CLICK EN LA LUPITA DE BUSQUEDA DE PERSONA")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='QUO SOLUCIONES SRL']"))
        print("🔵 SELECCION DE PERSONA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='operacion']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "COBRO DE FACTURA")
        print("🔵 SELECCION DE OPERACION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='concepto']"), "test forma cobro transf")
        print("🔵 INGRESO CONCEPTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importe']"), "1000")
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK EN CONTINUAR")

        find_and_click(driver, (By.XPATH, "//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "TRANSFERENCIA")
        print("🔵 SELECCION DE TRANSFERENCIA COMO FORMA DE COBRO")

        find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative w-100']//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LUPITA DE OPERACIONES A IMPUTAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='cuenta']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "TELEPAGOS")
        print("🔵 SELECCION DE CUENTA A IMPUTAR")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@class='ng-untouched ng-pristine ng-valid']//input[@type='text']"), "08052025")
        print("🔵 INGRESO DE FECHA")

        find_and_click(driver, (By.XPATH, "(//input[@type='text'])[29]"))
        seleccionar_opcion_ng_select_js(driver, "TRANSFERENCIA RECIBIDA A IMPUTAR")
        print("🔵 SELECCION DE OPERACION DE IMPUTACION")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='08/05/2025']"))
        print("🔵 SELECCION DE MOVIMIENTO A IMPUTAR")

        find_and_send_keys(driver, (By.XPATH, "//input[@class='text-right form-control w-100 ng-untouched ng-pristine ng-invalid']"), "1000")
        print("🔵 INGRESO IMPORTE A IMPUTAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR PARA CONFIRMAR EL MOVIMIENTO")

        validar_mensaje_snackbar(driver, "Movimiento confirmado con éxito!")

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