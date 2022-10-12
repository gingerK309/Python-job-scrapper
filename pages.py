from flask import Blueprint, render_template, request, redirect, send_file
from extractor.saramin import saramin_extract_jobs
from extractor.jobkorea import jobkorea_extract_jobs
from save_csv import save_to_csv
import os

bp = Blueprint('main',__name__,url_prefix='/') 


exp_jobs = {}

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/search')
def search():
    region = request.args.get('region')
    reg = region.replace(' ','').split(',')
    keyword = request.args.get('keyword')
    key = keyword.replace(' ','').split(',')
    if region is None or region=='' or len(reg)>5:
        return redirect('/')
    if keyword is None or keyword=='':
        return redirect('/')
    jobkorea = jobkorea_extract_jobs(key,reg)
    saramin = saramin_extract_jobs(key,reg)
    jobs = jobkorea + saramin 
    print(len(jobkorea))
    print(len(saramin))
    nums = len(jobs)
    exp_jobs[keyword] = jobs
    return render_template('search.html',region=region, keyword=keyword, jobs=jobs, nums = nums)
   
@bp.route('/export')
def export():
    current_path = os.getcwd()
    keyword = request.args.get('keyword').replace(' ','')
    region = request.args.get('region').replace(' ','')
    file_path = current_path + '/csv_files/'
    if keyword not in exp_jobs:
        return redirect(f'/search?region={region}&keyword={keyword}')
    save_to_csv(f"{keyword}_{region}",exp_jobs[keyword])
    if keyword.find(','):
        key = keyword.replace(',','-')
    if region.find(','):
        reg = region.replace(',','-')
    return send_file(f"{file_path}{keyword}_{region}.csv", as_attachment=True, download_name=f'{key}_{reg}.csv')