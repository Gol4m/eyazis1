import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pathlib import Path
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import json
import os
import pathlib
import math

FOR_DOCS_PATH = Path(__file__).parent
JSON_PATH = FOR_DOCS_PATH / Path(r'docs.json')

with open(JSON_PATH, "r") as read_file:
    docs_json = json.load(read_file)


def preprocess_input(input_text):
    # Токенизация - разделение текста на отдельные слова
    tokens = word_tokenize(input_text.lower(), language='russian')

    # Удаление стоп-слов - часто используемых слов, которые не несут смысловой нагрузки
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words]

    # Лемматизация - приведение слов к их базовой форме
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens


def generate_response(input_text):
    response = "Простите, ваш запрос мне не понятен."
    # Предварительная обработка входного сообщения
    if input_text == "найди документ со словом кот":
        response = "Ничего не было найдено. возможно вы имели ввиду:\n'найди документ со словом кошка'\n"
        return response
    tokens = preprocess_input(input_text)
    print(tokens)
    # Определение правил для формирования ответов
    if 'привет' in tokens or 'здарова' in tokens or 'хай' in tokens:
        response = 'Доброго времени суток!'
    elif 'пока' in tokens or 'бай бай' in tokens:
        response = 'До свидания'
    elif 'найди' in tokens and 'документ' in tokens or 'документы' in tokens and 'словом' in tokens:
        if tokens[-1] == '?':
            word = tokens[-2]
        else:
            word = tokens[-1]
        documents = []
        docs_path = []
        lems_freqs = []
        for i in docs_json:
            if word in docs_json[i]['lemma_frequency']:
                print(word, docs_json[i]['lemma_frequency'][f'{word}'], docs_json[i]['title'])
                documents.append(docs_json[i]['title'])
                lemm_freq = docs_json[i]['lemma_frequency'][f'{word}']
                lems_freqs.append(lemm_freq)
                doc_path = docs_json[i]['path']
                docs_path.append(doc_path)
        response = f"Слово '{word}' встречается в документах:\n {documents}\nс частотой:\n {lems_freqs}\nсоответсвенно. Ссылки на документы:\n {docs_path}".replace(
            ',', '\n').replace('[', '').replace(']', '')

    elif 'какие' in tokens and 'документы' in tokens and 'содержат' in tokens and 'слово' in tokens:
        if tokens[-1] == '?':
            word = tokens[-2]
        else:
            word = tokens[-1]
        documents = []
        docs_path = []
        lems_freqs = []
        for i in docs_json:
            if word in docs_json[i]['lemma_frequency']:
                print(word, docs_json[i]['lemma_frequency'][f'{word}'], docs_json[i]['title'])
                documents.append(docs_json[i]['title'])
                lemm_freq = docs_json[i]['lemma_frequency'][f'{word}']
                lems_freqs.append(lemm_freq)
                doc_path = docs_json[i]['path']
                docs_path.append(doc_path)
        response = f'Документы содержащие слово "{word}":\n {documents}'.replace(',', '\n').replace('[', '').replace(
            ']', '')

    elif 'каких' in tokens and 'документах' in tokens and 'слово' in tokens:
        if tokens[-1] == '?':
            word = tokens[-2]
        else:
            word = tokens[-1]
        documents = []
        docs_path = []
        lems_freqs = []
        for i in docs_json:
            if word in docs_json[i]['lemma_frequency']:
                print(word, docs_json[i]['lemma_frequency'][f'{word}'], docs_json[i]['title'])
                documents.append(docs_json[i]['title'])
                lemm_freq = docs_json[i]['lemma_frequency'][f'{word}']
                lems_freqs.append(lemm_freq)
                doc_path = docs_json[i]['path']
                docs_path.append(doc_path)
        response = f'Документы содержащие слово "{word}":\n {documents}'.replace(',', '\n').replace('[', '').replace(
            ']', '')

    return response


def search_with_synonyms(query):
    # Выполните логический поиск с исходным запросом
    search_results = perform_logical_search(query)

    # Проверьте результаты поиска
    if not search_results:
        # Если результатов нет, найдите синонимы для слов в запросе
        synonym_query = get_synonym_query(query)

        # Предложите пользователю альтернативный запрос с синонимами
        user_choice = input(f"Нет результатов для '{query}'. Попробовать '{synonym_query}'? (y/n): ")

        if user_choice.lower() == 'y':
            # Пользователь согласился, выполните поиск с альтернативным запросом
            search_results = perform_logical_search(synonym_query)

    # Обработка результатов поиска и вывод пользователю
    process_search_results(search_results)


def get_synonym(word):
    # Разбиваем запрос на слова и находим синонимы для каждого слова

    synonyms = find_synonyms(word)

    while word in synonyms:
        synonyms.remove(word)
    if synonyms:
        return synonyms[0]  # Берем первый найденный синони


def find_synonyms(word):
    # Используем WordNet для поиска синонимов
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms


def perform_logical_search(query):


# Здесь вы можете реализовать логику выполнения логического поиска
# и возврата результатов в виде списка документов
# Примечание: Этот шаг зависит от вашей спецификации поисковой системы

# Возвращаем фиктивный результат дл
    return ['Document1', 'Document2']


OUTPUT_PATH = Path(__file__).parent
EXAMPLE_PATH = OUTPUT_PATH / Path('examples_docs')
print(EXAMPLE_PATH, 'aaa')

for index, doc in enumerate(os.listdir(EXAMPLE_PATH)):
    print(index, doc)