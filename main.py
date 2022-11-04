import time
from bs4 import BeautifulSoup
import requests


def intersect_jobs(list1, list2):
    return len(list(set(list1) & set(list2))) == 0



print('Put some skill that you are not familiar with:')
unfamiliar_skills = [skills for skills in input('>>').split()]

print(f"Filtering out {unfamiliar_skills}")


def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from'
                             '=submit&txtKeywords=python&txtLocation=')
    soup = BeautifulSoup(html_text.content, features='lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    index = 1
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').text.replace(' ', '')
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_='srp-skills').text.replace(' ', '').split(',')
            more_info = job.header.h2.a['href']
            if intersect_jobs(skills, unfamiliar_skills):
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name : {company_name.strip()}\n")
                    f.write(f"skills : {' '.join(skills).strip()}\n")
                    f.write(f"More info : {more_info}\n")
                print(f'File saved: {index}')
                index += 1


if __name__ == '__main__':

    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes....')
        time.sleep(time_wait * 60)
