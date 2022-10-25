from requests import get
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from urllib.parse import quote

def saramin_find_region():
    code_dict = {}
    url = 'https://oapi.saramin.co.kr/guide/code-table2'
    if get(url).status_code ==200:
        code_table = BeautifulSoup(get(url).text,'html.parser')
        code = code_table.find('div',id='midCodelist').find_all('td')
        regions = []
        regions_code = []
        for idx, td in enumerate(code):
            if idx%2 == 1:
                regions.append(td.string)
            else:
                regions_code.append(td.string)
        code_dict = dict(zip(regions, regions_code))
    else:
        print('사이트 접근 거부')
    return code_dict

def saramin_search_region(region):
    try:
        r_list = saramin_find_region()
        if isinstance(region, list):
            rs = []
            for r in region:
                rs.append(r_list[r])
            region = ''.join(r+',' for r in rs)
            return region
    except:
        pass

def find_pages(search, region):
    region = saramin_search_region(region)
    base_url = f'https://www.saramin.co.kr/zf_user/search?'
    url = f'{base_url}&searchword={search}&loc_mcd={region}&recruitPageCount=100'
    header={'User-Agent':'Mozilla/5.0'}
    req = Request(url, headers = header, method ='POST')
    with urlopen(req) as res:
        if res.status != 200:
            print(res)
        else:
            try:
                page_cnt = 0
                html = res.read().decode()
                soup = BeautifulSoup(html,'html.parser')
                count = soup.find('span','cnt_result').string.replace('총','').replace('건','').replace(',','').replace(' ','')
                page_cnt = int(count)//100
                if page_cnt == 0:
                    page_cnt +=1
                return page_cnt
            except:
                pass
        
def saramin_extract_jobs(search, region):
    search = quote(''.join(s+',' for s in search))
    jobs = []
    pages =find_pages(search, region)
    region = saramin_search_region(region)
    base_url = f'https://www.saramin.co.kr/zf_user/search?'
    for page in range(1,pages+2):
        print(f'사람인 {page}페이지 추출중...')
        url = f'{base_url}&searchword={search}&loc_mcd={region}&recruitPageCount=100&recruitPage={page}'
        header={'User-Agent':'Mozilla/5.0'}
        req = Request(url, headers = header, method ='POST')
        with urlopen(req) as res:
            if res.status != 200:
                print(res)
            else:
                    html = res.read().decode()
                    soup = BeautifulSoup(html,'html.parser')
                    job_lists = soup.find_all('div','item_recruit')
                    for job_list in job_lists:
                        if job_lists is None:
                            break
                        else:
                            corp_data = job_list.find('a','track_event data_layer').string.strip()
                            job_list = job_list.find('div','area_job')
                            title = job_list.find('span').string
                            link = 'https://www.saramin.co.kr'+job_list.find('a')['href'].replace('/relay','')
                            date = job_list.find('span','date').string
                            conditions = job_list.find_all('div','job_condition')
                            job_conditions = []
                            for c in conditions:
                                detail_location = ''
                                career = c.find('span').find_next('span').string
                                education = career.find_next('span').string
                                contract = education.find_next('span').string
                                job_conditions.append(career)
                                job_conditions.append(education)
                                job_conditions.append(contract)
                                for loc in location:
                                    detail_location += loc.string +' '
                            sectors = job_list.find_all('div','job_sector')
                            sector = ''
                            for s in sectors:
                                sector = s.get_text().split('외')[0].lstrip('\n').split(',')
                            job_dict = {
                                'title': title,
                                'corp': corp_data,
                                'link':link,
                                'location': detail_location,
                                'dead_line': date,
                                'conditions': job_conditions,
                                'tech_stacks': sector
                            }
                            jobs.append(job_dict)
        print('완료')
    return jobs

