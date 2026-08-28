import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class Test_PlazoFijo_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_linea_plazo_fijo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Plazo fijo"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        print("🔵 INGRESO AL MODULO DE PLAZO FIJO PARAMETRIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcion']"), "Test Crear Linea Plazo Fijo")
        print("🔵 INGRESO DE DESCRIPCION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcionReducida']"), "Test Prueba")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaDesde']//input[@type='text']"), "10112027")
        print("🔵 INGRESO FECHA DESDE")

        input_moneda = find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='moneda']//input[@type='text']"), "Pesos")
        time.sleep(0.5)
        input_moneda.send_keys(Keys.ENTER)
        print("🔵 INGRESO MONEDA PESOS")

        find_and_click(driver, (By.XPATH, "//input[@formcontrolname='renovacionAutomatica']/following-sibling::span"))
        find_and_click(driver, (By.XPATH, "//input[@formcontrolname='actualizaInteresConCadaRenovacion']/following-sibling::span"))
        find_and_click(driver, (By.XPATH, "//input[@formcontrolname='renavacionForzada']/following-sibling::span"))
        print("🔵 CLICK EN LOS CHECKBOX DE RENOVACION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='renovaciones']"), "5")
        print("🔵 INGRESO NUMERO DE RENOVACIONES")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='capitalizaInteres']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "No")
        print("🔵 SELECCION CAPITALIZA INTERES")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='vencimiento']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día o hábil anterior")
        print("🔵 SELECCION VENCIMIENTOS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantidadMinimaDias']"), "1")
        print("🔵 INGRESO CANTIDAD MIN DE DIAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantidadMaximaDias']"), "30")
        print("🔵 INGRESO CANTIDAD MAX DE DIAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importeMinimo']"), "1000")
        print("🔵 INGRESO IMPORTE MIN")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importeMaximo']"), "5000")
        print("🔵 INGRESO IMPORTE MAX")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tnaMinima']"), "1")
        print("🔵 INGRESO TNA MIN")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tnaMaxima']"), "2.5")
        print("🔵 INGRESO TNA MAX")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        
        validar_mensaje_snackbar(driver, "Línea de plazo fijo creada correctamente")

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