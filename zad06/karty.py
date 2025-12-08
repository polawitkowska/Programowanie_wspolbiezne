import sysv_ipc #type: ignore
import sys
import time

KEY_BASE = 1
KEY_PW1 = 2
KEY_PW2 = 4
KEY_SEM1 = 8  
KEY_SEM2 = 16 
KEY_SEM_READY = 32 # Gotowość gracza 2

NULL_CHAR = 'STOP'
TOTAL_ROUNDS = 3

def write(mem, s):
    s += NULL_CHAR
    s = s.encode()
    mem.write(s)

def read(mem):
    s = mem.read()
    s = s.decode()
    i = s.find(NULL_CHAR)
    if i != -1:
        s = s[:i]
    return s

def cleanup_resources(pw1, pw2, sem1, sem2, sem_ready, test_sem):
    try:
        sysv_ipc.remove_shared_memory(pw1.id)
    except:
        pass
    try:
        sysv_ipc.remove_shared_memory(pw2.id)
    except:
        pass
    try:
        sysv_ipc.remove_semaphore(sem1.id)
    except:
        pass
    try:
        sysv_ipc.remove_semaphore(sem2.id)
    except:
        pass
    try:
        sysv_ipc.remove_semaphore(sem_ready.id)
    except:
        pass
    try:
        sysv_ipc.remove_semaphore(test_sem.id)
    except:
        pass

def get_valid_input(player_num):
    while True:
        try:
            choice = input(f"Gracz {player_num}: Wybierz literę (A, B lub C): ").upper()
            if choice in ['A', 'B', 'C']:
                return choice
            else:
                print("Nieprawidłowy wybór. Wybierz A, B lub C.")
        except EOFError:
            print("\nKoniec wprowadzania. Zakończenie programu.")
            sys.exit(0)

def player1_game():
    print("-" * 50)
    print("Jesteś GRACZEM 1")
    print("-" * 50)
    print("Czekam na Gracza 2...")
    
    try:
        #Tworzenie IPC
        pw1 = sysv_ipc.SharedMemory(KEY_PW1, sysv_ipc.IPC_CREX, size=1024) # pamięć dla wyboru gracza 1
        pw2 = sysv_ipc.SharedMemory(KEY_PW2, sysv_ipc.IPC_CREX, size=1024) # pamięć dla wyboru gracza 2

        sem1 = sysv_ipc.Semaphore(KEY_SEM1, sysv_ipc.IPC_CREX, 0o700, 0)
        sem2 = sysv_ipc.Semaphore(KEY_SEM2, sysv_ipc.IPC_CREX, 0o700, 1)
        sem_ready = sysv_ipc.Semaphore(KEY_SEM_READY, sysv_ipc.IPC_CREX, 0o700, 0)
        
        write(pw1, "")
        write(pw2, "")
        
    except Exception as e:
        print(f"Błąd podczas tworzenia zasobów: {e}")
        sys.exit(1)
    
    # Czekaj na sygnał od Gracza 2, że jest gotowy
    sem_ready.acquire()
    print("Gracz 2 dołączył!\n")
    
    player1_wins = 0
    player2_wins = 0
    
    try:
        for round_num in range(1, TOTAL_ROUNDS + 1):
            print(f"\n--- TURA {round_num} ---")
            sem2.acquire()  

            #1.
            choice1 = get_valid_input(1)
            write(pw1, choice1)
            print(f"Wybrałeś pozycję: {choice1}")
            sem1.release()  

            #3.
            sem1.acquire()  
            choice2 = read(pw2)

            print(f"Gracz 1 wybrał: {choice1}")
            print(f"Gracz 2 wybrał: {choice2}")

            if choice1 == choice2:
                print("PRZEGRAŁEŚ tę turę :(")
                player2_wins += 1
            else:
                print("WYGRAŁEŚ tę turę!")
                player1_wins += 1

            print(f"Wynik: Gracz 1: {player1_wins}, Gracz 2: {player2_wins}")
            sem2.release() 
        
        print("\n" + "-" * 50)
        print("GRA ZAKOŃCZONA!")
        print(f"Wynik końcowy: Gracz 1: {player1_wins}, Gracz 2: {player2_wins}")
        if player1_wins > player2_wins:
            print("WYGRAŁEŚ GRĘ!")
        elif player1_wins < player2_wins:
            print("PRZEGRAŁEŚ GRĘ!")
        else:
            print("REMIS!")
        print("-" * 50)
        
    except KeyboardInterrupt:
        print("\nPrzerwano grę.")
    finally:
        print("\nUsuwanie zasobów IPC...")
        cleanup_resources(pw1, pw2, sem1, sem2, sem_ready, test_sem=None)

def player2_game():
    print("-" * 50)
    print("Jesteś GRACZEM 2")
    print("-" * 50)
    
    try:
        # Dołącza do IPC
        pw1 = sysv_ipc.SharedMemory(KEY_PW1)
        pw2 = sysv_ipc.SharedMemory(KEY_PW2)
        sem1 = sysv_ipc.Semaphore(KEY_SEM1)
        sem2 = sysv_ipc.Semaphore(KEY_SEM2)
        sem_ready = sysv_ipc.Semaphore(KEY_SEM_READY)
    except Exception as e:
        print(f"Błąd podczas dołączania do zasobów: {e}")
        print("Upewnij się, że Gracz 1 już działa.")
        sys.exit(1)
    
    # Sygnalizuje Graczowi 1, że jest gotowy
    print("Dołączono do gry. Powiadamianie Gracza 1...\n")
    sem_ready.release()
    
    player1_wins = 0
    player2_wins = 0
    
    try:
        for round_num in range(1, TOTAL_ROUNDS + 1):
            print(f"\n--- TURA {round_num} ---")
            
            # 2. 
            sem1.acquire()  
            choice2 = get_valid_input(2)
            write(pw2, choice2)
            print(f"Wybrałeś pozycję: {choice2}")
            sem1.release()  

            # 4. 
            sem2.acquire() 
            choice1 = read(pw1)
            
            print(f"Gracz 1 wybrał: {choice1}")
            print(f"Gracz 2 wybrał: {choice2}")
            
            if choice1 == choice2:
                print("WYGRAŁEŚ tę turę!")
                player2_wins += 1
            else:
                print("PRZEGRAŁEŚ tę turę :(")
                player1_wins += 1
            
            print(f"Wynik: Gracz 1: {player1_wins}, Gracz 2: {player2_wins}")
            sem2.release()  
        
        print("\n" + "-" * 50)
        print("GRA ZAKOŃCZONA!")
        print(f"Wynik końcowy: Gracz 1: {player1_wins}, Gracz 2: {player2_wins}")
        if player2_wins > player1_wins:
            print("WYGRAŁEŚ GRĘ!")
        elif player2_wins < player1_wins:
            print("PRZEGRAŁEŚ GRĘ!")
        else:
            print("REMIS!")
        print("-" * 50)
        
    except KeyboardInterrupt:
        print("\nPrzerwano grę.")
    finally:
        print("\nUsuwanie zasobów IPC...")

def main():
    try:
        test_sem = sysv_ipc.Semaphore(KEY_BASE + 100, sysv_ipc.IPC_CREX, 0o700, 1)
        pierwszy = True
    except sysv_ipc.ExistentialError:
        test_sem = sysv_ipc.Semaphore(KEY_BASE + 100)
        pierwszy = False
        time.sleep(0.5) 
    
    if pierwszy:
        player1_game()
        test_sem.remove()  
    else:
        player2_game()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        print("Czyszczenie wszystkich zasobów IPC...")
        try:
            pw1 = sysv_ipc.SharedMemory(KEY_PW1)
            pw2 = sysv_ipc.SharedMemory(KEY_PW2)
            sem1 = sysv_ipc.Semaphore(KEY_SEM1)
            sem2 = sysv_ipc.Semaphore(KEY_SEM2)
            sem_ready = sysv_ipc.Semaphore(KEY_SEM_READY)
            test_sem = sysv_ipc.Semaphore(KEY_BASE + 100)
            cleanup_resources(pw1, pw2, sem1, sem2, sem_ready, test_sem)
            print("Wyczyszczono!")
        except Exception as e:
            print(f"Błąd: {e}")
    else:
        main()
