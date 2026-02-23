import unittest
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

def seleccionar_opcion_ng_select(driver, texto_opcion, wait_time=10):
    try:
        opciones = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ng-option"))
        )
        for opcion in opciones:
            if texto_opcion.lower() in opcion.text.lower():
                opcion.click()
                return True
        return False
    except Exception as e:
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

class TestCaja_Mov_Resta(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_ingresar_movimiento_caja_resta(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            print("🔵 INGRESO USUARIO Y CLAVE")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
            print("🔵 CLICK BOTON INGRESAR")

            find_and_click(driver, (By.LINK_TEXT, "Caja"))
            find_and_click(driver, (By.LINK_TEXT, "Puesto"))
            print("🔵 INGRESO MODULO CAJA")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='cajaAsignada']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Caja 3")
            print("🔵 SELECCION DE CAJA")

            find_and_send_keys(driver, (By.XPATH, "//input[@id='operacion']"), "96")
            print("🔵 INGRESO CODIGO DE OPERACION")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='tipoPersona']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Proveedor")
            print("🔵 SELECCION TIPO DE PERSONA")

            find_and_send_keys(driver, (By.XPATH, "//input[@id='persona']"), "41656139")
            print("🔵 INGRESO NUMERO DE DOCUMENTO")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='moneda']//div[@class='ng-select-container']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Pesos")
            print("🔵 SELECCION DE MONEDA")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Agregar']"))
            print("🔵 CLICK BOTON AGREGAR")

            find_and_send_keys(driver, (By.XPATH, "//input[@id='importe0']"), "1000")
            print("🔵 INGRESO IMPORTE")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
            print("🔵 CLICK BOTON ACEPTAR")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ejecutar']"))
            print("🔵 CLICK BOTON EJECUTAR")
            
            validar_mensaje_snackbar(driver, "Operaciones ejecutadas exitosamente")

        except TimeoutException:
            print("❌ El movimiento no se pudo ingresar porque un elemento no fue encontrado a tiempo.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)