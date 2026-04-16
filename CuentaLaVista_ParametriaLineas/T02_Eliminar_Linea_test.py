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

    def test_eliminar_linea_CV(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO DE LA CLAVE")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Seguridad"))
        find_and_click(driver, (By.XPATH, "//a[@href='#/seguridad/parametria']"))
        print("🔵 INGRESO SERVICIOS")

        find_and_click(driver, (By.XPATH, "//div[@class='w-50 input-container-search position-relative h-100']//button[@type='button']"))
        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Administrador']"))
        print("🔵 SELECCION DE GRUPO")

        find_and_click(driver, (By.XPATH, "//app-collapse[@title='Líneas']//i[@class='fa fas fa-chevron-down']"))
        find_and_send_keys(driver, (By.XPATH, "//input[@id='lineas']"), "LINEA PRUEBA TEST")
        print("🔵 DESPLIEGUE Y BUSQUEDA DE LA LINEA")

        click_checkbox(driver, (By.XPATH, "//body[1]/app-root[1]/app-main[1]/div[1]/app-parametria[1]/div[1]/app-tabs[1]/div[1]/div[1]/app-tab[1]/form[1]/app-collapse[1]/div[1]/div[2]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[2]/label[1]/span[1]"))
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Guardar']"))
        print("🔵 CLICK EN EL CHECKBOX Y GUARDADO")
        time.sleep(4)

        find_and_click(driver, (By.LINK_TEXT, "Cuentas a la vista"))
        find_and_click(driver, (By.XPATH, "(//span[contains(text(),'Parametría')])[2]"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO A LA PARAMETRIA")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='descripcion']"), "LINEA PRUEBA TEST")
        print("🔵 BUSQUEDA DE LA LINEA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='LINEA PRUEBA TEST']"))
        print("🔵 SELECCION DE LINEA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Eliminar']"))
        print("🔵 CLICK EN ELIMINAR")

        modal_locator = (By.XPATH, "//app-dialog-simple")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(modal_locator))

        boton_eliminar_final = (By.XPATH, "//app-dialog-simple//button[contains(text(), 'Eliminar')]")
        find_and_click(driver, boton_eliminar_final)

        validar_mensaje_snackbar(driver, "Línea eliminada exitosamente")

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