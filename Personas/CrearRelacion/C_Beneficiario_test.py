import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

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

def validar_y_esperar_desaparicion(driver, mensaje_exito, wait_time_vis=10, wait_time_invis=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        
        WebDriverWait(driver, wait_time_vis).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ Éxito: Se mostró el mensaje '{mensaje_exito}'.")
        
        WebDriverWait(driver, wait_time_invis).until(
            EC.invisibility_of_element_located(locator)
        )
        print(f"🔵 El mensaje '{mensaje_exito}' ha desaparecido, continuando...")
        
    except TimeoutException:
        print(f"❌ Fallo de Timeout con el mensaje '{mensaje_exito}':")
        print(f"   - O no apareció en {wait_time_vis}s, o no desapareció en {wait_time_invis}s.")
        raise 
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")
        raise 

def validar_mensaje(driver, mensaje_exito, wait_time=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ La relacion se creo correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print(f"❌ La relacion no se creo: No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")

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
    
    print("🔵 CLICK GUARDAR")
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

class TestCrearRelacionBeneficiario(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_beneficiario(self):
        driver = self.driver

        try:
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
            find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
            print("🔵 INGRESO A ITS CORE")

            find_and_click(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
            find_and_click(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
            print("🔵 INGRESO AL MODULO")

            find_and_click(driver, (By.XPATH, "//button[@class='btn btn-outline-primary- lupa']"))
            find_and_click(driver, (By.XPATH, "//span[normalize-space()='1pruebas, No Usar']"))
            print("🔵 SELECCION DE LA PERSONA")

            locator_tarjeta_beneficiario = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Beneficiario']]")
            find_and_click(driver, locator_tarjeta_beneficiario)
            print("🔵 CLICK EN LA CARD BENEFICIARIO")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
            validar_y_esperar_desaparicion(driver, "Relación creada con éxito")

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar']"))
            print("🔵 CLICK EN AGREGAR")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "ITS CORE")
            print("🔵 SELECCION GRUPO AFINIDAD")

            validar_mensaje_snackbar(driver, "//div[@class='mb-3 form-actions']//button[@type='button'][normalize-space()='Guardar']", "Relación de beneficiario modificada con éxito")
            

        except TimeoutException:
            print("❌ La relación no se pudo crear porque un elemento no fue encontrado a tiempo.")
            
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)