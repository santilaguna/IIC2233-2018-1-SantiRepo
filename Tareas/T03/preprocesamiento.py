# módulo destinado a procesar las reviews antes de comenzar

import re


def reviews_cleaner(line):
    """As seen at: https://stackoverflow.com/questions/9662346/
    python-code-to-remove-html-tags-from-a-string"""
    cleaner = re.compile('<.*?>')
    almostcleantext = re.sub(cleaner, '', line)
    cleantext = almostcleantext.replace("&nbsp", "")
    return cleantext


def vocabulary():
    with open("vocabulary.txt", "r", encoding="utf-8") as file:
        bot_words = (word.strip() for word in file)
        return set(bot_words)


def bot_cleaner(line, bot_words):
    lista_palabras = line.split()[1:]  # id pelicula
    if len(lista_palabras) not in range(6, 85):
        return True  # no cumple con la condición del bot -> review real
    palabras_bot = list(filter(lambda x: (word in x for word in bot_words),
                               lista_palabras))  # enjoy -> enjoyable
    palabras_dict = {word: palabras_bot.count(word) for word in bot_words if
                     palabras_bot.count(word) > 0}
    # se realiza con bot_words para que las palabras como liked no sean llaves
    if len(palabras_dict) < 4:
        return True
    if max(palabras_dict.values()) < 3:
        return True
    return False


def reviews_reader(path):
    with open(path, "r", encoding="utf-8", newline="") as file:
        file.readline()
        reviews = map(lambda x: reviews_cleaner(x.strip()), file)
        return list(filter(lambda x: bot_cleaner(x, vocabulary()), reviews))


def reviews_writer(path="clean_reviews.csv",
                   reader="TestingDatabase/reviews.csv"):
    reviews = reviews_reader(reader)
    with open(path, "w", encoding="utf-8") as file:
        file.write("id, review\n")
        for review in reviews:
            file.write(review + "\n")
