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
        EC.presence_of_element_located(by_locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.clear()
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20):
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located(by_locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.click()
    return element

def seleccionar_opcion_ng_select(driver, locator_input, texto_opcion, wait_time=10):
    find_and_send_keys(driver, locator_input, texto_opcion, wait_time)
    time.sleep(0.5) 
    
    try:
        opciones = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ng-option"))
        )
        
        for opcion in opciones:
            if texto_opcion.lower() in opcion.text.lower():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion)
                opcion.click()
                return True
                
        raise AssertionError(f"❌ Falló: No se encontró la opción '{texto_opcion}' en el desplegable filtrado.")
        
    except TimeoutException:
         raise AssertionError(f"❌ Falló: Las opciones del desplegable nunca cargaron al buscar '{texto_opcion}'.")

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

class TestAsientosAutomaticos(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_asiento_automatico(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 CLICK BOTON INGRESAR")

        find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Asientos automáticos"))
        print("🔵 INGRESO AL MODULO ASIENTOS AUTOMATICOS")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "//ng-select[@class='form-select ng-select-custom ng-select-searchable ng-select ng-select-single ng-untouched ng-pristine ng-invalid']//input[@type='text']"), "Banco")
        print("🔵 SELECCION OPERATORIA")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "//ng-select[@formcontrolname='operacion_id']//input[@type='text']"), "PAGO SUELDOS")
        print("🔵 SELECCION OPERACION")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "//ng-select[@formcontrolname='linea_id']//input[@type='text']"), "1 BANCO BBVA ARGENTINA S.A.")
        print("🔵 SELECCION LINEA BANCO")

        find_and_send_keys(driver, (By.XPATH, "//input[@class='form-control form-control-sm text-left pl-2']"), "10072025")
        print("🔵 SELECCION FECHA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
        print("🔵 CLICK BOTON CONTINUAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))
        print("🔵 CLICK EN AGREGAR IMPORTE")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "(//input[@type='text'])[6]"), "IMPORTE")
        print("🔵 SELECCION TIPO IMPORTE")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='numeroCuenta']"), "1.1.1.01.01.01")
        print("🔵 INGRESO CUENTA HABER")
        
        seleccionar_opcion_ng_select(driver, (By.XPATH, "(//input[@type='text'])[9]"), "+")
        print("🔵 SELECCION SIGNO")
        
        find_and_click(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/label[1]/span[1]"))
        print("🔵 SELECCION DEBE/HABER")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))
        print("🔵 CLICK EN AGREGAR IMPORTE")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "(//input[@type='text'])[10]"), "IMPORTE")
        print("🔵 SELECCION TIPO IMPORTE")

        find_and_send_keys(driver, (By.XPATH, "//tr[@class='ng-invalid ng-touched ng-dirty']//input[@id='numeroCuenta']"), "1.1.1.01.02.01")
        print("🔵 INGRESO CUENTA DEBE")

        seleccionar_opcion_ng_select(driver, (By.XPATH, "(//input[@type='text'])[13]"), "+")
        print("🔵 SELECCION SIGNO")

        find_and_click(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[2]/td[6]/div[1]/label[1]/span[1]"))
        print("🔵 SELECCION DEBE/HABER")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")
        validar_mensaje_snackbar(driver, "Asiento automatico creado correctamente")

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