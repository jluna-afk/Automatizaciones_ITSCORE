import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje_snackbar
)

class Test_Prestamos_Parametria(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_linea_prestamo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Amortizable"))
        find_and_click(driver, (By.LINK_TEXT, "Parametría"))
        find_and_click(driver, (By.LINK_TEXT, "Líneas"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS PARAMETRIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcion']"), "Test Crear Linea Prestamo")
        print("🔵 INGRESO DE DESCRIPCION")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='descripcionReducida']"), "TestPrueba")
        print("🔵 INGRESO DESCRIPCION REDUCIDA")
        
        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaDesde']//input[@type='text']"), "10112027")
        print("🔵 INGRESO FECHA DESDE")

        input_moneda = find_and_send_keys(driver, (By.XPATH, "//ng-select[@formcontrolname='moneda']//input[@type='text']"), "Pesos")
        time.sleep(0.5)
        input_moneda.send_keys(Keys.ENTER)
        print("🔵 INGRESO MONEDA PESOS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='agrupacion']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "General")
        print("🔵 SELECCION AGRUPACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='formaLiquidacion']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Amortizable")
        print("🔵 SELECCION FORMA LIQUIDACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='sistema']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Francés")
        print("🔵 SELECCION SISTEMA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='metodo']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Manual")
        print("🔵 SELECCION METODO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoTasa']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Fija")
        print("🔵 SELECCION FORMA LIQUIDACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='tipoIngresos']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Nominal")
        print("🔵 SELECCION TIPO DE INGRESOS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='claseTasa']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Vencida")
        print("🔵 SELECCION CLASE DE TASA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='claseTasa']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Vencida")
        print("🔵 SELECCION CLASE DE TASA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='moduloTasa']"), "1")
        print("🔵 INGRESO MODULO DE LA TASA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='unidadAmortizacion']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Meses")
        print("🔵 SELECCION CLASE DE TASA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantidadAmortizaciones']"), "1")
        print("🔵 INGRESO CANTIDAD DE AMORTIZACIONES")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='primeraCuota']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Igual")
        print("🔵 SELECCION PRIMERA CUOTA")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='vencimientos']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Mismo día o hábil posterior")
        print("🔵 SELECCION VENCIMIENTOS")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='importeCuotas']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "igual")
        print("🔵 SELECCION IMPORTE CUOTAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='diaPrimerVencimiento']"), "10")
        print("🔵 INGRESO DIA PRIMER VENCIMIENTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='diaCorte']"), "10")
        print("🔵 INGRESO DIA DE CORTE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='mesesDiferimientoPrimerCuota']"), "0")
        print("🔵 INGRESO MESES DE DIFERIMIENTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='periodoDiferimiento']"), "0")
        print("🔵 INGRESO PERIODO DE DIFEREMIENTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='diasGraciaCompensacion']"), "0")
        print("🔵 INGRESO DIAS DE GRACIA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tasaPunitorio']"), "0")
        print("🔵 INGRESO TASA PUNITORIO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tasaMinima']"), "1")
        print("🔵 INGRESO TASA MIN")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tasaMaxima']"), "10")
        print("🔵 INGRESO TASA MAX")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importeMinimo']"), "1000")
        print("🔵 INGRESO IMPORTE MIN")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='importeMaximo']"), "10000")
        print("🔵 INGRESO IMPORTE MAX")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantidadMinimaCuotas']"), "1")
        print("🔵 INGRESO CANTIDAD MIN CUOTAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='cantidadMaximaCuotas']"), "6")
        print("🔵 INGRESO CANTIDAD MAX CUOTAS")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='plazoDesde']"), "1")
        print("🔵 INGRESO PLAZO DESDE")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='plazoHasta']"), "6")
        print("🔵 INGRESO PLAZO HASTA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='tna']"), "5")
        print("🔵 INGRESO TNA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='gastoFijo']"), "0")
        print("🔵 INGRESO GASTO FIJO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='gastoFijoDistribuido']//div[contains(@class, 'ng-select-container')]"))
        seleccionar_opcion_ng_select_js(driver, "No")
        print("🔵 SELECCION DISTRIBUIDO")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='gastoVariable']"), "0")
        print("🔵 INGRESO GASTO VARIABLE")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='gastoVariableDistribuido']//div[contains(@class, 'ng-select-container')]"))
        seleccionar_opcion_ng_select_js(driver, "No")
        print("🔵 SELECCION DISTRIBUIDO")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='entidadCobro']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activos Provinciales Santa Fe")
        print("🔵 SELECCION ENTIDAD")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='estado']//input[@type='text']"))
        seleccionar_opcion_ng_select_js(driver, "Activa")
        print("🔵 SELECCION ESTADO")

        find_and_send_keys(driver, (By.XPATH, "//app-custom-date[@formcontrolname='fechaEstado']//input[@type='text']"), "14122027")
        print("🔵 INGRESO FECHA ESTADO")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        
        validar_mensaje_snackbar(driver, "Línea creada correctamente")

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