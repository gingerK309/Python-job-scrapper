import os, csv 

def save_to_csv(file_name, jobs):
    current_path = os.getcwd()
    file_path = current_path + '/csv_files/'
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    file = open(f'{file_path}{file_name}.csv', 'w', encoding='utf-8-sig')
    writer = csv.writer(file)
    writer.writerow(['공고', '회사명', '공고 링크', '위치', '모집 기한', '자격 조건','기술 스택'])
    for job in jobs:
        writer.writerow((list(job.values())))
    file.close()
    print('csv 파일 생성 완료.')

    
