from pprint import pprint
import re
import csv
import os
cwd = os.path.dirname(__file__)
file_name = 'phonebook_raw.csv'
new_file_name = 'phonebook.csv'
full_path = os.path.join(cwd, file_name)
new_full_path = os.path.join(cwd, new_file_name)

with open(full_path, 'r', encoding='UTF8') as file:
  rows = csv.reader(file, delimiter=",")
  contacts_list = list(rows)

lastname_list = [] #Список всех контактов
new_contacts_list = [] #Новый список обработанных контактов
for count in contacts_list:
  str = count[0] + ' ' + count[1] + ' '  + count[2]
  fio = re.split(r'\s+', str)
  lastname = fio[0]
  firstname = fio[1]
  surname = fio[2]
  organization = count[3]
  position = count[4]
  pattern = r"(\+7|8)?\s*?\(?(\d{3,5})\)?\s*?-?(\d{3,5})-?(\d{2,4})-?(\d{2,4})\s?\(?(\w*\W?)\s?(\d{4})?\)?"
  new_pattern = r'+7(\2)\3-\4-\5 \6\7'
  phone = re.sub(pattern, new_pattern, count[5])
  email = count[6]

  people = [lastname, firstname, surname, organization, position, phone, email] # Создадим список и занесем в него кантакт
  lastname_list.append(lastname) # Делаем список списков с контактами

  new_contacts_list.append(people)

del_el = [] # Список, в который помещаем индексы дублирующихся записейй для дальнейшего удаления
k = 0

# Проходим циклом по новому списку контактов и ищем совпадения
for i in new_contacts_list:
  for j in new_contacts_list[k + 1:]:
    if j[0] == i[0]:
      del_el.append(new_contacts_list.index(j))
      l = 0
      correct_list = []
      # Проходим циклом по каждому повторяещемуся контакту и объединяем в один 
      for item in j:
        if len(item) == 0: 
          correct_list.append(i[l]) # 
        else:
          correct_list.append(j[l])
        l += 1
        new_contacts_list[k] = correct_list
  k += 1

# Почистим новый список контактов от дублей
del_el.reverse()
for el in del_el:
  new_contacts_list.pop(el)
  
# Создаем новый файл и записываем в него новый список контактов
with open(new_full_path, "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contacts_list)