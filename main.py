from extractor.saramin import saramin_extract_jobs
from urllib.parse import quote

region = input('지역을 입력 해주세요:').split(',')
search = input('검색 키워드를 입력해 주세요:').split(',')
srch = quote(''.join(s+',' for s in search)) 

try:
    print(f'사람인에서 {search} 검색 결과를 추출합니다...')   
    saramin = saramin_extract_jobs(srch,region)
except KeyError:
    pass
 