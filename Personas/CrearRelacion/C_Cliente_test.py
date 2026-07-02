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
    validar_mensaje_snackbar_async_guardar
)

class TestCrearRelacionCliente(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_cliente(self):
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

        find_and_click(driver,(By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Cliente']]"))
        print("🔵 CLICK EN LA CARD CLIENTE")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoCliente']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Asociado Activo")
        print("🔵 SELECCION DE TIPO CLIENTE")

        find_and_click(driver,(By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        find_and_click(driver,(By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[1]"))
        print("🔵 CLICK EN AGREGAR")
        
        find_and_click(driver, (By.XPATH, "//div[@class='selector']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "IMPUESTO AL VALOR AGREGADO")
        print("🔵 SELECCION TIPO SITUACION")
        time.sleep(1)

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='subTipo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "RESPONSABLE INSCRIPTO")
        print("🔵 SELECCION SUBTIPO")
        time.sleep(1)

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='clase']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "TASA GENERAL")
        print("🔵 SELECCION CLASE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='numeroInscripcion']"), "123456")
        print("🔵 N° INSCRIPCION")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='pais']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ARGENTINA")
        print("🔵 SELECCION PAIS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='provincia']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "SANTA FE")
        print("🔵 SELECCION PROVINCIA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='localidad']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ROSARIO")
        print("🔵 SELECCION LOCALIDAD")

        find_and_click(driver,(By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[2]"))
        print("🔵 CLICK BOTON AGREGAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ITS CORE")
        print("🔵 SELECCION GRUPO AFINIDAD")

        find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative']//button[@type='button']"))
        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_apellido_nombre']"), "1pruebas, No Usar")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='1pruebas, No Usar']"))
        print("🔵 SELECCION PRINCIPAL GRUPO FAMILIAR")

        find_and_click(driver, (By.XPATH, "//body/div[@class='cdk-overlay-container']/div[@class='cdk-global-overlay-wrapper']/div[@id='cdk-overlay-1']/mat-dialog-container[@id='mat-mdc-dialog-1']/div[@class='mdc-dialog__container']/div[@class='mat-mdc-dialog-surface mdc-dialog__surface']/app-cliente[@class='mat-mdc-dialog-component-host']/div[@class='page-container modal-container']/div/div[4]/button[1]"))
        print("🔵 CLICK AGREGAR")

        find_and_click(driver, (By.XPATH, "//div[@class='col-md-5 pl-0']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Hermano/a")
        print("🔵 SELECCION TIPO PARENTESCO")

        find_and_click(driver, (By.XPATH, "//div[@class='col-md-7 pr-0']//button[@type='button']"))
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='RAPUZZI, FERNANDO LUIS']"))
        print("🔵 SELECCION PERSONA FAMILIAR")
        
        validar_mensaje_snackbar_async_guardar(driver, "//div[@class='mb-3 d-flex justify-content-end form-actions buttons']//button[@type='button'][normalize-space()='Guardar']", "Relación de cliente modificada con éxito")
            
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