# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:44:13 2021

@author: kaushik
"""


#%%
import numpy as np
import io
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import datetime
import glob2
import pandas as pd
import time
import matplotlib.pyplot as plt
from numba import jit

fatality_data = pd.DataFrame()


def get_cases_deaths(filename):
    
    global fatality_data
    
    print(filename)
    start_time = time.time()
    try:
        with open(filename, "rb") as fp:
                rsrcmgr = PDFResourceManager()
                outfp = io.StringIO()
                laparams = LAParams(char_margin=20)
                device = TextConverter(rsrcmgr, outfp, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.get_pages(fp):
                    interpreter.process_page(page)
        text = outfp.getvalue().lower()    
    except:
        return ([datetime.date(2019,1,1),0,0,0,0,0,0,0,0,0])
    text = ' '.join(text.split())
    text = text.replace("positive result","positivity")  
    text = text.replace("date of result","positivity")  
    text = text.replace("-years"," years")  
    text = text.replace("year"," year")  
    text = text.replace("years male"," years old male")  
    text = text.replace("years female"," years old female")  
    text = text.replace("oldmale","old male")  
    text = text.replace("oldfemale","old female")  
    text = text.replace("femal","female")  
    text = text.replace("femlae","female")  
    text = text.replace("femle","female")  
    text = text.replace("femal","female")  
    text = text.replace("femaleee","female")  
    
    text = text.replace("("," (")  
    text = text.replace("died at home","died")    
    
    text = text.replace(","," ")  
    text = text.replace("..",".")  
    text = text.replace("- ","-")  
    text = text.replace("edia bulletin"," media_bulletin")
    text = ' '.join(text.split('24*7 control room: 044-29510400  044-29510500  9444340496  8754448477 district control room – 1077. toll free number – 1800 1205 55550 www.stopcorona.tn.gov.in'))
    
    words = str(text).split()

 #   ages_all = np.array([int(''.join(filter(str.isdigit,words[i-1]))) for i, x in enumerate(words) if( x == "years" or x == "yeaars")])
 #   deaths_elderly = np.sum(ages_all>=60)
    try:
        tmp_str = text.split('60+')[0][-200:].split(" 0 ")[1]
    except:
        tmp_str = text.split('60+')[0][-200:]
    cum_cases = [int(i) for i in tmp_str.split() if (i.isdigit() and int(i)>75)]
    if len(cum_cases)==0:
        tmp_str = text.split('60+')[0][-200:]
        cum_cases = [int(i) for i in tmp_str.split() if (i.isdigit() and int(i)>75) and int(i)%1000 !=0]
    if len(cum_cases)==5:
        tmp_str = text.split('60+')[0][-500:].split("distribution")[1]
        cum_cases = [int(i) for i in tmp_str.split() if (i.isdigit() and int(i)>75) and int(i)%1000 !=0]
        
    if len(cum_cases)==6:
        tmp_str = text.split('60+')[1][0:50].split("24*7")[0]
        cases1 = [int(i) for i in tmp_str.split() if (i.isdigit() and int(i)>75)]
        if len(cases1)==3:
            cum_cases.insert(6,cases1[0])
            cum_cases.insert(7,cases1[1])
            cum_cases.insert(8,cases1[2])
        else:
            tmp_str = text.split('60+')[0][-500:].split("distribution")[1]
            cum_cases = [int(i) for i in tmp_str.split() if (i.isdigit() and int(i)>75) and int(i)%1000 !=0]
                
    if cum_cases[3]<cum_cases[6]:
        cum_cases[3],cum_cases[6]=cum_cases[6],cum_cases[3]
        cum_cases[4],cum_cases[7]=cum_cases[7],cum_cases[4]
        cum_cases[5],cum_cases[8]=cum_cases[8],cum_cases[5]

    cases_all = text.split("death case")[1:]
    dt = datetime.datetime.strptime(words[words.index('media_bulletin')+1],'%d.%m.%Y').date()    
    
    for case_hist in cases_all:
        words = case_hist.split()
        if len(words)>2:
            case_num = ''.join(filter(str.isdigit,words[0]+words[1 ]))
            try:
                #date_of_death = [words[i+2] for i, x in enumerate(words) if x == "died"]
                date_of_death =[case_hist.split("died")[1].split("on")[1].split()[0]]
            except:
                date_of_death=['-']
            try:
                date_of_positive = [words[i+2] for i, x in enumerate(words) if x == "positivity"]
            except:
                date_of_positive=['-']
            
            try:
                age_fatality = [words[i-1] for i, x in enumerate(words) if x in ["years","yeaars","year"]]
            except:
                age_fatality = ['-'] 
            try:    
                sex = [words[i+2] for i, x in enumerate(words) if x in ["years","yeaars","year"]]
                if sex[0]=="from":
                    sex = [words[i+1] for i, x in enumerate(words) if x in ["years","yeaars","year"]]
                if sex[0]=="old":
                    sex = [words[i+3] for i, x in enumerate(words) if x in ["years","yeaars","year"]]
                
            except:
                sex= ['-']

            if len(age_fatality)==0:
                age_fatality=['-']
                
                
            if "a" in age_fatality[0]:
                age_fatality[0]=age_fatality[0].strip("a")
            if len(date_of_death)==0:
                date_of_death=['-']
            if len(date_of_positive)==0:
                date_of_positive=['-']
            if date_of_death[0].count('-')==2:
                date_of_death[0]=date_of_death[0].replace("-",".")
            if "at" in date_of_death[0]:
                date_of_death[0] = date_of_death[0].strip("at")
            if date_of_positive[0].count('-')==2:
                date_of_positive[0]=date_of_positive[0].replace("-",".")
                
            if date_of_positive[0].count('.')>=3:
                date_of_positive[0]='.'.join(date_of_positive[0].split('.')[0:3])
            if '\\' in date_of_positive:
                date_of_positive[0] = date_of_positive[0].split('\\')[0]
            if len(age_fatality)==0:
                try:
                    age_fatality = case_hist.split("year")[0][-2:]
                    sex = [words[i+1] for i, x in enumerate(words) if x in ["old"]]
                    
                except:
                    age_fatality = ['-']    
                    sex= ['-']
            if len(sex)==0:
                sex= ['-']
                
            fatality_list = pd.DataFrame(
                {'Case_number':case_num,
                 'Date_detection': date_of_positive[0],
                 'Date_death': date_of_death[0],
                 'Age': age_fatality[0],
                 'Sex': sex[0]
                },index=[0])
            
            fatality_data=pd.concat([fatality_data,fatality_list],axis=0)
            fatality_data.reset_index(drop=True, inplace=True)
    cum_cases.insert(0,dt)    
    print(f'Elapsed time: {time.time()-start_time} seconds')
    return (cum_cases)
rows = []

# for filename in glob2.glob("./Media*.pdf"):
#     (dt,deaths_elderly,cum_cases_elderly) = get_cases_deaths(filename)
#     rows.append((dt,deaths_elderly,cum_cases_elderly))
# filename = './TN_archive/Media-Bulletin-05-05-21-COVID-19-6-PM.pdf'
# (dt,deaths_elderly,cum_cases_elderly) = get_cases_deaths(filename)  
# filename = './TN_archive/Media-Bulletin-06-05-21-COVID-19-6-PM.pdf'

files = ['./TN_archive/Media-Bulletin-29-05-21-cleaned.pdf','./TN_archive/Media-Bulletin-01.06.2020.pdf',
         './TN_archive/Media-Bulletin-20-05-20-COVID-19-6-PM.pdf']
#out = get_cases_deaths(files[0])  

data = pd.DataFrame([get_cases_deaths(filename) for filename in glob2.glob("./TN_archive/Media*.pdf")])    
#data = pd.DataFrame([get_cases_deaths(filename) for filename in files])    

data.index = data[0]

data.columns = ['Date','13-60T','13-60F','13-60M','60+T','60+F','60+M','13T','13F','13M']
data.to_csv('TN_Cases_data.csv')
#fatality_data['Date_death'] = pd.to_datetime(fatality_data.Date_death, format='%d.%m.%Y',exact=False,errors='coerce')
#fatality_data['Date_detection'] = pd.to_datetime(fatality_data.Date_detection, format='%d.%m.%Y',exact=False,errors='coerce')

#%%
fatality_data.index=fatality_data['Case_number']
fatality_data.index = pd.to_numeric(fatality_data.index,errors="coerce")
fatality_data.sort_index(inplace=True)

f1 = fatality_data[fatality_data.Age.apply(lambda x: x.isnumeric())]
f2 = f1[~f1['Date_death'].str.contains("[a-z-]").fillna(False)]
f2 = f2[pd.to_numeric(f2.Case_number,errors="coerce")<50000]
f2 = f2[f2.Sex.str.contains("male").fillna(False)]
f3 = pd.concat([fatality_data,f2]).drop_duplicates(keep=False)
f2.to_csv('TN_fatality_data.csv')

#%%

print(f2.shape[0]/(np.max(f2.index)-70))