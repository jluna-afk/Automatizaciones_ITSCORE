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
    copiar_y_pegar_importe_2,
    validar_mensaje_snackbar
)

class Test_PlazoFijo_Gestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_plazo_fijo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Plazo fijo"))
        find_and_click(driver, (By.LINK_TEXT, "Gestión"))
        print("🔵 INGRESO AL MODULO DE PLAZO FIJO PARAMETRIA")

        find_and_click(driver, (By.XPATH, "//div[@class='col-md-6 pl-0']//i[@class='fas fa-search']"))
        print("🔵 INGRESO MODAL DE BUSQUEDA LINEAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='descripcion']"), "PLAZO FIJO TEST FINAL")
        print("🔵 INGRESO DESCRIPCION DE LINEA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='PLAZO FIJO TEST FINAL']"))
        print("🔵 SELECCION PLAZO FIJO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoPersona']//input[@type='text']"), "Proveedor" + Keys.ENTER)
        print("🔵 SELECCION TIPO PERSONA")
        time.sleep(0.5)

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='codigo']"), "20579910")
        print("🔵 INGRESO DNI")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaSolicitud']//input[@type='text']"), "10112027")
        print("🔵 INGRESO FECHA SOLICITUD")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importeCapital']"), "1500")
        print("🔵 INGRESO IMPORTE CAPITAL")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='plazo']"), "5")
        print("🔵 INGRESO PLAZO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tasaNominal']"), "10")
        print("🔵 INGRESO TASA NOMINAL")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='observaciones']"), "TEST AUTOMATIZADO")
        print("🔵 INGRESO OBSERVACION")      

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK CREAR PLAZO FIJO")
        
        validar_mensaje_snackbar(driver, "Plazo fijo creado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK APROBAR PLAZO FIJO")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "Plazo fijo aprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Desaprobar']"))
        print("🔵 CLICK DESAPROBAR PLAZO FIJO")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "Plazo fijo desaprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK APROBAR NUEVAMENTE PLAZO FIJO")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "Plazo fijo aprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Liquidar']"))
        print("🔵 CLICK LIQUIDAR PLAZO FIJO")

        find_and_send_keys(driver, (By.XPATH, "//div[@class='ng-select-container']//input[@type='text']"), "Cuenta a la vista" + Keys.ENTER)
        print("🔵 SELECCION FORMA DE COBRO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='cuentaOrigen']//input[@type='text']"), "PROV. INFORMATICA" + Keys.ENTER)
        print("🔵 SELECCION CUENTA")

        copiar_y_pegar_importe_2(driver)
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[@type='submit']"))
        print("🔵 CLICK ACEPTAR")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "Plazo fijo liquidado correctamente")

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