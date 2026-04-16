import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

def find_and_send_keys(driver, by_locator, value, wait_time=50):
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20):
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    WebDriverWait(driver, wait_time).until(
        lambda d: not (
            element.get_attribute("disabled") == "true" or 
            "disabled" in (element.get_attribute("class") or "")
        )
    )
    element.click()
    return element

def seleccionar_opcion_ng_select(driver, texto_opcion, wait_time=15):
    try:
        options_locator = (By.CSS_SELECTOR, "div.ng-option")
        opciones = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located(options_locator)
        )
        
        for opcion in opciones:
            if texto_opcion.lower() in opcion.text.lower():
                driver.execute_script("arguments[0].click();", opcion)
                return True
        
        return False
    except TimeoutException:
        return False

def validar_mensaje_snackbar(driver, mensaje_exito, timeout=10):

    try:
        snackbar = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "simple-snack-bar, .mat-mdc-snack-bar-label")
            )
        )

        texto_capturado = snackbar.text.strip()

        if mensaje_exito.lower() in texto_capturado.lower():
            print(f"✅ EXITO: {texto_capturado}")
        else:
            print(f"❌ ERROR DETECTADO EN PANTALLA: {texto_capturado}")
            raise AssertionError(f"Mensaje inesperado: {texto_capturado}")

    except TimeoutException:
        driver.save_screenshot("fallo_captura_mensaje.png")
        raise AssertionError("No se detectó ningún mensaje Snackbar (Timeout)")

class TestMovimientosCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_CV_forma_pago_contabilidad(self):
        driver = self.driver

        
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.LINK_TEXT, "Movimientos"))
        print("🔵 INGRESO A MOVIMIENTOS DE CUENTA A LA VISTA")

        find_and_click(driver, (By.XPATH, "//span[@class='chevron rotated']//i[@class='fas fa-chevron-down']"))
        print("🔵 CLICK PARA OCULTAR MENU")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='linea']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "CUENTAS COMERCIALES")
        print("🔵 SELECCION DE LINEA")

        find_and_click(driver, (By.XPATH, "(//button[@type='button'])[1]"))
        print("🔵 CLICK EN LA LUPITA DE BUSQUEDA DE PERSONA")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='QUO SOLUCIONES SRL']"))
        print("🔵 SELECCION DE PERSONA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='operacion']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "SOLICITUD PAGO PROVEEDORES")
        print("🔵 SELECCION DE OPERACION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='concepto']"), "test forma pago contabilidad")
        print("🔵 INGRESO CONCEPTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importe']"), "1000")
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK EN CONTINUAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar forma de pago']"))
        print("🔵 CLICK EN AGREGAR FORMA DE PAGO")

        find_and_click(driver, (By.XPATH, "//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "CONTABILIDAD")
        print("🔵 SELECCION FORMA DE PAGO CONTABILIDAD")

        find_and_send_keys(driver, (By.XPATH, "//input[@class='text-right form-control w-100 ng-untouched ng-pristine ng-invalid']"), "1000")
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")

        validar_mensaje_snackbar(driver, "Movimiento confirmado con éxito!")

        find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
        find_and_click(driver, (By.LINK_TEXT, "Movimientos"))
        print("🔵INGRESO A CONTABILIDAD MOVIMIENTOS")

        find_and_click(driver, (By.XPATH, "//a[@title='Pendientes Movimientos']"))
        print("🔵 CLICK EN EL ICONO SECCION PENDIENTES")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='CONF PAGO A PROVE CORPORATIVA']"))  
        print("🔵 SELECCION OPERACION A CONFIRMAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK BOTON ACEPTAR")

        validar_mensaje_snackbar(driver, "Movimiento ejecutado correctamente")

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