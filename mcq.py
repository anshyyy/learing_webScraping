import pprint

from bs4 import BeautifulSoup
import requests
import re
import gspread

def fetch(index):
    url = requests.get(f'https://www.gktoday.in/quizbase/current-affairs-quiz-november-2022?pageno={index}')
    soup = BeautifulSoup(url.content, features='lxml')
    mcqs = soup.find_all('div', class_="sques_quiz")
    store = {}
    for mcq in mcqs:
        question = mcq.text
        q_text = question.split('Notes')[0].split('?')[0]
        options = question.split('Notes')[0].split('?')[1]
        answer = question.split('Notes')[0].split('?')[1].split('AnswerCorrect')[1].split(':')[1].split('[')[1].replace(
            ']', '')
        options = question.split('Notes')[0].split('?')[1].split('AnswerCorrect')[0].replace('Show', '').lstrip()
        pat = re.compile(r"] (.*?)(?:\[|$)")
        options = pat.findall(options)
        q = q_text.split(' ', 1)
        question_text = q[1]
        num = q[0].replace('.', '')
        mp = {
            'Text': question_text + '?',
            'Options': options,
            'Answer': answer
        }
        store['question_' + num] = mp
    return store


def wrtieToSheets(store):
    gc = gspread.service_account('creds.json')
    sh = gc.open('quizSpreadsheet').sheet1
    for i,val in enumerate(store):
        sh.append_row([str(i),store[val]['Text'],store[val]['Options'][0],store[val]['Options'][1],store[val]['Options'][2],store[val]['Options'][3],store[val]['Answer']])
    return


def getAllMcqOfaNovemberMonth():
    i = 1
    while(True):
        dataStore = fetch(i)
        if len(dataStore)==0:
            break
        i+=1
        wrtieToSheets(dataStore)


getAllMcqOfaNovemberMonth()



