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
    copiar_y_pegar_importe_6,
    validar_mensaje_snackbar
)

class Test_Prestamos_Cancelacion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_Cancelacion_Prestamo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Cancelación"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS CANCELACION")

        find_and_click(driver, (By.XPATH, "//input[@id='numeroPrestamo']/following-sibling::button"))
        print("🔵 CLICK EN LA LUPITA NUMERO PRESTAMO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='documento']"), "17635085")
        print("🔵 INGRESO NUMERO DOCUMENTO")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        time.sleep(0.5)
        print("🔵 CLICK EN BUSCAR")
        
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='COUDSI, SERGIO OMAR']"))
        print("🔵 SELECCION PRESTAMO DE OMAR COUDSI")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='operacion']"))
        seleccionar_opcion_ng_select(driver, "CANCELACION POR TERCERO (7)")
        print("🔵 SELECCION TIPO DE CANCELACION")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='formaPago']"))
        seleccionar_opcion_ng_select(driver, "Transferencia")
        print("🔵 SELECCION DE FORMA DE PAGO TRANSFERENCIA")

        find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative w-100']//i[@class='fas fa-search']"))
        find_and_click(driver, (By.XPATH, "//div[@class='col-md-2']//ng-select[@id='operacion']"))
        seleccionar_opcion_ng_select(driver, "TRANSFERENCIA RECIBIDA A IMPUTAR - (507)")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='08/05/2025']"))
        print("🔵 SELECCION DE OPERACION A IMPUTAR")
        
        copiar_y_pegar_importe_6(driver)
        print("🔵 INGRESO IMPORTE")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")
        time.sleep(0.5)

        validar_mensaje_snackbar(driver, "Operación ejecutada exitosamente")


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