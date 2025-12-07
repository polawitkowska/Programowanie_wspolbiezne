import socket
import sys

# Konfiguracja
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Port klienta jest przydzielany automatycznie przez system przy pierwszym sendto
    
    my_score = 0
    print("--- GRA PAPIER, KAMIEŃ, NOŻYCE (UDP) ---")
    print("Dostępne komendy: p (papier), k (kamień), n (nożyce)")
    print("Wpisz 'koniec' aby zakończyć grę.")
    print("------------------------------------------\n")

    while True:
        try:
            command = input("\nTwój wybór (p/k/n/koniec): ").strip().lower()

            if command not in ['p', 'k', 'n', 'koniec']:
                print("Niepoprawny wybór. Spróbuj ponownie.")
                continue

            # Wysyłanie wyboru do serwera
            client_socket.sendto(command.encode('utf-8'), (SERVER_IP, SERVER_PORT))

            if command == 'koniec':
                print("Zakończyłeś grę.")
                break

            print("Czekam na ruch drugiego gracza...")
            
            # Odbieranie odpowiedzi (blokujące)
            data, _ = client_socket.recvfrom(1024)
            response = data.decode('utf-8')

            # Obsługa nagłego zakończenia gry przez drugiego gracza
            if response == "KONIEC_GRY":
                print("\n!!! Drugi gracz zakończył rozgrywkę !!!")
                print("Gra przerwana. Zamykanie klienta.")
                break

            # Parsowanie odpowiedzi (WYNIK:RUCH_PRZECIWNIKA)
            parts = response.split(':')
            result = parts[0]
            opponent_move = parts[1] if len(parts) > 1 else "?"

            # Aktualizacja lokalnej punktacji
            if result == "WYGRANA":
                my_score += 1
            
            # Wyświetlanie wyniku
            print(f"\n--- RUNDA ZAKOŃCZONA ---")
            print(f"Twój wynik: {result}")
            print(f"Ruch przeciwnika: {opponent_move}")
            print(f"Twoje punkty łącznie: {my_score}")

        except KeyboardInterrupt:
            # Obsługa Ctrl+C
            print("\nPrzerwano działanie klienta.")
            client_socket.sendto("koniec".encode('utf-8'), (SERVER_IP, SERVER_PORT))
            break
        except Exception as e:
            print(f"Błąd komunikacji: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    run_client()