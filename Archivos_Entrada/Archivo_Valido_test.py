import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def find_and_send_keys(driver, by_locator, value, wait_time=20):
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

def validar_mensaje(driver, mensaje_esperado, wait_time=30):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_esperado}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ Validación exitosa: Se mostró el mensaje '{mensaje_esperado}'.")
    except TimeoutException:
        print(f"❌ Falló la validación: No apareció el mensaje '{mensaje_esperado}' en {wait_time} segundos.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado en la validación: {e}")

class TestSubirArchivoConTuFormato(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def upload_file_xpath(self, xpath_input, ruta_archivo, wait_time=15):
        try:
            elemento = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath_input))
            )
            elemento.send_keys(ruta_archivo)
            print(f"✅ Archivo '{os.path.basename(ruta_archivo)}' enviado correctamente.")
        except TimeoutException:
            print(f"❌ Error de tiempo: El elemento para subir el archivo no se encontró con el XPath: {xpath_input}")
        except Exception as e:
            print(f"❌ No se pudo enviar la ruta al elemento. Error: {e}")

    def test_subir_archivo_pago_mutual(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Archivos"))
        find_and_click(driver, (By.LINK_TEXT, "Entrada"))
        print("🔵 INGRESO A ARCHIVOS ENTRADA")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Generico']"))
        print("🔵 SELECCIÓN DEL GRUPO 'Generico'")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        nombre_archivo = 'pagos_.txt'
        ruta_archivo = r"C:\Users\Joaquin\Desktop\Archivos Pruebas\pagos_.txt"

        xpath_input_file = "//tr[contains(., 'Pagos AHORRO MUTUAL')]//input[@type='file']"
        
        self.upload_file_xpath(xpath_input_file, ruta_archivo)

        print("⏳ Esperando la validación del archivo...")
        validar_mensaje(driver, "Archivo válido")


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