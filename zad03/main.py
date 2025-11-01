import sys
import os

def read_file(file, s):
    counter = 0
    children = []

    with open(file, "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = file_content.splitlines()

        if file_content.strip():
            for line in lines:
                if line.startswith("\\input"):
                    new_file = line.split("{")[1].split("}")[0]

                    pid = os.fork()

                    if pid == 0: # zerowy pid oznacza, że jesteśmy w procesie potomnym
                        subcount = read_file(new_file, s)
                        os._exit(subcount)
                    else:
                        children.append(pid)
                else:
                    for word in line.split(" "):
                        if word == s:
                            counter+=1

    for pid in children:
        pid, status = os.waitpid(pid, 0)
        counter += os.WEXITSTATUS(status)
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