from bs4 import BeautifulSoup
import requests
import re
import gspread

months = [ 'february', 'march', 'april', 'may', 'june', 'august', 'september', 'october', 'november',
          'december']


def fetch(index, month):
    url = requests.get(f'https://www.gktoday.in/quizbase/current-affairs-quiz-{month}-2022?pageno={index}')
    if url.status_code // 100 == 4:
        return {}
    soup = BeautifulSoup(url.content, features='lxml')
    mcqs = soup.find_all('div', class_="sques_quiz")
    store = {}
    for mcq in mcqs:
        question = mcq.text
        q_text = question.split('Notes')[0].split('?')[0]
        try:
            options = question.split('Notes')[0].split('?')[1]
        except:
           continue

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


print(fetch(1,'june'))