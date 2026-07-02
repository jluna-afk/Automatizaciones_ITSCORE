import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys_with_clear,
    find_and_click_with_scroll,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class Test_PlazoFijo_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_modificar_linea_plazo_fijo(self):
        driver = self.driver

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Seguridad"))
        find_and_click_with_scroll(driver, (By.XPATH, "//a[@href='#/seguridad/parametria']"))
        print("🔵 INGRESO SERVICIOS")
        
        find_and_click_with_scroll(driver, (By.XPATH, "//div[@class='w-50 input-container-search position-relative h-100']//button[@type='button']"))
        find_and_click_with_scroll(driver, (By.XPATH, "//td[normalize-space()='Administrador']"))
        print("🔵 SELECCION DE GRUPO")

        find_and_click_with_scroll(driver, (By.XPATH, "//app-collapse[@title='Líneas']//i[@class='fa fas fa-chevron-down']"))
        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='lineas']"), "test crear linea plazo fijo")
        print("🔵 DESPLIEGUE Y BUSQUEDA DE LA LINEA")

        find_and_click_with_scroll(driver, (By.XPATH, "//td[contains(normalize-space(), 'Plazo Fijo - Test Crear Linea Plazo Fijo (12)')]/parent::tr//label"))
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN EL CHECKBOX Y GUARDADO")
        validar_mensaje_snackbar(driver, "Permisos modificados correctamente")

        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Plazo fijo"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Parametría"))
        print("🔵 INGRESO AL MODULO DE PLAZO FIJO PARAMETRIA")

        find_and_click_with_scroll(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@id='descripcion']"), "Test Crear Linea Plazo Fijo")
        print("🔵 INGRESO NOMBRE DE LA LINEA")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")
        
        find_and_click_with_scroll(driver, (By.XPATH, "//td[normalize-space()='Test Crear Linea Plazo Fijo']"))
        print("🔵 SELECCION DE LA LINEA")
        time.sleep(0.5)

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='cantidadMaximaDias']"), "60")
        print("🔵 MODIFICACION CANTIDAD DIAS MAXIMO")

        find_and_send_keys_with_clear(driver, (By.XPATH, "//input[@formcontrolname='importeMinimo']"), "1500")
        print("🔵 MODIFICACION IMPORTE MINIMO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='vencimiento']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día o hábil anterior")
        print("🔵 MODIFICACION VENCIMIENTO")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")
        
        validar_mensaje_snackbar(driver, "Línea de plazo fijo actualizada correctamente")

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