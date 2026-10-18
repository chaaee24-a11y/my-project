"""
====================================================================
PERMAINAN BOLA BALING TAHUN 5: KEMAHIRAN MENGHANTAR & MENERIMA BOLA
Pendidikan Jasmani & Kesihatan (PJK) KSSR Semakan Sekolah Rendah
====================================================================
Panduan Menjalankan:
1. Pastikan Python dipasang (https://www.python.org)
2. Pasang modul pygame di terminal/command prompt:
      pip install pygame
3. Jalankan permainan:
      python game_bola_baling.py
====================================================================
Kawalan Permainan:
- [PANDU / GERAK]: Kekunci Panah KIRI / KANAN atau [A] / [D]
- [PILIH HANTARAN]:
    [1] - Hantaran Aras Dada (Pantas, lurus melepasi ruang terbuka)
    [2] - Hantaran Atas Bahu (Kuat & laju)
    [3] - Hantaran Lantul (Memantul di lantai melepasi pertahanan tinggi)
    [4] - Hantaran Atas Kepala / Lob (Melengkung melepasi halangan rapat)
- [HANTAR / SERAP DAYA]: Kekunci [SPACE] (Ruang bar)
====================================================================
"""

import math
import random
import sys
import time

try:
    import pygame
except ImportError:
    print("\n[PERHATIAN] Modul 'pygame' belum dipasang.")
    print("Sila pasang menggunakan arahan:")
    print("   pip install pygame\n")
    print("Menutup permainan...")
    sys.exit()

# Inisialisasi Pygame
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except Exception:
    pass

# Tetapan Skrin
LEBAR_SKRIN = 900
TINGGI_SKRIN = 650
SKRIN = pygame.display.set_mode((LEBAR_SKRIN, TINGGI_SKRIN))
pygame.display.set_caption("Juara Bola Baling Tahun 5: Kemahiran Hantar & Terima")
JAM = pygame.time.Clock()
FPS = 60

# Warna Rasmi Gelanggang & Tema
WARNA_PADANG = (36, 110, 160)       # Lantai Gelanggang Biru Indoor
WARNA_KAWASAN_GOL = (230, 126, 34)   # Kawasan D Kuning-Jingga
WARNA_GARISAN = (255, 255, 255)
WARNA_KUNING_GARIS = (241, 196, 15)
WARNA_TEKS_GELAP = (30, 39, 46)
WARNA_TEKS_TERANG = (245, 246, 250)
WARNA_PEMAIN = (46, 204, 113)       # Hijau Pasukan Kita
WARNA_RAKAN = (52, 152, 219)        # Biru Rakan Sepasukan
WARNA_PERTAHANAN = (231, 76, 60)    # Merah Pasukan Lawan
WARNA_BOLA = (243, 156, 18)         # Jingga Bola Baling
WARNA_PANEL = (20, 30, 45)

# Fon Tulisan
def dapatkan_fon(saiz, tebal=False):
    try:
        return pygame.font.SysFont("Comic Sans MS", saiz, bold=tebal)
    except Exception:
        return pygame.font.SysFont("Arial", saiz, bold=tebal)

FON_BESAR = dapatkan_fon(38, True)
FON_SEDERHANA = dapatkan_fon(24, True)
FON_KECIL = dapatkan_fon(18)
FON_MIKRO = dapatkan_fon(15)

# Penjana Bunyi Sintetik Mudah (Mengelakkan kebergantungan fail audio luar)
def cipta_bunyi(frekuensi, durasi, jenis="sine"):
    try:
        sampel_kadar = 22050
        n_sampel = int(sampel_kadar * durasi)
        penimbal = bytearray()
        for i in range(n_sampel):
            t = float(i) / sampel_kadar
            if jenis == "sine":
                val = int(127.5 * (1 + math.sin(2 * math.pi * frekuensi * t)))
            elif jenis == "square":
                val = 220 if math.sin(2 * math.pi * frekuensi * t) > 0 else 30
            else:
                val = random.randint(50, 200)
            # Fade out
            val = int(val * (1.0 - (i / n_sampel)))
            penimbal.append(min(255, max(0, val)))
        return pygame.mixer.Sound(buffer=bytes(penimbal))
    except Exception:
        return None

BUNYI_HANTAR = cipta_bunyi(520, 0.12, "sine")
BUNYI_TANGKAP = cipta_bunyi(740, 0.15, "sine")
BUNYI_PINTAS = cipta_bunyi(180, 0.25, "square")
BUNYI_WISIL = cipta_bunyi(1100, 0.35, "sine")

def mainkan_bunyi(snd):
    if snd:
        try:
            snd.play()
        except Exception:
            pass

# Maklumat Jenis Hantaran PJK Tahun 5
JENIS_HANTARAN = {
    1: {
        "nama": "Hantaran Aras Dada",
        "penerangan": "Tolakan kuat dari dada, pantas & tepat ke dada rakan.",
        "kelajuan": 9,
        "ketinggian": 1,
        "lantulan": False,
        "kelebihan": "Pantas melepasi ruang terbuka jarak sederhana."
    },
    2: {
        "nama": "Hantaran Atas Bahu",
        "penerangan": "Tolak dari atas bahu menggunakan pergelangan tangan.",
        "kelajuan": 12,
        "ketinggian": 2,
        "lantulan": False,
        "kelebihan": "Hantaran paling kuat untuk jarak jauh & serangan pantas."
    },
    3: {
        "nama": "Hantaran Lantul",
        "penerangan": "Bola dilantun 2/3 perjalanan ke arah rakan.",
        "kelajuan": 8,
        "ketinggian": 0,
        "lantulan": True,
        "kelebihan": "Mudah mengelirukan penghadang lawan yang tinggi!"
    },
    4: {
        "nama": "Hantaran Atas Kepala (Lob)",
        "penerangan": "Kedua-dua tangan melepaskan bola tinggi di atas kepala.",
        "kelajuan": 7,
        "ketinggian": 3,
        "lantulan": False,
        "kelebihan": "Melengkung melepasi lawan yang menghadang rapat."
    }
}

TIPS_PJK = [
    "Tip PJK Tahun 5: Gunakan kedua-dua belah tangan membentuk huruf 'W' semasa menerima bola!",
    "Tip PJK Tahun 5: Bengkokkan siku ke arah dada untuk menyerap daya momentum bola.",
    "Tip PJK Tahun 5: Hantaran Lantul sesuai jika penghadang lawan berdiri tegak & mendepang tangan.",
    "Tip PJK Tahun 5: Bergerak ke hadapan menyambut bola, jangan tunggu bola sampai setempat!",
    "Tip PJK Tahun 5: Mata sentiasa fokus memandang arah pergerakan bola yang melayang."
]

class Pemain:
    def __init__(self, x, y, warna, label="Anda"):
        self.x = x
        self.y = y
        self.warna = warna
        self.label = label
        self.jejari = 22
        self.kelajuan = 5
        self.sedang_serap_daya = False
        self.pemasa_serap_daya = 0

    def gerak(self, dx):
        self.x += dx * self.kelajuan
        self.x = max(60, min(LEBAR_SKRIN - 60, self.x))

    def aktifkan_serap_daya(self):
        self.sedang_serap_daya = True
        self.pemasa_serap_daya = 25  # bingkai aktif

    def kemas_kini(self):
        if self.pemasa_serap_daya > 0:
            self.pemasa_serap_daya -= 1
        else:
            self.sedang_serap_daya = False

    def lukis(self, permukaan):
        # Efek visual serap daya (lingkaran penyerapan daya)
        if self.sedang_serap_daya:
            radius_efek = self.jejari + 14 + int(math.sin(pygame.time.get_ticks() * 0.02) * 4)
            pygame.draw.circle(permukaan, (241, 196, 15), (int(self.x), int(self.y)), radius_efek, 3)

        # Bayang
        pygame.draw.ellipse(permukaan, (20, 20, 20, 80), (self.x - 18, self.y + 16, 36, 14))

        # Badan pemain
        pygame.draw.circle(permukaan, self.warna, (int(self.x), int(self.y)), self.jejari)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(self.y)), self.jejari, 3)

        # Kepala & tangan (simbol posisi tangan 'W')
        pygame.draw.circle(permukaan, (253, 227, 167), (int(self.x), int(self.y - 4)), 10)
        
        # Penunjuk posisi 'W' serap daya di depan badan
        warna_tangan = (255, 255, 255) if not self.sedang_serap_daya else (241, 196, 15)
        pygame.draw.line(permukaan, warna_tangan, (self.x - 12, self.y - 12), (self.x - 6, self.y - 18), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x - 6, self.y - 18), (self.x, self.y - 14), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x, self.y - 14), (self.x + 6, self.y - 18), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x + 6, self.y - 18), (self.x + 12, self.y - 12), 3)

        # Teks label
        teks = FON_MIKRO.render(self.label, True, WARNA_TEKS_TERANG)
        permukaan.blit(teks, (self.x - teks.get_width() // 2, self.y + self.jejari + 4))

class PenghadangLawan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jejari = 20
        self.kelajuan = 2.8
        self.arah = random.choice([-1, 1])
        self.tinggi_hadangan = random.choice(["tinggi", "rendah", "normal"])
        self.masa_tukar_postur = 0

    def kemas_kini(self):
        self.x += self.arah * self.kelajuan
        if self.x < 150:
            self.x = 150
            self.arah = 1
        elif self.x > LEBAR_SKRIN - 150:
            self.x = LEBAR_SKRIN - 150
            self.arah = -1

        self.masa_tukar_postur += 1
        if self.masa_tukar_postur > 180:
            self.masa_tukar_postur = 0
            self.tinggi_hadangan = random.choice(["tinggi", "rendah", "normal"])

    def lukis(self, permukaan):
        # Bayang
        pygame.draw.ellipse(permukaan, (20, 20, 20, 80), (self.x - 18, self.y + 14, 36, 12))

        # Badan
        pygame.draw.circle(permukaan, WARNA_PERTAHANAN, (int(self.x), int(self.y)), self.jejari)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(self.y)), self.jejari, 3)

        # Tangan depang mengikut postur hadangan
        if self.tinggi_hadangan == "tinggi":
            # Tangan angkat tinggi ke atas (Lawan mudah diatasi dengan hantaran lantul!)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 18, self.y - 10), (self.x - 22, self.y - 30), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 18, self.y - 10), (self.x + 22, self.y - 30), 4)
            label = "Hadang Tinggi (Lantul!)"
            warna_label = (255, 235, 59)
        elif self.tinggi_hadangan == "rendah":
            # Tangan mendatar rendah (Sesuai lepasi dengan Atas Kepala / Dada laju)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 14, self.y + 6), (self.x - 28, self.y + 10), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 14, self.y + 6), (self.x + 28, self.y + 10), 4)
            label = "Hadang Rendah (Atas Bahu/Lob)"
            warna_label = (129, 236, 236)
        else:
            # Normal
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 16, self.y - 5), (self.x - 26, self.y - 5), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 16, self.y - 5), (self.x + 26, self.y - 5), 4)
            label = "Penghadang Lawan"
            warna_label = (255, 177, 166)

        teks = FON_MIKRO.render(label, True, warna_label)
        permukaan.blit(teks, (self.x - teks.get_width() // 2, self.y - 38))

class Bola:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sasaran_x = x
        self.sasaran_y = y
        self.bergerak = False
        self.arah_kembali = False  # True jika bola sedang dipulangkan oleh rakan
        self.jenis_hantaran = 1
        self.jejari_asas = 10
        self.jejari_semasa = 10
        self.progres = 0.0
        self.mula_x = x
        self.mula_y = y
        self.jarak_keseluruhan = 1
        self.kelajuan = 0.02
        self.lantunan_tercapai = False

    def lancar(self, dari_x, dari_y, ke_x, ke_y, jenis, kembali=False):
        self.mula_x = dari_x
        self.mula_y = dari_y
        self.x = dari_x
        self.y = dari_y
        self.sasaran_x = ke_x
        self.sasaran_y = ke_y
        self.jenis_hantaran = jenis
        self.arah_kembali = kembali
        self.bergerak = True
        self.progres = 0.0
        self.lantunan_tercapai = False

        dx = ke_x - dari_x
        dy = ke_y - dari_y
        self.jarak_keseluruhan = max(1, math.hypot(dx, dy))

        spd = JENIS_HANTARAN[jenis]["kelajuan"] if not kembali else 9
        self.kelajuan = spd / self.jarak_keseluruhan

    def kemas_kini(self):
        if not self.bergerak:
            return

        self.progres += self.kelajuan

        if self.progres >= 1.0:
            self.progres = 1.0
            self.x = self.sasaran_x
            self.y = self.sasaran_y
            self.bergerak = False
            return

        # Interpolasi kedudukan
        self.x = self.mula_x + (self.sasaran_x - self.mula_x) * self.progres
        self.y = self.mula_y + (self.sasaran_y - self.mula_y) * self.progres

        # Efek visual ketinggian 3D (Aras dada, bahu, lantul, lob)
        maklumat = JENIS_HANTARAN[self.jenis_hantaran]
        if maklumat["lantulan"]:
            # Melantun pada 60% perjalanan
            if self.progres < 0.6:
                arc = math.sin((self.progres / 0.6) * math.pi) * 6
                self.jejari_semasa = self.jejari_asas + int(arc)
            else:
                arc = math.sin(((self.progres - 0.6) / 0.4) * math.pi) * 8
                self.jejari_semasa = self.jejari_asas + int(arc)
        elif maklumat["ketinggian"] == 3:  # Lob / Atas kepala
            arc = math.sin(self.progres * math.pi) * 20
            self.jejari_semasa = self.jejari_asas + int(arc)
        elif maklumat["ketinggian"] == 2:  # Atas bahu
            arc = math.sin(self.progres * math.pi) * 10
            self.jejari_semasa = self.jejari_asas + int(arc)
        else:  # Dada
            arc = math.sin(self.progres * math.pi) * 4
            self.jejari_semasa = self.jejari_asas + int(arc)

    def lukis(self, permukaan):
        if not self.bergerak:
            return

        # Bayang di atas lantai
        tinggi_bayang = (self.jejari_semasa - self.jejari_asas) * 1.5
        pygame.draw.ellipse(
            permukaan, (20, 20, 20, 100),
            (self.x - self.jejari_asas, self.y + tinggi_bayang, self.jejari_asas * 2, 8)
        )

        # Bola
        pos_y_fizikal = self.y - (self.jejari_semasa - self.jejari_asas)
        pygame.draw.circle(permukaan, WARNA_BOLA, (int(self.x), int(pos_y_fizikal)), self.jejari_semasa)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(pos_y_fizikal)), self.jejari_semasa, 2)
        
        # Corak jalur bola baling
        pygame.draw.arc(
            permukaan, (230, 81, 0),
            (int(self.x - self.jejari_semasa * 0.8), int(pos_y_fizikal - self.jejari_semasa * 0.8),
             int(self.jejari_semasa * 1.6), int(self.jejari_semasa * 1.6)),
            0, math.pi, 2
        )

class Gelanggang:
    @staticmethod
    def lukis(permukaan):
        # Latar Belakang Gelanggang Bola Baling (Dewan Sukan Sekolah)
        permukaan.fill(WARNA_PADANG)

        # Corak Jalur Kayu/Lantai Gelanggang
        for y in range(80, TINGGI_SKRIN - 90, 40):
            pygame.draw.line(permukaan, (41, 128, 185), (30, y), (LEBAR_SKRIN - 30, y), 1)

        # Garisan Tepi Gelanggang
        pygame.draw.rect(permukaan, WARNA_GARISAN, (30, 75, LEBAR_SKRIN - 60, TINGGI_SKRIN - 165), 4)

        # Garisan Tengah (Center line)
        tengah_y = (75 + TINGGI_SKRIN - 90) // 2
        pygame.draw.line(permukaan, WARNA_GARISAN, (30, tengah_y), (LEBAR_SKRIN - 30, tengah_y), 3)
        pygame.draw.circle(permukaan, WARNA_GARISAN, (LEBAR_SKRIN // 2, tengah_y), 45, 3)

        # Kawasan D Gol Atas (Garisan 6 Meter Gol Lawan)
        pygame.draw.arc(permukaan, WARNA_KAWASAN_GOL, (LEBAR_SKRIN // 2 - 130, 40, 260, 90), 0, math.pi, 4)
        # Garisan 9 Meter Balingan Percuma (Putus-putus)
        for sudut in range(10, 170, 20):
            rad1 = math.radians(sudut)
            rad2 = math.radians(sudut + 10)
            p1 = (LEBAR_SKRIN // 2 + int(160 * math.cos(rad1)), 80 + int(90 * math.sin(rad1)))
            p2 = (LEBAR_SKRIN // 2 + int(160 * math.cos(rad2)), 80 + int(90 * math.sin(rad2)))
            pygame.draw.line(permukaan, WARNA_KUNING_GARIS, p1, p2, 3)

        # Kawasan D Bawah (Kawasan Pasukan Anda)
        bawah_y = TINGGI_SKRIN - 90
        pygame.draw.arc(permukaan, WARNA_KAWASAN_GOL, (LEBAR_SKRIN // 2 - 140, bawah_y - 70, 280, 90), math.pi, 2 * math.pi, 4)

        # Tiang Gol Visual
        pygame.draw.rect(permukaan, (255, 255, 255), (LEBAR_SKRIN // 2 - 70, 60, 140, 15))
        pygame.draw.rect(permukaan, (192, 57, 43), (LEBAR_SKRIN // 2 - 70, 60, 140, 15), 3)

# ----------------- KELAS UTAMA PERMAINAN -----------------
class PermainanBolaBaling:
    def __init__(self):
        self.keadaan = "MENU"  # MENU, BERMAIN, SELESAI
        self.skor = 0
        self.streak = 0
        self.hantaran_berjaya = 0
        self.tangkapan_sempurna = 0
        self.bola_terlepas = 0
        self.masa_tinggal = 60  # saat
        self.masa_mula = 0

        self.jenis_pilihan = 1  # 1: Dada, 2: Bahu, 3: Lantul, 4: Lob
        self.pemain = Pemain(LEBAR_SKRIN // 2, 490, WARNA_PEMAIN, "Murid (Anda)")
        self.rakan = Pemain(LEBAR_SKRIN // 2, 130, WARNA_RAKAN, "Rakan Penerima")
        self.penghadang = PenghadangLawan(LEBAR_SKRIN // 2, 310)
        self.bola = Bola(self.pemain.x, self.pemain.y)

        self.memegang_bola = True  # True: pemain pegang bola, False: bola di udara/rakan
        self.mesej_maklum_balas = "Pilih jenis hantaran (1-4) & tekan SPACE untuk hantar!"
        self.warna_maklum_balas = (255, 255, 255)
        self.masa_maklum_balas = 0
        self.tip_semasa = random.choice(TIPS_PJK)
        self.pemasa_tip = 0

    def mula_baru(self):
        self.keadaan = "BERMAIN"
        self.skor = 0
        self.streak = 0
        self.hantaran_berjaya = 0
        self.tangkapan_sempurna = 0
        self.bola_terlepas = 0
        self.masa_tinggal = 60
        self.masa_mula = time.time()
        self.memegang_bola = True
        self.jenis_pilihan = 1
        self.pemain.x = LEBAR_SKRIN // 2
        self.rakan.x = LEBAR_SKRIN // 2
        self.penghadang.x = LEBAR_SKRIN // 2
        self.beri_maklum_balas("Perlawanan bermula! Lakukan hantaran yang tepat!", (46, 204, 113))
        mainkan_bunyi(BUNYI_WISIL)

    def beri_maklum_balas(self, teks, warna=(255, 255, 255)):
        self.mesej_maklum_balas = teks
        self.warna_maklum_balas = warna
        self.masa_maklum_balas = 120

    def proses_input(self):
        kekunci = pygame.key.get_pressed()

        for peristiwa in pygame.event.get():
            if peristiwa.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if peristiwa.type == pygame.KEYDOWN:
                if self.keadaan == "MENU":
                    if peristiwa.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.mula_baru()
                elif self.keadaan == "SELESAI":
                    if peristiwa.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.mula_baru()
                elif self.keadaan == "BERMAIN":
                    # Tukar mod hantaran
                    if peristiwa.key == pygame.K_1:
                        self.jenis_pilihan = 1
                        self.beri_maklum_balas("Mod: Hantaran Aras Dada dipilih!", (241, 196, 15))
                    elif peristiwa.key == pygame.K_2:
                        self.jenis_pilihan = 2
                        self.beri_maklum_balas("Mod: Hantaran Atas Bahu dipilih!", (241, 196, 15))
                    elif peristiwa.key == pygame.K_3:
                        self.jenis_pilihan = 3
                        self.beri_maklum_balas("Mod: Hantaran Lantul dipilih!", (241, 196, 15))
                    elif peristiwa.key == pygame.K_4:
                        self.jenis_pilihan = 4
                        self.beri_maklum_balas("Mod: Hantaran Atas Kepala (Lob) dipilih!", (241, 196, 15))

                    # Tekan SPACE untuk menghantar ATAU menyerap daya (tangkapan)
                    elif peristiwa.key == pygame.K_SPACE:
                        if self.memegang_bola and not self.bola.bergerak:
                            # Hantar bola kepada rakan
                            self.memegang_bola = False
                            self.bola.lancar(
                                self.pemain.x, self.pemain.y - 10,
                                self.rakan.x, self.rakan.y + 10,
                                self.jenis_pilihan, kembali=False
                            )
                            mainkan_bunyi(BUNYI_HANTAR)
                        elif not self.memegang_bola and self.bola.arah_kembali:
                            # Aktifkan lakuan 'serap daya' ketika bola menghampiri
                            self.pemain.aktifkan_serap_daya()

        if self.keadaan == "BERMAIN":
            dx = 0
            if kekunci[pygame.K_LEFT] or kekunci[pygame.K_a]:
                dx -= 1
            if kekunci[pygame.K_RIGHT] or kekunci[pygame.K_d]:
                dx += 1
            if dx != 0:
                self.pemain.gerak(dx)

    def logik_permainan(self):
        if self.keadaan != "BERMAIN":
            return

        # Kira baki masa
        masa_lalu = int(time.time() - self.mula_mula)
        self.masa_tinggal = max(0, 60 - masa_lalu)
        if self.masa_tinggal <= 0:
            self.keadaan = "SELESAI"
            mainkan_bunyi(BUNYI_WISIL)
            return

        # Kemas kini pemain & penghadang lawan
        self.pemain.kemas_kini()
        self.penghadang.kemas_kini()

        # Rakan penerima bergerak sedikit mencari ruang terbuka
        sasaran_rakan_x = self.pemain.x + math.sin(pygame.time.get_ticks() * 0.003) * 140
        self.rakan.x += (sasaran_rakan_x - self.rakan.x) * 0.05
        self.rakan.x = max(100, min(LEBAR_SKRIN - 100, self.rakan.x))

        # Tip berkala
        self.pemasa_tip += 1
        if self.pemasa_tip > 350:
            self.pemasa_tip = 0
            self.tip_semasa = random.choice(TIPS_PJK)

        if self.masa_maklum_balas > 0:
            self.masa_maklum_balas -= 1

        # Jika sedang memegang bola, bola kekal di tangan pemain
        if self.memegang_bola and not self.bola.bergerak:
            self.bola.x = self.pemain.x
            self.bola.y = self.pemain.y - 12
            return

        # Kemas kini kedudukan bola di udara
        self.bola.kemas_kini()

        # 1. PERIKSA HADANGAN LAWAN SEMASA BOLA MENUJU KE RAKAN
        if self.bola.bergerak and not self.bola.arah_kembali:
            jarak_ke_lawan = math.hypot(self.bola.x - self.penghadang.x, self.bola.y - self.penghadang.y)
            
            # Jika bola dekat dengan penghadang lawan
            if jarak_ke_lawan < 36:
                kena_hadang = False
                postur = self.penghadang.tinggi_hadangan

                # Analisis taktikal jenis hantaran vs postur penghadang (Konsep PJK Tahun 5):
                if self.bola.jenis_hantaran == 1:  # Dada
                    kena_hadang = True
                    sebab = "Hantaran aras dada terhalang! Lawan berada tepat di laluan."
                elif self.bola.jenis_hantaran == 2:  # Bahu laju
                    if postur == "tinggi" or abs(self.bola.x - self.penghadang.x) < 18:
                        kena_hadang = True
                        sebab = "Hantaran atas bahu dipintas pertahanan lawan!"
                elif self.bola.jenis_hantaran == 3:  # Lantul
                    # Lantul melepasi jika lawan hadang tinggi, tapi terperangkap jika lawan hadang rendah
                    if postur == "rendah":
                        kena_hadang = True
                        sebab = "Hantaran lantul terkena kaki penghadang yang membongkok!"
                    else:
                        kena_hadang = False  # Berjaya melepasi hadangan tinggi!
                elif self.bola.jenis_hantaran == 4:  # Atas kepala (Lob)
                    # Lob melepasi kecuali jika lawan melompat tinggi tepat pada jarak
                    if postur == "tinggi" and jarak_ke_lawan < 15:
                        kena_hadang = True
                        sebab = "Lawan melonjak tinggi menyekat bola atas kepala!"

                if kena_hadang:
                    mainkan_bunyi(BUNYI_PINTAS)
                    self.streak = 0
                    self.skor = max(0, self.skor - 5)
                    self.bola_terlepas += 1
                    self.beri_maklum_balas(sebab, (231, 76, 60))
                    # Pulangkan bola ke tangan pemain semula selepas terlepas
                    self.memegang_bola = True
                    self.bola.bergerak = False
                    return

            # Sampai kepada rakan penerima
            if not self.bola.bergerak:
                self.hantaran_berjaya += 1
                self.skor += 10
                self.streak += 1
                mainkan_bunyi(BUNYI_TANGKAP)
                self.beri_maklum_balas("Hantaran kemas! Rakan menyambut bola. Bersedia menerima!", (46, 204, 113))

                # Rakan bersedia hantar semula kepada kita
                self.bola.lancar(
                    self.rakan.x, self.rakan.y + 10,
                    self.pemain.x, self.pemain.y - 10,
                    self.jenis_pilihan, kembali=True
                )

        # 2. PERIKSA TANGKAPAN & SERAP DAYA SEMASA BOLA KEMBALI KEPADA KITA
        elif self.bola.bergerak and self.bola.arah_kembali:
            jarak_ke_pemain = math.hypot(self.bola.x - self.pemain.x, self.bola.y - self.pemain.y)

            # Zon tangkapan aktif
            if jarak_ke_pemain < 40 and not self.bola.bergerak:
                pass  # ditangani di blok bawah apabila tiba

            if not self.bola.bergerak:
                # Bola telah sampai ke posisi pemain. Nilai teknik serap daya!
                if self.pemain.sedang_serap_daya:
                    # Murid melakukan teknik serap daya (menekan SPACE pada masa tepat)!
                    self.tangkapan_sempurna += 1
                    mata_bonus = 15 + (self.streak * 2)
                    self.skor += mata_bonus
                    mainkan_bunyi(BUNYI_TANGKAP)
                    self.beri_maklum_balas(f"SEMPURNA! Lakuan Serap Daya Tangan 'W' (+{mata_bonus} Mata)", (241, 196, 15))
                else:
                    # Tangkapan biasa tanpa serap daya
                    self.skor += 5
                    mainkan_bunyi(BUNYI_TANGKAP)
                    self.beri_maklum_balas("Bola diterima. (Tip: Tekan SPACE semasa bola sampai untuk SERAP DAYA!)", (255, 235, 59))

                self.memegang_bola = True

    def lukis_panel_status(self):
        # Bar Atas (Header Status)
        pygame.draw.rect(SKRIN, WARNA_PANEL, (0, 0, LEBAR_SKRIN, 70))
        pygame.draw.line(SKRIN, (50, 70, 95), (0, 70), (LEBAR_SKRIN, 70), 2)

        # Skor & Streak
        teks_skor = FON_SEDERHANA.render(f"SKOR: {self.skor}", True, (241, 196, 15))
        SKRIN.blit(teks_skor, (25, 12))

        teks_streak = FON_MIKRO.render(f"KOMBO: {self.streak}x | SEMPURNA: {self.tangkapan_sempurna}", True, (46, 204, 113))
        SKRIN.blit(teks_streak, (25, 42))

        # Pemasa
        warna_masa = (231, 76, 60) if self.masa_tinggal <= 10 else (245, 246, 250)
        teks_masa = FON_BESAR.render(f"{self.masa_tinggal}s", True, warna_masa)
        SKRIN.blit(teks_masa, (LEBAR_SKRIN // 2 - teks_masa.get_width() // 2, 8))
        teks_label_masa = FON_MIKRO.render("MASA PERLAWANAN", True, (180, 190, 205))
        SKRIN.blit(teks_label_masa, (LEBAR_SKRIN // 2 - teks_label_masa.get_width() // 2, 46))

        # Pemilihan Jenis Hantaran Semasa
        nama_pilihan = JENIS_HANTARAN[self.jenis_pilihan]["nama"]
        teks_hantar = FON_SEDERHANA.render(f"[{self.jenis_pilihan}] {nama_pilihan}", True, (52, 152, 219))
        SKRIN.blit(teks_hantar, (LEBAR_SKRIN - teks_hantar.get_width() - 25, 12))

        teks_pilih_arahan = FON_MIKRO.render("Tukar Hantaran: Tekan Kekunci [1, 2, 3, 4]", True, (200, 210, 225))
        SKRIN.blit(teks_pilih_arahan, (LEBAR_SKRIN - teks_pilih_arahan.get_width() - 25, 42))

        # Bar Bawah (Panduan & Maklum Balas)
        bar_bawah_y = TINGGI_SKRIN - 80
        pygame.draw.rect(SKRIN, WARNA_PANEL, (0, bar_bawah_y, LEBAR_SKRIN, 80))
        pygame.draw.line(SKRIN, (50, 70, 95), (0, bar_bawah_y), (LEBAR_SKRIN, bar_bawah_y), 2)

        # Mesej Maklum Balas Dinamik
        teks_mb = FON_SEDERHANA.render(self.mesej_maklum_balas, True, self.warna_maklum_balas)
        SKRIN.blit(teks_mb, (LEBAR_SKRIN // 2 - teks_mb.get_width() // 2, bar_bawah_y + 8))

        # Tip PJK
        teks_tip = FON_MIKRO.render(self.tip_semasa, True, (241, 196, 15))
        SKRIN.blit(teks_tip, (LEBAR_SKRIN // 2 - teks_tip.get_width() // 2, bar_bawah_y + 45))

    def lukis_menu(self):
        # Latar Belakang Separuh Lutsinar
        lapisan = pygame.Surface((LEBAR_SKRIN, TINGGI_SKRIN), pygame.SRCALPHA)
        lapisan.fill((15, 25, 40, 235))
        SKRIN.blit(lapisan, (0, 0))

        kotak = pygame.Rect(80, 50, LEBAR_SKRIN - 160, TINGGI_SKRIN - 100)
        pygame.draw.rect(SKRIN, (25, 38, 55), kotak, border_radius=18)
        pygame.draw.rect(SKRIN, (241, 196, 15), kotak, 4, border_radius=18)

        tajuk = FON_BESAR.render("CABARAN BOLA BALING TAHUN 5", True, (241, 196, 15))
        SKRIN.blit(tajuk, (LEBAR_SKRIN // 2 - tajuk.get_width() // 2, 80))

        sub = FON_SEDERHANA.render("Kemahiran Asas: Menghantar dan Menerima Bola (KSSR)", True, (236, 240, 241))
        SKRIN.blit(sub, (LEBAR_SKRIN // 2 - sub.get_width() // 2, 130))

        # Arahan 4 Jenis Hantaran
        y_pos = 185
        senarai_panduan = [
            ("[1] Hantaran Aras Dada", "Tolak bola paras dada. Sesuai untuk hantaran pantas & jarak dekat."),
            ("[2] Hantaran Atas Bahu", "Hantaran paling kuat untuk mengatasi jarak jauh atau larian pantas."),
            ("[3] Hantaran Lantul", "Lantun bola ke lantai untuk mengelirukan penghadang lawan yang tinggi!"),
            ("[4] Hantaran Atas Kepala", "Hantaran melengkung melepasi pertahanan yang mengawal ketat.")
        ]
        for nama, huraian in senarai_panduan:
            t_nama = FON_SEDERHANA.render(nama, True, (52, 152, 219))
            SKRIN.blit(t_nama, (120, y_pos))
            t_hur = FON_KECIL.render(huraian, True, (200, 214, 229))
            SKRIN.blit(t_hur, (140, y_pos + 26))
            y_pos += 56

        # Panduan Menerima
        t_terima = FON_SEDERHANA.render("Kemahiran Menerima Bola (Serap Daya):", True, (46, 204, 113))
        SKRIN.blit(t_terima, (120, y_pos + 8))
        t_terima_desc = FON_KECIL.render("Tekan [SPACE] tepat ketika bola sampai untuk serap daya dengan tangan 'W'!", True, (255, 235, 59))
        SKRIN.blit(t_terima_desc, (140, y_pos + 36))

        # Butang Mula
        butang_rect = pygame.Rect(LEBAR_SKRIN // 2 - 180, TINGGI_SKRIN - 140, 360, 50)
        pygame.draw.rect(SKRIN, (46, 204, 113), butang_rect, border_radius=12)
        pygame.draw.rect(SKRIN, (255, 255, 255), butang_rect, 2, border_radius=12)
        teks_mula = FON_SEDERHANA.render("TEKAN [SPACE] UNTUK MULA", True, (20, 30, 45))
        SKRIN.blit(teks_mula, (LEBAR_SKRIN // 2 - teks_mula.get_width() // 2, TINGGI_SKRIN - 128))

    def lukis_selesai(self):
        lapisan = pygame.Surface((LEBAR_SKRIN, TINGGI_SKRIN), pygame.SRCALPHA)
        lapisan.fill((15, 25, 40, 240))
        SKRIN.blit(lapisan, (0, 0))

        kotak = pygame.Rect(120, 80, LEBAR_SKRIN - 240, TINGGI_SKRIN - 160)
        pygame.draw.rect(SKRIN, (25, 38, 55), kotak, border_radius=18)
        pygame.draw.rect(SKRIN, (46, 204, 113), kotak, 4, border_radius=18)

        tajuk = FON_BESAR.render("TAMAT MASA PERLAWANAN!", True, (241, 196, 15))
        SKRIN.blit(tajuk, (LEBAR_SKRIN // 2 - tajuk.get_width() // 2, 110))

        # Gred Pencapaian
        if self.skor >= 200:
            gred = "Cemerlang (Tahap Penguasaan 6 / Bintang 3) ★★★"
            warna_gred = (46, 204, 113)
        elif self.skor >= 100:
            gred = "Sangat Baik (Tahap Penguasaan 4-5 / Bintang 2) ★★☆"
            warna_gred = (52, 152, 219)
        else:
            gred = "Boleh Dipertingkatkan (Bintang 1) ★☆☆"
            warna_gred = (241, 196, 15)

        t_gred = FON_SEDERHANA.render(gred, True, warna_gred)
        SKRIN.blit(t_gred, (LEBAR_SKRIN // 2 - t_gred.get_width() // 2, 170))

        # Statistik
        baris_stat = [
            f"Jumlah Skor Keseluruhan: {self.skor} Mata",
            f"Hantaran Berjaya: {self.hantaran_berjaya} kali",
            f"Tangkapan Sempurna (Serap Daya 'W'): {self.tangkapan_sempurna} kali",
            f"Bola Dipintas Lawan: {self.bola_terlepas} kali"
        ]
        y_s = 230
        for s in baris_stat:
            t = FON_SEDERHANA.render(s, True, (245, 246, 250))
            SKRIN.blit(t, (LEBAR_SKRIN // 2 - t.get_width() // 2, y_s))
            y_s += 42

        # Butang Main Semula
        butang = pygame.Rect(LEBAR_SKRIN // 2 - 180, TINGGI_SKRIN - 180, 360, 48)
        pygame.draw.rect(SKRIN, (52, 152, 219), butang, border_radius=12)
        pygame.draw.rect(SKRIN, (255, 255, 255), butang, 2, border_radius=12)
        teks_ulang = FON_SEDERHANA.render("TEKAN [SPACE] MAIN SEMULA", True, (255, 255, 255))
        SKRIN.blit(teks_ulang, (LEBAR_SKRIN // 2 - teks_ulang.get_width() // 2, TINGGI_SKRIN - 170))

    def lari(self):
        while True:
            self.proses_input()
            self.logik_permainan()

            # Lukis visual
            Gelanggang.lukis(SKRIN)

            if self.keadaan == "BERMAIN":
                self.penghadang.lukis(SKRIN)
                self.rakan.lukis(SKRIN)
                self.pemain.lukis(SKRIN)
                self.bola.lukis(SKRIN)
                self.lukis_panel_status()
            elif self.keadaan == "MENU":
                Gelanggang.lukis(SKRIN)
                self.lukis_menu()
            elif self.keadaan == "SELESAI":
                self.lukis_selesai()

            pygame.display.flip()
            JAM.tick(FPS)

if __name__ == "__main__":
    permainan = PermainanBolaBaling()
    permainan.lari()
