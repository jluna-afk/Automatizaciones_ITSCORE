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
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar_async_crear
)

class TestPersonaGestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_nueva_persona(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A ITS CORE")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
        find_and_click(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
        print("🔵 INGRESO AL MODULO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='nombre']"), "Jagger")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='apellido']"), "Luna")
        print("🔵 INGRESO DEL NOMBRE")
        
        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='sexo']//input[@type='text']"), "Masculino")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Masculino']"))
        print("🔵 INGRESO SEXO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='estado_civil']//input[@type='text']"), "Soltero")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Soltero/a']"))
        print("🔵 INGRESO ESTADO CIVIL")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='tipo_documento']//input[@type='text']"), "masculino")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='DNI Masculino']"))
        print("🔵 INGRESO TIPO DOC")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='documento']"), "77777777")
        print("🔵 INGRESO N° DNI")
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fecha_nacimiento']//input[@type='text']"), "21102021")
        print("🔵 INGRESO FECHA NAC")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='nacionalidad']//input[@type='text']"), "argentina")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='ARGENTINA']"))
        print("🔵 INGRESO NACIONALIDAD")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_tributario']"), "20777777778")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='calle']"), "Juan Manuel de Rosas")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='numero']"), "987")
        print("🔵 INGRESO DOMICILIO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='pais']//input[@type='text']"), "ARGENTINA")
        find_and_click(driver, (By.XPATH, "(//span[@class='ng-option-label'][normalize-space()='ARGENTINA'])[1]"))
        print("🔵 INGRESO PAIS")

        find_and_click(driver, (By.CSS_SELECTOR, "ng-select#provincia div[role='combobox']"))
        find_and_send_keys(driver, (By.XPATH, "//div[@aria-expanded='true']//input[@type='text']"), "Santa Fe")
        find_and_click(driver, (By.XPATH, "(//span[normalize-space()='Santa Fe'])[1]"))
        print("🔵 INGRESO LOCALIDAD")

        find_and_click(driver, (By.CSS_SELECTOR, "ng-select#localidad div[role='combobox']"))
        find_and_send_keys(driver, (By.CSS_SELECTOR, "ng-select#localidad div[role='combobox'] input[type='text']"), "Stephenson")
        time.sleep(1)  
        seleccionar_opcion_ng_select_js(driver, "Stephenson - (2103)")
        print("🔵 INGRESO CIUDAD")

        find_and_click(driver, (By.XPATH, "(//ng-select[@id='tipo'])[1]//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Telefono movil")
        find_and_send_keys(driver, (By.XPATH, "(//input[@id='dato'])[1]"), "3416956694")
        print("🔵 INGRESO TELEFONO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar medio de comunicación']"))
        find_and_click(driver, (By.XPATH, "(//ng-select[@id='tipo'])[2]//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Correo electronico")
        find_and_send_keys(driver, (By.XPATH, "(//input[@id='dato'])[2]"), "jluna@quo.ar")
        print("🔵 INGRESO CORREO ELECTRONICO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='cbu']"), "0170282040000036262342")
        print("🔵 INGRESO CBU")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='alias']"), "Jagger.luna")
        print("🔵 INGRESO ALIAS")
        find_and_click(driver, (By.XPATH, "//ng-select[@id='estado']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activa")
        print("🔵 INGRESO ESTADO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='empresa']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activos Provinciales Santa Fe")
        print("🔵 INGRESO ENTIDAD COBRO")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='identificadorDescuento']"), "123456789")
        print("🔵 INGRESO ID DE DESCUENTO")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='sueldo_bruto']"), "1200000")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='sueldo_neto']"), "1000000")
        print("🔵 INGRESO SUELDOS")
        find_and_click(driver, (By.XPATH, "//ng-select[@id='estado']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activo")
        print("🔵 INGRESO ESTADO LEGAJO")
        
        find_and_click(driver, (By.CSS_SELECTOR, "ng-select[id='actividad'] input[type='text']"))
        find_and_send_keys(driver, (By.CSS_SELECTOR, "ng-select[id='actividad'] input[type='text']"), "monotributista")
        seleccionar_opcion_ng_select_js(driver, "Monotributista")
        print("🔵 INGRESO ACTIVIDAD")

        validar_mensaje_snackbar_async_crear(driver, "//button[normalize-space()='Crear']", "Persona ingresada o actualizada exitosamente")

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