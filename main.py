import csv
import re
from collections import defaultdict

# Читаем исходные данные
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# Функция для приведения телефонов в единый формат
def format_phone(phone):
    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*(доб\.)\s*(\d+))?")
    formatted_phone = pattern.sub(r"+7(\2)\3-\4-\5 \7\8", phone).strip()
    return formatted_phone


# Приведение фамилии, имени и отчества к нужному формату
for contact in contacts_list:
    # Пропускаем пустые строки
    if not any(contact):
        continue

    full_name = ' '.join(contact[:3]).split()
    contact[:3] = full_name + [''] * (3 - len(full_name))

    # Проверяем, есть ли в списке контактный телефон (6-й элемент)
    if len(contact) > 5 and contact[5]:
        # Форматируем телефон
        contact[5] = format_phone(contact[5])

# Объединение дубликатов по фамилии и имени
contacts_dict = defaultdict(dict)
for contact in contacts_list[1:]:
    if not any(contact):
        continue

    full_name_key = (contact[0], contact[1])
    if full_name_key in contacts_dict:
        existing_contact = contacts_dict[full_name_key]
        for i in range(2, len(contact)):
            if not existing_contact.get(i):
                existing_contact[i] = contact[i]
    else:
        contacts_dict[full_name_key] = {i: contact[i] for i in range(len(contact))}

# Создаем новый список контактов из объединенных данных
final_contacts_list = [contacts_list[0]]  # Добавляем заголовки
for key, contact_dict in contacts_dict.items():
    contact = [contact_dict.get(i, '') for i in range(len(contacts_list[0]))]
    final_contacts_list.append(contact)

# Записываем результат в новый CSV файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)
