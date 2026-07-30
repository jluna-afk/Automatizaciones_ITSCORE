import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys_with_clear,
    find_and_click,
    validar_mensaje_snackbar
)

class Test_PrendaValores_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_modificar_linea_prenda_valores(self):
        driver = self.driver

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Seguridad"))
        find_and_click(driver, (By.XPATH, "//a[@href='#/seguridad/parametria']"))

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='grupo']"), "1" + Keys.TAB)
        print("🔵 SELECCION DE GRUPO")

        find_and_click(driver, (By.XPATH, "//app-collapse[@title='Líneas']//i[@class='fa fas fa-chevron-down']"))
        print("🔵 DESPLIEGUE DE LINEAS")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='lineas']"), "Test Crear Linea Prestamo")
        print("🔵 BUSQUEDA DE LA LINEA")

        find_and_click(driver, (By.XPATH, "//tr[contains(., 'Préstamo con prenda de valores - Test Crear Linea Prestamo')]//span[@class='checkmark']"))
        print("🔵 CLIC CHECKBOX DE LA LINEA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")

        validar_mensaje_snackbar(driver, "Permisos modificados correctamente")

        find_and_click(driver, (By.LINK_TEXT, "Prést. con prenda valores"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRENDA VALORES PARAMETRIA")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='descripcion']"), "Test Crear Linea Prestamo")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Test Crear Linea Prestamo']"))
        print("🔵 SELECCION PRESTAMO")

        time.sleep(1)

        valor_esperado = "10"
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='tna']"), valor_esperado)
        print("🔵 INGRESO GASTO FIJO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")
        
        validar_mensaje_snackbar(driver, "Línea actualizada correctamente")

        try:
            time.sleep(1)
            gasto_fijo_input = driver.find_element(By.XPATH, "//input[@formcontrolname='tna']")
            valor_actual = gasto_fijo_input.get_attribute("value")
            print(f"🔵 VERIFICANDO TNA EN PANTALLA: Encontrado '{valor_actual}'")
        except NoSuchElementException:
            self.fail("❌ ERROR: No se pudo localizar el campo 'TNA' para validar su valor después de guardar.")

        self.assertEqual(
                valor_actual, 
                valor_esperado, 
                f"El TNA esperado era '{valor_esperado}', pero se visualiza '{valor_actual}'."
            )
        print("✅ EXITO: El importe de TNA se visualiza correctamente tras guardar.")


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