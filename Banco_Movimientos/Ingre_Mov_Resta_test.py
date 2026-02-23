import unittest
import time
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

class TestBancoMovimiento(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_ingresar_movimiento(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            print("🔵 INGRESO USUARIO Y CLAVE")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
            print("🔵 CLICK BOTON INGRESAR")

            find_and_click(driver, (By.XPATH, "//span[normalize-space()='Banco']"))
            find_and_click(driver, (By.LINK_TEXT, "Movimientos"))
            print("🔵 INGRESO A BANCO - MOVIMIENTOS")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='cuenta']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "2 - 45 - TELEPAGOS - 493")
            print("🔵 SELECCIONO CUENTA BANCARIA")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='operacion']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "pago sueldos")
            print("🔵 SELECCIONO OPERACION")

            find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importe']"), "3000.00")
            print("🔵 INGRESO IMPORTE")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))
            print("🔵 CLICK BOTON CONTINUAR")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
            print("🔵 CLICK BOTON ACEPTAR")
            validar_mensaje_snackbar(driver, "Movimiento ingresado correctamente")

        except TimeoutException:
            print("❌ El movimiento no se pudo ingresar porque un elemento no fue encontrado a tiempo.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)