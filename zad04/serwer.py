import os
import errno
import time
import signal
import struct
import atexit

#variables
SERVER = "/tmp/kolejka"
PID = os.getpid()
running = True

def cleanup():
    try:
        if os.path.exists(SERVER):
            os.unlink(SERVER)
            print("Usunięto FIFO serwera:", SERVER)
    except Exception as e:
        print("Błąd usuwania FIFO:", e)

# rejestrujemy cleanup na normalne zakończenie
atexit.register(cleanup)

#signal handling
def handle_usr1(signum, frame):
    global running
    print("\nOtrzymano SIGUSR1: serwer kończy działanie.")
    running = False
signal.signal(signal.SIGHUP, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, handle_usr1)

#write pid to file and create fifo
with open("./serwer_pid.txt", "w") as file:
    file.write(f"{PID}")
print("PID serwera to:", PID)

try:
    os.mkfifo(SERVER)
    print('FIFO serwera utworzone.')
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

#create an example of a database
postac1 = {'ID': 1, 'Nazwisko': 'Kowalski'}
postac2 = {'ID': 2, 'Nazwisko': 'Nowak'}
postac3 = {'ID': 3, 'Nazwisko': 'A'}
postac4 = {'ID': 4, 'Nazwisko': 'B'}
baza_danych = [postac1, postac2, postac3, postac4]

#find by id in database
def find(ID):
    print("Szukam postaci o ID:", ID)
    for character in baza_danych:
        if character['ID'] == ID:
            return character['Nazwisko']
    return "Nie ma."

try:
    #server 
    while running:
        fd = os.open(SERVER, os.O_RDONLY)
        header = os.read(fd, 8) #only read header first

        if not header:
            os.close(fd)
            continue

        length, ID = struct.unpack("!II", header)
        client_path = os.read(fd, length - 4).decode("utf-8")
        os.close(fd)

        print(f"Otrzymano ID={ID}.")

        # simulation of slower server
        # print("Serwer przetwarza zapytanie...")
        # time.sleep(5)

        result = find(ID)

        payload = result.encode("utf-8")
        msg = struct.pack("!I", len(payload)) + payload
        
        fd_client = os.open(client_path, os.O_WRONLY)
        os.write(fd_client, msg)
        os.close(fd_client)
        
        print("Serwer wysłał odpowiedź.")
        time.sleep(0.5)
finally:
    cleanup()