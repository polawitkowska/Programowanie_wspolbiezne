import socket

# Konfiguracja serwera
HOST = '127.0.0.1'
PORT = 12000

def run_server():
    # Tworzenie gniazda UDP (SOCK_DGRAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"Serwer nasłuchuje na {HOST}:{PORT}")
    print("Czekam na graczy...")

    # Struktury danych
    clients = []      # Lista adresów: [(ip, port), (ip, port)]
    moves = {}        # Słownik ruchów: {adres: 'p'/'k'/'n'}
    scores = {}       # Słownik punktów: {adres: int}

    # Zasady gry (klucz pokonuje wartość)
    rules = {'k': 'n', 'n': 'p', 'p': 'k'}
    names = {'k': 'Kamień', 'n': 'Nożyce', 'p': 'Papier', 'koniec': 'Koniec'}

    while True:
        try:
            message, addr = server_socket.recvfrom(1024)
            msg_str = message.decode('utf-8').lower().strip()

            # Logika rejestracji graczy
            if addr not in clients:
                if len(clients) < 2:
                    clients.append(addr)
                    scores[addr] = 0
                    print(f"[+] Dołączył nowy gracz: {addr}")
                else:
                    continue

            if msg_str == 'koniec':
                print(f"Gracz {addr} zakończył grę.")
                # Poinformuj drugiego gracza (jeśli istnieje)
                for client in clients:
                    if client != addr:
                        server_socket.sendto("KONIEC_GRY".encode('utf-8'), client)
                
                # Reset serwera
                clients.clear()
                moves.clear()
                scores.clear()
                print("--- RESET STANU GRY. Czekam na nową parę graczy ---\n")
                continue

            # --- OBSŁUGA RUCHU GRY ---
            if msg_str in ['p', 'k', 'n']:
                moves[addr] = msg_str
                print(f"Otrzymano ruch od {addr}")
            else:
                continue

            # Sprawdzenie, czy mamy ruchy od obu graczy
            if len(moves) == 2:
                p1_addr = clients[0]
                p2_addr = clients[1]
                
                m1 = moves[p1_addr]
                m2 = moves[p2_addr]

                result_p1 = ""
                result_p2 = ""

                # Logika wyłaniania zwycięzcy
                if m1 == m2:
                    result_p1 = "REMIS"
                    result_p2 = "REMIS"
                elif rules[m1] == m2:
                    result_p1 = "WYGRANA"
                    result_p2 = "PRZEGRANA"
                    scores[p1_addr] += 1
                else:
                    result_p1 = "PRZEGRANA"
                    result_p2 = "WYGRANA"
                    scores[p2_addr] += 1

                # Wyświetlanie wyników na serwerze
                print(f"\n--- WYNIK RUNDY ---")
                print(f"Gracz 1 ({p1_addr}): {names[m1]} | Pkt: {scores[p1_addr]}")
                print(f"Gracz 2 ({p2_addr}): {names[m2]} | Pkt: {scores[p2_addr]}")
                print("-------------------\n")

                # Wysyłanie odpowiedzi do klientów
                # Format: "WYNIK:RUCH_PRZECIWNIKA"
                msg_p1 = f"{result_p1}:{names[m2]}"
                msg_p2 = f"{result_p2}:{names[m1]}"

                server_socket.sendto(msg_p1.encode('utf-8'), p1_addr)
                server_socket.sendto(msg_p2.encode('utf-8'), p2_addr)

                # Wyczyszczenie ruchów przed następną rundą
                moves.clear()

        except KeyboardInterrupt:
            print("\nZamykanie serwera.")
            break
        except Exception as e:
            print(f"Błąd: {e}")

    server_socket.close()

if __name__ == "__main__":
    run_server()