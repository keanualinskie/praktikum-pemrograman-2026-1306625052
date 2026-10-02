print(" konversi suhu ")
print("Nama: Keanu ")
print("NIM:1306625052")

suhu_awal = float(input("suhu_awal :"))
suhu_akhir = float(input("suhu_akhir :"))
selang = float(input("selang = "))


if selang <= 0:
    print(" selang tidak boleh 0 atau negatif ")
else:
    print("Tabel Konversi")
    print("="*47)
    print(f"| {'No.':<4} | {'celcius':<10} | {'Reamur':<10} | {'Farenheit':<10} |")
    print("="*45)

    c = suhu_awal
    no = 1
    while c <= suhu_akhir:
        r = 0.8 * c
        f = 1.8 * c + 32
        
        print(f"| {no:<4} | {c:<10.1f} | {r:<10.1f} | {f:<10.1f} |")
        
        c += selang
        no += 1

    print("="*45)