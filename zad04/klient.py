import os
import errno
import time


SERVER = "/tmp/kolejka"
CLIENT = "/tmp/klient"

try:
    os.mkfifo(CLIENT)
    print("FIFO klienta utworzone.")
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

ID = input("Podaj ID, które chcesz wyszukać: ")

with open(SERVER, "w") as fifo:
    fifo.write(f"{ID},{CLIENT}")
    print("Wysłano ID.")


with open(CLIENT, "r") as fifo:
    result = fifo.read().strip()
    print("Odpowiedź serwera:", result)