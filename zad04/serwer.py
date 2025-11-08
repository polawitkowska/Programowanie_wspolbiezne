import os
import errno
import time

FIFO_PATH = "/tmp/kolejka"

postac1 = set(1, 'Kowalski')
postac2 = set(2, 'Nowak')
postac3 = set(3, 'Witkowska')
postac4 = set(4, 'Szymanski')

baza_danych = [postac1, postac2, postac3, postac4]

while True:
    try:
        os.mkfifo(FIFO_PATH)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    with open(FIFO_PATH, "w") as fifo:
        print(fifo)
