from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
import gspread

months = [('january', 1), ('february', 2), ('march', 3), ('april', 4), ('may', 5), ('june', 6), ('july', 7),
          ('august', 8), ('september', 9), ('october', 10), ('november', 11),
          ('december', 12)]


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


def wrtieToSheets(month):
    curr_month = datetime.datetime.now()
    curr_month = curr_month.strftime('%m')
    if month[1] > int(curr_month):
        return

    month = month[0]
    gc = gspread.service_account('creds.json')
    sh = gc.open('quizSpreadsheet')
    worksheet = sh.add_worksheet(title=month, rows=200, cols=6)

    worksheet.format('A1:G1', {'textFormat': {'bold': True}})
    worksheet.append_row(['Serial No.', "Question", "A", "B", "C", "D", "Answer"])
    page_id = 1
    s_id = 1
    while True:
        store = fetch(page_id, month)
        if len(store) == 0:
            break
        for i, val in enumerate(store):
            try:
                worksheet.append_row([str(s_id), store[val]['Text'], store[val]['Options'][0], store[val]['Options'][1],
                                      store[val]['Options'][2], store[val]['Options'][3], store[val]['Answer']])
            except:
                pass
            s_id += 1
        page_id += 1

    return


def getAllMcqOfaAllMonth():
    for month in months:
        wrtieToSheets(month)
        time.sleep(60)


getAllMcqOfaAllMonth()
