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
    seleccionar_opcion_ng_select,
    copiar_y_pegar_importe_3,
    validar_mensaje_snackbar
)

class Test_Prestamos_Gestion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")

    def test_crear_prestamo(self):
        driver = self.driver

        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Usuario']"), "joaquinluna")
        find_and_send_keys(driver, (By.XPATH, "//input[@placeholder='Clave']"), "joaquin")
        print("🔵 INGRESO CREDENCIALES")
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Ingresar']"))
        print("🔵 INGRESO A LA PLATAFORMA")

        find_and_click(driver, (By.LINK_TEXT, "Préstamos"))
        find_and_click(driver, (By.LINK_TEXT, "Gestión"))
        print("🔵 INGRESO AL MODULO DE PRESTAMOS PARAMETRIA")

        find_and_click(driver, (By.XPATH, "//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA LINEA")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='PRESTAMO AMORTIZABLE']"))
        print("🔵 SELECCION PRESTAMO")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//input[@id='persona']/following-sibling::button"))
        print("🔵 CLICK EN LA LUPITA PERSONA")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='id_apellido_nombre']"), "coudsi")
        print("🔵 INGRESO NOMBRE")
        
        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Buscar']"))
        print("🔵 CLICK EN BUSCAR")
        
        find_and_click(driver, (By.XPATH, "//span[normalize-space()='COUDSI, SERGIO OMAR']"))
        print("🔵 SELECCION PERSONA")

        find_and_send_keys(driver, (By.XPATH, "//input[@formcontrolname='capital']"), "10000")
        print("🔵 INGRESO MONTO")

        find_and_send_keys(driver, (By.XPATH, "//input[@id='cuotas']"), "6")
        print("🔵 INGRESO CUOTAS")

        find_and_click(driver, (By.XPATH, "//div[@class='row mt-4']//i[@class='fas fa-search']"))
        print("🔵 CLICK EN LA LUPITA VENDEDOR")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='TELEPAGOS']"))
        print("🔵 SELECCION VENDEDOR")

        find_and_click(driver, (By.XPATH, "//input[@id='entidad']/following-sibling::button"))
        print("🔵 CLICK EN LA LUPITA ENTIDAD COBRO")

        find_and_click(driver, (By.XPATH, "//td[normalize-space()='Activos Provinciales Santa Fe']"))
        print("🔵 SELECCION ENTIDAD COBRO")
        time.sleep(0.5)

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Crear']"))
        print("🔵 CLICK EN CREAR")
        
        validar_mensaje_snackbar(driver, "Préstamo web creado correctamente.")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK EN APROBAR")

        validar_mensaje_snackbar(driver, "Préstamo aprobado correctamente.")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Desaprobar']"))
        print("🔵 CLICK EN DESAPROBAR")

        validar_mensaje_snackbar(driver, "Préstamo desaprobado correctamente.")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aprobar']"))
        print("🔵 CLICK EN APROBAR")

        validar_mensaje_snackbar(driver, "Préstamo aprobado correctamente.")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Liquidar']"))
        print("🔵 CLICK EN LIQUIDAR")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='formaPago']"))
        seleccionar_opcion_ng_select(driver, "Cuenta a la vista")
        print("🔵 SELECCION DE FORMA DE PAGO")

        find_and_click(driver, (By.XPATH, "//ng-select[@id='cuentaDestino']"))
        seleccionar_opcion_ng_select(driver, "PROV GASTOS VARIOS")
        print("🔵 SELECCION DE CUENTA DESTINO")

        copiar_y_pegar_importe_3(driver)
        print("🔵 INGRESO IMPORTE")

        find_and_click(driver, (By.XPATH, "//button[normalize-space()='Aceptar']"))
        print("🔵 CLICK EN ACEPTAR")

        validar_mensaje_snackbar(driver, "Préstamo liquidado correctamente")


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
            
            nombre_archivo = f"{nombre_test}.png"
            ruta_completa = os.path.join(carpeta_screenshots, nombre_archivo)
            
            self.driver.save_screenshot(ruta_completa)
            print(f"\n📸 ERROR DETECTADO: Captura de pantalla guardada en -> {ruta_completa}")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)