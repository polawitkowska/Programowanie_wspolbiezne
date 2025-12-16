import threading
import math
import time

LICZBA_WATKOW = 4
wynik = []

lock = threading.Lock()
bariera = threading.Barrier(LICZBA_WATKOW + 1) 

def czy_pierwsza(liczba):
    if liczba <= 1: return False
    if liczba == 2: return True
    if liczba % 2 == 0: return False
    
    limit = math.isqrt(liczba) + 1
    for i in range(3, limit, 2):
        if liczba % i == 0:
            return False
    return True

def watek_praca(podlista):
    global wynik
    lokalne_pierwsze = []
    
    for liczba in podlista:
        if czy_pierwsza(liczba):
            lokalne_pierwsze.append(liczba)
    
    with lock:
        wynik.extend(lokalne_pierwsze)
    
    try:
        bariera.wait()
    except threading.BrokenBarrierError:
        pass

def get_range():
    while True:
        try:
            start = int(input("Podaj początek zakresu: "))
            end = int(input("Podaj koniec zakresu: "))
            if start < end:
                return list(range(start, end + 1))
            else:
                print("Początek musi być mniejszy od końca.")
        except ValueError:
            print("Podaj poprawne liczby.")

def main():
    global wynik
    lista_liczb = get_range()
    
    dlugosc = len(lista_liczb)
    rozmiar_kawalka = math.ceil(dlugosc / LICZBA_WATKOW)
    
    watki = []
    print(f"Uruchamianie {LICZBA_WATKOW} wątków...")
    start_time = time.time()

    for i in range(LICZBA_WATKOW):
        start = i * rozmiar_kawalka
        end = start + rozmiar_kawalka
        fragment = lista_liczb[start:end]

        t = threading.Thread(target=watek_praca, args=(fragment,))
        watki.append(t)
        t.start()

    print("Główny wątek czeka na barierze...")
    bariera.wait()
    
    end_time = time.time()

    wynik.sort()
    print("-" * 30)
    print(f"Znaleziono {len(wynik)} liczb pierwszych.")
    print(f"Wynik: {wynik}")
    print(f"Czas obliczeń: {end_time - start_time:.5f} s")

if __name__ == "__main__":
    main()