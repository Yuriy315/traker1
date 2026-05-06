from tkinter import *
import json
from datetime import datetime
import os

window = Tk()
window.title("Weather Diary - Дневник погоды")
window.geometry("1200x800")
window.configure(bg="#f0f0f0")

records = []  # список для хранения записей
filtered_records = []  # список для отфильтрованных записей


def save_to_json():
    # сохраняет записи в JSON файл
    try:
        with open("weather_data.json", "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
        result_label.config(text="Данные сохранены в weather_data.json!", fg="green")
    except Exception as e:
        result_label.config(text=f"Ошибка сохранения: {e}", fg="red")


def load_from_json():
    # загружает записи из JSON файла
    global records, filtered_records
    try:
        if not os.path.exists("weather_data.json"):
            result_label.config(text="Файл weather_data.json не найден!", fg="red")
            return

        with open("weather_data.json", "r", encoding="utf-8") as f:
            records = json.load(f)

        # сортировка по дате
        records.sort(key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"))

        filtered_records = []
        update_listbox()
        result_label.config(text=f"Загружено {len(records)} записей!", fg="green")
    except Exception as e:
        result_label.config(text=f"Ошибка загрузки: {e}", fg="red")


def add_record():
    # добавляет новую запись
    global records

    date = date_entry.get()
    temp_str = temp_entry.get()
    description = desc_entry.get()
    precipitation = precip_var.get()

    # проверка на пустые поля
    if not date or not temp_str or not description:
        result_label.config(text="Заполните все поля!", fg="red")
        return

    # проверка формата даты
    try:
        datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        result_label.config(text="Неверный формат даты! Используйте ДД.ММ.ГГГГ", fg="red")
        return

    # проверка температуры
    try:
        temp = float(temp_str)
    except ValueError:
        result_label.config(text="Температура должна быть числом!", fg="red")
        return

    # создание записи
    record = {
        "date": date,
        "temperature": temp,
        "description": description,
        "precipitation": precipitation
    }

    records.append(record)

    # сортировка по дате
    records.sort(key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"))

    # очистка полей
    date_entry.delete(0, END)
    temp_entry.delete(0, END)
    desc_entry.delete(0, END)

    update_listbox()
    result_label.config(text="Запись добавлена!", fg="green")


def update_listbox():
    # обновляет список на экране
    listbox.delete(0, END)

    # определяем какие записи показывать
    display_records = filtered_records if filtered_records else records

    for record in display_records:
        # форматирование строки
        precip_text = "Осадки: да" if record["precipitation"] == "да" else "Осадки: нет"
        task_str = f"{record['date']} | {record['temperature']}°C | {record['description']} | {precip_text}"
        listbox.insert(END, task_str)

    # обновление статистики
    total = len(records)
    filtered = len(filtered_records) if filtered_records else total
    stats_label.config(text=f"Всего записей: {total} | Отфильтровано: {filtered}")


def delete_selected():
    # удаляет выбранную запись
    global records, filtered_records

    selection = listbox.curselection()

    if not selection:
        result_label.config(text="Выберите запись для удаления!", fg="red")
        return

    # определяем индекс в реальном списке
    display_records = filtered_records if filtered_records else records
    selected_index = selection[0]

    if display_records:
        selected_record = display_records[selected_index]

        # удаляем из основного списка
        for i, record in enumerate(records):
            if record == selected_record:
                records.pop(i)
                break

        # очищаем фильтры
        filtered_records = []
        date_filter_entry.delete(0, END)
        temp_filter_entry.delete(0, END)

        update_listbox()
        result_label.config(text="Запись удалена!", fg="green")


def delete_all():
    # удаляет все записи
    global records, filtered_records
    records = []
    filtered_records = []
    update_listbox()
    result_label.config(text="Все записи удалены!", fg="green")


def filter_by_date():
    # фильтрует записи по дате
    global filtered_records

    date_filter = date_filter_entry.get()

    if not date_filter:
        result_label.config(text="Введите дату для поиска!", fg="red")
        return

    # проверка формата даты
    try:
        datetime.strptime(date_filter, "%d.%m.%Y")
    except ValueError:
        result_label.config(text="Неверный формат даты! Используйте ДД.ММ.ГГГГ", fg="red")
        return

    filtered_records = []
    count = 0

    for record in records:
        if record["date"] == date_filter:
            filtered_records.append(record)
            count = count + 1

    update_listbox()

    if count == 0:
        result_label.config(text=f"Нет записей с датой '{date_filter}'", fg="red")
    else:
        result_label.config(text=f"Найдено {count} записей", fg="green")


def filter_by_temp_above():
    # фильтрует записи с температурой выше заданной
    global filtered_records

    temp_filter_str = temp_filter_entry.get()

    if not temp_filter_str:
        result_label.config(text="Введите значение температуры!", fg="red")
        return

    try:
        temp_filter = float(temp_filter_str)
    except ValueError:
        result_label.config(text="Температура должна быть числом!", fg="red")
        return

    filtered_records = []
    count = 0

    for record in records:
        if record["temperature"] > temp_filter:
            filtered_records.append(record)
            count = count + 1

    update_listbox()

    if count == 0:
        result_label.config(text=f"Нет записей с температурой выше {temp_filter}°C", fg="red")
    else:
        result_label.config(text=f"Найдено {count} записей с температурой выше {temp_filter}°C", fg="green")


def filter_by_temp_below():
    # фильтрует записи с температурой ниже заданной
    global filtered_records

    temp_filter_str = temp_filter_entry.get()

    if not temp_filter_str:
        result_label.config(text="Введите значение температуры!", fg="red")
        return

    try:
        temp_filter = float(temp_filter_str)
    except ValueError:
        result_label.config(text="Температура должна быть числом!", fg="red")
        return

    filtered_records = []
    count = 0

    for record in records:
        if record["temperature"] < temp_filter:
            filtered_records.append(record)
            count = count + 1

    update_listbox()

    if count == 0:
        result_label.config(text=f"Нет записей с температурой ниже {temp_filter}°C", fg="red")
    else:
        result_label.config(text=f"Найдено {count} записей с температурой ниже {temp_filter}°C", fg="green")


def filter_by_temp_equal():
    # фильтрует записи с температурой равной заданной
    global filtered_records

    temp_filter_str = temp_filter_entry.get()

    if not temp_filter_str:
        result_label.config(text="Введите значение температуры!", fg="red")
        return

    try:
        temp_filter = float(temp_filter_str)
    except ValueError:
        result_label.config(text="Температура должна быть числом!", fg="red")
        return

    filtered_records = []
    count = 0

    for record in records:
        if record["temperature"] == temp_filter:
            filtered_records.append(record)
            count = count + 1

    update_listbox()

    if count == 0:
        result_label.config(text=f"Нет записей с температурой {temp_filter}°C", fg="red")
    else:
        result_label.config(text=f"Найдено {count} записей", fg="green")


def show_all():
    # показывает все записи (сбрасывает фильтры)
    global filtered_records
    filtered_records = []
    date_filter_entry.delete(0, END)
    temp_filter_entry.delete(0, END)
    update_listbox()
    result_label.config(text="Показаны все записи", fg="green")


# ЗАГОЛОВОК
Label(text="ДНЕВНИК ПОГОДЫ", font="Arial 22 bold", bg="#f0f0f0", fg="#333333").place(x=450, y=15)

# ПОЛЯ ДЛЯ ВВОДА
Label(text="Дата (ДД.ММ.ГГГГ)", font="Arial 12", bg="#f0f0f0").place(x=50, y=65)
date_entry = Entry(font="Arial 12", width=30, bg="white", relief="solid")
date_entry.place(x=50, y=90)

Label(text="Температура (°C)", font="Arial 12", bg="#f0f0f0").place(x=50, y=125)
temp_entry = Entry(font="Arial 12", width=30, bg="white", relief="solid")
temp_entry.place(x=50, y=150)

Label(text="Описание погоды", font="Arial 12", bg="#f0f0f0").place(x=50, y=185)
desc_entry = Entry(font="Arial 12", width=30, bg="white", relief="solid")
desc_entry.place(x=50, y=210)

Label(text="Осадки", font="Arial 12", bg="#f0f0f0").place(x=50, y=245)
precip_var = StringVar(value="нет")

Radiobutton(text="Да", font="Arial 11", variable=precip_var, value="да", bg="#f0f0f0").place(x=50, y=275)
Radiobutton(text="Нет", font="Arial 11", variable=precip_var, value="нет", bg="#f0f0f0").place(x=120, y=275)

# КНОПКИ ДЛЯ ДОБАВЛЕНИЯ И УДАЛЕНИЯ
Button(text="ДОБАВИТЬ", font="Arial 10", command=add_record, bg="#4CAF50", fg="white", width=14).place(x=50, y=315)
Button(text="УДАЛИТЬ", font="Arial 10", command=delete_selected, bg="#F44336", fg="white", width=14).place(x=190, y=315)

# КНОПКИ ДЛЯ РАБОТЫ С JSON
Button(text="СОХРАНИТЬ В JSON", font="Arial 9", command=save_to_json, bg="#9C27B0", fg="white", width=17).place(x=50, y=350)
Button(text="ЗАГРУЗИТЬ ИЗ JSON", font="Arial 9", command=load_from_json, bg="#9C27B0", fg="white", width=17).place(x=190, y=350)
Button(text="ОЧИСТИТЬ ВСЁ", font="Arial 9", command=delete_all, bg="#F44336", fg="white", width=14).place(x=330, y=350)

# СООБЩЕНИЯ
result_label = Label(font="Arial 9", fg="red", text="", bg="#f0f0f0")
result_label.place(x=50, y=390)

# ФИЛЬТР ПО ДАТЕ
Label(text="ФИЛЬТР ПО ДАТЕ", font="Arial 12 bold", bg="#f0f0f0", fg="#333333").place(x=50, y=430)
date_filter_entry = Entry(font="Arial 12", width=20, bg="white", relief="solid")
date_filter_entry.place(x=50, y=460)
Button(text="НАЙТИ ПО ДАТЕ", font="Arial 10", command=filter_by_date, bg="#2196F3", fg="white", width=14).place(x=240, y=458)

# ФИЛЬТР ПО ТЕМПЕРАТУРЕ
Label(text="ФИЛЬТР ПО ТЕМПЕРАТУРЕ", font="Arial 12 bold", bg="#f0f0f0", fg="#333333").place(x=50, y=500)
temp_filter_entry = Entry(font="Arial 12", width=20, bg="white", relief="solid")
temp_filter_entry.place(x=50, y=530)

Button(text="ВЫШЕ", font="Arial 10", command=filter_by_temp_above, bg="#FF9800", fg="white", width=8).place(x=50, y=560)
Button(text="НИЖЕ", font="Arial 10", command=filter_by_temp_below, bg="#FF9800", fg="white", width=8).place(x=130, y=560)
Button(text="РАВНО", font="Arial 10", command=filter_by_temp_equal, bg="#FF9800", fg="white", width=8).place(x=210, y=560)

# КНОПКА ПОКАЗАТЬ ВСЕ
Button(text="ПОКАЗАТЬ ВСЕ", font="Arial 10", command=show_all, bg="#4CAF50", fg="white", width=14).place(x=50, y=600)

# СТАТИСТИКА
stats_label = Label(font="Arial 9", fg="#666666", text="Всего записей: 0 | Отфильтровано: 0", bg="#f0f0f0")
stats_label.place(x=50, y=640)

# СПИСОК ЗАПИСЕЙ
listbox = Listbox(font="Arial 12", width=70, height=36, bg="white", relief="solid", selectbackground="#4CAF50")
listbox.place(x=500, y=60)

# ЗАПУСК ПРОГРАММЫ
window.mainloop()