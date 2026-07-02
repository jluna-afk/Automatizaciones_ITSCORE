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
    find_and_click_with_retries,
    validar_mensaje_snackbar_async_guardar_boton,
    ContadorSecuencial
)

class TestAgregarCheque(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

        self.generador_cheques = ContadorSecuencial(
            archivo_contador="contador_cheque.txt",
            min_valor=17,
            max_valor=50
        )

    def test_agregar_cheque(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click_with_retries(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵INGRESO A LA PLATAFORMA")

        find_and_click_with_retries(driver, (By.XPATH, "//span[normalize-space()='Banco']"))
        find_and_click_with_retries(driver, (By.XPATH, "//a[contains(@href, '#/banco/gestion')]"))
        print("🔵INGRESO A BANCO GESTION")

        find_and_click_with_retries(driver, (By.XPATH, "//button[@class='btn btn-outline-primary lupa']"))          
        find_and_click_with_retries(driver, (By.XPATH, "(//td[contains(text(),'45 - TELEPAGOS')])[1]"))
        print("🔵SELECCION DE CUENTA BANCARIA")

        find_and_click_with_retries(driver, (By.XPATH, "(//td[@class='d-flex justify-content-end align-items-center pr-tabla'])[1]"))
        print("🔵ABRIENDO CHEQUERA")

        find_and_click_with_retries(driver, (By.XPATH, "//button[normalize-space()='+ Agregar cheque']"))

        numero_cheque_unico = self.generador_cheques.obtener_siguiente()

        input_numero_cheque = (By.XPATH, "//tbody/tr[last()]//input[@id='numero']")
        find_and_send_keys(driver, input_numero_cheque, numero_cheque_unico)
        print("🔵INGRESANDO NUMERO CHEQUE")
        
        find_and_send_keys(driver, (By.XPATH, "//tbody/tr[last()]/td[4]//app-custom-date//input"), "31/12/2027")
        print("🔵INGRESANDO FECHA VENCIMIENTO")

        find_and_click_with_retries(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='Guardar'])[2]"))
        print("🔵CLICK BOTON GUARDAR")

        validar_mensaje_snackbar_async_guardar_boton(driver, "//button[@type='submit']", "Chequera actualizada correctamente")

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