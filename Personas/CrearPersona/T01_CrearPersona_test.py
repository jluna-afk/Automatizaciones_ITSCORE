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
    except Exception:
        return False

def validar_mensaje(driver, mensaje_exito, wait_time=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ La persona se creo correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print("❌ La persona no se creo: No apareció el mensaje de éxito esperado.")
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
    
    print("🔵 CLICK SEGUNDO BOTON ELIMINAR")
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

class TestPersonaGestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_nueva_persona(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A ITS CORE")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
        find_and_click(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
        print("🔵 INGRESO AL MODULO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='nombre']"), "Jagger")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='apellido']"), "Luna")
        print("🔵 INGRESO DEL NOMBRE")
        
        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='sexo']//input[@type='text']"), "Masculino")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Masculino']"))
        print("🔵 INGRESO SEXO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='estado_civil']//input[@type='text']"), "Soltero")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='Soltero/a']"))
        print("🔵 INGRESO ESTADO CIVIL")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='tipo_documento']//input[@type='text']"), "masculino")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='DNI Masculino']"))
        print("🔵 INGRESO TIPO DOC")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='documento']"), "77777777")
        print("🔵 INGRESO N° DNI")
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fecha_nacimiento']//input[@type='text']"), "21102021")
        print("🔵 INGRESO FECHA NAC")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='nacionalidad']//input[@type='text']"), "argentina")
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='ARGENTINA']"))
        print("🔵 INGRESO NACIONALIDAD")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_tributario']"), "20777777778")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='calle']"), "Juan Manuel de Rosas")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='numero']"), "987")
        print("🔵 INGRESO DOMICILIO")

        find_and_send_keys(driver, (By.XPATH, "//ng-select[@id='pais']//input[@type='text']"), "ARGENTINA")
        find_and_click(driver, (By.XPATH, "(//span[@class='ng-option-label'][normalize-space()='ARGENTINA'])[1]"))
        print("🔵 INGRESO PAIS")

        find_and_click(driver, (By.CSS_SELECTOR, "ng-select#provincia div[role='combobox']"))
        find_and_send_keys(driver, (By.XPATH, "//div[@aria-expanded='true']//input[@type='text']"), "Santa Fe")
        find_and_click(driver, (By.XPATH, "(//span[normalize-space()='Santa Fe'])[1]"))
        print("🔵 INGRESO LOCALIDAD")

        find_and_click(driver, (By.CSS_SELECTOR, "ng-select#localidad div[role='combobox']"))
        find_and_send_keys(driver, (By.CSS_SELECTOR, "ng-select#localidad div[role='combobox'] input[type='text']"), "Stephenson")
        time.sleep(1)  
        seleccionar_opcion_ng_select(driver, "Stephenson - (2103)")
        print("🔵 INGRESO CIUDAD")

        find_and_click(driver, (By.XPATH, "(//ng-select[@id='tipo'])[1]//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Telefono movil")
        find_and_send_keys(driver, (By.XPATH, "(//input[@id='dato'])[1]"), "3416956694")
        print("🔵 INGRESO TELEFONO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar medio de comunicación']"))
        find_and_click(driver, (By.XPATH, "(//ng-select[@id='tipo'])[2]//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Correo electronico")
        find_and_send_keys(driver, (By.XPATH, "(//input[@id='dato'])[2]"), "jluna@quo.ar")
        print("🔵 INGRESO CORREO ELECTRONICO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='cbu']"), "0170282040000036262342")
        print("🔵 INGRESO CBU")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='alias']"), "Jagger.luna")
        print("🔵 INGRESO ALIAS")
        find_and_click(driver, (By.XPATH, "//ng-select[@id='estado']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Activa")
        print("🔵 INGRESO ESTADO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='empresa']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Activos Provinciales Santa Fe")
        print("🔵 INGRESO ENTIDAD COBRO")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='identificadorDescuento']"), "123456789")
        print("🔵 INGRESO ID DE DESCUENTO")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='sueldo_bruto']"), "1200000")
        find_and_send_keys(driver, (By.XPATH, "//input[@id='sueldo_neto']"), "1000000")
        print("🔵 INGRESO SUELDOS")
        find_and_click(driver, (By.XPATH, "//ng-select[@id='estado']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select(driver, "Activo")
        print("🔵 INGRESO ESTADO LEGAJO")
        
        find_and_click(driver, (By.CSS_SELECTOR, "ng-select[id='actividad'] input[type='text']"))
        find_and_send_keys(driver, (By.CSS_SELECTOR, "ng-select[id='actividad'] input[type='text']"), "monotributista")
        seleccionar_opcion_ng_select(driver, "Monotributista")
        print("🔵 INGRESO ACTIVIDAD")

        validar_mensaje_snackbar(driver, "//button[normalize-space()='Crear']", "Persona ingresada o actualizada exitosamente")

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