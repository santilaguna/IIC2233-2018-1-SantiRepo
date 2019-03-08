# módulo destinado a las funcionalidades de los highscores.

import os


def cargar_highscores():
    if not os.path.isfile("highscores.txt"):
        return []
    with open("highscores.txt", "r", encoding="utf-8") as file:
        highscores = []
        for line in file:
            nombre, puntaje = line.strip().split(",")
            highscores.append([nombre, int(puntaje)])
        highscores.sort(key=lambda x: x[1], reverse=True)
    return highscores


def guardar_scores(highscores):
    with open("highscores.txt", "w", encoding="utf-8") as file:
        i = 0
        for name, score in highscores:
            i += 1
            file.write("{},{}\n".format(name, str(score)))
            if i == 10:
                break
