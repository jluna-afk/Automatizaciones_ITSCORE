import unittest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje
)

class TestCrearRelacionProveedor(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_proveedor(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A ITS CORE")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
        find_and_click(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
        print("🔵 INGRESO AL MODULO")

        find_and_click(driver, (By.XPATH, "//button[@class='btn btn-outline-primary- lupa']"))
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='1pruebas, No Usar']"))
        print("🔵 SELECCION PERSONA")

        locator_tarjeta_proveedor = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Proveedor']]")
        find_and_click(driver, locator_tarjeta_proveedor)
        time.sleep(1)
        print("🔵 CLICK CARD")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        validar_mensaje(driver, "Relación creada con éxito")

        find_and_click(driver, (By.XPATH, "//button[@class='btn-outline-primary-its w-100 mt-2 mb-5']"))
        print("🔵 CLICK EN AGREGAR")

        find_and_click(driver, (By.XPATH, "//div[@class='selector']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "IMPUESTO AL VALOR AGREGADO")
        print("🔵 SELECCION DE TIPO")
        time.sleep(1)

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='subTipo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "RESPONSABLE INSCRIPTO")
        print("🔵 SELECCION DE SUBTIPO")
        time.sleep(1)

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='clase']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "TASA GENERAL")
        print("🔵 SELECCION DE CLASE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='numeroInscripcion']"), "123456")
        print("🔵 INGRESO N° INSCRIPCION")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='pais']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ARGENTINA")
        print("🔵 SELECCION DE PAIS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='provincia']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "SANTA FE")
        print("🔵 SELECCION DE PROVINCIA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='localidad']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ROSARIO")
        print("🔵 SELECCION DE LOCALIDAD")

        find_and_click(driver, (By.XPATH, "//button[@class='btn-outline-primary-its w-100 mt-1 mb-5']"))
        print("🔵 CLICK AGREGAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ITS CORE")
        print("🔵 SELECCION DE GRUPO AFINIDAD")

        find_and_click(driver, (By.XPATH, "//div[@class='form-actions mb-3']//button[@type='button'][normalize-space()='Guardar']"))
        print("🔵 CLICK GUARDAR")
        time.sleep(0.5)

        validar_mensaje(driver, "Relación de proveedor modificada con éxito")
            
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