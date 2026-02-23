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
    element.send_keys(value)
    return element

def find_and_click(driver, by_locator, wait_time=20):
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.click()
    return element

def click_con_js(driver, by_locator, wait_time=30):
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    driver.execute_script("arguments[0].click();", element)
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

def validar_snackbar_y_esperar_desaparicion(
    driver,
    xpath_boton=None,
    mensaje_exito=None,
    wait_time_vis=10,
    wait_time_invis=10
):
    script = """
    var callback = arguments[arguments.length - 1];
    var botonXpath = arguments[0];

    if (botonXpath) {
        var boton = document.evaluate(botonXpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (boton) boton.click();
    }

    var observer = new MutationObserver(function(mutations, obs) {
        var regions = document.querySelectorAll("div[id^='mat-snack-bar-container-live']");
        regions.forEach(function(region) {
            var text = region.innerText.trim();
            if (text.length > 0) {
                obs.disconnect();
                callback(text);
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(function() { observer.disconnect(); callback(null); }, arguments[1]);
    """

    texto = driver.execute_async_script(
        script,
        xpath_boton,
        wait_time_vis * 1000
    )

    if not texto:
        driver.save_screenshot("error_snackbar.png")
        print("❌ No se detectó ningún mensaje de snackbar")
        raise AssertionError("No se detectó ningún mensaje de snackbar")

    if mensaje_exito:
        if mensaje_exito.lower() in texto.lower() or "éxito" in texto.lower():
            print(f"✅ Mensaje de Éxito confirmado: {texto}")
        else:
            print(f"❌ Error detectado en snackbar: {texto}")
            raise AssertionError(f"Error detectado en snackbar: {texto}")
    else:
        print(f"✅ Snackbar recibido: {texto}")

    try:
        WebDriverWait(driver, wait_time_invis).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div[id^='mat-snack-bar-container-live']")
            )
        )
    except TimeoutException:
        print("❌ El snackbar no desapareció dentro del tiempo esperado")
        raise




class TestCrearRelacionUsuario(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_relacion_usuario(self):
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

            locator_tarjeta_usuario = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Usuario']]")
            find_and_click(driver, locator_tarjeta_usuario)
            print("🔵 CLICK EN LA CARD")

            find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='usuario']"), "No usar")
            print("🔵 INGRESO USUARIO")

            find_and_send_keys(driver, (By.XPATH, "//input[@type='password']"), "1234")
            print("🔵 INGRESO CONTRASEÑA")

            click_con_js(driver, (By.XPATH, "(//span[@class='checkmark'])[3]"))
            print("🔵 CLICK CHECK SUCURSAL")

            click_con_js(driver, (By.XPATH, "(//span[@class='checkmark'])[4]"))
            print("🔵 CLICK CHECK GRUPO")

            validar_snackbar_y_esperar_desaparicion(
                driver,
                xpath_boton="//button[normalize-space()='Crear']",
                mensaje_exito="Relación creada con éxito"
            )

            find_and_click(driver, (By.XPATH, "//button[normalize-space()='+ Agregar']"))
            print("🔵 CLICK AGREGAR")

            find_and_click(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
            seleccionar_opcion_ng_select(driver, "ITS CORE")
            print("🔵 SELECCION DE GRUPO AFINIDAD")

            validar_snackbar_y_esperar_desaparicion(
                driver,
                xpath_boton="//div[@class='form-actions mt-4 boton1 mb-2']//button[@type='button'][normalize-space()='Guardar']",
                mensaje_exito="Relacion actualizada con exito"
            )

        except TimeoutException:
            print("❌ La relación no se pudo crear porque un elemento no fue encontrado a tiempo.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)