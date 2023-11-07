import os
from datetime import datetime
from pathlib import Path
import shutil
import PyPDF2
import json
from collections import Counter
current_directory = Path.cwd()

#
FOR_DOCS_PATH = Path(__file__).parent

DOC_BASE_PATH = FOR_DOCS_PATH / Path(r'doc_base/')
EXAMPLE_PATH = FOR_DOCS_PATH / Path(r'examples_docs/')
JSON_PATH = FOR_DOCS_PATH / Path(r'docs.json')


import spacy

nlp = spacy.load("ru_core_news_sm")

class Documentt:
    title = str()
    text = str()
    date = str()
    time = str()
    docID = int()

    path = str()

    # добавить док в базу
    def addDocumentToBase(self, filepath):
        print(filepath)
        if filepath != "":
            if filepath[-4::] != '.pdf':
                print('это не pdf')
            else:
                with open(filepath, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    text = ''
                    for i in range(num_pages):
                        page = reader.pages[i]
                        text += page.extract_text()

                    lines = text.splitlines()
                    text = ' '.join(lines)
        self.text = text

        self.title = os.path.basename(f"{filepath}")
        self.date = datetime.today().date()
        self.time = datetime.now().time()
        self.docID = len(list(Path(DOC_BASE_PATH).iterdir()))
        shutil.copy(filepath, f"{DOC_BASE_PATH}\\{os.path.basename(f'{filepath}')}")

        self.path = f"{DOC_BASE_PATH}\\{self.title}"
        print(f'document {filepath} added')

    # удалить док из базы
    def deleteDocumentFromBase(self, file_path):
        new_data = {}
        with open(JSON_PATH, "r") as read_file:
            data = json.load(read_file)

        title = os.path.basename(file_path)

        for i in data:
            if data[i]['title'] == title:
                os.remove(f"{DOC_BASE_PATH}{title}")

        for i in data:
            if data[i]['title'] != title:
                data_ = {
                    f'{i}': {
                    "docID": data[i]['docID'],
                    "title": data[i]['title'],
                    "date": data[i]['date'],
                    "time": data[i]['time'],
                    "text": data[i]['text']
                }
            }
                new_data.update(data_)
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
                    "lemma_frequency": word_freq
                }
            }
            new_data.update(data_)
        # Откройте файл в режиме записи и перезапишите его новыми данными
        with open(JSON_PATH, "w") as write_file:
            json.dump(new_data, write_file, indent=4)  # indent для красивого форматирования
        print(f'document {file_path} deleted')

    # получить частоту леммы(исходная форма слова) с документа
    def getLemmInverseFrequency(self, lemmId, result):
        pass

    # получить вес слов из документа
    def getWordWeightInDocument(self, lemmStr, docID, result):
        pass

    # получить вес леммы из документа
    def getLemmWeightInDocument(self):
        pass