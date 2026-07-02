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
    validar_mensaje_snackbar_async_crear
)

class TestCrearCuentaDuplicada(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_cuenta(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        print("🔵 INGRESO USUARIO")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CLAVE")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Banco']"))
        find_and_click(driver, (By.XPATH, "//a[contains(@href, '#/banco/gestion')]"))
        print("🔵 INGRESO A BANCO GESTION")
        
        find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative']//button[@type='button']"))
        print("🔵 INGRESO A BUSQUEDA DE ENTIDAD")
        
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='TELEPAGOS']"))
        print("🔵 SELECCION DE ENTIDAD")
        
        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='moneda']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Pesos")
        print("🔵 SELECCION DE MONEDA")
        
        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipo_cuenta']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Cuenta Virtual")
        print("🔵 SELECCION DE TIPO CUENTA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cbu']"), "0000045100000000063630")
        print("🔵 INGRESO CBU")
        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='numero_cuenta']"), "0000000006363")
        print("🔵 INGRESO NUMERO CUENTA")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK BOTON CREAR")

        validar_mensaje_snackbar_async_crear(driver, "//button[normalize-space()='Aceptar']", "El CBU/CVU ya se encuentra registrado en el sistema.")

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