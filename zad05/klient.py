import sysv_ipc # type: ignore
import os
import time

INPUT_KEY = 1234
OUTPUT_KEY = 5678

# Podłączanie do istniejących kolejek
input_queue = sysv_ipc.MessageQueue(INPUT_KEY)
output_queue = sysv_ipc.MessageQueue(OUTPUT_KEY)

pid = os.getpid()
message = input("Podaj slowo do przetlumaczenia, lub 'stop' aby zakonczyc dzialanie serwera: ")

if message.lower() != "stop":
    # symulacja zapełnienia serwera
    # for i in range(20):
    #     # Wysyłanie komunikatu do serwera z typem wiadomości = PID klienta
    #     input_queue.send(message.encode(), type=pid)
    #     time.sleep(1)
    input_queue.send(message.encode(), type=pid)


    # Odbieranie odpowiedzi
    while True:
        response, mtype = output_queue.receive(type=pid)  # filtrujemy po PID
        print(f"Klient {pid} otrzymal: {response.decode()}")
        break

else:
    input_queue.send(message.encode(), type=pid)
    print("Wyslano komunikat stop do serwera.")