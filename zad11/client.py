import socket

HOST = '127.0.0.1'
PORT = 5000

def move(client):
    while True:
        move = input("Podaj ruch (np. 1 3): ")
        try:
            a, b = move.split()
            client.sendall(f"MOVE {a} {b}\n".encode())
            return
        except:
            print("Zły format wejścia")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    waiting_printed = False

    while True:
        data = client.recv(1024).decode().strip()
        if not data:
            break

        for message in data.splitlines():

            if message.startswith("YOU_ARE"):
                _, color = message.split()
                print(f"Grasz jako: {color}")

            elif message == "YOUR_TURN":
                print("Twoja tura.")
                waiting_printed = False
                move(client)
                
            elif message == "WAIT":
                if not waiting_printed:
                    print("Czekaj na ruch przeciwnika...")
                    waiting_printed = True

            elif message == "OK":
                print("Ruch zaakceptowany.")
                waiting_printed = False

            elif message == "ILLEGAL":
                print("Niepoprawny ruch, spróbuj ponownie.")

            elif message == "WIN":
                print("Wygrałeś!")
                client.close()
                return

            elif message == "LOSE":
                print("Przegrałeś, utworzyłeś trójkąt.")
                client.close()
                return

    client.close()


if __name__ == "__main__":
    main()
