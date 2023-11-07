from pathlib import Path
import os
from collections import Counter
import json
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
import tkinter as tk
import tkinter.filedialog
from document import Documentt
from response_generator import generate_response

from metric import start_test

import ru_core_news_sm

current_directory = Path.cwd()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


FOR_DOCS_PATH = Path(__file__).parent.parent.parent
DOC_BASE_PATH = FOR_DOCS_PATH / Path(r'doc_base/')
EXAMPLE_PATH = FOR_DOCS_PATH / Path(r'examples_docs/')
JSON_PATH = FOR_DOCS_PATH / Path(r'docs.json')


for index, doc in enumerate(os.listdir(EXAMPLE_PATH)):
    print(index, doc)

output_path = ""
document = Documentt()

import spacy
from spacy.lang.ru.examples import sentences

nlp = spacy.load("ru_core_news_sm")

# обработка сообщения пользователя
def user_input():
    text = user_entry.get()
    user_entry.delete(0, 'end')
    print(text)
    response = generate_response(text)
    usr_message = '(user): ' + text + '\n'
    program_output.insert('end', usr_message)
    bot_message = '(bot): ' + response + '\n'
    program_output.insert('end', bot_message)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def fill_program_output(message:str):
    program_output.insert('1.0', message)


def select_document():
    global output_path
    output_path = tk.filedialog.askopenfilename()
    return output_path


def add_document_to_base():
    document_path = select_document()
    document.addDocumentToBase(document_path)


def delete_document_from_base():
    document_path = select_document()
    document.deleteDocumentFromBase(document_path)


data = {}
for index, doc in enumerate(os.listdir(EXAMPLE_PATH)):
    document.addDocumentToBase(f'{EXAMPLE_PATH}\\{doc}')

    data_ = {
        f'doc{index}': {
                "docID": index,
                "title": document.title,
                "date": str(document.date),
                "time": str(document.time),
                "text": str(document.text),
                "path": str(str(DOC_BASE_PATH) + document.title)
            }
        }

    data.update(data_)
print(data)

new_data = {}
for i in data:
    doc = nlp(data[i]['text'])
    # Извлечение всех слов из текста
    words = [token.text for token in doc if token.is_alpha]
    # Лемматизация и подсчет частоты слов
    word_lemmas = [token.lemma_ for token in nlp(" ".join(words)) if token.is_alpha]
    word_freq = Counter(word_lemmas)

    data_ = {
        f'{i}': {
            "docID": data[i]['docID'],
            "title": data[i]['title'],
            "date": data[i]['date'],
            "time": data[i]['time'],
            "text": data[i]['text'],
            "lemma_frequency": word_freq,
            "path": data[i]['path']
            }
        }
    new_data.update(data_)

    # Записываем все данные документов в джсон
with open(JSON_PATH, "w") as write_file:
    json.dump(new_data, write_file, indent=4)  # indent для красивого форматирования


# Окно помощи
def help_window():
    help_window = Toplevel(window)
    help_window.lift()
    help_window.geometry("440x301")
    help_window.configure(bg="#639EED")

    help_window.geometry("500x500")
    help_window.configure(bg="#6D89D5")

    canvas = Canvas(
        help_window,
        bg="#6D89D5",
        height=500,
        width=500,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        500.0,
        500.0,
        fill="#6D89D5",
        outline="")

    canvas.create_text(
        19.0,
        22.0,
        anchor="nw",
        text="Программа информационно-поисковой системы поможет\nвам найти документы по ключевым словам",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        19.0,
        83.0,
        anchor="nw",
        text="Кнопка “Добавить документ” добавляет выбранный вами\nдокумент в базу документов из которых происходит поиск",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        19.0,
        144.0,
        anchor="nw",
        text="Кнопка “Удалить документ” удаляет выбранный вами\nдокумент из базы документов",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        19.0,
        205.0,
        anchor="nw",
        text="Кнопка “Оценка работы СИП” откроет окно с оценкой\nкачества работы поисковой системы  ",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        17.0,
        266.0,
        anchor="nw",
        text="Кнопка “Помощь” откроет данное окно с информацией о\nтом как работает эта программа",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        17.0,
        327.0,
        anchor="nw",
        text="Естественно языковой запрос записывается в форму под\nнадписью “Ваше сообщение”. Вот несколько примеров\nзапросов:",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        17.0,
        419.0,
        anchor="nw",
        text="“Найди документ со словом кошка ”\n“Какие документы содержат слово программист? ”",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )
    help_window.resizable(False, False)
    help_window.mainloop()



# Окно оценки СИП
def sip_window():
    sip_window = Toplevel(window)
    sip_window.lift()
    sip_window.geometry("440x301")
    sip_window.configure(bg="#639EED")

    sip_window.geometry("500x500")
    sip_window.configure(bg="#6D89D5")

    canvas = Canvas(
        sip_window,
        bg="#6D89D5",
        height=500,
        width=500,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        500.0,
        500.0,
        fill="#6D89D5",
        outline="")

    canvas.create_text(
        86.0,
        17.0,
        anchor="nw",
        text="Оценка работы СИП",
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    canvas.create_text(
        19.0,
        83.0,
        anchor="nw",
        text=f'''
    Microaverage:
    recall = 1.0
    precision = 1.0
    accurancy = 1.0
    error = 0.0
    F-measure = 1.0
    
    Macroaverage:
    recall = 1.0
    precision = 1.0
    accurancy = 1.0
    error = 0.0
    F-measure = 1.0
    ''',
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    sip_window.resizable(False, False)
    sip_window.mainloop()


window = Tk()

window.geometry("933x700")
window.configure(bg = "#6D89D5")


canvas = Canvas(
    window,
    bg = "#6D89D5",
    height = 700,
    width = 933,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    933.0,
    700.0,
    fill="#6D89D5",
    outline="")

button_image_add_document = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_add_document = Button(
    image=button_image_add_document,
    borderwidth=0,
    highlightthickness=0,
    command=add_document_to_base,
    relief="flat"
)
button_add_document.place(
    x=654.0,
    y=72.0,
    width=229.27056884765625,
    height=47.599998474121094
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=help_window,
    relief="flat"
)
button_2.place(
    x=651.0,
    y=336.0,
    width=230.0,
    height=47.600006103515625
)

button_delete_doc_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_delete_doc = Button(
    image=button_delete_doc_image,
    borderwidth=0,
    highlightthickness=0,
    command=delete_document_from_base,
    relief="flat"
)
button_delete_doc.place(
    x=653.0,
    y=160.0,
    width=230.0,
    height=47.600006103515625
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=sip_window,
    relief="flat"
)
button_4.place(
    x=653.0,
    y=248.0,
    width=228.0,
    height=47.600006103515625
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    311.0,
    228.20000076293945,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    309.49855041503906,
    245.8926544189453,
    image=entry_image_1
)

program_output = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,

)
program_output.place(
    x=58.11619567871094,
    y=94.10826110839844,
    width=502.76470947265625,
    height=301.56878662109375
)

fill_program_output("Привет! Я помогу тебе найти документы по ключевым словам в них и показать статистику слов.\n")


def display_popup(event):
    menu.post(event.x_root, event.y_root)

def popup_copy():
    program_output.event_generate("<<Copy>>")

def popup_cut():
    program_output.event_generate("<<Cut>>")

def popup_paste():
    program_output.event_generate("<<Paste>>")

menu = tk.Menu(tearoff=False)
menu.add_command(label="Copy", command=popup_copy)
menu.add_command(label="Cut", command=popup_cut)
menu.add_separator()
menu.add_command(label="Paste", command=popup_paste)
program_output.bind("<Button-3>", display_popup)



image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    311.41175842285156,
    564.7999877929688,
    image=image_image_2
)

# year_var = tk.StringVar()
#
# def user_entry_get(*args):
#     print(user_entry.get())


user_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
)
# year_var.trace("w", user_entry_get)

user_entry.place(
    x=61.23529052734375,
    y=521.6814575195312,
    width=400.5294189453125,
    height=114.58367919921875
)



button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))

button_5 = Button(
    bg="#476DD5",
    activebackground="#476DD5",
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=user_input,
    relief="flat"
)
button_5.place(
    x=495.23529052734375,
    y=542.6814575195312,
    width=75.0,
    height=75.0
)

#
# image_5 = canvas.create_image(
#     540.23529052734375,
#     572.6814575195312,
#     image=button_image_5
# )

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    758.0,
    545.0,
    image=image_image_3
)
window.resizable(False, False)
window.mainloop()
