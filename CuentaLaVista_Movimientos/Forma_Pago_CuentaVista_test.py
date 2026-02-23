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

class TestMovimientosCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_forma_pago_cuenta(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))

            find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
            find_and_click(driver, (By.LINK_TEXT, "Movimientos"))

            find_and_click(driver, (By.XPATH, "//ng-select[@id='linea']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "CUENTAS COMERCIALES")

            find_and_click(driver, (By.XPATH, "(//button[@type='button'])[1]"))

            find_and_click(driver, (By.XPATH, "//td[normalize-space()='QUO SOLUCIONES SRL']"))

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))

            find_and_click(driver, (By.XPATH, "//ng-select[@id='operacion']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "SOLICITUD PAGO PROVEEDORES")

            find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importe']"), "4000")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar forma de pago']"))

            find_and_click(driver, (By.XPATH, "//div[@class='ng-select-container']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "CUENTA A LA VISTA")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='cuentaDestino']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "PROV. INFORMATICA")

            find_and_send_keys(driver, (By.XPATH, "//input[@class='text-right form-control w-100 ng-untouched ng-pristine ng-invalid']"), "4000")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))

            validar_mensaje(driver, "Movimiento confirmado con éxito!")


        except TimeoutException:
            print("❌ El movimiento no se pudo ingresar.")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)