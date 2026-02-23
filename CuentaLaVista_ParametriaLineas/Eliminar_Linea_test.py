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
    driver.execute_script("arguments[0].click();", element)
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

def click_checkbox(driver, locator, wait_time=10):
    try:
        checkbox = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"🔵 Hizo clic en el checkbox: {locator}")
    except TimeoutException:
        print(f"❌ No se encontró el checkbox con el localizador: {locator}")
        raise

class TestLineasCuentaVista(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_eliminar_linea(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
            print("🔵 INGRESO A LA PLATAFORMA")

            find_and_click(driver, (By.LINK_TEXT, "Seguridad"))
            find_and_click(driver, (By.XPATH, "//a[@href='#/seguridad/parametria']"))
            print("🔵 INGRESO SERVICIOS")

            find_and_click(driver, (By.XPATH, "//div[@class='w-50 input-container-search position-relative h-100']//button[@type='button']"))
            find_and_click(driver, (By.XPATH, "//td[normalize-space()='Administrador']"))
            print("🔵 SELECCION DE GRUPO")

            find_and_click(driver, (By.XPATH, "//app-collapse[@title='Líneas']//i[@class='fa fas fa-chevron-down']"))
            find_and_send_keys(driver, (By.XPATH, "//input[@id='lineas']"), "LINEA PRUEBA")
            print("🔵 DESPLIEGUE Y BUSQUEDA DE LA LINEA")

            click_checkbox(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-parametria[1]/div[1]/app-tabs[1]/div[1]/div[1]/app-tab[1]/form[1]/app-collapse[1]/div[1]/div[2]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[2]/label[1]/span[1]"))
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
            print("🔵 CLICK EN EL CHECKBOX Y GUARDADO")

            find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
            find_and_click(driver, (By.XPATH, "(//span[contains(text(),'Parametría')])[2]"))
            find_and_click(driver, (By.LINK_TEXT, "Líneas"))
            print("🔵 INGRESO A LA PARAMETRIA")

            find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
            find_and_send_keys(driver, (By.XPATH, "//input[@id='descripcion']"), "LINEA PRUEBA")
            find_and_click(driver, (By.XPATH, "//td[normalize-space()='LINEA PRUEBA']"))
            print("🔵 BUSQUEDA Y SELECCION DE LINEA")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Eliminar']"))

            modal_locator = (By.XPATH, "//app-dialog-simple")
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(modal_locator))

            boton_eliminar_final = (By.XPATH, "//app-dialog-simple//button[contains(text(), 'Eliminar')]")
            find_and_click(driver, boton_eliminar_final)

            validar_mensaje(driver, "Línea eliminada exitosamente")


        except TimeoutException:
            print("❌ La linea no se pudo eliminar.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)