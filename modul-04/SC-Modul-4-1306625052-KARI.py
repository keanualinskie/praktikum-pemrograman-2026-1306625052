import pandas as pd

def hitung_grade(na):
    if na >= 86:
        return "A"
    elif na >= 81:
        return "A-"
    elif na >= 76:
        return "B+"
    elif na >= 71:
        return "B"
    elif na >= 66:
        return "B-"
    elif na >= 61:
        return "C+"
    elif na >= 56:
        return "C"
    else:
        return "TL"

def main():
    print("Program Grading")
    print("Nama: Keanu Alinskie Raffi Ibrahim")
    print("NIM: 1306635052")
    print("\nLAPORAN GRADING MAHASISWA")

    
    file_path = r'C:\Users\LENOVO\Downloads\DataNilai.xlsx'
    
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan. Pastikan file ada di folder yang benar.")
        return

    col_nama = df.columns[0]
    col_lain2 = df.columns[2]
    col_UTS = df.columns[3]
    col_UAS = df.columns[4]

    rekap = {
        "A": 0, "A-": 0, "B+": 0, "B": 0, 
        "B-": 0, "C+": 0, "C": 0, "TL": 0
    }

    print("-" * 45)
    print(f"{'No':<4} | {'Nama Mahasiswa':<15} | {'NA':<11} | {'Grade':<5}")
    print("-" * 45)

    total_mahasiswa = len(df)

    for i, row in df.iterrows():
        nama_mhs = str(row[col_nama])
        n_lain2 = float(row[col_lain2])
        n_uts = float(row[col_UTS])
        n_uas = float(row[col_UAS])

        na = (0.30 * n_lain2) + (0.35 * n_uts) + (0.35 * n_uas)
        grade = hitung_grade(na)

        if grade in rekap:
            rekap[grade] += 1

        print(f"{i + 1:<4} | {nama_mhs:<15} | {na:<11.2f} | {grade:<5}")

    print("-" * 45)
    print("\nRekapitulasi :")
    for grade, jumlah in rekap.items():
        print(f"Grade {grade}: {jumlah}")
    print(f"Tidak Lulus (TL) = {rekap['TL']}")
    print(f"Total Mahasiswa = {total_mahasiswa}")

if __name__ == "__main__":
    main()