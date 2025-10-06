import time

while True:
    with open("./zad01/dane.txt", "r") as file:
        file_content = file.read()
        if file_content.strip():
            print("Plik dane.txt zawiera dane:", file_content.strip())

            x =int(file_content)
            wynik = (x*x)+(2*x)

            with open("./zad01/wyniki.txt", "w") as file:
                file.write(f"{wynik}")

            with open("./zad01/dane.txt", "w") as file:
                pass

            time.sleep(5)
        else:
            print("Plik dane.txt jest pusty")
            time.sleep(5)