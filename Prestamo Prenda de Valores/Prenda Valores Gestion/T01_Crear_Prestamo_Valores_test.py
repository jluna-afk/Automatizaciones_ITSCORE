import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    validar_mensaje_snackbar,
    seleccionar_opcion_ng_select_js,
    copiar_y_pegar_importe_3,
    ContadorSecuencial
)

class Test_PrendaValores_Gestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

        self.generador_cheques = ContadorSecuencial(
                    archivo_contador="contador_cheque.txt",
                    min_valor=11111111111111111111111111111,
                    max_valor=22222222222222222222222222222
                )

    def test_crear_prestamo_prenda_valores(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Prést. con prenda valores"))
        find_and_click(driver, (By.LINK_TEXT, "Gestión"))
        print("🔵 INGRESO AL MODULO DE PRENDA VALORES GESTION")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK LUPITA LINEA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='descripcion']"), "Prestamo basico")
        print("🔵 INGRESO DE DESCRIPCION")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='PRESTAMO BASICO']"))
        print("🔵 SELECCION LINEA")

        find_and_click(driver, (By.XPATH, "//form[@class='ng-untouched ng-pristine ng-invalid']//div//div[@class='d-flex mt-3']//i[@class='fas fa-search']"))
        print("🔵 CLICK LUPITA PERSONA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_apellido_nombre']"), "WHPEI")
        print("🔵 INGRESO PERSONA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 SELECCION LINEA")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='WHPEI, SANTIAGO ELIAS']"))
        print("🔵 SELECCION PERSONA")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        
        validar_mensaje_snackbar(driver, "Préstamo creado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingreso de Valores']"))
        print("🔵 CLICK EN INGRESO DE VALORES")

        numero_cheque_unico = self.generador_cheques.obtener_siguiente()
        input_numero_cheque = (By.XPATH, "//input[@id='codigoCheque']")
        find_and_send_keys(driver, input_numero_cheque, numero_cheque_unico)
        print("🔵 INGRESANDO NUMERO CHEQUE")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='cuit']"), "20416561398")
        print("🔵INGRESANDO CUIT")
        
        find_and_send_keys(driver, (By.XPATH, "//input[@id='diasCamara']"), "1")
        print("🔵INGRESANDO DIAS DE CAMARA")
    
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaEmision']//input"), "19/07/2028")
        print("🔵INGRESANDO FECHA EMISION")
                
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaVencimiento']//input"), "19/07/2028")
        print("🔵INGRESANDO FECHA VENCIMIENTO")
        
        find_and_send_keys(driver, (By.XPATH, "//input[@id='importe']"), "1500")
        print("🔵INGRESANDO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 CLICK EN GUARDAR")

        validar_mensaje_snackbar(driver, "Cuota agregada correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Cerrar']"))
        print("🔵 CLICK EN CERRAR")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK EN APROBAR")

        validar_mensaje_snackbar(driver, "Préstamo aprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Desaprobar']"))
        print("🔵 CLICK EN DESAPROBAR")

        validar_mensaje_snackbar(driver, "Préstamo desaprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK EN APROBAR")
        
        validar_mensaje_snackbar(driver, "Préstamo aprobado correctamente")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Liquidar']"))
        print("🔵 CLICK EN LIQUIDAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='formaPago']"))
        seleccionar_opcion_ng_select_js(driver,"Cuenta a la vista")
        print("🔵 SELECCION FORMA DE PAGO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='cuentaDestino']"))
        seleccionar_opcion_ng_select_js(driver,"CUENTAS COMERCIALES")
        print("🔵 SELECCION CUENTA DESTINO")
        time.sleep(0.5)

        copiar_y_pegar_importe_3(driver, wait_time=10)
        print("🔵INGRESANDO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")

        validar_mensaje_snackbar(driver, "Préstamo prenda de valores liquidado correctamente")


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