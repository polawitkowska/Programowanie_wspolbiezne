import socket
import threading
import time
from game_logic import make_move, edges, all_edges

HOST = '127.0.0.1'
PORT = 5000

clients = []
players = ['R', 'B']
current_player = 0
game_over = False

all_edges = set()

edges = {
    'R': set(),
    'B': set()
}

lock = threading.Lock()

def handle_client(conn, player_id):
    global current_player, game_over

    conn.sendall(f"YOU_ARE {players[player_id]}\n".encode())

    while not game_over:
        if current_player != player_id:
            conn.sendall(b"WAIT\n")
            time.sleep(0.1)  # Krótkie oczekiwanie przed ponownym sprawdzeniem
            continue

        conn.sendall(b"YOUR_TURN\n")

        try:
            data = conn.recv(1024).decode().strip()
        except:
            break

        if not data:
            break

        parts = data.split()
        if parts[0] != "MOVE" or len(parts) != 3:
            conn.sendall(b"ILLEGAL\n")
            continue

        a, b = int(parts[1]), int(parts[2])

        with lock:
            result = make_move(players[player_id], a, b)

            if result == "Illegal move":
                conn.sendall(b"ILLEGAL\n")

            elif result == "Game ended":
                conn.sendall(b"LOSE\n")
                other = clients[1 - player_id]
                other.sendall(b"WIN\n")
                game_over = True

            else:
                conn.sendall(b"OK\n")
                current_player = 1 - current_player

    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)

    print("Oczekiwanie na graczy...")

    while len(clients) < 2:
        conn, addr = server.accept()
        print("Dołączył:", addr)
        clients.append(conn)

    for i, conn in enumerate(clients):
        thread = threading.Thread(target=handle_client, args=(conn, i))
        thread.start()


if __name__ == "__main__":
    main()
