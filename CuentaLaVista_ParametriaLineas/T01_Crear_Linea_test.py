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

class TestLineasCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_linea_CV(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO A LA PARAMETRIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcion']"), "LINEA PRUEBA TEST")
        print("🔵 INGRESO DE LA DESCRIPCION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcionReducida']"), "LP")
        print("🔵 INGRESO DE LA DESCRIPCION REDUCIDA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='moneda']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Pesos")
        print("🔵 SELECCION DE MONEDA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tna']"), "10")
        print("🔵 INGRESO DE LA TNA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tope']"), "10000")
        print("🔵 INGRESO DEL TOPE")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='liquidacion']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Diario")
        print("🔵 SELECCION DE MONEDA")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaDesde']//input[@type='text']"), "25082025")
        print("🔵 SELECCION DE FECHA DESDE")

        find_and_click(driver, (By.XPATH, "//label[normalize-space()='Descubierto']"))
        print("🔵 SELECCION DE DESCUBIERTO")

        find_and_click(driver, (By.XPATH, "//label[normalize-space()='Permite Pagos Automáticos']"))
        print("🔵 SELECCION DE PAGOS AUTOMÁTICOS")

        find_and_click(driver, (By.XPATH, "//label[normalize-space()='Permite Cobros Automáticos']"))
        print("🔵 SELECCION DE COBROS AUTOMÁTICOS")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        validar_mensaje_snackbar(driver, "Línea creada exitosamente")

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