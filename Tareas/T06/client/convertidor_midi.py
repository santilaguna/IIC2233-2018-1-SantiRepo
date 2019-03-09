# módulo destinado a convertir los bytes en un archivo midi.

def convertir_a_midi(song, song_bytes):
    with open("downloads/" + song + ".mid", 'wb') as file:
        file.write(song_bytes)

if __name__ == '__main__':
    pass
