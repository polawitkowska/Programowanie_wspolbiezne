import threading
import random
import time

ROZMIAR_LISTY = 1000000
LICZBA_WATKOW = 4

calkowita_suma = 0

def watek_sumowania(fragment_listy, numer_watku):

    global calkowita_suma

    suma_lokalna = sum(fragment_listy)

    with threading.Lock():
        calkowita_suma += suma_lokalna

def main():
    global calkowita_suma
    
    print(f"Generowanie listy {ROZMIAR_LISTY} elementów...")
    lista_liczb = [random.randint(1, 100) for _ in range(ROZMIAR_LISTY)]
    
    start_time = time.time()
    wynik_referencyjny = sum(lista_liczb)
    end_time = time.time()
    print(f"Suma referencyjna (jednowątkowo): {wynik_referencyjny}")
    print(f"Czas (single-thread): {end_time - start_time:.5f} s\n")

    watki = []
    dlugosc_kawalka = len(lista_liczb) // LICZBA_WATKOW
    
    print(f"Uruchamianie {LICZBA_WATKOW} wątków...")
    start_time_multi = time.time()

    for i in range(LICZBA_WATKOW):
        start = i * dlugosc_kawalka
        if i == LICZBA_WATKOW - 1:
            end = len(lista_liczb)
        else:
            end = (i + 1) * dlugosc_kawalka
            
        fragment = lista_liczb[start:end]

        t = threading.Thread(target=watek_sumowania, args=(fragment, i+1))
        watki.append(t)
        t.start()

    for t in watki:
        t.join()

    end_time_multi = time.time()

    print(f"-"*30)
    print(f"Suma obliczona wielowątkowo:    {calkowita_suma}")
    print(f"Czy wynik poprawny?             {'TAK' if calkowita_suma == wynik_referencyjny else 'NIE'}")
    print(f"Czas (multi-thread):            {end_time_multi - start_time_multi:.5f} s")

main()