import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import os

def find_and_send_keys(driver, by_locator, value, wait_time=50):
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.clear()
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20):
    for intento in range(3):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable(by_locator)
            )
            try:
                element.click()
            except Exception:
                driver.execute_script("arguments[0].click();", element)
            return element
        
        except StaleElementReferenceException:
            if intento == 2:  
                raise
            time.sleep(0.5)

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


class Test_Prestamos_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_modificar_linea_prestamo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Amortizable"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS PARAMETRIA")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='descripcion']"), "Test Crear Linea Prestamo")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Test Crear Linea Prestamo']"))
        print("🔵 SELECCION PRESTAMO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='sistema']"))
        seleccionar_opcion_ng_select(driver, "Francés con IVA")
        print("🔵 SELECCION SISTEMA")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='vencimientos']"))
        seleccionar_opcion_ng_select(driver, "Mismo día o hábil anterior")
        print("🔵 SELECCION VENCIMIENTOS")

        valor_esperado = "20"
        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='gastoFijo']"), valor_esperado)
        print("🔵 INGRESO GASTO FIJO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN GUARDAR")
        
        validar_mensaje_snackbar(driver, "Línea actualizada correctamente")

        try:
            gasto_fijo_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='gastoFijo']"))
            )
            
            valor_actual = gasto_fijo_input.get_attribute("value")
            print(f"🔵 VERIFICANDO GASTO FIJO EN PANTALLA: Encontrado '{valor_actual}'")

            self.assertEqual(
                valor_actual, 
                valor_esperado, 
                f"El gasto fijo esperado era '{valor_esperado}', pero se visualiza '{valor_actual}'."
            )
            print("✅ EXITO: El importe de gasto fijo se visualiza correctamente tras guardar.")
            
        except TimeoutException:
            self.fail("❌ ERROR: No se pudo localizar el campo 'gastoFijo' para validar su valor después de guardar.")

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