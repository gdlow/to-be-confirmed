import numpy as np
import pandas as pd
from docx import Document

#Step 1: Parse train diagram word document
document = Document('WC May LTP all 221.docx')
docText = b'\n\n'.join([
    paragraph.text.encode('utf-8') for paragraph in document.paragraphs
])
docText = docText.decode('utf-8')
docText.replace("\t"," ")
docText = docText.split('\n\n')

#Step 2: Create virgin_wc list
virgin_wc = []
for i in range(len(docText)):
    if docText[i].startswith('\tDiagram'):
        print(docText[i])
        virgin_wc.append(docText[i])
    elif docText[i] == '\t':
        if docText[i+2].startswith('\tHolyhead') == False:
            print(docText[i+1])
            virgin_wc.append(docText[i+1])
        else:
            print(docText[i+2])
            virgin_wc.append(docText[i+2])
    elif docText[i] == '\t\t\t\t\t\t\t':
        if docText[i-1] != '\t\t\t\t\tFUEL\t\t':
            print(docText[i-2])
            virgin_wc.append(docText[i-2])
            print(docText[i-1])
            virgin_wc.append(docText[i-1])
        else:
            print(docText[i-4])
            virgin_wc.append(docText[i-4])
            print(docText[i-3])
            virgin_wc.append(docText[i-3])

#Step 3: Create virgin_wc dict
virgin_wc_dict = {'Diagram': [], 'Departure': [], 'Arrival': [], 'ArrivalHC':[]}
for i in range(len(virgin_wc)):
    if virgin_wc[i].startswith('\tDiagram :'):
        virgin_wc_dict['Diagram'].append(virgin_wc[i])
        virgin_wc_dict['Departure'].append(virgin_wc[i+1])
        try:
            virgin_wc_dict['ArrivalHC'].append(virgin_wc[i+2])
            virgin_wc_dict['Arrival'].append(virgin_wc[i+3])
        except:
            virgin_wc_dict['ArrivalHC'].append('Na')
            virgin_wc_dict['Arrival'].append('Na')
    else:
        pass

#Step 4: Create pd.DataFrame
new_virgin_wc_dict = {'diagramCode':[],'fromDate':[],'tillDate':[],'day':[],'depLocation':[],'depHC':[],'depTime':[],'arrLocation':[],'arrTime':[],'arrHC':[]}
for i in range(76): #take only representative samples
    new_virgin_wc_dict['diagramCode'].append(virgin_wc_dict['Diagram'][i].split('\t')[2] + ' '+ virgin_wc_dict['Diagram'][i].split('\t')[3])
    new_virgin_wc_dict['fromDate'].append(virgin_wc_dict['Diagram'][i].split('\t')[5])
    new_virgin_wc_dict['tillDate'].append(virgin_wc_dict['Diagram'][i].split('\t')[6])
    new_virgin_wc_dict['day'].append(virgin_wc_dict['Diagram'][i].split('\t')[4])
    new_virgin_wc_dict['depLocation'].append(virgin_wc_dict['Departure'][i].split('\t')[1])
    new_virgin_wc_dict['depHC'].append(virgin_wc_dict['Departure'][i].split('\t')[4])
    new_virgin_wc_dict['depTime'].append(virgin_wc_dict['Departure'][i].split('\t')[3])
    new_virgin_wc_dict['arrLocation'].append(virgin_wc_dict['Arrival'][i].split('\t')[1])
    new_virgin_wc_dict['arrTime'].append(virgin_wc_dict['Arrival'][i].split('\t')[2])
    new_virgin_wc_dict['arrHC'].append(virgin_wc_dict['ArrivalHC'][i].split('\t')[4])

new_virgin_wc_df = pd.DataFrame(new_virgin_wc_dict)
new_virgin_wc_df['tillDate'] = pd.to_datetime(new_virgin_wc_df['tillDate'],dayfirst=True)
new_virgin_wc_df['fromDate'] = pd.to_datetime(new_virgin_wc_df['fromDate'])
december_only = new_virgin_wc_df[new_virgin_wc_df['tillDate'] > '2017-12-01']

#Step 4.1 : Instantiate Weekday thang
december_only['Sun'] = december_only['day']
december_only['Mon'] = december_only['day']
december_only['Tue'] = december_only['day']
december_only['Wed'] = december_only['day']
december_only['Thurs'] = december_only['day']
december_only['Fri'] = december_only['day']
december_only['Sat'] = december_only['day']
december_only['Sun'] = december_only['Sun'].replace('Su',1)
december_only['Sun'] = december_only['Sun'].replace([ 'MTWO', 'ThFO', 'SO', 'FO', 'MTO', 'WO', 'ThO', 'SX', 'FSX', 'MO', 'TWThO', 'TWO'],0)
december_only['Mon'] = december_only['Mon'].replace(['Su', 'ThFO', 'SO', 'FO', 'WO', 'ThO','TWThO', 'TWO'],0)
december_only['Mon'] = december_only['Mon'].replace([ 'MTWO', 'MTO', 'SX', 'FSX','MO'],1)
december_only['Tue'] = december_only['Tue'].replace(['Su', 'ThFO', 'SO', 'FO', 'WO', 'ThO', 'MO'],0)
december_only['Tue'] = december_only['Tue'].replace([ 'MTWO', 'MTO', 'SX', 'FSX', 'TWThO', 'TWO'],1)
december_only['Wed'] = december_only['Wed'].replace([ 'Su','ThFO', 'SO', 'FO', 'MTO', 'ThO', 'MO'],0)
december_only['Wed'] = december_only['Wed'].replace([ 'MTWO','WO', 'SX', 'FSX', 'TWThO', 'TWO'],1)
december_only['Thurs'] = december_only['Thurs'].replace(['Su', 'MTWO', 'SO', 'FO', 'MTO', 'WO', 'MO', 'TWO'],0)
december_only['Thurs'] = december_only['Thurs'].replace(['ThFO', 'ThO', 'TWThO', 'SX', 'FSX'],1)
december_only['Fri'] = december_only['Fri'].replace(['Su', 'MTWO', 'SO', 'MTO', 'WO', 'ThO', 'MO', 'TWThO', 'TWO'],0)
december_only['Fri'] = december_only['Fri'].replace(['ThFO', 'FO', 'SX'],1)
december_only['Sat'] = december_only['Sat'].replace(['SO'],1)
december_only['Sat'] = december_only['Sat'].replace(['Su', 'MTWO', 'ThFO', 'FO', 'MTO', 'WO', 'ThO', 'SX', 'FSX', 'MO', 'TWThO', 'TWO'],0)


def dayoftheweek(dayinput):
	num2strdays = {0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thurs',5:'Fri',6:'Sat'}
	return december_only[december_only[num2strdays[dayinput]] == 1][['depLocation','arrLocation']]

def matrixgeneration(dayoftheweek):
    m1 = dayoftheweek['depLocation'].tolist()
    m2 = dayoftheweek['arrLocation'].tolist()
    #iterate down list
    for index, item in enumerate(m1):
        if item == 'BrtnUNCmd':
            m1[index] = 0
        elif item == 'Crewe CS':
            m1[index] = 1
        elif item == 'Holyhead':
            m1[index] = 2
        elif item == 'PoldieCMD':
            m1[index] = 3
    for index, item in enumerate(m2):
        if item == 'BrtnUNCmd':
            m2[index] = 0
        elif item == 'Crewe CS':
            m2[index] = 1
        elif item == 'Holyhead':
            m2[index] = 2
        elif item == 'PoldieCMD':
            m2[index] = 3
    return m1, m2

#test data
for i in range(1,3):
	depmatrix,arrmatrix = matrixgeneration(dayoftheweek(i))
	#print(dayoftheweek(i))
	print(depmatrix)
	print(arrmatrix)


