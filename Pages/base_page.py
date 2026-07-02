import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException


# ==============================================================================
# 1. VARIANTES DE ESCRIBIR (find_and_send_keys)
# ==============================================================================

def find_and_send_keys(driver, by_locator, value, wait_time=50):
    """Variante estándar: Espera visibilidad del elemento y escribe (sin clear)."""
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.send_keys(value)
    return element


def find_and_send_keys_with_clear(driver, by_locator, value, wait_time=50):
    """Variante con limpieza: Espera visibilidad, limpia el campo con .clear() y escribe."""
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.clear()
    element.send_keys(value)
    return element


def find_and_send_keys_with_scroll(driver, by_locator, value, wait_time=50):
    """Variante con Scroll: Espera presencia, centra la pantalla en el elemento, espera visibilidad, limpia y escribe."""
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located(by_locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    element.clear()
    element.send_keys(value)
    return element


def find_and_send_keys_clickable(driver, by_locator, value, wait_time=50):
    """Variante Clickable: Espera a que el elemento sea explícitamente cliqueable antes de escribir."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.send_keys(value)
    return element


# ==============================================================================
# 2. VARIANTES DE CLIC (find_and_click / click_js)
# ==============================================================================


def find_and_click(driver, by_locator, wait_time=20):
    """Espera a que sea cliqueable y hace clic convencional. 
    Si falla por intercepción (animaciones/spinners), lo fuerza mediante JavaScript."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    try:
        element.click()
    except (ElementClickInterceptedException, WebDriverException):
        driver.execute_script("arguments[0].click();", element)
        
    return element


def find_and_click_with_retries(driver, by_locator, wait_time=20, retries=3):
    """Variante con reintentos: Maneja excepciones de StaleElementReferenceException volviendo a intentar el clic."""
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


def find_and_click_with_scroll(driver, by_locator, wait_time=20):
    """Variante con Scroll: Espera presencia, centra el elemento en pantalla, espera que sea cliqueable y hace clic."""
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located(by_locator)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.click()
    return element


def find_and_click_check_disabled(driver, by_locator, wait_time=20):
    """Variante con validación de deshabilitado: Espera que sea cliqueable y asegura mediante una condición lambda que no posea atributos de 'disabled'."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    WebDriverWait(driver, wait_time).until(
        lambda d: not (
            element.get_attribute("disabled") == "true" or 
            "disabled" in (element.get_attribute("class") or "")
        )
    )
    element.click()
    return element


def find_and_click_via_js(driver, by_locator, wait_time=20):
    """Variante JS Nativo: Espera que sea cliqueable y ejecuta el clic forzado directamente por JavaScript."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    driver.execute_script("arguments[0].click();", element)
    return element


def wait_and_click_js(driver, by_locator, wait_time=15):
    """Variante JS con Scroll Superior: Espera que sea cliqueable, desplaza la pantalla arriba, pausa 0.5s y hace clic por JS."""
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable(by_locator)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", element)
        return element
    except TimeoutException:
        print(f"❌ No se pudo hacer clic con JS en el elemento: {by_locator}")
        raise


def click_con_js(driver, by_locator, wait_time=30):
    """Variante JS estándar: Espera que sea cliqueable (hasta 30s) y realiza el clic mediante JavaScript."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(by_locator)
    )
    driver.execute_script("arguments[0].click();", element)
    return element


def find_and_force_click(driver, by_locator, wait_time=20):
    """Variante Clic Forzado Visibilidad: Espera visibilidad del elemento y fuerza el clic mediante JavaScript."""
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(by_locator)
    )
    driver.execute_script("arguments[0].click();", element)
    return element


# ==============================================================================
# 3. VARIANTES DE CHECKBOX
# ==============================================================================

def click_checkbox(driver, locator, wait_time=10):
    """Variante Checkbox Visibilidad: Espera visibilidad, centra pantalla y hace clic por JS."""
    try:
        checkbox = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"🔵 Hizo clic en el checkbox: {locator}")
    except TimeoutException:
        print(f"❌ No se encontró el checkbox con el localizador: {locator}")
        raise


def Checkbox_Xpath(driver, xpath, wait_time=10):
    """Variante Checkbox Clickable: Espera a que sea cliqueable, centra pantalla y hace clic convencional."""
    try:
        val = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(xpath))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", val)
        val.click()
        print("Click en el elemento {}".format(xpath))
    except TimeoutException:
        print("No se encontro el Elemento" + str(xpath))
        raise


# ==============================================================================
# 4. VARIANTES DE DESPLEGABLES (seleccionar_opcion_ng_select)
# ==============================================================================

def seleccionar_opcion_ng_select(driver, texto_opcion, wait_time=10):
    """NG-Select Básico: Busca todas las opciones presentes y hace clic convencional sobre la que coincida."""
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


def seleccionar_opcion_ng_select_with_filter(driver, locator_input, texto_opcion, wait_time=10):
    """NG-Select Filtrado: Interactúa primero escribiendo en el input buscador, desplaza la opción al centro y la selecciona controlando con aserciones."""
    find_and_send_keys(driver, locator_input, texto_opcion, wait_time)
    time.sleep(0.5) 
    try:
        opciones = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ng-option"))
        )
        for opcion in opciones:
            if texto_opcion.lower() in opcion.text.lower():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion)
                opcion.click()
                return True
        raise AssertionError(f"❌ Falló: No se encontró la opción '{texto_opcion}' en el desplegable filtrado.")
    except TimeoutException:
         raise AssertionError(f"❌ Falló: Las opciones del desplegable nunca cargaron al buscar '{texto_opcion}'.")


def seleccionar_opcion_ng_select_js(driver, texto_opcion, wait_time=15):
    """NG-Select con Clic JS: Busca las opciones basándose en un tiempo extendido (15s) y ejecuta la selección forzada mediante JavaScript."""
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
    


# ==============================================================================
# 5. VARIANTES DE COPIAR IMPORTE
# ==============================================================================

def copiar_y_pegar_importe_3(driver, wait_time=10):
    """Lee el importe total desde el campo '#importe3' e inyecta el valor en el último campo de cobro activo por JS."""
    campo_total = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='importe3']"))
    )
    valor_copiado = campo_total.get_attribute("value") 
    campo_cobro = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, "(//input[@formcontrolname='importe'])[last()]"))
    )
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", campo_cobro, valor_copiado)
    return campo_cobro


def copiar_y_pegar_importe_2(driver, wait_time=10):
    """Lee el importe total desde el campo '#importe2' e inyecta el valor en el último campo de cobro activo por JS."""
    campo_total = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='importe2']"))
    )
    valor_copiado = campo_total.get_attribute("value") 
    campo_cobro = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, "(//input[@formcontrolname='importe'])[last()]"))
    )
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", campo_cobro, valor_copiado)
    return campo_cobro


# ==============================================================================
# 6. VARIANTES DE VALIDACIÓN DE TEXTOS EN PANTALLA (validar_mensaje)
# ==============================================================================

def validar_mensaje(driver, mensaje_esperado, wait_time=30):
    """Validación estándar genérica."""
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


def validar_mensaje_sesion(driver, mensaje_exito, wait_time=10):
    """Validación específica de inicio de sesión exitoso."""
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ Se inicio sesion correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print("❌ No se inicio sesion: No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")


def validar_mensaje_persona_creada(driver, mensaje_exito, wait_time=10):
    """Validación específica de creación de persona."""
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


def validar_mensaje_relacion_creada(driver, mensaje_exito, wait_time=10):
    """Validación específica de creación de relación."""
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ La relacion se creo correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print("❌ La relacion no se creo: No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")


def validar_mensaje_persona_eliminada(driver, mensaje_exito, wait_time=10):
    """Validación específica de eliminación de persona."""
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ La persona se elimino correctamente: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print("❌ La persona no se elimino: No apareció el mensaje de éxito esperado.")
    except Exception as e:
        print(f"❌ Ocurrió un error en la validación del mensaje: {e}")


def validar_y_esperar_desaparicion(driver, mensaje_exito, wait_time_vis=10, wait_time_invis=10):
    """Controla secuencialmente la aparición de un mensaje y su posterior desaparición absoluta de la interfaz."""
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


# ==============================================================================
# 7. VARIANTES DE VALIDACIÓN SNACKBAR (DOM Mutation & CSS Selectors)
# ==============================================================================

def validar_mensaje_snackbar(driver, mensaje_exito, timeout=10):
    """Snackbar convencional por CSS: Localiza de forma directa el contenedor nativo mediante selectores de Selenium."""
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


def validar_mensaje_snackbar_async_crear(driver, xpath_boton, mensaje_exito, timeout=5):
    """Snackbar Asíncrono de Creación: Utiliza un MutationObserver nativo de JS capturando el evento al pulsar el botón CREAR."""
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
    print("🔵 CLICK SEGUNDO BOTON CREAR")
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


def validar_mensaje_snackbar_async_eliminar(driver, xpath_boton, mensaje_exito, timeout=5):
    """Snackbar Asíncrono de Eliminación (Simple Log): Observer de JS que escribe log simple de un clic al eliminar."""
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


def validar_mensaje_snackbar_async_eliminar_click_click(driver, xpath_boton, mensaje_exito, timeout=5):
    """Snackbar Asíncrono de Eliminación (Doble Log): Observer de JS idéntico con registro en consola de doble clic secuencial."""
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
    print("🔵 CLICK CLICK SEGUNDO BOTON ELIMINAR")
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


def validar_mensaje_snackbar_async_guardar(driver, xpath_boton, mensaje_exito, timeout=5):
    """Snackbar Asíncrono de Guardado (Log Corto): Observer de JS que registra un log corto al presionar el botón de guardado."""
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


def validar_mensaje_snackbar_async_guardar_boton(driver, xpath_boton, mensaje_exito, timeout=5):
    """Snackbar Asíncrono de Guardado (Log Extendido): Observer de JS idéntico que registra un log extendido indicando el elemento exacto del botón."""
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


def validar_snackbar_y_esperar_desaparicion(driver, xpath_boton=None, mensaje_exito=None, wait_time_vis=10, wait_time_invis=10):
    """Snackbar Avanzado con Invisibilidad: Captura asíncronamente por JS el snackbar y luego fuerza por Selenium a esperar que desaparezca por completo antes de continuar con la prueba."""
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
    texto = driver.execute_async_script(script, xpath_boton, wait_time_vis * 1000)

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


# ==============================================================================
# 8. ESTRUCTURA DE CONTROL DE CONTADORES (Clase ContadorSecuencial)
# ==============================================================================

class ContadorSecuencial:
    """Clase encapsuladora para controlar la persistencia de números de control numérico incremental."""
    
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