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
    find_and_click_with_scroll,
    seleccionar_opcion_ng_select_with_filter,
    validar_mensaje_snackbar
)

class TestAsientosAutomaticos(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_asiento_monedas_distintas(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 CLICK BOTON INGRESAR")

        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Contabilidad"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Asientos automáticos"))
        print("🔵 INGRESO AL MODULO ASIENTOS AUTOMATICOS")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "(//input[@type='text'])[1]"), "Banco")
        print("🔵 SELECCION OPERATORIA")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "//ng-select[@formcontrolname='operacion_id']//input[@type='text']"), "DEBITO POR MOVIMIENTO ENTRE CUENTAS")
        print("🔵 SELECCION OPERACION")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "//ng-select[@class='form-select ng-select-custom ng-select-searchable ng-select ng-select-single ng-untouched ng-pristine ng-invalid']//input[@type='text']"), "1 BANCO BBVA ARGENTINA S.A.")
        print("🔵 SELECCION LINEA")

        find_and_send_keys(driver, (By.XPATH, "//input[@class='form-control form-control-sm text-left pl-2']"), "21082025")
        print("🔵 INGRESO FECHA")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))
        print("🔵 CLICK EN AGREGAR IMPORTE")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "(//input[@type='text'])[6]"), "IMPORTE")
        print("🔵 SELECCION TIPO IMPORTE")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='numeroCuenta']"), "1.1.1.01.01.01")
        print("🔵 INGRESO CUENTA HABER")
        
        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "(//input[@type='text'])[9]"), "+")
        print("🔵 SELECCION SIGNO +")
        
        find_and_click_with_scroll(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/label[1]/span[1]"))
        print("🔵 CLICK EN CHECK DE IMPORTE HABER")
        
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))
        print("🔵 CLICK EN AGREGAR IMPORTE")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "(//input[@type='text'])[10]"), "IMPORTE")
        print("🔵 SELECCION TIPO IMPORTE")

        find_and_send_keys(driver, (By.XPATH, "//tr[@class='ng-invalid ng-touched ng-dirty']//input[@id='numeroCuenta']"), "1.1.5.01.01.01")
        print("🔵 INGRESO CUENTA DEBE")

        seleccionar_opcion_ng_select_with_filter(driver, (By.XPATH, "(//input[@type='text'])[13]"), "+")
        print("🔵 SELECCION SIGNO +")

        find_and_click_with_scroll(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[2]/td[6]/div[1]/label[1]/span[1]"))
        print("🔵 CLICK EN CHECK DE IMPORTE DEBE")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")

        validar_mensaje_snackbar(driver, "Todas las cuentas deben pertenecer a la misma moneda.")

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