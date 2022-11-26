# ## Факт

import pandas as pd
import numpy as np
import datetime

cur_date = pd.to_datetime(datetime.date.today())
fact_mk = pd.read_excel("data_source.xlsx", sheet_name = 'Маркетплейсы')
fact_is = pd.read_excel("data_source.xlsx", sheet_name = 'ИМ')

# ### преобразуем таблицу ИМ
# 1-я строка в качестве заголовков

fact_is.columns = fact_is.iloc[0] 
fact_is = fact_is[1:]

# переименовали столбцы, удалили пустые строки из выгрузки

fact_is.columns.values[0] = 'Период'
fact_is.columns.values[1] = 'Контрагент'
fact_is.dropna(subset=['Контрагент'], inplace=True)

# делаем условный столбец Торговая марка и отфильтровываем только нужных поставщиков

conditions = [
    (fact_is['Контрагент'] == '1.ИМ Томас Мюнц')|(fact_is['Контрагент'] == '3.Мобильное приложение ТМ')|\
    (fact_is['Контрагент'] == '6.ИМ Томас Мюнц предоплата самовывоз'),
    (fact_is['Контрагент'] == '2.ИМ Рикер'),
    (fact_is['Контрагент'] == '4.ИМ Salamander')|(fact_is['Контрагент'] == '3.1.Мобильное приложение SR')
]

choices = ['Thomas Munz', 'Rieker','Salamander']
fact_is['Торговая марка'] = np.select(conditions,choices, default='0')

fact_is = fact_is[fact_is['Торговая марка'] != '0']
fact_is['Контрагент2'] = 'ИМ'

# меняем типы данных в столбцах

fact_is = fact_is.astype({'Стоимость': np.float,'Валовый Доход': np.float,'Маржа': np.float,'Количество': np.int16})
fact_is['Период'] = pd.to_datetime(fact_is['Период'], format="%d.%m.%Y %H:%M:%S")

# ### преобразуем таблицу Маркетплейсы
# 1-я строка в качестве заголовков

fact_mk.columns = fact_mk.iloc[0] 
fact_mk = fact_mk[1:]

# переименовали столбцы, удалили пустые строки из выгрузки

fact_mk.columns.values[0] = 'Период'
fact_mk.columns.values[1] = 'Контрагент'
fact_mk.columns.values[2] = 'Торговая марка'

fact_mk.rename(columns = {'Стоимость регл оборот':'Стоимость','Валовый доход':'Валовый Доход','Количество оборот':'Количество'}, inplace = True)

fact_mk.dropna(subset=['Контрагент','Торговая марка'], inplace=True)

# делаем условный столбец Контрагент2

conditions = [
    (fact_mk['Контрагент'] == 'Вайлдберриз-Thomas Muenz')|(fact_mk['Контрагент'] == 'Вайлдберриз ООО'),
    (fact_mk['Контрагент'] == 'Купишуз ООО'),
    (fact_mk['Контрагент'] == 'Интернет Решения ООО Thomas Munz (Озон)')
]

choices = ['Вайлдберриз', 'Ламода','ОЗОН']

fact_mk['Контрагент2'] = np.select(conditions,choices, default='0')

# заменяем null на 0

fact_mk['Количество'] = fact_mk['Количество'].fillna(0)

# меняем типы данных в столбцах

fact_mk = fact_mk.astype({'Стоимость': np.float,'Валовый Доход': np.float,'Маржа': np.float,'Количество': np.int16})
fact_mk['Период'] = pd.to_datetime(fact_mk['Период'], format="%d.%m.%Y %H:%M:%S")

# ### объединяем 2 таблицы в общую таблицу Факт
# объединили 2 таблицы

fact = pd.concat([fact_is,fact_mk])

fact['Торговая марка'].unique()

# Создаем новый столбец Тип

fact['Тип'] = 'Факт'

# делаем условный столбец Торговая марка (сгруппированно)

conditions = [
    (fact['Торговая марка'] == 'Salamander')|(fact['Торговая марка'] == 'LURCHI'),
    (fact['Торговая марка'] == 'Rieker')|(fact['Торговая марка'] == 'POLARIS')|(fact['Торговая марка'] == 'REMONTE')|\
    (fact['Торговая марка'] == 'LUMBERJACK')|(fact['Торговая марка'] == 'U.S. POLO ASSN.')
]

choices = ['Salamander', 'ПТМ']

fact['Торговая марка (сгруппированно)'] = np.select(conditions,choices, default='Thomas Munz')

# группируем таблицу по полям ниже -> избавляемся от более мелких аттрибутов: Контрагент и Торговая марка

fact_gr = fact.groupby(['Период','Контрагент2','Торговая марка (сгруппированно)','Тип'],as_index=False).sum()

# меняем имена столбцов

fact_gr.rename(columns = {'Контрагент2':'Контрагент','Торговая марка (сгруппированно)':'ТМ'}, inplace = True)

# удаляем ненужные столбцы

###fact_gr.drop(['Маржа','Количество'] ,axis = 1, inplace = True)
fact_gr.drop(['Маржа'] ,axis = 1, inplace = True)

# загружаем результирующую таблицу в csv файл

fact_gr.to_csv('fact.csv', encoding = 'utf-8', sep = ',',index=False)

# ## План

cal_plan = pd.read_excel("data_source.xlsx", sheet_name = 'Календарь для плана')
plan = pd.read_excel("data_source.xlsx", sheet_name = 'План')

cal_plan_unpvt = cal_plan.melt(id_vars=['Период'], var_name='Контрагент', value_name='Выручка доли %')

# делаем вспомогательный столбцы и на основании них делаем cross join

cal_plan_unpvt['key'] = 1
plan['key'] = 1

cal_plan1 = cal_plan_unpvt.merge(plan, on=['key','Контрагент'], how='outer').drop('key',axis = 1)

# раскидываем план по долям по дням и удаляем ненужные столбцы

cal_plan1['Стоимость'] = cal_plan1['План Выручка']*cal_plan1['Выручка доли %']
cal_plan1['Валовый Доход'] = cal_plan1['План Вал']*cal_plan1['Выручка доли %']

cal_plan1.drop(['Выручка доли %','План Выручка','План Вал'] ,axis = 1, inplace = True)

# создаем новый столбец Тип

cal_plan1['Тип'] = 'План'

cal_plan1['Количество'] = 0

# сохраняем итоговую таблицу в csv файл

cal_plan1.to_csv('plan.csv', encoding = 'utf-8', sep = ',',index=False)

# ## Прогноз

cal = pd.read_excel("data_source.xlsx", sheet_name = 'Календарь для прогноза')
df_f = pd.read_csv("fact.csv", sep = ',', encoding = 'utf-8')

# создаем вспомогательные столбцы чтобы потом сделать cross join 

cal['key'] = 1
df_f['key'] = 1

# cross join календарь и связку Контрагент - ТМ

cal1 = cal.merge(df_f[['Контрагент','ТМ','key']], on='key', how='outer')

# преобразуем формат столбца с датой

df_f['Период'] = df_f['Период'].astype('datetime64[ns]')
cal1['Период'] = cal1['Период'].astype('datetime64[ns]')

# подтягиваем фактические значения к новой таблице с прогнозом

cal2 = cal1.merge(df_f,how = 'left', left_on = ['Контрагент','ТМ','Период'],right_on = ['Контрагент','ТМ','Период']).drop(['key_y','key_x','Тип'],axis = 1)
cal2= cal2.drop_duplicates()

cal3 = cal2.groupby(['Контрагент','ТМ'],as_index=False).mean()
cal2 = cal2.merge(cal3, how = 'left', on=['ТМ','Контрагент'])

# меняем пустые значения на средние в тех строках, где дата >= сегодня

cal2['Стоимость_x'][cal2['Период']>= cur_date ] = cal2['Стоимость_x'][cal2['Период']>= cur_date].fillna(cal2['Стоимость_y'][cal2['Период']>= cur_date])
cal2['Валовый Доход_x'][cal2['Период']>= cur_date] = cal2['Валовый Доход_x'][cal2['Период']>= cur_date].fillna(cal2['Валовый Доход_y'][cal2['Период']>= cur_date])
cal2['Количество_x'][cal2['Период']>= cur_date] = cal2['Количество_x'][cal2['Период']>= cur_date].fillna(cal2['Количество_y'][cal2['Период']>= cur_date])

# удаляем ненужные столбцы

cal2.drop(['Стоимость_y','Валовый Доход_y','Количество_y'],axis = 1, inplace =  True)

# создаем новый столбец Тип

cal2['Тип'] = 'Прогноз'
cal2.rename(columns = {'Стоимость_x':'Стоимость','Валовый Доход_x':'Валовый Доход','Количество_x':'Количество'}, inplace = True)

# сохраняем результирующую таблицу в csv файл

cal2.to_csv('forecast.csv', encoding = 'utf-8', sep = ',',index=False)

all_df = pd.concat([cal2,cal_plan1,fact_gr])

seller = pd.DataFrame({'seller_name': ['ИМ', 'ОЗОН', 'Вайлдберриз', 'Ламода'], 'seller_id': [1, 2, 3, 4]})
brand = pd.DataFrame({'brand_name': ['Salamander', 'Thomas Munz', 'ПТМ'], 'brand_id': [1, 2, 3]})
report_type = pd.DataFrame({'type_name': ['Прогноз', 'План', 'Факт'], 'type_id': [1, 2, 3]})

all_df = all_df.merge(seller,how = 'left', left_on = ['Контрагент'],right_on = ['seller_name']).drop(['Контрагент','seller_name'],axis = 1)
all_df = all_df.merge(brand,how = 'left', left_on = ['ТМ'],right_on = ['brand_name']).drop(['ТМ', 'brand_name'],axis = 1)
all_df = all_df.merge(report_type,how = 'left', left_on = ['Тип'],right_on = ['type_name']).drop(['Тип', 'type_name'],axis = 1)
all_df.drop(['Количество'],axis = 1, inplace=True)

all_df.to_csv('all_df.csv', encoding = 'utf-8', sep = ',',  index=False)
seller.to_csv('seller.csv', encoding = 'utf-8', sep = ',',index=False)
brand.to_csv('brand.csv', encoding = 'utf-8', sep = ',',index=False)
report_type.to_csv('report_type.csv', encoding = 'utf-8', sep = ',',index=False)


