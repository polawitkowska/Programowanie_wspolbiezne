import time
import os

printed = False
while True:
    if not os.path.exists("bufor.txt"):
        open("bufor.txt", "w").close()

    with open("bufor.txt", "r+") as bufor:
        bufor_content = bufor.read()
        lines = bufor_content.splitlines()

        if bufor_content.strip():
            file_name = lines[0]
            remaining_content = '\n'.join(lines[1:-1])
            
            if remaining_content.strip():
                print("Klient napisał:\n", remaining_content)

            answer = input("Podaj odpowiedz dla klienta: ")
            with open(file_name, "w") as client_file:
                client_file.write(answer+"\nEND")

            print("Odpowiedz zostala wyslana klientowi.")
            open("bufor.txt", "w").close()
            printed = False

        else:
            if not printed:
                print("Czekam na dane od klienta...")
                printed = True
            time.sleep(1)
                