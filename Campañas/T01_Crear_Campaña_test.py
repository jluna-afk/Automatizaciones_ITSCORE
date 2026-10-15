import unittest
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class TestCampaña(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_Campaña(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Campañas"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        print("🔵 INGRESO A LA PARAMETRIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='nombre']"), "CAMPAÑA PRUEBA TEST")
        print("🔵 INGRESO DEL NOMBRE DE CAMPAÑA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='cuenta']"))
        seleccionar_opcion_ng_select_js(driver, "13 - 45 - TELEPAGOS - 493")
        print("🔵 SELECCION DE CUENTA")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='desde']//input[@type='text']"), "25082025")
        print("🔵 SELECCION DE FECHA DESDE")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='hasta']//input[@type='text']"), "25082030")
        print("🔵 SELECCION DE FECHA HASTA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='vencimiento']"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día o hábil anterior")
        print("🔵 SELECCION DE VENCIMIENTO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='operatoria']"))
        seleccionar_opcion_ng_select_js(driver, "Servicio")
        print("🔵 SELECCION DE OPERATORIA")

        find_and_click(driver, (By.XPATH, "//button[@class='search-icon']//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA LINEA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='codigo']"), "1")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 INGRESO CODIGO")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='No Recurrente']"))
        print("🔵 SELECCION DE LINEA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='situacion']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Deuda total")
        print("🔵 SELECCION DE TIPO DEUDA")

        find_and_click(driver, (By.XPATH, "//input[@formcontrolname='entidadCobroDesc']"))
        print("🔵 CLICK EN LA LUPITA ENTIDAD COBRO")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Sin entidad']"))
        print("🔵 CLICK EN LA ENTIDAD DE COBRO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aplicar']"))
        print("🔵 CLICK BOTON APLICAR")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='titulo']"), "prueba")
        print("🔵 INGRESO DE TITULO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='canal']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "WhatsApp")
        print("🔵 SELECCION DE CANAL")

        find_and_send_keys(driver, (By.XPATH, "//input[@type='number']"), "1")
        print("🔵 INGRESO DE CANTIDAD DE DIAS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='plazo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Dias anteriores")
        print("🔵 SELECCION DE MOMENTO DE ENVIO")

        find_and_send_keys(driver, (By.XPATH, "//input[@type='time']"), "1030")
        print("🔵 INGRESO DE HORA INICIO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Contenido']"))
        print("🔵 CLICK EN CONTENIDO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='template']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Proximo vencimiento sin linkdepago")
        print("🔵 SELECCION DE TEMPLATE")        

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")       

        find_and_click(driver, (By.XPATH, "//button[@class='btn-outline-primary-its w-100 mt-2 font-weight-bold']"))
        print("🔵 CLICK EN AGREGAR TIPO DE COMUNICACION")

        find_and_send_keys(driver, (By.XPATH, "(//input[@formcontrolname='titulo'])[last()]"), "prueba 2")
        print("🔵 INGRESO DE TITULO")

        find_and_click(driver, (By.XPATH, "(//ng-select[@formcontrolname='canal']//input[@type='text'])[last()]"))
        seleccionar_opcion_ng_select_js(driver, "Email")
        print("🔵 SELECCION DE CANAL")

        find_and_click(driver, (By.XPATH, "(//ng-select[@formcontrolname='plazo']//input[@type='text'])[last()]"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día")
        print("🔵 SELECCION DE MOMENTO DE ENVIO")

        find_and_send_keys(driver, (By.XPATH, "(//input[@type='time'])[last()]"), "1030")
        print("🔵 INGRESO DE HORA INICIO")

        find_and_click(driver, (By.XPATH, "(//button[normalize-space()='Contenido'])[last()]"))
        print("🔵 CLICK EN CONTENIDO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='template']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Test email")
        print("🔵 SELECCION DE TEMPLATE")        

        find_and_send_keys(driver, (By.XPATH, "//div[@class='form-control rich-editor single-line']"), "test")
        print("🔵 INGRESO ASUNTO")
        time.sleep(1)

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")   

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        validar_mensaje_snackbar(driver, "Campaña creada correctamente.")

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