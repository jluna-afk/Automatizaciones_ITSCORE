import unittest
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Pages.base_page import (
    find_and_send_keys,
    find_and_click,
    seleccionar_opcion_ng_select_js,
    validar_mensaje
)

class TestCrearRelacionParticipante(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://qa.itscore.its.com.ar:3080/#/login")
    
    def test_crear_relacion_participante(self):
        driver = self.driver

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

        find_and_click(driver,(By.XPATH, "//div[contains(@class, 'relation-card-btn') and .//h3[text()='Participante']]"))
        print("🔵 CLICK EN LA CARD PARTICIPANTE")
        
        find_and_click(driver, (By.XPATH, "//input[@formcontrolname='persona']/following-sibling::button"))
        print("🔵 CLICK EN LA LUPITA PERSONA")

        find_and_click(driver, (By.XPATH, "//span[normalize-space()='A2WEG TECNOLOGIA FINANCIERA S.R.L,']"))
        print("🔵 CLICK EN LA PERSONA")
        time.sleep(1)

        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, "ng-dropdown-panel")))

        find_and_click(driver, (By.XPATH, "//mat-dialog-container//ng-select[@formcontrolname='tipo']//div[contains(@class, 'ng-select-container')]"))
        seleccionar_opcion_ng_select_js(driver, "Propiedad y Capital")
        print("🔵 SELECCION TIPO DE PARTICIPACION")

        find_and_click(driver, (By.XPATH, "//ng-select[@formcontrolname='subTipo']//div[contains(@class, 'ng-select-container')]"))
        seleccionar_opcion_ng_select_js(driver, "Titulares")
        print("🔵 SELECCION DE PARTICIPACION")

        find_and_click(driver, (By.XPATH, "//div[@class='form-actions mb-3']//button[@type='button'][normalize-space()='Guardar']"))

        validar_mensaje(driver, "Participantes modificados con éxito")
            
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