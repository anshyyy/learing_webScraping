from bs4 import BeautifulSoup
import requests
import re
import os
import datetime
import csv

months = [('january', 1), ('february', 2), ('march', 3), ('april', 4), ('may', 5), ('june', 6), ('july', 7),
          ('august', 8), ('september', 9), ('october', 10), ('november', 11),
          ('december', 12)]
years = ['2017','2018','2019','2020','2021','2022']

def fetch(index, month, year):
    url = requests.get(f'https://www.gktoday.in/quizbase/current-affairs-quiz-{month}-{year}?pageno={index}')

    if url.status_code // 100 == 4:
        url = requests.get(f'https://www.gktoday.in/quizbase/current-affairs-quiz-questions-{month}-{year}?pageno={index}')
        if url.status_code //100 == 4:
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


def wrtieToSheets(month,year):
    today = datetime.datetime.now()
    curr_month = today.strftime('%m')
    curr_year = today.strftime('%Y')
    if month[1] > int(curr_month) and year == curr_year :
        return

    month = month[0]
    # gc = gspread.service_account('creds.json')
    # sh = gc.open('quizSpreadsheet')
    # worksheet = sh.add_worksheet(title=month, rows=200, cols=6)
    try :
        with open(f'F:/Current Affairs/{year}/{month}.csv', 'w') as file:
            worksheet = csv.writer(file)
    except FileNotFoundError:
        path_dir = "F:/Current Affairs/" + year
        os.mkdir(path_dir)
    finally:
        # worksheet.format('A1:G1', {'textFormat': {'bold': True}})
        with open(f'F:/Current Affairs/{year}/{month}.csv', 'w') as file:
            worksheet = csv.writer(file)
            worksheet.writerow(['Serial No.', "Question", "A", "B", "C", "D", "Answer"])
            page_id = 1
            s_id = 1
            while True:
                # print(month,year)
                store = fetch(page_id, month,year)
                # print(store)
                if len(store) == 0:
                    break
                for val in store:
                    try:
                        worksheet.writerow(
                            [str(s_id), store[val]['Text'], store[val]['Options'][0], store[val]['Options'][1],
                             store[val]['Options'][2], store[val]['Options'][3], store[val]['Answer']])
                    except:
                        pass
                    s_id += 1
                page_id += 1

        return


def getAllMcqOfaAllMonth(year):
    for month in months:
        wrtieToSheets(month,year)
        # time.sleep(60)

def getAllYear():
    for y in years:
        getAllMcqOfaAllMonth(y)

getAllYear()

