import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def find_and_send_keys(driver, by_locator, value, wait_time=50):
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20):
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located(by_locator)
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element
    )
    WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.click()
    return element

def Checkbox_Xpath(driver, xpath, wait_time=10):
    try:
        val = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(xpath))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", val)
        val.click()
        print("Click en el elemento {}".format(xpath))
        
    except TimeoutException:
        print("No se encontro el Elemento" + str(xpath))
        raise


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
    
    print("🔵 CLICK BOTON CREAR")
    texto_capturado = driver.execute_async_script(script)
    
    if texto_capturado:
        if mensaje_exito.lower() in texto_capturado.lower() or "éxito" in texto_capturado.lower():
            print(f"✅ EXITO: {texto_capturado}")
        else:
            print(f"❌ ERROR DETECTADO EN PANTALLA: {texto_capturado}")
            raise AssertionError(f"Fallo en la prueba: Se detectó un error en pantalla: {texto_capturado}")
    else:
        driver.save_screenshot("fallo_captura_mensaje.png"),
        print("❌ No se capturó ningún mensaje. Se guardó captura: fallo_captura_mensaje.png")
        raise AssertionError("Fallo en la prueba: No se detectó ningún mensaje de confirmación o error (Timeout)")

class TestGrupoAfinidad(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_nuevo_grupoafinidad(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Personas"))
        find_and_click(driver, (By.LINK_TEXT, "Grupos de afinidad"))
        print("🔵 INGRESO AL MODULO")

        find_and_send_keys(driver, (By.XPATH, "//div[@class='col-md-4 pl-0']//input[@type='text']"), "Prueba")
        print("🔵 INGRESO DESCRIPCION")
        find_and_send_keys(driver, (By.XPATH, "//div[@class='col-md-2']//input[@type='text']"), "PP")
        print("🔵 INGRESO DE DESC REDUCIDA")
        find_and_send_keys(driver, (By.XPATH, "//div[@class='col-md-6']//input[@type='text']"), "Test de Prueba")
        print("🔵 INGRESO DE OBSERVACIONES")

        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Usuario']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Cliente']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Proveedor']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Entidad de cobro']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Vendedor']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Banco']/preceding-sibling::span[@class='checkmark']"))
        Checkbox_Xpath(driver, (By.XPATH, "//p[normalize-space()='Beneficiario']/preceding-sibling::span[@class='checkmark']"))
        print("🔵 CLICK EN EL CHECKBOX")

        validar_mensaje_snackbar(driver, "//button[normalize-space()='Crear']", "El grupo de afinidad fue creado correctamente.")

          
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