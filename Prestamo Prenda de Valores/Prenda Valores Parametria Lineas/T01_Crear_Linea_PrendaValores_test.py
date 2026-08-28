import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    Checkbox_Xpath,
    validar_mensaje_snackbar
)

class Test_PrendaValores_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_linea_prenda_valores(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Prést. con prenda valores"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRENDA VALORES PARAMETRIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcion']"), "Test Crear Linea Prestamo")
        print("🔵 INGRESO DE DESCRIPCION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcionReducida']"), "TestPrueba")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='vigenciaDesde']//input[@type='text']"), "10112027")
        print("🔵 INGRESO FECHA DESDE")

        input_moneda = find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='moneda']//input[@type='text']"), "Pesos")
        time.sleep(0.5)
        input_moneda.send_keys(Keys.ENTER)
        print("🔵 INGRESO MONEDA PESOS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantMinCuotas']"), "1")
        print("🔵 INGRESO CANTIDAD MIN CUOTAS")
        
        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantMaxCuotas']"), "6")
        print("🔵 INGRESO CANTIDAD MAX CUOTAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='valorMinimo']"), "1000")
        print("🔵 INGRESO IMPORTE MIN")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='valorMaximo']"), "10000")
        print("🔵 INGRESO IMPORTE MAX")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='plazoMaximo']"), "365")
        print("🔵 INGRESO PLAZO MAX")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantDiasDesde']"), "1")
        print("🔵 INGRESO PLAZO DESDE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantDiasHasta']"), "6")
        print("🔵 INGRESO PLAZO HASTA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tna']"), "5")
        print("🔵 INGRESO TNA")

        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Asociado Activo']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Asociado Adherente']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Asociado externo']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Asociado Honorario']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Banco']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Beneficiario']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Cotitular']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Entidad de cobro']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Participantes']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Proveedor']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Vendedor']/preceding-sibling::span[@class='checkmark']"))
        print("🔵 CLICK EN LOS CHECKBOX")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        
        validar_mensaje_snackbar(driver, "Línea creada correctamente")

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
            
            nombre_archivo = f"{nombre_test}.png"
            ruta_completa = os.path.join(carpeta_screenshots, nombre_archivo)
            
            self.driver.save_screenshot(ruta_completa)
            print(f"\n📸 ERROR DETECTADO: Captura de pantalla guardada en -> {ruta_completa}")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)