import time
import math
from multiprocessing import Pool, cpu_count
from pierwszePlus import pierwsza1

def znajdz_male_pierwsze(r):
	mlp = []
	s = math.ceil(math.sqrt(r))
	for i in range(2, s + 1):
		if all(i % p != 0 for p in mlp if p * p <= i):
			mlp.append(i)
	return mlp

def znajdz_blizniacze_sekwencyjnie(l, r):
	mlp = znajdz_male_pierwsze(r)
	blizniaki = []
	for i in range(l, r - 1):
		if pierwsza1(i, mlp) and pierwsza1(i + 2, mlp):
			blizniaki.append((i, i + 2))
	return blizniaki

def blizniaki_fragment(args):
	l, r, mlp = args
	blizniaki = []
	for i in range(l, r):
		if pierwsza1(i, mlp) and pierwsza1(i + 2, mlp):
			blizniaki.append((i, i + 2))
	return blizniaki

def znajdz_blizniacze_rownolegle(l, r, nproc):
	mlp = znajdz_male_pierwsze(r)
	zakres = r - l
	krok = zakres // nproc
	args = []
	for i in range(nproc):
		start = l + i * krok
		end = l + (i + 1) * krok if i < nproc - 1 else r - 1
		args.append((start, end, mlp))
	with Pool(processes=nproc) as pool:
		wyniki = pool.map(blizniaki_fragment, args)
	blizniaki = [item for sublist in wyniki for item in sublist]
	return blizniaki

if __name__ == "__main__":
	l = 1
	r = 200
	print(f"Zakres: {l} - {r}")
	print("Sekwencyjnie:")
	start = time.time()
	blizniaki_seq = znajdz_blizniacze_sekwencyjnie(l, r)
	czas_seq = time.time() - start
	print(f"Czas: {czas_seq:.2f} s, liczba par: {len(blizniaki_seq)}")

	print("\nRównolegle:")
	nproc = cpu_count()
	start = time.time()
	blizniaki_par = znajdz_blizniacze_rownolegle(l, r, nproc)
	czas_par = time.time() - start
	print(f"Czas: {czas_par:.2f} s, liczba par: {len(blizniaki_par)}")
	print(f"Przyspieszenie: {czas_seq/czas_par:.2f}x przy {nproc} procesach")
