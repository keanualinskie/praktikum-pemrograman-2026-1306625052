print(" himpunan faktor suatu bilangan ")
print("Nama: Keanu Alinskie Raffi Ibrahim")
print("NIM:1306625052")
print()
while True:
    angka = int(input("masukkan sembarang bilangan <100 :"))
    if angka == 0:
        print("Program selesai. Terima kasih!")
        break     
    himpunan_faktor = []
    for i in range(1, angka + 1):
        if angka % i == 0:
            himpunan_faktor.append(i)

    print("faktor dari", angka, "adalah", himpunan_faktor)
    print()  