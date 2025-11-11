import os
import errno
import struct

SERVER = "/tmp/kolejka"
CLIENT = "/tmp/klient"
client_path = CLIENT.encode("utf-8")

try:
    os.mkfifo(CLIENT)
    print("FIFO klienta utworzone.")
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

ID = input("Podaj ID, które chcesz wyszukać: ").encode("utf-8")
msg = struct.pack("!II", 4 + len(client_path), int(ID)) + client_path

fd = os.open(SERVER, os.O_WRONLY)
os.write(fd, msg)
os.close(fd)

fd_client = os.open(CLIENT, os.O_RDONLY)
response = os.read(fd_client, 1024).decode("utf-8")
os.close(fd_client)

print("Odpowiedź serwera:", response)