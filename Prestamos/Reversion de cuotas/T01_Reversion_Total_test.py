import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select,
    click_checkbox,
    validar_mensaje_snackbar
)

class Test_Reversion_Cuotas(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_Reversion_Cuota_Total(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Reversión de cuotas"))
        print("🔵 INGRESO AL MODULO DE REVERSION DE CUOTAS")

        find_and_click(driver, (By.XPATH, "//input[@id='numeroPrestamo']/following-sibling::button"))
        print("🔵 CLICK EN LA LUPITA NUMERO PRESTAMO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='numero_prestamo']"), "224")
        print("🔵 INGRESO NOMBRE")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        time.sleep(0.5)
        print("🔵 CLICK EN BUSCAR")
        
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='224']"))
        print("🔵 SELECCION PRESTAMO 224")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//ng-select[@id='tipoPago']"))
        seleccionar_opcion_ng_select(driver, "REVERSION TOTAL (14)")
        print("🔵 SELECCION TIPO DE REVERSION")
        time.sleep(0.5)

        click_checkbox(driver, (By.XPATH, "(//input[@formcontrolname='pagar_cuota'])[1]"))
        print("🔵 SELECCION DE CUOTA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "La operación de reversión se ha ejecutado correctamente.")


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