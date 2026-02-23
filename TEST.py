import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Funciones.Funciones import Funciones

def validar_mensaje(driver, mensaje_exito, wait_time=10):
    try:
        locator = (By.XPATH, f"//*[contains(text(), '{mensaje_exito}')]")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"✅ Validación exitosa: Se mostró el mensaje '{mensaje_exito}'.")
    except TimeoutException:
        print(f"❌ Falló la validación: No apareció el mensaje '{mensaje_exito}'.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado en la validación: {e}")

class base_test(unittest.TestCase):

    def setUp(self):
        self.chromedriver_path = r"C:\Users\Joaquin\Desktop\Drivers\chromedriver.exe"
        self.service = Service(executable_path=self.chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service)
        
    def test1(self):
        driver = self.driver
        f = Funciones(driver)
        f.Navegar("http://qa.itscore.its.com.ar:3080/#/login")
        f.Texto_Xpath("//input[@placeholder='Usuario']", "Joaquinluna")
        f.Texto_Xpath("//input[@placeholder='Clave']", "joaquin")
        f.Click_Xpath("//button[@type='submit']")
        f.Click_LinkText("Sistema")
        f.Click_LinkText("Parametría")
        f.Click_LinkText("Días hábiles y Feriados")
        f.Tiempo(1)
        f.Checkbox_Xpath("(//span[@class='checkmark'])[1]")
        f.Checkbox_Xpath("(//span[@class='checkmark'])[2]")
        f.Checkbox_Xpath("(//span[@class='checkmark'])[3]")
        f.Checkbox_Xpath("(//span[@class='checkmark'])[4]")
        f.Checkbox_Xpath("(//span[@class='checkmark'])[5]")
        f.Checkbox_Xpath("(//span[@class='checkmark'])[6]")
        f.Tiempo(1)
        for num in range(1,5,8):
            f.Checkbox_Xpath_Multiples("(//span[@class='checkmark'])["+str(num)+"]")
        
        

        f.Tiempo(5)
        
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
