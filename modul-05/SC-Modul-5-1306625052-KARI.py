Nilai = [85, 13, 99, 34, 71, 15, 82, 24, 64, 61, 67, 99, 50, 68, 25, 37, 32, 27, 14, 91, 79, 15, 47, 48, 74, 88,
64, 53, 77, 50, 24, 91, 87, 55, 60, 75, 91, 22, 47, 63, 81, 88, 26, 48, 69, 59, 84, 77, 28, 36, 59, 74, 89, 73,
91, 64, 55, 88, 90, 48, 73, 97, 98, 40, 93, 50, 78, 60, 44, 77, 82, 51, 53, 65, 98, 59, 94, 91, 52, 44, 65, 85,
72, 92, 49, 67, 58, 48, 62, 54, 89, 67, 58, 48, 85, 45, 77, 76, 81, 77]
print("Program Sorting")
print("Nama : Keanu Alinskie Raffi Ibrahim")
print("NIM : 1306625052")


print("\nData sebelum Sorting : ") 
i = 0
while i < len(Nilai):
    print(f"{Nilai[i]:2}", end=" ")

    if (i + 1) % 10 == 0:
        print()
    else:
        print(",", end="")

    i += 1

n = len(Nilai)
i = 0
while i < n - 1:
    j = 0
    while j < n - i - 1:
        if Nilai[j] > Nilai[j + 1]:
            temp = Nilai[j]
            Nilai[j] = Nilai[j + 1]
            Nilai[j + 1] = temp
        j += 1
    i += 1

print("\nData Nilai Setelah Sorting : ") 
i = 0
while i < len(Nilai):
    print(f"{Nilai[i]:2}", end=" ")

    if (i + 1) % 10 == 0:
        print()
    else:
        print(",", end="")

    i += 1

print("selesai")