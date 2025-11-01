import sys

def read_file(file, s):
    counter = 0

    with open(file, "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = file_content.splitlines()

        if file_content.strip():
            for line in lines:
                if line.startswith("\\input"):
                    new_file = line.split("{")[1].split("}")[0]
                    counter += read_file(new_file, s)
                else:
                    for word in line.split(" "):
                        if word == s:
                            counter+=1

    return counter

def main():
    try:
        if sys.argv[1]:
            if sys.argv[2]:
                p, s = sys.argv[1], sys.argv[2]
    except IndexError as e:
        print("Error: nie podano dwoch argumentow.")
        return
    
    counter = read_file(p, s)
    
    print("Liczba slow", s, "w plikach:", counter)

main()