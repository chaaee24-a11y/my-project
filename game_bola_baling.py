"""
====================================================================
YEAR 5 PRIMARY SCHOOL HANDBALL SKILLS GAME: PASSING & RECEIVING
JUARA BOLA BALING TAHUN 5: KEMAHIRAN MENGHANTAR & MENERIMA BOLA
Pendidikan Jasmani & Kesihatan (PJK) KSSR Semakan / Primary School PE
====================================================================
How to Run:
1. Ensure Python 3 is installed (https://www.python.org)
2. Install pygame library:
      pip install pygame
3. Run the game:
      python game_bola_baling.py

(Tip: If you do not have pygame installed, you can also run
 the zero-dependency terminal simulation directly:
      python game_terminal_pjk.py)
====================================================================
Controls / Kawalan:
- [MOVE / GERAK]: Left / Right Arrow Keys or [A] / [D]
- [SELECT PASS / PILIH HANTARAN]:
    [1] - Chest Pass (Hantaran Aras Dada)
    [2] - Shoulder Pass (Hantaran Atas Bahu)
    [3] - Bounce Pass (Hantaran Lantul)
    [4] - Overhead / Lob Pass (Hantaran Atas Kepala)
- [PASS / ABSORB FORCE / HANTAR & SERAP DAYA]: [SPACE] Bar
- [TOGGLE LANGUAGE / TUKAR BAHASA]: [L] Key (English / Bahasa Melayu)
====================================================================
"""

import math
import random
import sys
import time

try:
    import pygame
except ImportError:
    print("\n" + "=" * 65)
    print(" [NOTE / PERHATIAN] The 'pygame' module is not installed.")
    print(" To play the full 2D graphical game, install pygame using:")
    print("      pip install pygame")
    print("      python game_bola_baling.py")
    print("\n Or run the zero-dependency terminal version right now:")
    print("      python game_terminal_pjk.py")
    print("=" * 65 + "\n")
    sys.exit()

# Initialize Pygame
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except Exception:
    pass

# Screen Settings
LEBAR_SKRIN = 900
TINGGI_SKRIN = 650
SKRIN = pygame.display.set_mode((LEBAR_SKRIN, TINGGI_SKRIN))
pygame.display.set_caption("Year 5 Handball Champions: Passing & Receiving Skills")
JAM = pygame.time.Clock()
FPS = 60

# Court Colors & Themes
WARNA_PADANG = (36, 110, 160)       # Indoor Blue Court
WARNA_KAWASAN_GOL = (230, 126, 34)   # Orange 6m D-Zone
WARNA_GARISAN = (255, 255, 255)
WARNA_KUNING_GARIS = (241, 196, 15)
WARNA_TEKS_GELAP = (30, 39, 46)
WARNA_TEKS_TERANG = (245, 246, 250)
WARNA_PEMAIN = (46, 204, 113)       # Green (Our Player)
WARNA_RAKAN = (52, 152, 219)        # Blue (Teammate)
WARNA_PERTAHANAN = (231, 76, 60)    # Red (Defender)
WARNA_BOLA = (243, 156, 18)         # Orange Handball
WARNA_PANEL = (20, 30, 45)

# Font Loader
def dapatkan_fon(saiz, tebal=False):
    try:
        return pygame.font.SysFont("Comic Sans MS", saiz, bold=tebal)
    except Exception:
        return pygame.font.SysFont("Arial", saiz, bold=tebal)

FON_BESAR = dapatkan_fon(36, True)
FON_SEDERHANA = dapatkan_fon(22, True)
FON_KECIL = dapatkan_fon(17)
FON_MIKRO = dapatkan_fon(14)

# Synthetic Sound Generator (No external audio files needed)
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

# Pass Physics Characteristics
PROFIL_HANTARAN = {
    1: {"kelajuan": 9, "ketinggian": 1, "lantulan": False},
    2: {"kelajuan": 12, "ketinggian": 2, "lantulan": False},
    3: {"kelajuan": 8, "ketinggian": 0, "lantulan": True},
    4: {"kelajuan": 7, "ketinggian": 3, "lantulan": False}
}

# Bilingual Localization Data (English & Bahasa Melayu)
DATA_BAHASA = {
    "en": {
        "title": "YEAR 5 HANDBALL CHAMPIONS",
        "subtitle": "Passing & Receiving Skills (Year 5 PE Curriculum)",
        "press_start": "PRESS [SPACE] TO START GAME",
        "press_restart": "PRESS [SPACE] TO PLAY AGAIN",
        "switch_lang_hint": "[L] Bahasa Melayu",
        "score_label": "SCORE",
        "streak_label": "COMBO",
        "perfect_label": "PERFECT 'W'",
        "time_label": "MATCH TIME",
        "pass_mode_hint": "Select Pass: [1, 2, 3, 4] | [L] Language",
        "player_tag": "You (Player)",
        "teammate_tag": "Teammate",
        "def_high": "High Block (Bounce Pass!)",
        "def_low": "Low Block (Lob/Overhead)",
        "def_normal": "Opponent Defender",
        "passes": {
            1: {"name": "Chest Pass", "desc": "Fast push from chest. Best for short-medium open spaces."},
            2: {"name": "Shoulder Pass", "desc": "Powerful & fast. Best for long distance & fast breaks."},
            3: {"name": "Bounce Pass", "desc": "Bounces off the floor to sneak under tall raised arms!"},
            4: {"name": "Overhead / Lob", "desc": "High arcing pass over tight, crouched defenders."}
        },
        "catch_title": "Receiving & Force Absorption ('W' Hands):",
        "catch_desc": "Press [SPACE] precisely when the ball arrives to absorb force with 'W' hands!",
        "tips": [
            "Year 5 PE Tip: Form a 'W' shape with thumbs & fingers to catch the ball securely!",
            "Year 5 PE Tip: Bend your elbows towards your chest to absorb the ball's momentum.",
            "Year 5 PE Tip: Use a Bounce Pass when the defender stands tall with arms raised.",
            "Year 5 PE Tip: Step forward to meet the incoming ball; don't wait flat-footed!",
            "Year 5 PE Tip: Keep your eyes focused on the flight of the ball at all times."
        ],
        "game_over_title": "FULL TIME! MATCH OVER",
        "grades": {
            "top": "Outstanding (Mastery Level 6) ★★★",
            "mid": "Very Good (Mastery Level 4-5) ★★☆",
            "low": "Needs Practice (Mastery Level 3) ★☆☆"
        },
        "stats_score": "Total Final Score: {} Points",
        "stats_passes": "Successful Passes: {} times",
        "stats_catches": "Perfect 'W' Force Absorptions: {} times",
        "stats_intercepted": "Passes Intercepted: {} times",
        "msg_start": "Match started! Execute accurate passes past the defender!",
        "msg_selected": "Pass Selected: {}!",
        "msg_chest_blocked": "Chest pass blocked! Defender is directly in the path.",
        "msg_shoulder_blocked": "Shoulder pass intercepted by defender!",
        "msg_bounce_blocked": "Bounce pass hit the defender's crouched legs!",
        "msg_lob_blocked": "Defender leaped high to block the overhead ball!",
        "msg_teammate_caught": "Crisp pass! Teammate caught the ball. Get ready to receive!",
        "msg_absorb_perfect": "PERFECT! 'W' Hand Force Absorption (+{} Points)",
        "msg_absorb_missed": "Ball received. (Tip: Press SPACE when ball arrives to ABSORB FORCE!)"
    },
    "bm": {
        "title": "CABARAN BOLA BALING TAHUN 5",
        "subtitle": "Kemahiran Menghantar & Menerima Bola (KSSR PJK)",
        "press_start": "TEKAN [SPACE] UNTUK MULA",
        "press_restart": "TEKAN [SPACE] MAIN SEMULA",
        "switch_lang_hint": "[L] English Language",
        "score_label": "SKOR",
        "streak_label": "KOMBO",
        "perfect_label": "SEMPURNA 'W'",
        "time_label": "MASA PERLAWANAN",
        "pass_mode_hint": "Tukar Hantaran: [1, 2, 3, 4] | [L] Bahasa",
        "player_tag": "Murid (Anda)",
        "teammate_tag": "Rakan Penerima",
        "def_high": "Hadang Tinggi (Lantul!)",
        "def_low": "Hadang Rendah (Atas Bahu/Lob)",
        "def_normal": "Penghadang Lawan",
        "passes": {
            1: {"name": "Hantaran Aras Dada", "desc": "Tolakan paras dada. Sesuai untuk hantaran pantas ruang terbuka."},
            2: {"name": "Hantaran Atas Bahu", "desc": "Hantaran paling kuat untuk jarak jauh atau larian pantas."},
            3: {"name": "Hantaran Lantul", "desc": "Melantun di lantai untuk lepasi pertahanan tinggi!"},
            4: {"name": "Hantaran Atas Kepala (Lob)", "desc": "Hantaran melengkung melepasi pertahanan rapat."}
        },
        "catch_title": "Kemahiran Menerima Bola (Serap Daya):",
        "catch_desc": "Tekan [SPACE] tepat ketika bola sampai untuk serap daya dengan tangan 'W'!",
        "tips": [
            "Tip PJK Tahun 5: Gunakan kedua-dua belah tangan membentuk huruf 'W' semasa menerima bola!",
            "Tip PJK Tahun 5: Bengkokkan siku ke arah dada untuk menyerap daya momentum bola.",
            "Tip PJK Tahun 5: Hantaran Lantul sesuai jika penghadang lawan berdiri tegak & mendepang tangan.",
            "Tip PJK Tahun 5: Bergerak ke hadapan menyambut bola, jangan tunggu bola sampai setempat!",
            "Tip PJK Tahun 5: Mata sentiasa fokus memandang arah pergerakan bola yang melayang."
        ],
        "game_over_title": "TAMAT MASA PERLAWANAN!",
        "grades": {
            "top": "Cemerlang (Tahap Penguasaan 6 / Bintang 3) ★★★",
            "mid": "Sangat Baik (Tahap Penguasaan 4-5 / Bintang 2) ★★☆",
            "low": "Boleh Dipertingkatkan (Bintang 1) ★☆☆"
        },
        "stats_score": "Jumlah Skor Keseluruhan: {} Mata",
        "stats_passes": "Hantaran Berjaya: {} kali",
        "stats_catches": "Tangkapan Sempurna (Serap Daya 'W'): {} kali",
        "stats_intercepted": "Bola Dipintas Lawan: {} kali",
        "msg_start": "Perlawanan bermula! Lakukan hantaran yang tepat!",
        "msg_selected": "Mod: {} dipilih!",
        "msg_chest_blocked": "Hantaran aras dada terhalang! Lawan berada tepat di laluan.",
        "msg_shoulder_blocked": "Hantaran atas bahu dipintas pertahanan lawan!",
        "msg_bounce_blocked": "Hantaran lantul terkena kaki penghadang yang membongkok!",
        "msg_lob_blocked": "Lawan melonjak tinggi menyekat bola atas kepala!",
        "msg_teammate_caught": "Hantaran kemas! Rakan menyambut bola. Bersedia menerima!",
        "msg_absorb_perfect": "SEMPURNA! Lakuan Serap Daya Tangan 'W' (+{} Mata)",
        "msg_absorb_missed": "Bola diterima. (Tip: Tekan SPACE semasa bola sampai untuk SERAP DAYA!)"
    }
}

class Pemain:
    def __init__(self, x, y, warna, label_key="player_tag"):
        self.x = x
        self.y = y
        self.warna = warna
        self.label_key = label_key
        self.jejari = 22
        self.kelajuan = 5
        self.sedang_serap_daya = False
        self.pemasa_serap_daya = 0

    def gerak(self, dx):
        self.x += dx * self.kelajuan
        self.x = max(60, min(LEBAR_SKRIN - 60, self.x))

    def aktifkan_serap_daya(self):
        self.sedang_serap_daya = True
        self.pemasa_serap_daya = 25  # frames active

    def kemas_kini(self):
        if self.pemasa_serap_daya > 0:
            self.pemasa_serap_daya -= 1
        else:
            self.sedang_serap_daya = False

    def lukis(self, permukaan, L):
        # Force absorption visual ring effect
        if self.sedang_serap_daya:
            radius_efek = self.jejari + 14 + int(math.sin(pygame.time.get_ticks() * 0.02) * 4)
            pygame.draw.circle(permukaan, (241, 196, 15), (int(self.x), int(self.y)), radius_efek, 3)

        # Shadow
        pygame.draw.ellipse(permukaan, (20, 20, 20, 80), (self.x - 18, self.y + 16, 36, 14))

        # Body
        pygame.draw.circle(permukaan, self.warna, (int(self.x), int(self.y)), self.jejari)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(self.y)), self.jejari, 3)

        # Head
        pygame.draw.circle(permukaan, (253, 227, 167), (int(self.x), int(self.y - 4)), 10)
        
        # 'W' Hand formation symbol in front of torso
        warna_tangan = (255, 255, 255) if not self.sedang_serap_daya else (241, 196, 15)
        pygame.draw.line(permukaan, warna_tangan, (self.x - 12, self.y - 12), (self.x - 6, self.y - 18), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x - 6, self.y - 18), (self.x, self.y - 14), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x, self.y - 14), (self.x + 6, self.y - 18), 3)
        pygame.draw.line(permukaan, warna_tangan, (self.x + 6, self.y - 18), (self.x + 12, self.y - 12), 3)

        # Label
        label_text = L.get(self.label_key, "Player")
        teks = FON_MIKRO.render(label_text, True, WARNA_TEKS_TERANG)
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

    def lukis(self, permukaan, L):
        # Shadow
        pygame.draw.ellipse(permukaan, (20, 20, 20, 80), (self.x - 18, self.y + 14, 36, 12))

        # Body
        pygame.draw.circle(permukaan, WARNA_PERTAHANAN, (int(self.x), int(self.y)), self.jejari)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(self.y)), self.jejari, 3)

        # Defender arm positions reflecting blocking posture
        if self.tinggi_hadangan == "tinggi":
            # Arms raised high up (Bypass with Bounce Pass!)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 18, self.y - 10), (self.x - 22, self.y - 30), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 18, self.y - 10), (self.x + 22, self.y - 30), 4)
            label = L["def_high"]
            warna_label = (255, 235, 59)
        elif self.tinggi_hadangan == "rendah":
            # Arms crouched low (Bypass with Overhead Lob or Fast High Shoulder Pass)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 14, self.y + 6), (self.x - 28, self.y + 10), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 14, self.y + 6), (self.x + 28, self.y + 10), 4)
            label = L["def_low"]
            warna_label = (129, 236, 236)
        else:
            # Normal stance
            pygame.draw.line(permukaan, (255, 255, 255), (self.x - 16, self.y - 5), (self.x - 26, self.y - 5), 4)
            pygame.draw.line(permukaan, (255, 255, 255), (self.x + 16, self.y - 5), (self.x + 26, self.y - 5), 4)
            label = L["def_normal"]
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
        self.arah_kembali = False  # True when teammate returns ball
        self.jenis_hantaran = 1
        self.jejari_asas = 10
        self.jejari_semasa = 10
        self.progres = 0.0
        self.mula_x = x
        self.mula_y = y
        self.jarak_keseluruhan = 1
        self.kelajuan = 0.02

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

        dx = ke_x - dari_x
        dy = ke_y - dari_y
        self.jarak_keseluruhan = max(1, math.hypot(dx, dy))

        spd = PROFIL_HANTARAN[jenis]["kelajuan"] if not kembali else 9
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

        # Position interpolation
        self.x = self.mula_x + (self.sasaran_x - self.mula_x) * self.progres
        self.y = self.mula_y + (self.sasaran_y - self.mula_y) * self.progres

        # 3D visual height simulation (Chest, Shoulder, Bounce, Lob)
        profil = PROFIL_HANTARAN[self.jenis_hantaran]
        if profil["lantulan"]:
            # Bounces on court floor at 60% of trajectory
            if self.progres < 0.6:
                arc = math.sin((self.progres / 0.6) * math.pi) * 6
                self.jejari_semasa = self.jejari_asas + int(arc)
            else:
                arc = math.sin(((self.progres - 0.6) / 0.4) * math.pi) * 8
                self.jejari_semasa = self.jejari_asas + int(arc)
        elif profil["ketinggian"] == 3:  # Lob / Overhead pass
            arc = math.sin(self.progres * math.pi) * 20
            self.jejari_semasa = self.jejari_asas + int(arc)
        elif profil["ketinggian"] == 2:  # Shoulder pass
            arc = math.sin(self.progres * math.pi) * 10
            self.jejari_semasa = self.jejari_asas + int(arc)
        else:  # Chest pass
            arc = math.sin(self.progres * math.pi) * 4
            self.jejari_semasa = self.jejari_asas + int(arc)

    def lukis(self, permukaan):
        if not self.bergerak:
            return

        # Floor shadow
        tinggi_bayang = (self.jejari_semasa - self.jejari_asas) * 1.5
        pygame.draw.ellipse(
            permukaan, (20, 20, 20, 100),
            (self.x - self.jejari_asas, self.y + tinggi_bayang, self.jejari_asas * 2, 8)
        )

        # Handball
        pos_y_fizikal = self.y - (self.jejari_semasa - self.jejari_asas)
        pygame.draw.circle(permukaan, WARNA_BOLA, (int(self.x), int(pos_y_fizikal)), self.jejari_semasa)
        pygame.draw.circle(permukaan, (255, 255, 255), (int(self.x), int(pos_y_fizikal)), self.jejari_semasa, 2)
        
        # Handball seam pattern
        pygame.draw.arc(
            permukaan, (230, 81, 0),
            (int(self.x - self.jejari_semasa * 0.8), int(pos_y_fizikal - self.jejari_semasa * 0.8),
             int(self.jejari_semasa * 1.6), int(self.jejari_semasa * 1.6)),
            0, math.pi, 2
        )

class Gelanggang:
    @staticmethod
    def lukis(permukaan):
        # Indoor Handball Court (Blue surface)
        permukaan.fill(WARNA_PADANG)

        # Court wood-floor texture lines
        for y in range(80, TINGGI_SKRIN - 90, 40):
            pygame.draw.line(permukaan, (41, 128, 185), (30, y), (LEBAR_SKRIN - 30, y), 1)

        # Court Outer Boundary Lines
        pygame.draw.rect(permukaan, WARNA_GARISAN, (30, 75, LEBAR_SKRIN - 60, TINGGI_SKRIN - 165), 4)

        # Center Line & Center Circle
        tengah_y = (75 + TINGGI_SKRIN - 90) // 2
        pygame.draw.line(permukaan, WARNA_GARISAN, (30, tengah_y), (LEBAR_SKRIN - 30, tengah_y), 3)
        pygame.draw.circle(permukaan, WARNA_GARISAN, (LEBAR_SKRIN // 2, tengah_y), 45, 3)

        # Top Goal Area (6m D-Zone)
        pygame.draw.arc(permukaan, WARNA_KAWASAN_GOL, (LEBAR_SKRIN // 2 - 130, 40, 260, 90), 0, math.pi, 4)
        
        # 9m Dashed Free-Throw Line
        for sudut in range(10, 170, 20):
            rad1 = math.radians(sudut)
            rad2 = math.radians(sudut + 10)
            p1 = (LEBAR_SKRIN // 2 + int(160 * math.cos(rad1)), 80 + int(90 * math.sin(rad1)))
            p2 = (LEBAR_SKRIN // 2 + int(160 * math.cos(rad2)), 80 + int(90 * math.sin(rad2)))
            pygame.draw.line(permukaan, WARNA_KUNING_GARIS, p1, p2, 3)

        # Bottom Goal Area (Our Team's End)
        bawah_y = TINGGI_SKRIN - 90
        pygame.draw.arc(permukaan, WARNA_KAWASAN_GOL, (LEBAR_SKRIN // 2 - 140, bawah_y - 70, 280, 90), math.pi, 2 * math.pi, 4)

        # Goal Post Visual
        pygame.draw.rect(permukaan, (255, 255, 255), (LEBAR_SKRIN // 2 - 70, 60, 140, 15))
        pygame.draw.rect(permukaan, (192, 57, 43), (LEBAR_SKRIN // 2 - 70, 60, 140, 15), 3)

# ----------------- MAIN GAME CLASS -----------------
class PermainanBolaBaling:
    def __init__(self):
        self.keadaan = "MENU"  # MENU, BERMAIN, SELESAI
        self.bahasa = "en"     # "en" or "bm"
        self.skor = 0
        self.streak = 0
        self.hantaran_berjaya = 0
        self.tangkapan_sempurna = 0
        self.bola_terlepas = 0
        self.masa_tinggal = 60
        self.masa_mula = 0

        self.jenis_pilihan = 1  # 1: Chest, 2: Shoulder, 3: Bounce, 4: Lob
        self.pemain = Pemain(LEBAR_SKRIN // 2, 490, WARNA_PEMAIN, "player_tag")
        self.rakan = Pemain(LEBAR_SKRIN // 2, 130, WARNA_RAKAN, "teammate_tag")
        self.penghadang = PenghadangLawan(LEBAR_SKRIN // 2, 310)
        self.bola = Bola(self.pemain.x, self.pemain.y)

        self.memegang_bola = True
        self.mesej_maklum_balas = ""
        self.warna_maklum_balas = (255, 255, 255)
        self.masa_maklum_balas = 0
        self.tip_semasa = ""
        self.pemasa_tip = 0
        self.kemas_kini_teks_bahasa()

    def kemas_kini_teks_bahasa(self):
        L = DATA_BAHASA[self.bahasa]
        self.mesej_maklum_balas = L["msg_start"]
        self.tip_semasa = random.choice(L["tips"])
        pygame.display.set_caption(L["title"])

    def tukar_bahasa(self):
        self.bahasa = "bm" if self.bahasa == "en" else "en"
        self.kemas_kini_teks_bahasa()
        mainkan_bunyi(BUNYI_HANTAR)

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
        L = DATA_BAHASA[self.bahasa]
        self.beri_maklum_balas(L["msg_start"], (46, 204, 113))
        mainkan_bunyi(BUNYI_WISIL)

    def beri_maklum_balas(self, teks, warna=(255, 255, 255)):
        self.mesej_maklum_balas = teks
        self.warna_maklum_balas = warna
        self.masa_maklum_balas = 130

    def proses_input(self):
        kekunci = pygame.key.get_pressed()
        L = DATA_BAHASA[self.bahasa]

        for peristiwa in pygame.event.get():
            if peristiwa.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if peristiwa.type == pygame.KEYDOWN:
                # Toggle language with 'L' key at any time
                if peristiwa.key == pygame.K_l:
                    self.tukar_bahasa()

                if self.keadaan in ("MENU", "SELESAI"):
                    if peristiwa.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.mula_baru()
                elif self.keadaan == "BERMAIN":
                    # Switch pass types
                    if peristiwa.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        mapping = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}
                        self.jenis_pilihan = mapping[peristiwa.key]
                        nama_pass = L["passes"][self.jenis_pilihan]["name"]
                        self.beri_maklum_balas(L["msg_selected"].format(nama_pass), (241, 196, 15))

                    # Press SPACE to Pass OR Absorb Force on Catch
                    elif peristiwa.key == pygame.K_SPACE:
                        if self.memegang_bola and not self.bola.bergerak:
                            # Pass to teammate
                            self.memegang_bola = False
                            self.bola.lancar(
                                self.pemain.x, self.pemain.y - 10,
                                self.rakan.x, self.rakan.y + 10,
                                self.jenis_pilihan, kembali=False
                            )
                            mainkan_bunyi(BUNYI_HANTAR)
                        elif not self.memegang_bola and self.bola.arah_kembali:
                            # Active force-absorption catch
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

        L = DATA_BAHASA[self.bahasa]

        # Timer
        masa_lalu = int(time.time() - self.masa_mula)
        self.masa_tinggal = max(0, 60 - masa_lalu)
        if self.masa_tinggal <= 0:
            self.keadaan = "SELESAI"
            mainkan_bunyi(BUNYI_WISIL)
            return

        # Updates
        self.pemain.kemas_kini()
        self.penghadang.kemas_kini()

        # Teammate AI gently shifts looking for passing lanes
        sasaran_rakan_x = self.pemain.x + math.sin(pygame.time.get_ticks() * 0.003) * 140
        self.rakan.x += (sasaran_rakan_x - self.rakan.x) * 0.05
        self.rakan.x = max(100, min(LEBAR_SKRIN - 100, self.rakan.x))

        # Periodic tips
        self.pemasa_tip += 1
        if self.pemasa_tip > 350:
            self.pemasa_tip = 0
            self.tip_semasa = random.choice(L["tips"])

        if self.masa_maklum_balas > 0:
            self.masa_maklum_balas -= 1

        # While holding ball
        if self.memegang_bola and not self.bola.bergerak:
            self.bola.x = self.pemain.x
            self.bola.y = self.pemain.y - 12
            return

        # Ball in flight update
        self.bola.kemas_kini()

        # 1. CHECK DEFENDER INTERCEPTIONS ON OUTBOUND PASS
        if self.bola.bergerak and not self.bola.arah_kembali:
            jarak_ke_lawan = math.hypot(self.bola.x - self.penghadang.x, self.bola.y - self.penghadang.y)
            
            if jarak_ke_lawan < 36:
                kena_hadang = False
                postur = self.penghadang.tinggi_hadangan

                # Tactical rules matching Year 5 PE curriculum:
                if self.bola.jenis_hantaran == 1:  # Chest Pass
                    kena_hadang = True
                    sebab = L["msg_chest_blocked"]
                elif self.bola.jenis_hantaran == 2:  # Shoulder Pass
                    if postur == "tinggi" or abs(self.bola.x - self.penghadang.x) < 18:
                        kena_hadang = True
                        sebab = L["msg_shoulder_blocked"]
                elif self.bola.jenis_hantaran == 3:  # Bounce Pass
                    # Bounce pass sneaks under tall defenders, blocked if defender is low
                    if postur == "rendah":
                        kena_hadang = True
                        sebab = L["msg_bounce_blocked"]
                    else:
                        kena_hadang = False  # Successfully bypassed high block!
                elif self.bola.jenis_hantaran == 4:  # Overhead / Lob Pass
                    # Arcs over defender unless defender leaps on high stance
                    if postur == "tinggi" and jarak_ke_lawan < 15:
                        kena_hadang = True
                        sebab = L["msg_lob_blocked"]

                if kena_hadang:
                    mainkan_bunyi(BUNYI_PINTAS)
                    self.streak = 0
                    self.skor = max(0, self.skor - 5)
                    self.bola_terlepas += 1
                    self.beri_maklum_balas(sebab, (231, 76, 60))
                    self.memegang_bola = True
                    self.bola.bergerak = False
                    return

            # Ball reaches teammate successfully
            if not self.bola.bergerak:
                self.hantaran_berjaya += 1
                self.skor += 10
                self.streak += 1
                mainkan_bunyi(BUNYI_TANGKAP)
                self.beri_maklum_balas(L["msg_teammate_caught"], (46, 204, 113))

                # Teammate passes ball back
                self.bola.lancar(
                    self.rakan.x, self.rakan.y + 10,
                    self.pemain.x, self.pemain.y - 10,
                    self.jenis_pilihan, kembali=True
                )

        # 2. CHECK RECEIVING & FORCE ABSORPTION ON RETURN PASS
        elif not self.bola.bergerak and self.bola.arah_kembali:
            # Ball arrived back to player. Evaluate force-absorption!
            if self.pemain.sedang_serap_daya:
                self.tangkapan_sempurna += 1
                mata_bonus = 15 + (self.streak * 2)
                self.skor += mata_bonus
                mainkan_bunyi(BUNYI_TANGKAP)
                self.beri_maklum_balas(L["msg_absorb_perfect"].format(mata_bonus), (241, 196, 15))
            else:
                self.skor += 5
                mainkan_bunyi(BUNYI_TANGKAP)
                self.beri_maklum_balas(L["msg_absorb_missed"], (255, 235, 59))

            self.memegang_bola = True

    def lukis_panel_status(self):
        L = DATA_BAHASA[self.bahasa]

        # Top Header Bar
        pygame.draw.rect(SKRIN, WARNA_PANEL, (0, 0, LEBAR_SKRIN, 70))
        pygame.draw.line(SKRIN, (50, 70, 95), (0, 70), (LEBAR_SKRIN, 70), 2)

        # Score & Streak
        teks_skor = FON_SEDERHANA.render(f"{L['score_label']}: {self.skor}", True, (241, 196, 15))
        SKRIN.blit(teks_skor, (25, 12))

        teks_streak = FON_MIKRO.render(f"{L['streak_label']}: {self.streak}x | {L['perfect_label']}: {self.tangkapan_sempurna}", True, (46, 204, 113))
        SKRIN.blit(teks_streak, (25, 42))

        # Match Timer
        warna_masa = (231, 76, 60) if self.masa_tinggal <= 10 else (245, 246, 250)
        teks_masa = FON_BESAR.render(f"{self.masa_tinggal}s", True, warna_masa)
        SKRIN.blit(teks_masa, (LEBAR_SKRIN // 2 - teks_masa.get_width() // 2, 8))
        teks_label_masa = FON_MIKRO.render(L["time_label"], True, (180, 190, 205))
        SKRIN.blit(teks_label_masa, (LEBAR_SKRIN // 2 - teks_label_masa.get_width() // 2, 46))

        # Active Pass Selection
        nama_pilihan = L["passes"][self.jenis_pilihan]["name"]
        teks_hantar = FON_SEDERHANA.render(f"[{self.jenis_pilihan}] {nama_pilihan}", True, (52, 152, 219))
        SKRIN.blit(teks_hantar, (LEBAR_SKRIN - teks_hantar.get_width() - 25, 12))

        teks_pilih_arahan = FON_MIKRO.render(L["pass_mode_hint"], True, (200, 210, 225))
        SKRIN.blit(teks_pilih_arahan, (LEBAR_SKRIN - teks_pilih_arahan.get_width() - 25, 42))

        # Bottom Bar (Feedback & PE Tips)
        bar_bawah_y = TINGGI_SKRIN - 80
        pygame.draw.rect(SKRIN, WARNA_PANEL, (0, bar_bawah_y, LEBAR_SKRIN, 80))
        pygame.draw.line(SKRIN, (50, 70, 95), (0, bar_bawah_y), (LEBAR_SKRIN, bar_bawah_y), 2)

        # Dynamic Feedback
        teks_mb = FON_SEDERHANA.render(self.mesej_maklum_balas, True, self.warna_maklum_balas)
        SKRIN.blit(teks_mb, (LEBAR_SKRIN // 2 - teks_mb.get_width() // 2, bar_bawah_y + 8))

        # PE Tip
        teks_tip = FON_MIKRO.render(self.tip_semasa, True, (241, 196, 15))
        SKRIN.blit(teks_tip, (LEBAR_SKRIN // 2 - teks_tip.get_width() // 2, bar_bawah_y + 45))

    def lukis_menu(self):
        L = DATA_BAHASA[self.bahasa]

        lapisan = pygame.Surface((LEBAR_SKRIN, TINGGI_SKRIN), pygame.SRCALPHA)
        lapisan.fill((15, 25, 40, 235))
        SKRIN.blit(lapisan, (0, 0))

        kotak = pygame.Rect(70, 40, LEBAR_SKRIN - 140, TINGGI_SKRIN - 80)
        pygame.draw.rect(SKRIN, (25, 38, 55), kotak, border_radius=18)
        pygame.draw.rect(SKRIN, (241, 196, 15), kotak, 4, border_radius=18)

        tajuk = FON_BESAR.render(L["title"], True, (241, 196, 15))
        SKRIN.blit(tajuk, (LEBAR_SKRIN // 2 - tajuk.get_width() // 2, 60))

        sub = FON_SEDERHANA.render(L["subtitle"], True, (236, 240, 241))
        SKRIN.blit(sub, (LEBAR_SKRIN // 2 - sub.get_width() // 2, 105))

        # Language Switch Badge
        t_lang = FON_MIKRO.render(L["switch_lang_hint"], True, (56, 189, 248))
        SKRIN.blit(t_lang, (LEBAR_SKRIN // 2 - t_lang.get_width() // 2, 140))

        # Pass Descriptions
        y_pos = 175
        for p_idx in (1, 2, 3, 4):
            item = L["passes"][p_idx]
            t_nama = FON_SEDERHANA.render(f"[{p_idx}] {item['name']}", True, (52, 152, 219))
            SKRIN.blit(t_nama, (100, y_pos))
            t_hur = FON_KECIL.render(item["desc"], True, (200, 214, 229))
            SKRIN.blit(t_hur, (120, y_pos + 26))
            y_pos += 56

        # Catching Guide
        t_terima = FON_SEDERHANA.render(L["catch_title"], True, (46, 204, 113))
        SKRIN.blit(t_terima, (100, y_pos + 6))
        t_terima_desc = FON_KECIL.render(L["catch_desc"], True, (255, 235, 59))
        SKRIN.blit(t_terima_desc, (120, y_pos + 34))

        # Start Button
        butang_rect = pygame.Rect(LEBAR_SKRIN // 2 - 200, TINGGI_SKRIN - 110, 400, 48)
        pygame.draw.rect(SKRIN, (46, 204, 113), butang_rect, border_radius=12)
        pygame.draw.rect(SKRIN, (255, 255, 255), butang_rect, 2, border_radius=12)
        teks_mula = FON_SEDERHANA.render(L["press_start"], True, (20, 30, 45))
        SKRIN.blit(teks_mula, (LEBAR_SKRIN // 2 - teks_mula.get_width() // 2, TINGGI_SKRIN - 100))

    def lukis_selesai(self):
        L = DATA_BAHASA[self.bahasa]

        lapisan = pygame.Surface((LEBAR_SKRIN, TINGGI_SKRIN), pygame.SRCALPHA)
        lapisan.fill((15, 25, 40, 240))
        SKRIN.blit(lapisan, (0, 0))

        kotak = pygame.Rect(110, 70, LEBAR_SKRIN - 220, TINGGI_SKRIN - 140)
        pygame.draw.rect(SKRIN, (25, 38, 55), kotak, border_radius=18)
        pygame.draw.rect(SKRIN, (46, 204, 113), kotak, 4, border_radius=18)

        tajuk = FON_BESAR.render(L["game_over_title"], True, (241, 196, 15))
        SKRIN.blit(tajuk, (LEBAR_SKRIN // 2 - tajuk.get_width() // 2, 95))

        # Achievement Grades
        if self.skor >= 200:
            gred = L["grades"]["top"]
            warna_gred = (46, 204, 113)
        elif self.skor >= 100:
            gred = L["grades"]["mid"]
            warna_gred = (52, 152, 219)
        else:
            gred = L["grades"]["low"]
            warna_gred = (241, 196, 15)

        t_gred = FON_SEDERHANA.render(gred, True, warna_gred)
        SKRIN.blit(t_gred, (LEBAR_SKRIN // 2 - t_gred.get_width() // 2, 150))

        # Statistics
        baris_stat = [
            L["stats_score"].format(self.skor),
            L["stats_passes"].format(self.hantaran_berjaya),
            L["stats_catches"].format(self.tangkapan_sempurna),
            L["stats_intercepted"].format(self.bola_terlepas)
        ]
        y_s = 205
        for s in baris_stat:
            t = FON_SEDERHANA.render(s, True, (245, 246, 250))
            SKRIN.blit(t, (LEBAR_SKRIN // 2 - t.get_width() // 2, y_s))
            y_s += 38

        # Play Again Button
        butang = pygame.Rect(LEBAR_SKRIN // 2 - 190, TINGGI_SKRIN - 160, 380, 48)
        pygame.draw.rect(SKRIN, (52, 152, 219), butang, border_radius=12)
        pygame.draw.rect(SKRIN, (255, 255, 255), butang, 2, border_radius=12)
        teks_ulang = FON_SEDERHANA.render(L["press_restart"], True, (255, 255, 255))
        SKRIN.blit(teks_ulang, (LEBAR_SKRIN // 2 - teks_ulang.get_width() // 2, TINGGI_SKRIN - 150))

    def lari(self):
        while True:
            self.proses_input()
            self.logik_permainan()

            # Render Court
            Gelanggang.lukis(SKRIN)

            L = DATA_BAHASA[self.bahasa]

            if self.keadaan == "BERMAIN":
                self.penghadang.lukis(SKRIN, L)
                self.rakan.lukis(SKRIN, L)
                self.pemain.lukis(SKRIN, L)
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
