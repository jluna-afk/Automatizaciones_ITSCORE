import unittest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click_with_scroll,
    find_and_click_via_js,
    seleccionar_opcion_ng_select_js,
    validar_mensaje,
    validar_mensaje_snackbar_async_guardar
)

class TestCrearRelacionEntidadCobro(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_entidad_cobro(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A ITS CORE")

        find_and_click_with_scroll(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
        find_and_click_with_scroll(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
        print("🔵 INGRESO AL MODULO")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[@class='btn btn-outline-primary- lupa']"))
        find_and_click_with_scroll(driver, (By.XPATH, "//span[normalize-space()='1pruebas, No Usar']"))
        print("🔵 SELECCION PERSONA")

        locator_tarjeta_entidad = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Entidad de cobro']]")
        find_and_click_with_scroll(driver, locator_tarjeta_entidad)
        print("🔵 ABRIR CARD")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        validar_mensaje(driver, "Relación creada con éxito")

        find_and_click_via_js(driver, (By.XPATH, "//button[@class='btn-secondary-its mr-2']"))
        print("🔵 CLICK EN CANCELAR")

        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click_with_scroll(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS PARAMETRIA")

        find_and_click_with_scroll(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA")

        find_and_click_with_scroll(driver, (By.XPATH, "//td[normalize-space()='LINEA DE PRESTAMO GENERICA']"))
        print("🔵 SELECCION PRESTAMO")
        time.sleep(1)

        find_and_click_with_scroll(driver, (By.XPATH, "//button[normalize-space()='+ Agregar Entidad de cobro']"))
        print("🔵 CLICK EN AGREGAR ENTIDAD DE COBRO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='entidadCobro']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "1pruebas, No Usar")
        print("🔵 SELECCION DE LA ENTIDAD 'PRUEBAS NO USAR'")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='estado']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activa")
        print("🔵 SELECCION DE ESTADO")

        input_fecha = driver.find_element(By.XPATH, "(//app-custom-date[@formcontrolname='fechaEstado']//input)[2]")
        
        actions = ActionChains(driver)
        actions.move_to_element(input_fecha).click().perform()
        time.sleep(0.2)

        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.send_keys(Keys.BACKSPACE).perform()
        time.sleep(0.2)

        fecha_a_ingresar = "21102026" 
        for digito in fecha_a_ingresar:
            actions.send_keys(digito).perform()
            time.sleep(0.05)  

        actions.send_keys(Keys.TAB).perform()
        print("🔵 INGRESO FECHA ESTADO (SEGUNDA FILA - SIMULACIÓN HUMANA COMPLETA)")
        time.sleep(0.5)


        validar_mensaje_snackbar_async_guardar(driver, "//button[normalize-space()='Guardar']","Línea actualizada correctamente")
        print("🔵 GUARDO LA RELACION")

        find_and_click_with_scroll(driver, (By.XPATH, "//span[normalize-space()='Personas']"))
        find_and_click_with_scroll(driver, (By.XPATH, "//a[@href='#/personas/gestion']"))
        print("🔵 INGRESO AL MODULO")

        find_and_click_with_scroll(driver, (By.XPATH, "//button[@class='btn btn-outline-primary- lupa']"))
        find_and_click_with_scroll(driver, (By.XPATH, "//span[normalize-space()='1pruebas, No Usar']"))
        print("🔵 SELECCION PERSONA")

        locator_tarjeta_entidad = (By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Entidad de cobro']]")
        find_and_click_with_scroll(driver, locator_tarjeta_entidad)
        print("🔵 ABRIR CARD")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='diaCorte']"), "1")
        print("🔵 INGRESO DIA DE CORTE")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='cantMesesDiferimiento']"), "0")
        print("🔵 INGRESO MESES DE DIFERIMIENTO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoEnvioCuotaPrestamo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Siguiente no enviada")
        print("🔵 SELECCION TIPO ENVIO PRESTAMO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoEnvioCuotaServicio']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Siguiente no enviada")
        print("🔵 SELECCION TIPO ENVIO SERVICIO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='envioTipoMora']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "D - Deuda")
        time.sleep(1)
        print("🔵 SELECCION TIPO ENVIO MORA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='envioPorcentajeMora']"), "50")
        print("🔵 INGRESO PORCENTAJE MORA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='topeImporte']"), "1000")
        print("🔵 INGRESO TOPE REGISTRO")

        find_and_click_with_scroll(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[1]"))
        print("🔵 CLICK EN AGREGAR")
        
        find_and_click_with_scroll(driver, (By.XPATH, "//div[@class='selector']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "IMPUESTO AL VALOR AGREGADO")
        print("🔵 SELECCION TIPO SITUACION")
        time.sleep(1)

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='subTipo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "RESPONSABLE INSCRIPTO")
        print("🔵 SELECCION SUBTIPO")
        time.sleep(1)

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='clase']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "TASA GENERAL")
        print("🔵 SELECCION CLASE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='numeroInscripcion']"), "123456")
        print("🔵 N° INSCRIPCION")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='pais']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ARGENTINA")
        print("🔵 SELECCION PAIS")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@formcontrolname='provincia']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "SANTA FE")
        print("🔵 SELECCION PROVINCIA")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='localidad']//div[@class='ng-select-container']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ROSARIO")
        print("🔵 SELECCION LOCALIDAD")

        find_and_click_with_scroll(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[2]"))     
        print("🔵 CLICK EN AGREGAR PORCENTAJE")   

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='operatoria_prueba']"))
        seleccionar_opcion_ng_select_js(driver, "Préstamo (6)")
        print("🔵 SELECCION OPERATORIA PORCENTAJE")
        time.sleep(1)

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='linea_prueba']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "LINEA DE PRESTAMO GENERICA (1)")
        print("🔵 SELECCION LINEA PORCENTAJE")
        time.sleep(0.5)

        find_and_click_with_scroll(driver, (By.XPATH, "(//ng-select[@formcontrolname='envioTipoMora']//input[@type='text'])[2]"))
        seleccionar_opcion_ng_select_js(driver, "D - Deuda")
        print("🔵 SELECCION TIPO ENVIO MORA PORCENTAJE")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='envioPorcentajeMoraPrueba']"), "50")
        print("🔵 INGRESO PORCENTAJE MORA")

        find_and_click_with_scroll(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[3]"))     
        print("🔵 CLICK EN AGREGAR PRIORIDAD")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='operatoria_id']"))
        seleccionar_opcion_ng_select_js(driver, "Préstamo (6)")
        print("🔵 SELECCION OPERATORIA PRIORIDAD")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='linea_id']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "LINEA DE PRESTAMO GENERICA (1)")
        print("🔵 SELECCION LINEA PRIORIDAD")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='porcentaje']"), "50")
        print("🔵 INGRESO PORCENTAJE PRIORIDAD")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='orden']"), "1")
        print("🔵 INGRESO PORCENTAJE ORDEN")

        find_and_click_with_scroll(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[4]"))     
        print("🔵 CLICK EN AGREGAR CODIGO DESCUENTO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='operatoria_cd']"))
        seleccionar_opcion_ng_select_js(driver, "Préstamo (6)")
        print("🔵 SELECCION OPERATORIA CODIGO DESCUENTO")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='linea_cd']"))
        seleccionar_opcion_ng_select_js(driver, "LINEA DE PRESTAMO GENERICA (1)")
        print("🔵 SELECCION LINEA CODIGO DESCUENTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='codigo_descuento']"), "1")
        print("🔵 INGRESO CODIGO DESCUENTO")

        find_and_click_with_scroll(driver, (By.XPATH, "(//button[@type='button'][normalize-space()='+ Agregar'])[5]"))
        print("🔵 CLICK EN AGREGAR")

        find_and_click_with_scroll(driver, (By.XPATH, "//ng-select[@id='grupo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "ITS CORE")
        print("🔵 SELECCION GRUPO AFINIDAD")

        validar_mensaje_snackbar_async_guardar(driver, "(//button[@type='button'][normalize-space()='Guardar'])[2]", "Relación modificada con éxito")

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