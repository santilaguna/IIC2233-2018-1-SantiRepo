# módulo destinado a cargar lo archivos
import csv

def competidores():
    with open("competidores.csv", "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        return [x for x in reader]
