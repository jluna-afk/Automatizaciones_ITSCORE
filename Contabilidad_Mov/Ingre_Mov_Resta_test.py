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
    element.clear()
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

def validar_mensaje(driver, mensaje_exito, wait_time=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ El movimiento se ingreso correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print(f"❌ El movimiento no se ingreso: No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")

class TestContabilidadMovimiento(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_ingresar_movimiento_operacion_488(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))

            find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
            find_and_click(driver, (By.LINK_TEXT, "Movimientos"))

            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[2]"))
            seleccionar_opcion_ng_select(driver, "Pesos")

            find_and_send_keys(driver, (By.XPATH, "//input[@id='operacion']"), "496")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipo_persona']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Proveedor")

            find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='persona']"), "41656139")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))

            find_and_send_keys(driver, (By.XPATH, "//input[@id='importe0']"), "2000")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
            validar_mensaje(driver, "Movimiento ejecutado correctamente")

        except TimeoutException:
            print("❌ El movimiento no se pudo ingresar porque un elemento no fue encontrado a tiempo.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)