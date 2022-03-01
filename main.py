import textract
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# try_this_path = 'tags = driver.find_element(By.XPATH,"//textarea[@aria-label='tags']
ADD_CARD_PATH = "#addRow > span > button"
TEST = "aria-label='+ Add Card'"
ANSWER_ENTRY_PATH = "DefinitionSide"
QUESTION_ENTRY_PATH = 'ProseMirror'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
LOG_IN_PATH = '//*[@id="page"]/div/div[4]/div/p[2]/a[2]'
USERNAME_PATH = '//*[@id="username"]'
PASSWORD_PATH = '//*[@id="password"]'
LOG_IN_BUTTON = '/html/body/div[9]/div/div/div[2]/section/div[2]/div/form/button'

# IGNORE
# for i in range (0, 136):
#     add_card.click()
#     time.sleep(1)
#
# add_card.click()
# add_card.click()
# add_card.click()
# IGNORE

"""
This is responsible for extracting questions and answers from test bank
"""

text = textract.process('/Users/ianveilleux/PycharmProjects/attempt/TG02.docx')
text = text.decode('utf8')

string_text = str(text)

text_list = string_text.split('Answer:')
text_bank = []
for index, sentence in enumerate(text_list):
    try:
        try:
            list_of_questions = text_list[index].split()
            list_to_str = ' '

            text = list_to_str.join(list_of_questions)
            question = text.split('Bloomcode:')[-1]
            true_question = list_of_questions.pop(0)
        except ValueError:
            continue
        list_to_str = ' '
        answer = text_list[index + 1].split()[0]
        text_bank.append((question, answer))
    except IndexError:
        continue

for i in text_bank:
    print(f'\n\n{i[0]}')
    print(f'\nanswer: {i[1]}')

'''
This is the beginning of selenium quizlet inputting
'''
s = Service('/Users/ianveilleux/development/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get(f"https://quizlet.com/675420025/edit")
log_in_button = driver.find_element(By.XPATH, LOG_IN_PATH)
log_in_button.click()
user_box = driver.find_element(By.XPATH, USERNAME_PATH)
pass_box = driver.find_element(By.XPATH, PASSWORD_PATH)
second_log_button = driver.find_element(By.XPATH, LOG_IN_BUTTON)

user_box.send_keys(USERNAME)
pass_box.send_keys(PASSWORD)
second_log_button.click()

time.sleep(5)
question_box = driver.find_elements(By.CLASS_NAME, QUESTION_ENTRY_PATH)

for i in range(0, 130):
    add_card = driver.find_elements(By.CSS_SELECTOR, ADD_CARD_PATH)
    time.sleep(0.50)
    for button in add_card:
        button.click()

question_box = driver.find_elements(By.CSS_SELECTOR, "[aria-labelledby='editor-term-side']")
answer_box = driver.find_elements(By.CSS_SELECTOR, "[aria-labelledby='editor-definition-side']")


for index, question in enumerate(question_box):
    try:
        question.send_keys(f'{text_bank[index][0]}')
    except IndexError:
        continue
for index, question in enumerate(answer_box):
    question.send_keys(f'{text_bank[index][1]}')

# for a in answer_box:
#     for question in text_bank:
#         a.send_keys(f'{question[1]}')
