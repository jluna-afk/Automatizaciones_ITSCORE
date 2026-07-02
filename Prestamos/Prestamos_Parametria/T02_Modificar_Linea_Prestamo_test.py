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
    find_and_send_keys_with_clear,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class Test_Prestamos_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_modificar_linea_prestamo(self):
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

        find_and_click(driver, (By.XPATH, "//tr[contains(., 'Préstamo - Test Crear Linea Prestamo')]//span[@class='checkmark']"))
        print("🔵 CLIC CHECKBOX DE LA LINEA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")

        validar_mensaje_snackbar(driver, "Permisos modificados correctamente")
        print("✅ EXITO: PERMISOS MODIFICADOS CORRECTAMENTE")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS PARAMETRIA")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='descripcion']"), "Test Crear Linea Prestamo")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Test Crear Linea Prestamo']"))
        print("🔵 SELECCION PRESTAMO")

        time.sleep(1)
        find_and_click(driver, (By.XPATH, "//ng-select[@id='sistema']//div[@role='combobox']"))
        seleccionar_opcion_ng_select_js(driver, "Francés con IVA")
        print("🔵 SELECCION SISTEMA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='vencimientos']"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día o hábil anterior")
        print("🔵 SELECCION VENCIMIENTOS")

        valor_esperado = "20"
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='gastoFijo']"), valor_esperado)
        print("🔵 INGRESO GASTO FIJO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")
        
        validar_mensaje_snackbar(driver, "Línea actualizada correctamente")

        try:
            time.sleep(1)
            gasto_fijo_input = driver.find_element(By.XPATH, "//input[@formcontrolname='gastoFijo']")
            valor_actual = gasto_fijo_input.get_attribute("value")
            print(f"🔵 VERIFICANDO GASTO FIJO EN PANTALLA: Encontrado '{valor_actual}'")

            self.assertEqual(
                valor_actual, 
                valor_esperado, 
                f"El gasto fijo esperado era '{valor_esperado}', pero se visualiza '{valor_actual}'."
            )
            print("✅ EXITO: El importe de gasto fijo se visualiza correctamente tras guardar.")
            
        except Exception:
            self.fail("❌ ERROR: No se pudo localizar el campo 'gastoFijo' para validar su valor después de guardar.")

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