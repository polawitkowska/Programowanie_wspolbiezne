import time

def wpisz_dane():
    try:
        dane = int(input("Podaj pojedynczą liczbę całkowita: "))
        with open("./zad01/dane.txt", "w") as file:  
            file.write(f"{dane}")

    except ValueError:
        print("Podana wartość nie jest liczbą całkowitą! Spróbuj jeszcze raz")
        wpisz_dane()
        
wpisz_dane()
while True:
    time.sleep(5)

    with open("./zad01/wyniki.txt", "r") as file:
        file_content = file.read()
        if file_content.strip():
            print("Plik wyniki.txt zawiera dane:", file_content.strip())

            with open("./zad01/wyniki.txt", "w") as file:
                pass
            break
        else:
            print("Plik wyniki.txt jest pusty")