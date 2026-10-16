import math as m

def faktorial(n):
    hasil = 1
    for i in range(2, n + 1):
        hasil *= i
    return hasil

def error_relatif(tv, av):
    return abs((tv - av) / tv) * 100

def suku_sin(n, x):
    return (-1)**n * x**(2*n + 1) / faktorial(2*n + 1)

def suku_cos(n, x):
    return (-1)**n * x**(2*n) / faktorial(2*n)

print("program sinus-cosinus")
print("Nama: Keanu Alinskie Raffi Ibrahim")
print("NIM: 1306625052")
print()
ulang="y"
while ulang == "y":
    sudut=float(input("masukkan sudut: "))

    x=m.radians(sudut)
    tv_sin=m.sin(x)
    tv_cos=m.cos(x)

    print(f"true value sin ({sudut:g})= {tv_sin}")
    print(f"true value cos ({sudut:g})={tv_cos}")
    print("-" * 50)

    if abs(tv_sin) < 1e-9 or abs(tv_cos) < 1e-9:
        print("Er tidak bisa dihitung karena true value mendekati 0.")
    else:
        print(f"{'Jumlah':^8}|{'AV':^12}|{'ER':^10}|{'AV':^12}|{'ER':^10}|")
        print(f"{'Suku':^8}|{'sinus':^12}|{'sinus':^10}|{'cosinus':^12}|{'cos':^10}|")
        print("-" * 8 + "|" + "-" * 12 + "|" + "-" * 10 + "|" + "-" * 12 + "|" + "-" * 10 + "|")

        n = 1
        av_sin = av_cos = 0
        er_sin = er_cos = 100

        while er_sin >= 5 or er_cos >= 5:
            av_sin += suku_sin(n - 1, x)
            av_cos += suku_cos(n - 1, x)
            er_sin = error_relatif(tv_sin, av_sin)
            er_cos = error_relatif(tv_cos, av_cos)
            print(f"{n:^8}|{av_sin:^12.6f}|{er_sin:^9.4f}%|{av_cos:^12.6f}|{er_cos:^9.4f}%")
            n += 1

    print()
    ulang = input("Mau menghitung lagi (y/t) ? ").lower().strip()
print ("selamat tinggal")

   

