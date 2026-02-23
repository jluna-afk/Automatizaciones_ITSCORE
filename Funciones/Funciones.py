import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Funciones:
    def __init__(self, driver):
        self.driver = driver
        self.wait_time = 10

    def Tiempo(self, tie):
        t=time.sleep(tie)
        return t
    
    def Navegar(self, Url):
        self.driver.get(Url)
        self.driver.maximize_window()
    
    def Texto_Xpath(self, xpath, texto):
        try:
            element = WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(texto)
            print("escribiendo en el campo{} el texto {}".format(xpath,texto))
        except TimeoutException:
            print(f"Error: Elemento con XPath '{xpath}' no encontrado o no visible después de {self.wait_time} segundos.")
            raise NoSuchElementException(f"Elemento con XPath '{xpath}' no encontrado o no visible.")
        except NoSuchElementException:
            print(f"Error: Elemento con XPath '{xpath}' no existe en el DOM.")
            raise

    def Click_Xpath(self, xpath):
        try:
            element = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
        except TimeoutException:
            print(f"Error: Elemento con XPath '{xpath}' no clicable o no encontrado después de {self.wait_time} segundos.")
            raise NoSuchElementException(f"Elemento con XPath '{xpath}' no clicable o no encontrado.")
        except NoSuchElementException:
            print(f"Error: Elemento con XPath '{xpath}' no existe en el DOM.")
            raise

    def Click_LinkText(self, linktext):
        try:
            locator = (By.LINK_TEXT, linktext)
            element = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            element.click()
            print(f"Click exitoso en el link: '{linktext}'")

        except TimeoutException:
            error_msg = f"Error: El elemento con texto de link '{linktext}' no se encontró o no fue clicable después de {self.wait_time} segundos."
            print(error_msg)
            raise Exception(error_msg)
        
    def copiar_pegar(self, xpath_origen, xpath_destino):
        try:
            origen = WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath_origen))
            )
            
            destino = WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath_destino))
            )

            acciones = ActionChains(self.driver)
            
            acciones.click(origen) \
                    .key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL) \
                    .key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL) \
                    .click(destino) \
                    .key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL) \
                    .perform()

            print(f"Texto copiado de '{xpath_origen}' y pegado en '{xpath_destino}' exitosamente.")

        except TimeoutException:
            print(f"Error: No se pudo localizar el elemento de origen o destino en el tiempo especificado.")
            raise
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            raise

    def Checkbox_Xpath(self, xpath):
        try:
            val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView();", val)
            val.click()
            print("Click en el elemento {}".format(xpath))
            
        except TimeoutException as ex:
            print(ex.msg)
            print("No se encontro el Elemento" + xpath)

    def Checkbox_Xpath_Multiples(self, *args):
        try:
            for num in args:
                val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, num)))
                self.driver.execute_script("arguments[0].scrollIntoView();", val)
                val.click()
                print("Click en el elemento {}".format(num))
            
        except TimeoutException as ex:
            for num in args:
                print(ex.msg)
                print("No se encontro el Elemento" + num)
            

    def upload_file_xpath(self, xpath_input, ruta_archivo, wait_time=10):
        try:
            wait = WebDriverWait(self.driver, wait_time)
            
            elemento = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath_input))
            )
            
            elemento.send_keys(ruta_archivo)
            print(f"✅ Ruta '{ruta_archivo}' enviada correctamente al elemento.")

        except TimeoutException:
            print(f"❌ Error de tiempo: El elemento para subir el archivo no se encontró en {wait_time} segundos con el XPath: {xpath_input}")
        except Exception as e:
            print(f"❌ No se pudo enviar la ruta al elemento. Error: {e}")

    def validar_mensaje(driver, mensaje_exito, wait_time=10):
        try:
            locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
            WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
            )
            print(f"✅ La persona se creo correctamente: Se mostró el mensaje '{mensaje_exito}'.")
        except TimeoutException:
            print(f"❌ La persona no se creo: No apareció el mensaje de éxito esperado.")
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
    

    def Mouse_Doble(self,tipo,selector,tiempo=.2):
        if(tipo=="xpath"):
            try:
                val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, selector)))
                val = self.driver.execute_script("arguments[0].scrollIntoView();", val)
                val = self.driver.find_element_by_xpath(selector)
                act = ActionChains(self.driver)
                act.double_click(val).perform()
                print("DoubleClick en {}".format(selector))
                t = time.sleep(tiempo)
                return t
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                return t
        elif(tipo == "id"):
            try:
                val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, selector)))
                val = self.driver.execute_script("arguments[0].scrollIntoView();", val)
                val = self.driver.find_element_by_id(selector)
                act = ActionChains(self.driver)
                act.double_click(val).perform()
                print("DoubleClick en {}".format(selector))
                t = time.sleep(tiempo)
                return t
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                return t
            
    def Mouse_Derecho(self,tipo,selector,tiempo=.2):
        if(tipo=="xpath"):
            try:
                val=self.SEX(selector)
                act = ActionChains(self.driver)
                act.context_click(val).perform()
                print("ClickDerecho en {}".format(selector))
                t = time.sleep(tiempo)
                return t
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                return t
        elif(tipo == "id"):
            try:
                val=self.SEI(selector)
                act = ActionChains(self.driver)
                act.context_click(val).perform()
                print("ClickDerecho en {}".format(selector))
                t = time.sleep(tiempo)
                return t
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                return t
            
    def Mouse_DragDrop(self,tipo,selector,destino):
        if(tipo=="xpath"):
            try:
                val=self.SEX(selector)
                val2=self.SEX(destino)
                act = ActionChains(self.driver)
                act.drag_and_drop(val,val2).perform()
                print("Se solto el elemento {}".format(selector))
                
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                
        elif(tipo == "id"):
            try:
                val=self.SEI(selector)
                val2=self.SEI(destino)
                act = ActionChains(self.driver)
                act.drag_and_drop(val,val2).perform()
                print("Se solto el elemento {}".format(selector))
            
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)

    def Mouse_DragDrop_Coordenas(self,tipo,selector,x,y):
        if(tipo=="xpath"):
            try:
                self.driver.switch_to.frame(0)
                val=self.SEX(selector)
                act = ActionChains(self.driver)
                act.drag_and_drop_by_offset(val,x,y).perform()
                print("Se solto el elemento {}".format(selector))
                
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                
        elif(tipo == "id"):
            try:
                self.driver.switch_to.frame(0)
                val=self.SEI(selector)
                act = ActionChains(self.driver)
                act.drag_and_drop_by_offset(val,x,y).perform()
                print("Se solto el elemento {}".format(selector))
            
            except TimeoutException as ex:
                print(ex.msg)
                print("No se encontro el Elemento" + selector)
                
    
    def SEX(self, elemento):
        val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, elemento)))
        self.driver.execute_script("arguments[0].scrollIntoView();", val)
        return val

    def SEI(self, elemento):
        val = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, elemento)))
        self.driver.execute_script("arguments[0].scrollIntoView();", val)
        return val
    
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
    

    def Texto_ID(self, ID, texto):
        valor=self.driver.find_element(By.ID, ID)
        valor.clear()
        valor.send_keys(texto)
        

    def find_and_send_keys(self, by_locator, value, wait_time=50):
        element = WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(by_locator)
        )
        element.send_keys(value)
        return element

    def find_and_click(self, by_locator, wait_time=20):
        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(by_locator)
        )
        element.click()
        return element
    
    def find_and_click_js(driver, by_locator, wait_time=20):
        """
        Espera a que un elemento sea visible y luego le hace clic usando JavaScript.
        Ideal para elementos que Selenium no considera 'clicables'.
        """
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located(by_locator)
            )
            driver.execute_script("arguments[0].click();", element)
            return element
        except TimeoutException:
            print(f"No se pudo encontrar o hacer clic (JS) en el elemento: {by_locator}")
            raise

    def seleccionar_opcion_ng_select(self, texto_opcion, wait_time=10):
        try:
            opciones = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ng-option"))
            )
            for opcion in opciones:
                if texto_opcion.lower() in opcion.text.lower():
                    opcion.click()
                    return True
            return False
        except Exception as e:
            return False

    def validar_mensaje(self, mensaje_exito, wait_time=10):
        try:
            locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            print(f"✅ La relacion se creo correctamente: Se mostró el mensaje '{mensaje_exito}'.")
        except TimeoutException:
            print(f"❌ La relacion no se creo: No apareció el mensaje de éxito esperado.")
        except Exception as e:
            print(f"❌ Ocurrió un error en la validación del mensaje: {e}")

    def select_by_value(self, by, locator, value):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by, locator))
        )
        dropdown_select = Select(dropdown)
        dropdown_select.select_by_value(value)

    def rellenar_campo(self, campo_id, valor):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, campo_id))
        )
        campo = self.driver.find_element(By.ID, campo_id)
        campo.clear()
        campo.send_keys(valor)

    def visibility(self, by, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        return element

    def invisibility(self, by, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, locator))
        )
        return element

    def located(self, by, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return element

    def clickeable(self, by, locator, click=False, keys=False, clear=False):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by, locator))
        )
        if click:
            element.click()
        if clear:
            element.clear()
        if keys:
            element.send_keys(keys)
        return element

    def clickear_elemento_correspondiente_por_operacion(
        self, numero_operacion, id_prefix_span, id_prefix_click, click=False
    ):
        try:
            # Busca el elemento <span> que contiene el texto del número de operación
            elemento_span = self.driver.find_elements(
                By.CSS_SELECTOR, f"[id^='{id_prefix_span}']"
            )
            numero_final = None
            # Itera sobre los elementos encontrados
            for elemento in elemento_span:
                texto_elemento = elemento.text
                if numero_operacion in elemento.text:
                    span_id = elemento.get_attribute("id")
                    numero_final = span_id.split("_")[-1]
                    break
            if numero_final:
                # Construye el id del elemento a clickear usando id_prefix_click y el número extraído
                id_click = f"{id_prefix_click}_{numero_final}"
                # Encuentra y clickea el elemento correspondiente
                elemento_click = self.clickeable(By.ID, id_click)
                if click:
                    elemento_click.click()
                return elemento_click
        except NoSuchElementException:
            print(
                f"No se encontró el elemento con número de operación: {numero_operacion}"
            )
            self.close()

    def close(self):
        try:
            self.driver.quit()
            return True
        except Exception as e:
            return False

    def loader(self):
        print("loader")
        try:
            self.located(By.CLASS_NAME, "gx-mask", 3)
        except Exception as e:
            print("no encontrado")
        try:
            self.invisibility(By.CLASS_NAME, "gx-mask", 10)
        except Exception as e:
            print("visible")
        return True