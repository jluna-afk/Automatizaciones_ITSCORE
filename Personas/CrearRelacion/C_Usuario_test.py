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
    click_con_js,
    seleccionar_opcion_ng_select_js,
    validar_mensaje
)

class TestCrearRelacionUsuario(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_relacion_usuario(self):
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
        print("🔵 SELECCION DE LA PERSONA")

        locator_tarjeta_usuario = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Usuario']]")
        find_and_click(driver, locator_tarjeta_usuario)
        print("🔵 CLICK EN LA CARD")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='usuario']"), "No usar")
        print("🔵 INGRESO USUARIO")

        find_and_send_keys(driver, (By.XPATH, "//input[@type='password']"), "1234")
        print("🔵 INGRESO CONTRASEÑA")

        click_con_js(driver, (By.XPATH, "(//span[@class='checkmark'])[3]"))
        print("🔵 CLICK CHECK SUCURSAL")

        click_con_js(driver, (By.XPATH, "(//span[@class='checkmark'])[4]"))
        print("🔵 CLICK CHECK GRUPO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        validar_mensaje(driver,"Relación creada con éxito")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar']"))
        print("🔵 CLICK AGREGAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ITS CORE")
        print("🔵 SELECCION DE GRUPO AFINIDAD")

        find_and_click(driver, (By.XPATH, "//div[@class='form-actions mt-4 boton1 mb-2']//button[@type='button'][normalize-space()='Guardar']"))
        print("🔵 BOTON GUARDAR")

        validar_mensaje(driver, "Relación actualizada con éxito")

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