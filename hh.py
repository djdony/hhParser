import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
search = input('Please enter search: ')
base_url = 'https://hh.ru/search/vacancy?search_period=3&clusters=true&area=1&text='+search

def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url,headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all( 'a', attrs= {'data-qa': 'pager-page'} )
            total_pages = int(pagination[-1].text)
            for i in range(total_pages):
                url = base_url+f'&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div',attrs=
            {'data-qa': ['vacancy-serp__vacancy', 'vacancy-serp__vacancy vacancy-serp__vacancy_premium']})
            for div in divs:
                try:

                    title = div.find('a',attrs = {'data-qa':'vacancy-serp__vacancy-title'}).text
                    href = div.find('a',attrs = {'data-qa':'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a',attrs = {'data-qa':'vacancy-serp__vacancy-employer'}).text
                    responsibility = div.find('div',attrs = {'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
                    requirement = div.find('div',attrs = {'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'responsibility': responsibility,
                        'requirement': requirement,
                    })
                except:
                    pass
    else:
        print('Status Code =' + str(request.status_code))
    return jobs

def write_file(jobs):
    with open(search+'.csv','a') as file:
        a_pen = csv.writer(file)
        a_pen.writerow((
            'Название',
            'Компания',
            'Должность',
            'Обязаности'
            'Ссылка'
        ))
        for job in jobs:
            a_pen.writerow((
                job['title'],
                job['company'],
                job['responsibility'],
                job['requirement'],
                job['href']
            ))
jobs = hh_parse(base_url, headers)
print('Found total' + str(len(jobs)) + 'jobs')
write_file(jobs)



#
# r = requests.get('https://www.tez-tour.com/catalog/turkey/antalya.html')
# html1 = BS(r.content, 'html.parser')
# file = open('other.html','w')
# html=html1.find(id="hotel-list-place")
# for tr in html.find_all('tr'):
#     print(tr)
#
#
# #for el in html.select('hotel-list-place'):
# #    title = el.select('.hotel-list')
# #    print(title)
#
# file.write(str(html1))
# file.close()