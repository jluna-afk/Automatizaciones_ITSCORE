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

def validar_mensaje(driver, mensaje_exito, wait_time=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print(f"❌ No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")

class TestAsientosAutomaticos(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_asiento_automatico(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))

            find_and_click(driver, (By.LINK_TEXT, "Contabilidad"))
            find_and_click(driver, (By.LINK_TEXT, "Parametría"))
            find_and_click(driver, (By.LINK_TEXT, "Asientos Automáticos"))

            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[1]"))
            seleccionar_opcion_ng_select(driver, "Banco")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='operacion_id']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "DEBITO POR MOVIMIENTO ENTRE CUENTAS")

            find_and_click(driver, (By.XPATH, "//ng-select[@class='form-select ng-select-custom ng-select-searchable ng-select ng-select-single ng-untouched ng-pristine ng-invalid']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "1 BANCO BBVA ARGENTINA S.A.")

            find_and_send_keys(driver, (By.XPATH, "//input[@max='9999-12-31']"), "21082025")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Continuar']"))

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))

            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[6]"))
            seleccionar_opcion_ng_select(driver, "1 - IMPORTE")

            find_and_send_keys(driver, (By.XPATH, "//input[@id='numeroCuenta']"), "1.1.1.01.01.01")
            
            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[9]"))
            seleccionar_opcion_ng_select(driver, "+")
            
            find_and_click(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/label[1]/span[1]"))
            
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar importe']"))

            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[10]"))
            seleccionar_opcion_ng_select(driver, "1 - IMPORTE")

            find_and_send_keys(driver, (By.XPATH, "//tr[@class='ng-invalid ng-touched ng-dirty']//input[@id='numeroCuenta']"), "1.1.5.01.01.01")

            find_and_click(driver, (By.XPATH, "(//input[@type='text'])[13]"))
            seleccionar_opcion_ng_select(driver, "+")

            find_and_click(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-asientos-automaticos[1]/div[1]/form[1]/div[3]/table[1]/tbody[1]/tr[2]/td[6]/div[1]/label[1]/span[1]"))

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
            validar_mensaje(driver, "Todas las cuentas deben pertenecer a la misma moneda.")

        except TimeoutException:
            print("❌ No se pudo crear porque un elemento no fue encontrado a tiempo.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)