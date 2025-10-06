import time

def wpisz_dane():
    try:
        dane = int(input("Podaj pojedynczą liczbę całkowita: "))
        with open("./dane.txt", "w") as file:  
            file.write(f"{dane}")

    except ValueError:
        print("Podana wartość nie jest liczbą całkowitą! Spróbuj jeszcze raz")
        wpisz_dane()
        
wpisz_dane()
while True:
    time.sleep(2)

    with open("./wyniki.txt", "r") as file:
        file_content = file.read()
        if file_content.strip():
            print("Wynik to:", file_content.strip())

            with open("./wyniki.txt", "w") as file:
                pass
            break
        else:
            print("Plik wyniki.txt jest pusty")