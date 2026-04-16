import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  StaleElementReferenceException
import os

class GeneradorNumeroSecuencial:
    def __init__(self, archivo_contador, min_valor, max_valor):
        self.archivo_contador = archivo_contador
        self.min_valor = min_valor
        self.max_valor = max_valor

    def obtener_siguiente(self):
        try:
            with open(self.archivo_contador, 'r') as f:
                numero_actual = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            numero_actual = self.min_valor

        if numero_actual > self.max_valor:
            numero_actual = self.min_valor
            
        proximo_numero = numero_actual + 1
        with open(self.archivo_contador, 'w') as f:
            f.write(str(proximo_numero))
            
        return str(numero_actual)

def find_and_send_keys(driver, by_locator, value, wait_time=50):
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20, retries=3):
    attempts = 0
    while attempts < retries:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable(by_locator)
            )
            element.click()
            return element
        except StaleElementReferenceException:
            print(f"Advertencia: StaleElementReferenceException. Reintentando clic... Intento {attempts + 1}")
            attempts += 1
            time.sleep(0.5)
    raise Exception(f"No se pudo hacer clic en el elemento {by_locator} después de {retries} intentos.")


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
    except Exception:
        return False

def validar_mensaje_snackbar(driver, xpath_boton, mensaje_exito, timeout=5):
    script = f"""
    var callback = arguments[arguments.length - 1];
    var boton = document.evaluate("{xpath_boton}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    
    var observer = new MutationObserver(function(mutations, obs) {{
        var regions = document.querySelectorAll("div[id^='mat-snack-bar-container-live']");
        regions.forEach(function(region) {{
            var text = region.innerText.trim();
            if (text.length > 0) {{
                obs.disconnect();
                callback(text);
            }}
        }});
    }});

    observer.observe(document.body, {{ childList: true, subtree: true }});
    if (boton) {{ boton.click(); }}
    setTimeout(function() {{ observer.disconnect(); callback(null); }}, {timeout * 1000});
    """
    
    print("🔵 CLICK BOTON GUARDAR")
    texto_capturado = driver.execute_async_script(script)
    
    if texto_capturado:
        if mensaje_exito.lower() in texto_capturado.lower() or "éxito" in texto_capturado.lower():
            print(f"✅ EXITO: {texto_capturado}")
        else:
            print(f"❌ ERROR DETECTADO EN PANTALLA: {texto_capturado}")
            raise AssertionError(f"Fallo en la prueba: Se detectó un error en pantalla: {texto_capturado}")
            
    else:
        driver.save_screenshot("fallo_captura_mensaje.png")
        print("❌ No se capturó ningún mensaje. Se guardó captura: fallo_captura_mensaje.png")
        raise AssertionError("Fallo en la prueba: No se detectó ningún mensaje de confirmación o error (Timeout)")

class TestAgregarCheque(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

        self.generador_cheques = GeneradorNumeroSecuencial(
            archivo_contador="contador_cheque.txt",
            min_valor=17,
            max_valor=50
        )

    def test_agregar_cheque(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Banco']"))
        find_and_click(driver, (By.XPATH, "//a[contains(@href, '#/banco/gestion')]"))
        print("🔵INGRESO A BANCO GESTION")

        find_and_click(driver, (By.XPATH, "//button[@class='btn btn-outline-primary lupa']"))          
        find_and_click(driver, (By.XPATH, "(//td[contains(text(),'45 - TELEPAGOS')])[1]"))
        print("🔵SELECCION DE CUENTA BANCARIA")

        find_and_click(driver, (By.XPATH, "(//td[@class='d-flex justify-content-end align-items-center pr-tabla'])[1]"))
        print("🔵ABRIENDO CHEQUERA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar cheque']"))

        numero_cheque_unico = self.generador_cheques.obtener_siguiente()

        input_numero_cheque = (By.XPATH, "//tbody/tr[last()]//input[@id='numero']")
        find_and_send_keys(driver, input_numero_cheque, numero_cheque_unico)
        print("🔵INGRESANDO NUMERO CHEQUE")
        
        find_and_send_keys(driver, (By.XPATH, "//tbody/tr[last()]/td[4]//app-custom-date//input"), "31/12/2027")
        print("🔵INGRESANDO FECHA VENCIMIENTO")

        find_and_click(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='Guardar'])[2]"))
        print("🔵CLICK BOTON GUARDAR")

        validar_mensaje_snackbar(driver, "//button[@type='submit']", "Chequera actualizada correctamente")


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