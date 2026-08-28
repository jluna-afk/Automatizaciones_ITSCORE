import os
import sys
import time
import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys_clickable,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    copiar_y_pegar_importe_3,
    validar_mensaje_snackbar
)

class Test_PlazoFijo_Cancelacion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_cancelar_plazo_fijo(self):
        driver = self.driver

        find_and_send_keys_clickable(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys_clickable(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Plazo fijo"))
        find_and_click(driver, (By.LINK_TEXT, "Cancelación"))
        print("🔵 INGRESO AL MODULO DE PLAZO FIJO CANCELACION")

        find_and_send_keys_clickable(driver, (By.XPATH, "//input[@formcontrolname='linea']"), "11")
        print("🔵 INGRESO DE LINEA")

        find_and_click(driver, (By.XPATH, "//div[@class='col-md-2']//button[@type='button']"))
        print("🔵 CLICK LUPITA")

        find_and_send_keys_clickable(driver, (By.XPATH, "//input[@formcontrolname='documento']"), "27205799104")
        print("🔵 INGRESO DNI")    

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK BOTON BUSCAR")
        
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='AYALA GAUNA, DANIELA']"))
        print("🔵 SELECCION PLAZO FIJO")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='operacion']"))
        seleccionar_opcion_ng_select_js(driver, "cancelacion")
        print("🔵 SELECCION DE OPERACION")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='formaPago']"))
        seleccionar_opcion_ng_select_js(driver, "Cuenta a la vista")
        print("🔵 SELECCION FORMA PAGO CUENTA A LA VISTA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='cuentaDestino']"))
        seleccionar_opcion_ng_select_js(driver, "PROV. INFORMATICA")
        print("🔵 SELECCION CUENTA DESTINO")

        copiar_y_pegar_importe_3(driver)
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK BOTON ACEPTAR")

        validar_mensaje_snackbar(driver, "Plazo fijo cancelado correctamente")

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