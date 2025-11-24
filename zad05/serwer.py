import sysv_ipc # type: ignore
import time

# Klucze dla kolejek
INPUT_KEY = 1234
OUTPUT_KEY = 5678

dictionary = {"hej": "hello", "kot": "cat", "pies": "dog", "pa": "bye"}

try:
    input_queue = sysv_ipc.MessageQueue(INPUT_KEY, sysv_ipc.IPC_CREAT)
except sysv_ipc.ExistentialError:
    input_queue = sysv_ipc.MessageQueue(INPUT_KEY)

print("Serwer rozpoczal dzialanie...")

try:
    output_queue = sysv_ipc.MessageQueue(OUTPUT_KEY, sysv_ipc.IPC_CREAT)
except sysv_ipc.ExistentialError:
    output_queue = sysv_ipc.MessageQueue(OUTPUT_KEY)

def translate(word):
    for w in dictionary:
        if w == word:
            return dictionary[w]
        
    return "Nie znam takiego slowa"

try:
    while True:
        # Odbieranie komunikatu
        message, mtype = input_queue.receive()  # mtype = PID klienta
        pid = mtype
        text = message.decode()

        if text.lower() == "stop":
            print("Otrzymano komunikat stop.")
            break

        print(f"Serwer otrzymal od PID {pid}: {text}")

        # Wysyłanie odpowiedzi
        response = translate(text)
        output_queue.send(response.encode(), type=pid)
except KeyboardInterrupt:
    print("ERROR. Serwer konczy dzialanie...")
    input_queue.remove()
    output_queue.remove()
finally:
    print("Serwer konczy dzialanie...")
    input_queue.remove()
    output_queue.remove()