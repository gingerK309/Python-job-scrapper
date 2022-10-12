import json,os
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import quote

def jobkorea_find_region():
    json_data = {}
    current_path = os.getcwd()
    file_path  = current_path + '/extractor'
    with open(f'{file_path}/jobkorea_region_code.json','r',encoding='utf-8') as f:
        json_data = json.load(f)
        return json_data

def jobkorea_search_region(region):
    r_list = jobkorea_find_region()
    if isinstance(region, list):
        rs = []
        for r in region:
            rs.append(r_list[r])
        region = ''.join(r+',' for r in rs)
        return region

def find_pages(search,region):
    region = jobkorea_search_region(region)
    base_url = f'https://www.jobkorea.co.kr/Search/?stext={search}&local={region}'
    request = get(base_url, headers={'User-Agent':'Mozilla/5.0'})
    if request.status_code != 200:
        print("페이지가 응답하지 않음")
    else:
        soup = BeautifulSoup(request.text, "html.parser")
        count = int(soup.find('strong','dev_tot').string)
        pages = count//20 + 1
    return pages
    

def jobkorea_extract_jobs(search,region):
    search = quote(''.join(s+',' for s in search))
    pages = find_pages(search, region)
    region = jobkorea_search_region(region)
    base_url = f'https://www.jobkorea.co.kr/Search/?stext={search}&local={region}'
    jobs = []
    temps = []
    labels = ['title','corp','link','location','dead_line','conditions','tech_stacks']
    for page in range(1,pages+1):
        print(f'잡코리아 {page}페이지 추출중...')
        url = f'{base_url}&Page_No={page}'
        request = get(url, headers={'User-Agent':'Mozilla/5.0'})
        if request.status_code != 200:
            print("페이지가 응답하지 않음")
        else:
            try:
                soup = BeautifulSoup(request.text, "html.parser")
                job_lists =  soup.find('div','list-default').find_all('li','list-post')
                for job_list in job_lists:
                    if job_list.find('a') != -1 and job_list:
                        title = job_list.find('a','title').string.strip()
                        corp_data = job_list.find('a','name').string.strip()
                        link =  'https://www.jobkorea.co.kr'+job_list.find('a','title')['href']
                        detail_location = job_list.find('span','loc long').string
                        date = job_list.find('span','date').string.strip()
                        job_conditons = job_list.find('p','option').find_all('span')[0:3]
                        conditions = []
                        for condition in job_conditons:
                            conditions.append(condition.string)
                        stacks = job_list.find('p','etc').string.strip()
                        if title and corp_data and link and detail_location and date and conditions and stacks:
                            temps = [title, corp_data,link,detail_location,date,conditions,stacks]
                        while None in temps:
                            temps.clear()
                        if temps:
                            job_dict = dict(zip(labels, temps))
                            jobs.append(job_dict)
                print('완료')
            except AttributeError:
                return jobs
    return jobs
