import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click_with_scroll,
    Checkbox_Xpath,
    validar_mensaje_snackbar_async_guardar_boton
)

class TestGrupoAfinidad(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_grupo_sin_relaciones(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Personas"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Grupos de afinidad"))
        print("🔵 INGRESO AL MODULO")
        time.sleep(0.5)

        filas = driver.find_elements(By.XPATH, "//tr[contains(@class, 'tr-body')]")
        encontrado = False

        for fila in filas:
            input_desc = fila.find_element(By.XPATH, ".//input[@formcontrolname='descripcion']")
            if input_desc.get_attribute("value") == "Prueba":
                chevron = fila.find_element(By.XPATH, ".//i[contains(@class, 'fa-chevron-down')]")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chevron)
                chevron.click()
                encontrado = True
                print("🔵 DESPLIEGUE DEL GRUPO (Encontrado dinámicamente)")
                break

        if not encontrado:
            raise RuntimeError("❌ No se pudo encontrar ninguna fila con la descripción 'Prueba'")  
        time.sleep(1)

        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Usuario']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Cliente']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Proveedor']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Entidad de cobro']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Vendedor']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Banco']]"))
        Checkbox_Xpath(driver, (By.XPATH, "//tr[contains(@class, 'details-row')]//label[p[normalize-space()='Beneficiario']]"))
        print("🔵 CLICK EN LOS CHECKBOX")

        validar_mensaje_snackbar_async_guardar_boton(
            driver, 
            xpath_boton="//button[normalize-space()='Guardar']", 
            mensaje_exito="Es obligatorio que el grupo tenga al menos un tipo de clasificacion de persona en el sistema."
        )

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