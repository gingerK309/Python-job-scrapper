import json,os
from bs4 import BeautifulSoup
from requests import get

region = ['대전','충북']
search = ['파이썬']


def jobkorea_find_region():
    json_data = {}
    current_path = os.getcwd()
    file_path  = current_path + '/job_scraper/extractor'
    with open(f'{file_path}/jobkorea_region_code.json','r',encoding='utf-8') as f:
        json_data = json.load(f)
        return json_data

def jobkorea_search_region(region):
    try:
        r_list = jobkorea_find_region()
        if isinstance(region, list):
            rs = []
            for r in region:
                rs.append(r_list[r])
            region = ''.join(r+',' for r in rs)
            return region
    except:
        pass

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
    pages = find_pages(search, region)
    region = jobkorea_search_region(region)
    base_url = f'https://www.jobkorea.co.kr/Search/?stext={search}&local={region}'
    jobs = []
    for page in range(1,pages+1):
        print(f'잡코리아 {page}페이지 추출중...')
        url = f'{base_url}&Page_No={page}'
        request = get(url, headers={'User-Agent':'Mozilla/5.0'})
        if request.status_code != 200:
            print("페이지가 응답하지 않음")
        else:
            soup = BeautifulSoup(request.text, "html.parser")
            job_lists =  soup.find('div','list-default').find_all('li')
            for job_list in job_lists:
                title = job_list.find('a','title').string.strip()
                corp_name = job_list.find('a','name').string.strip()
                link =  'https://www.jobkorea.co.kr'+job_list.find('a','title')['href']
                location = job_list.find('span','loc long').string
                date = job_list.find('span','date').string.strip()
                job_conditons = job_list.find('p','option').find_all('span')[0:3]
                conditions = []
                for condition in job_conditons:
                    conditions.append(condition.string)
                stacks = job_list.find('p','etc').string.strip()
                job_dict = {
                                '공고': title,
                                '회사명': corp_name,
                                '공고 링크':link,
                                '위치': location,
                                '모집 기한': date,
                                '자격 조건': conditions,
                                '기술 스택': stacks
                            }
                jobs.append(job_dict)
            print('완료')
    return jobs

