def get_arguments():
    filename = input("Podaj nazwę pliku klienta: ")

    with open("bufor.txt", "w") as bufor:
        bufor.write(filename + "\n")

        print("Wpisz tekst lub zakończ wpisywanie wpisując 'END':")
        while True:
            line = input()
            if line == "END":
                bufor.write("END\n")
                break
            bufor.write(line + "\n")

    print("Dane zostały wpisane do bufora.")

get_arguments()