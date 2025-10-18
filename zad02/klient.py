import os
import time

cannot_inclue = ['<', '>', ':', '"', '/', '\\', '|', '*', '?']

def get_filename():
    filename = input("Podaj nazwę pliku klienta: ")
    invalid_chars = [char for char in filename if char in cannot_inclue]

    if invalid_chars:
        print("Nazwa pliku nie moze zawierac " + ", ".join(invalid_chars))
        return get_filename()

    if not filename.endswith(".txt"):
        filename += ".txt"

    return filename

def send_to_server():
    while True:
        printed = False
        while os.path.exists("lockfile"):
            if not printed:
                print("Serwer zajęty, proszę czekać")
                printed = True
            time.sleep(1)
        else:
            open("lockfile", "w").close()
            filename = get_filename()

            with open("bufor.txt", "w") as bufor:
                bufor.write(filename + "\n")

                print("Wpisz tekst lub zakończ wpisywanie wpisując 'END':")
                while True:
                    line = input()
                    if line == "END":
                        bufor.write("END\n")
                        break
                    bufor.write(line + "\n")

            print("Dane zostały wpisane do bufora.")
            read_from_server(filename)
            break

def read_from_server(filename):
    print("Czekam na odpowiedz serwera...")
    while True:
        if os.path.exists(filename):
            with open(filename, "r") as client_file:
                answer = client_file.read()

                lines = answer.splitlines()
                print("Odpowiedz serwera:", "\n".join(lines[:-1]))

            os.remove(filename)
            os.remove("lockfile")
            break
        else: time.sleep(1)

send_to_server()