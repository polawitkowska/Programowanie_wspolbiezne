import os

fifo_path = "/tmp/kolejka"

with open(fifo_path, "r") as fifo:
    print("Odebrano:")
    for line in fifo:
        print(line.strip())
