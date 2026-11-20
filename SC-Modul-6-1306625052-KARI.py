
import pygame
import sys

# ---------------------------------------------------------------
# 1. PENGATURAN AWAL
# ---------------------------------------------------------------
pygame.init()

LEBAR, TINGGI = 800, 600
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Simulasi Jatuh Bebas & Pantulan")
jam = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)

# Warna (R, G, B)
PUTIH = (255, 255, 255)
HITAM = (20, 20, 20)
BIRU_LANGIT = (135, 206, 235)
HIJAU = (60, 160, 70)
MERAH = (220, 50, 50)

# ---------------------------------------------------------------
# 2. KONSTANTA FISIKA
# ---------------------------------------------------------------
g = 9.8             # percepatan gravitasi (m/s^2)
e = 0.8             # koefisien restitusi (0 = tidak memantul, 1 = pantulan sempurna)
SKALA = 50          # 1 meter = 50 piksel
RADIUS = 20         # jari-jari bola (piksel)
TANAH_Y = 560       # posisi tanah di layar (piksel)
BATAS_BERHENTI = 0.5  # jika kecepatan pantul < 0.5 m/s, bola dianggap berhenti

# ---------------------------------------------------------------
# 3. KONDISI AWAL
# ---------------------------------------------------------------
H_AWAL = 10.0       # ketinggian awal (meter)
x = LEBAR // 2      # posisi horizontal bola (piksel)
h = H_AWAL          # ketinggian dasar bola dari tanah (meter)
v = 0.0             # kecepatan (m/s), positif = ke atas
jumlah_pantulan = 0
berhenti = False


def reset(tinggi, posisi_x):
    """Mengembalikan bola ke kondisi awal."""
    global h, v, x, jumlah_pantulan, berhenti
    h = tinggi
    v = 0.0
    x = posisi_x
    jumlah_pantulan = 0
    berhenti = False


# ---------------------------------------------------------------
# 4. LOOP UTAMA PROGRAM
# ---------------------------------------------------------------
berjalan = True
while berjalan:
    dt = jam.tick(60) / 1000.0   # selang waktu antar frame (detik)

    # --- a. Membaca input pengguna ---
    for kejadian in pygame.event.get():
        if kejadian.type == pygame.QUIT:
            berjalan = False
        elif kejadian.type == pygame.MOUSEBUTTONDOWN:
            mx, my = kejadian.pos
            tinggi_klik = (TANAH_Y - RADIUS - my) / SKALA   # ubah piksel ke meter
            tinggi_klik = max(tinggi_klik, 0.5)
            reset(tinggi_klik, mx)
        elif kejadian.type == pygame.KEYDOWN:
            if kejadian.key == pygame.K_ESCAPE:
                berjalan = False
            elif kejadian.key == pygame.K_SPACE:
                reset(H_AWAL, LEBAR // 2)
            elif kejadian.key == pygame.K_UP:
                e = min(1.0, round(e + 0.1, 1))
            elif kejadian.key == pygame.K_DOWN:
                e = max(0.0, round(e - 0.1, 1))
            elif kejadian.key == pygame.K_RIGHT:
                g = round(g + 1.0, 1)
            elif kejadian.key == pygame.K_LEFT:
                g = max(1.0, round(g - 1.0, 1))

    # --- b. Menghitung fisika ---
    if not berhenti:
        v = v - g * dt          # kecepatan berubah karena gravitasi
        h = h + v * dt          # posisi berubah karena kecepatan

        if h <= 0:              # bola menyentuh tanah
            h = 0
            v = -e * v          # kecepatan dibalik dan dikalikan e
            jumlah_pantulan += 1
            if v < BATAS_BERHENTI:   # pantulan terlalu kecil -> berhenti
                v = 0
                berhenti = True

    # --- c. Menggambar ke layar ---
    layar.fill(BIRU_LANGIT)
    pygame.draw.rect(layar, HIJAU, (0, TANAH_Y, LEBAR, TINGGI - TANAH_Y))

    y_layar = TANAH_Y - h * SKALA - RADIUS   # ubah meter ke piksel (pusat bola)
    pygame.draw.circle(layar, MERAH, (int(x), int(y_layar)), RADIUS)
    pygame.draw.circle(layar, HITAM, (int(x), int(y_layar)), RADIUS, 2)

    teks = [
        f"Ketinggian : {h:6.2f} m",
        f"Kecepatan  : {v:6.2f} m/s",
        f"Gravitasi g: {g:.1f} m/s^2",
        f"Restitusi e: {e:.1f}",
        f"Pantulan   : {jumlah_pantulan}",
        "Klik = jatuhkan | SPASI = reset | Atas/Bawah = e | Kiri/Kanan = g",
    ]
    for i, baris in enumerate(teks):
        layar.blit(font.render(baris, True, HITAM), (10, 10 + i * 24))

    pygame.display.flip()

pygame.quit()
sys.exit()