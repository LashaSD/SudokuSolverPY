from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep 
import math
import json

class SudokuSolver:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://sudoku.com/evil/")
        self.actions = ActionChains(self.driver)
        self.driver.maximize_window()
        self.driver.fullscreen_window()
        self.driver.refresh()
        self.mainElement = self.driver.find_element(By.XPATH, '//*[@id="game"]/canvas')
        self.getAnswers()
        sleep(150)
    
    def getCoordsAndClick(self, num):
        x = num > 0 and num % 9 == 0 and 9 or num % 9
        y = math.floor(num / 9) >= 9 and 9 or math.ceil(num / 9)
        x1 = -200 + ((x - 1) * 50)
        y1 = -200 + ((y - 1) * 50)
        self.actions.move_to_element_with_offset(self.mainElement, 0, 0)
        self.actions.move_by_offset(x1, y1).click().perform()
        self.actions.move_to_element_with_offset(self.mainElement, 0, 0)
    
    def inputValue(self, num):
        numpad = self.driver.find_elements(By.CLASS_NAME ,'numpad-item')
        for element in numpad:
            if element.get_attribute('data-value') == str(num):
                element.click()

    def getAnswers(self):
        n = 0
        tempBut = self.driver.find_element(By.XPATH, '//*[@id="game-controls"]/div[3]')
        tempBut.click()
        for i in [10,12]:
            self.getCoordsAndClick(i)
            self.inputValue(8)
        tempBut.click()
        self.inputSheet = self.driver.execute_script("return window.localStorage.userGrid")
        self.answerSheet = self.driver.execute_script("return window.localStorage.puzzleGrid")
        self.inputSheet = json.loads(self.inputSheet)
        self.answerSheet = json.loads(self.answerSheet)
        for i in self.inputSheet:
            if str(i).strip() == '0':
                answer = self.answerSheet[n]
                self.getCoordsAndClick(n+1)
                self.inputValue(answer)
            n += 1


SudokuSolver()