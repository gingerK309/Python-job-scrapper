from requests import get
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import traceback

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

def saramin_search_region(region=None):
    try:
        r_list = saramin_find_region()
        if isinstance(region, list):
            if region is not (None or ''):
                rs = []
                for r in region:
                    rs.append(r_list[r])
                region = ''.join(r+',' for r in rs)
            return region
    except:
        pass

def find_pages(search, region):
    region = saramin_search_region(region)
    base_url = f'https://www.saramin.co.kr/zf_user/search?&searchword={search}'
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
                nums = soup.find_all('div','header')[0]
                count = nums.find('span').string.replace('총','').replace('건','').replace(',','').replace(' ','')
                page_cnt = int(count)//100
                if page_cnt == 0:
                    page_cnt +=1
                return page_cnt
            except:
                pass
        
def saramin_extract_jobs(search, region):
    pages = find_pages(search, region)
    region = saramin_search_region(region)
    base_url = f'https://www.saramin.co.kr/zf_user/search?&searchword={search}'
    jobs = []
    for page in range(1,pages+2):
        print(f'{page}페이지 추출중...')
        url = f'{base_url}&searchword={search}&loc_mcd={region}&recruitPageCount=100&recruitPage={page}'
        header={'User-Agent':'Mozilla/5.0'}
        req = Request(url, headers = header, method ='POST')
        with urlopen(req) as res:
            if res.status != 200:
                print(res)
            else:
                try:
                    html = res.read().decode()
                    soup = BeautifulSoup(html,'html.parser')
                    search_info = soup.find_all('div','header')[0]
                    search_info = search_info.find('h2').string + ' ' + search_info.find('span').string
                    job_lists = soup.find_all('div','item_recruit')
                    for job_list in job_lists:
                        corp_data = job_list.find('a','track_event data_layer').string.replace('                            ','').replace('\n','').replace(
                        '                        ','')
                        job_list = job_list.find('div','area_job')
                        title = job_list.find('span').string
                        link = 'https://www.saramin.co.kr'+job_list.find('a')['href'].replace('/relay','')
                        date = job_list.find('span','date').string
                        conditions = job_list.find_all('div','job_condition')
                        job_conditions = []
                        for c in conditions:
                            career = c.find('span').find_next('span').string
                            education = career.find_next('span').string
                            job_conditions.append(career)
                            job_conditions.append(education)
                        sectors = job_list.find_all('div','job_sector')
                        sector = ''
                        for s in sectors:
                            sector = s.get_text().split('외')[0].lstrip('\n').split(',')
                        job_dict = {
                            '공고': title,
                            '회사명': corp_data,
                            '공고 링크':link,
                            '모집 기한': date,
                            '자격 조건': job_conditions,
                            '기술 스택': sector
                        }
                        jobs.append(job_dict)
                    print('완료')   
                except Exception as e:
                    trace_back = traceback.format_exc()
                    message = str(e)+ "\n" + str(trace_back)
                    print('에러 발생:',message)
    return jobs

