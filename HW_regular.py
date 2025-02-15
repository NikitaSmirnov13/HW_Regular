import csv
import re


# Функция для разделения ФИО на фамилию, имя и отчество
def split_fio(fio):
    parts = fio.split()
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        return parts[0], parts[1], ''
    else:
        return fio, '', ''


# Функция для форматирования телефонного номера
def format_phone(phone):
    # Убираем все нецифровые символы, кроме "доб."
    digits = re.sub(r'[^0-9доб]', '', phone)

    # Ищем добавочный номер
    extension_match = re.search(r'доб(\d+)', digits)
    extension = extension_match.group(1) if extension_match else None

    # Убираем "доб" и оставляем только цифры
    digits = re.sub(r'доб\d+', '', digits)

    # Проверяем, что номер содержит 11 цифр (российский номер)
    if len(digits) == 11:
        formatted_phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', digits)
    else:
        formatted_phone = phone  # Если номер не соответствует формату, оставляем как есть

    # Добавляем добавочный номер, если он есть
    if extension:
        formatted_phone += f' доб.{extension}'

    return formatted_phone


# Чтение исходного файла
with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

# Словарь для группировки записей по фамилии и имени
contacts_dict = {}

# Обработка данных
header = contacts_list[0]
for row in contacts_list[1:]:
    # Разделяем ФИО на фамилию, имя и отчество
    lastname, firstname, surname = split_fio(' '.join(row[:3]))

    # Группируем только по фамилии и имени
    key = (lastname, firstname)

    # Форматируем телефон
    row[5] = format_phone(row[5])

    # Если запись с таким ключом уже есть, объединяем данные
    if key in contacts_dict:
        existing_row = contacts_dict[key]

        # Обновляем отчество, если оно отсутствует в существующей записи
        if not existing_row[2] and surname:
            existing_row[2] = surname

        # Обновляем остальные поля
        for i in range(3, len(row)):
            if not existing_row[i] and row[i]:
                existing_row[i] = row[i]
    else:
        # Создаём новую запись с правильным ФИО
        new_row = [lastname, firstname, surname] + row[3:]
        contacts_dict[key] = new_row

# Преобразуем словарь обратно в список
processed_contacts = [header]
for key, row in contacts_dict.items():
    processed_contacts.append(row)

# Запись обработанных данных в новый файл
with open('phonebook.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(processed_contacts)

print("Запись завершилась успехом")