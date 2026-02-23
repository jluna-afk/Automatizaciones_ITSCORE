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

class TestCrearRelacionCliente(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_cliente(self):
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
            print("🔵 SELECCION PERSONA")

            find_and_click(driver,(By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Cliente']]"))
            print("🔵 CLICK EN LA CARD CLIENTE")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoCliente']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Asociado Activo")
            print("🔵 SELECCION DE TIPO CLIENTE")

            find_and_click(driver,(By.XPATH, "//button[normalize-space()='Crear']"))
            print("🔵 CLICK EN CREAR")

            find_and_click(driver,(By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[1]"))
            print("🔵 CLICK EN AGREGAR")
            
            find_and_click(driver, (By.XPATH, "//div[@class='selector']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "IMPUESTO AL VALOR AGREGADO")
            print("🔵 SELECCION TIPO SITUACION")
            time.sleep(1)

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='subTipo']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "RESPONSABLE INSCRIPTO")
            print("🔵 SELECCION SUBTIPO")
            time.sleep(1)

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='clase']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "TASA GENERAL")
            print("🔵 SELECCION CLASE")

            find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='numeroInscripcion']"), "123456")
            print("🔵 N° INSCRIPCION")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='pais']//div[@class='ng-select-container']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "ARGENTINA")
            print("🔵 SELECCION PAIS")

            find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='provincia']//div[@class='ng-select-container']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "SANTA FE")
            print("🔵 SELECCION PROVINCIA")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='localidad']//div[@class='ng-select-container']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "ROSARIO")
            print("🔵 SELECCION LOCALIDAD")

            find_and_click(driver,(By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[2]"))
            print("🔵 CLICK BOTON AGREGAR")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "ITS CORE")
            print("🔵 SELECCION GRUPO AFINIDAD")

            find_and_click(driver, (By.XPATH, "//div[@class='input-container-search position-relative']//button[@type='button']"))
            find_and_send_keys(driver, (By.XPATH, "//input[@id='id_apellido_nombre']"), "1pruebas, No Usar")
            find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
            find_and_click(driver, (By.XPATH, "//td[normalize-space()='1pruebas, No Usar']"))
            print("🔵 SELECCION PRINCIPAL GRUPO FAMILIAR")

            find_and_click(driver, (By.XPATH, "//body/div[@class='cdk-overlay-container']/div[@class='cdk-global-overlay-wrapper']/div[@id='cdk-overlay-1']/mat-dialog-container[@id='mat-mdc-dialog-1']/div[@class='mdc-dialog__container']/div[@class='mat-mdc-dialog-surface mdc-dialog__surface']/app-cliente[@class='mat-mdc-dialog-component-host']/div[@class='page-container modal-container']/div/div[4]/button[1]"))
            print("🔵 CLICK AGREGAR")

            find_and_click(driver, (By.XPATH, "//div[@class='col-md-5 pl-0']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "Hermano/a")
            print("🔵 SELECCION TIPO PARENTESCO")

            find_and_click(driver, (By.XPATH, "//div[@class='col-md-7 pr-0']//button[@type='button']"))
            find_and_click(driver, (By.XPATH, "//td[normalize-space()='RAPUZZI, FERNANDO LUIS']"))
            print("🔵 SELECCION PERSONA FAMILIAR")
            
            validar_mensaje_snackbar(driver, "//div[@class='mb-3 d-flex justify-content-end form-actions buttons']//button[@type='button'][normalize-space()='Guardar']", "Relación de cliente modificada con éxito")

        except TimeoutException:
            print("❌ La relación no se pudo crear porque un elemento no fue encontrado a tiempo.")
            
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)