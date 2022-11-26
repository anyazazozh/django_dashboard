import csv
import requests
import pandas as pd
import json


df = pd.read_csv('forecast.csv', encoding='utf-8', sep=',')
sellers = df['Контрагент'].unique()
brands = df['ТМ'].unique()
report_type = df['Тип'].unique()
print(df)


sellers_d = requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json()
sellers_dict = dict((elem['name'], elem['id']) for elem in sellers_d)

for elem in sellers:
    if elem not in sellers_dict.values():
        requests.post('http://127.0.0.1:8000/api/sellers/?format=json', data={'name': elem})


brands_d = requests.get('http://127.0.0.1:8000/api/brands/?format=json').json()
brands_dict = dict((elem['name'], elem['id']) for elem in brands_d)

for elem in brands:
    if elem not in brands_dict.values():
        requests.post('http://127.0.0.1:8000/api/brands/?format=json', data={'name': elem})


report_type_d = requests.get('http://127.0.0.1:8000/api/report-types/?format=json').json()
report_type_dict = dict((elem['name'], elem['id']) for elem in report_type_d)

for elem in report_type:
    if elem not in report_type_dict.values():
        requests.post('http://127.0.0.1:8000/api/report-types/?format=json', data={'name': elem})


reports_d = json.loads(json.dumps(list(df.T.to_dict().values())))
sellers_d = requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json()
sellers_dict = dict((elem['name'], elem['id']) for elem in sellers_d)

brands_d = requests.get('http://127.0.0.1:8000/api/brands/?format=json').json()
brands_dict = dict((elem['name'], elem['id']) for elem in brands_d)

report_type_d = requests.get('http://127.0.0.1:8000/api/report-types/?format=json').json()
report_type_dict = dict((elem['name'], elem['id']) for elem in report_type_d)

for elem in reports_d:
    print(elem, elem.get('Контрагент'))
    for key_elem in sellers_dict.keys():
        print(key_elem)
        if elem.get('Контрагент') == key_elem:
            print(elem, elem.get('Контрагент'))
            elem['Контрагент'] = sellers_dict.get(key_elem)
            print(sellers_dict.get('key_elem'))


for elem in reports_d:
    print(elem, elem.get('ТМ'))
    for key_elem in brands_dict.keys():
        print(key_elem)
        if elem.get('ТМ') == key_elem:
            print(elem, elem.get('ТМ'))
            elem['ТМ'] = brands_dict.get(key_elem)
            print(brands_dict.get('key_elem'))


for elem in reports_d:
    print(elem, elem.get('Тип'))
    for key_elem in report_type_dict.keys():
        print(key_elem)
        if elem.get('Тип') == key_elem:
            print(elem, elem.get('Тип'))
            elem['Тип'] = report_type_dict.get(key_elem)
            print(report_type_dict.get('key_elem'))

print(reports_d)

report_dict1 = requests.get('http://127.0.0.1:8000/api/reports/?format=json').json()


for elem_dict in report_dict1:
    print(elem_dict)
    for elem in reports_d:
        print(elem)
        if ((elem.get('Период') != elem_dict['date']) and
            (elem.get('Контрагент') != elem_dict['seller']) and
            (elem.get('Тип') != elem_dict['report_type']) and
            (elem.get('ТМ') != report_dict1['brand'])) :

            d, s, b, t, m, rt = elem.get('Период'), elem.get('Контрагент'), elem.get('ТМ'), elem.get('Стоимость'), elem.get('Валовый Доход'), elem.get('Тип')
            requests.post('http://127.0.0.1:8000/api/reports/?format=json',
                          data={'date': d, 'seller': s, 'brand': b, 'turnover': t, 'margin': m, 'report type': rt})
            print(elem)
        else:
            t, m = elem.get('Стоимость'), elem.get('Валовый Доход')
            requests.put('http://127.0.0.1:8000/api/reports/{}/?format=json'.format(elem_dict['id']), data={'turnover': t, 'margin': m})
            print(elem, 'else')

# не понимаю как сделать put взамен существующих строк



# with open('plan.csv', 'r', encoding='utf-8') as f:
#     reader = list(csv.reader(f))
#     for row in reader[1:]:
#         d, s, b, t, m, rt = row[0], row[1], row[2], row[3], row[4], row[5]
#         requests.post('http://127.0.0.1:8000/api/reports/?format=json', data={'Date':d, 'Seller':s, 'Brand':b, 'Turnover':t, 'Margin':m, 'Report type':rt})



# req = requests.get('http://127.0.0.1:8000/api/sellers/?format=json')
# sellers = req.json()
# sellers_dict = dict((elem['name'], elem['id']) for elem in sellers)
# print(sellers_dict)
# requests.post('http://127.0.0.1:8000/api/sellers/?format=json', data = {'name':'sssaaaa'})
# print(req.json())
# requests.delete('http://127.0.0.1:8000/api/sellers/4/?format=json', data={'name':'sssaaaa'})
# requests.put('http://127.0.0.1:8000/api/sellers/1/?format=json', data={'name':'dddd'})
# print(requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json())