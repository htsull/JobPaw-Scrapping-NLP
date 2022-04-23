from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}


def getLastPage():
    url = "https://www.jobpaw.com/pont/professionnels.php?id=55"
    r =  requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    lastPageButton = soup.find_all('tr')[-1].find_all('li')
    numberOfPages = int(str(lastPageButton[2]).split('&')[0].split('=')[2])
    return numberOfPages

allJobs = []

def getJobs(page):
    url = f'https://www.jobpaw.com/pont/professionnels.php?pageNum_RS_job={page}&id=55'
    # url = "https://www.jobpaw.com/pont/professionnels.php?id=55"
    r =  requests.get(url, headers=headers)
    # creating the soup
    soup = BeautifulSoup(r.text, 'html.parser')
    # grabbing the concerned table
    jobs = soup.find_all('tr')[8:-2]
    
    for item in jobs:
        listOfJobs = {
        'institution' : item.find('td').text.strip(),
        'link' : 'https://www.jobpaw.com/pont/professionnels.php' + item.find('a')['href'],
        'titre' : item.find_all('td')[1].text.strip(),
        'domaine' : item.find_all('td')[2].text.strip(),
        'dateLimite' : item.find_all('td')[3].text.strip()
    }
        allJobs.append(listOfJobs)
    return allJobs


lastPage = getLastPage()

for i in range(lastPage, lastPage + 1, 1):
    getJobs(i)

pd.DataFrame(allJobs).to_excel('jobpaw.xlsx', index=False)