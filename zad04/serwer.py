import os
import errno
import time
import signal
import sys

running = True

def handle_usr1(signum, frame):
    global running
    print("\nOtrzymano SIGUSR1: serwer kończy działanie.")
    running = False

signal.signal(signal.SIGHUP, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, handle_usr1)

SERVER = "/tmp/kolejka"
PID = os.getpid()

with open("./serwer_pid.txt", "w") as file:
    file.write(f"{PID}")
print("PID serwera to:", PID)

try:
    os.mkfifo(SERVER)
    print('FIFO serwera utworzone.')
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

postac1 = {'ID': '1', 'Nazwisko': 'Kowalski'}
postac2 = {'ID': '2', 'Nazwisko': 'Nowak'}
postac3 = {'ID': '3', 'Nazwisko': 'A'}
postac4 = {'ID': '4', 'Nazwisko': 'B'}

baza_danych = [postac1, postac2, postac3, postac4]

def find(ID):
    print("Szukam postaci o ID:", ID)
    for character in baza_danych:
        if character['ID'] == ID:
            return character['Nazwisko']
    return "Nie ma."

while running:
    with open(SERVER, "r") as fifo:
        data = fifo.read().strip()

        args = data.split(",")
        ID, CLIENT = args[0], args[1]
        print("Serwer otrzymał od klienta ID:", ID)

    result = find(ID)

    with open(CLIENT, "w") as fifo:
        fifo.write(result)
    
    print("Serwer wysłał odpowiedź.")
    time.sleep(0.5)
