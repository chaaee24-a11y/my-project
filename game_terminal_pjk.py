"""
=============================================================================
SIMULASI TEKSTUAL: AKADEMI BOLA BALING TAHUN 5 (KSSR SEMAKAN PJK)
Modul Latihan Kemahiran Menghantar dan Menerima Bola Baling
Boleh dijalankan terus dalam mana-mana terminal Python tanpa pasang library!
=============================================================================
"""

import time
import random
import sys

def garisan():
    print("=" * 65)

def teks_perlahan(ayat, kelajuan=0.02):
    for aksara in ayat:
        sys.stdout.write(aksara)
        sys.stdout.flush()
        time.sleep(kelajuan)
    print()

JENIS_HANTARAN = {
    "1": {
        "nama": "Hantaran Aras Dada (Chest Pass)",
        "sesuai_untuk": "Jarak dekat / sederhana & laluan bebas tanpa penghadang tegak.",
        "keterangan": "Tolakan kuat daripada paras dada menggunakan kedua-dua belah tangan."
    },
    "2": {
        "nama": "Hantaran Atas Bahu (Overarm / Shoulder Pass)",
        "sesuai_untuk": "Jarak jauh & serangan pantas (fast-break).",
        "keterangan": "Hantaran paling kuat dan laju dalam sukan bola baling."
    },
    "3": {
        "nama": "Hantaran Lantul (Bounce Pass)",
        "sesuai_untuk": "Penghadang lawan berdiri tegak tinggi mendepang tangan.",
        "keterangan": "Melantunkan bola di atas lantai kira-kira 2/3 perjalanan ke rakan."
    },
    "4": {
        "nama": "Hantaran Atas Kepala / Lob (Overhead Pass)",
        "sesuai_untuk": "Penghadang lawan mengawal rapat atau membongkok rendah.",
        "keterangan": "Melayangkan bola melengkung melepasi jangkauan tangan penghadang."
    }
}

SITUASI_LATIHAN = [
    {
        "situasi": "Rakan anda (Aiman) sedang membuat larian pantas ke arah gol lawan sejauh 15 meter!",
        "lawan": "Penghadang lawan mengejar dari belakang tetapi jaraknya jauh.",
        "jawapan_betul": "2",
        "ulasan": "Tepat sekali! Hantaran Atas Bahu memberi daya tolakan paling kuat untuk hantaran jarak jauh."
    },
    {
        "situasi": "Pemain pertahanan lawan yang bertubuh tinggi berdiri tegak betul-betul di hadapan anda sambil mengangkat kedua-dua tangan ke atas.",
        "lawan": "Tangan lawan terangkat tinggi menghadang laluan bola aras dada.",
        "jawapan_betul": "3",
        "ulasan": "Hebat! Hantaran Lantul membolehkan bola memantul di bawah jangkauan tangan lawan yang tinggi."
    },
    {
        "situasi": "Rakan anda berada 4 meter di sebelah anda dalam posisi terbuka tanpa sebarang halangan.",
        "lawan": "Tiada halangan langsung di antara anda dan rakan.",
        "jawapan_betul": "1",
        "ulasan": "Bagus! Hantaran Aras Dada adalah yang paling pantas dan tepat untuk jarak dekat dan ruang terbuka."
    },
    {
        "situasi": "Penghadang lawan mengawal sangat rapat dan membongkokkan badan untuk menyekat hantaran rendah dan lantul.",
        "lawan": "Lawan mendepangkan tangan ke bawah.",
        "jawapan_betul": "4",
        "ulasan": "Cemerlang! Hantaran Atas Kepala (Lob) melengkung melepasi atas kepala lawan yang rendah."
    }
]

def uji_menerima_bola():
    garisan()
    print(">> CABARAN KEMAHIRAN MENERIMA BOLA (SERAP DAYA) <<")
    garisan()
    print("Rakan anda membalas hantaran! Bola sedang melayang laju ke arah anda...")
    print("Tips PJK Tahun 5: Buka jari membentuk 'W' dan serap daya dengan membengkokkan siku!")
    print()
    
    input("Tekan [ENTER] apabila anda bersedia...")
    
    print("\nBola dilepaskan...")
    time.sleep(random.uniform(1.2, 2.5))
    
    mula = time.time()
    tindak = input(">>> TANGKAP SEKARANG! (Tekan ENTER secepat mungkin!) <<< ")
    tamat = time.time()
    
    masa_reaksi = tamat - mula
    print(f"\nMasa reaksi anda: {masa_reaksi:.3f} saat")
    
    if masa_reaksi < 0.25:
        print("⚡ LUAR BIASA PANTAS! Tangkapan kemas dengan serap daya sempurna!")
        print("Kedudukan tangan 'W' yang kukuh menyerap hentaman bola! (+25 Markah)")
        return 25
    elif masa_reaksi < 0.55:
        print("👏 TANGKAPAN BAIK! Bola berjaya ditangkap dengan selamat. (+15 Markah)")
        return 15
    elif masa_reaksi < 0.90:
        print("⚠️ Tangkapan sedikit lambat, tetapi bola masih dapat dikawal. (+8 Markah)")
        return 8
    else:
        print("❌ ALAMAK! Bola terlepas daripada tangan kerana lambat bertindak! (0 Markah)")
        return 0

def main_simulasi():
    garisan()
    print("   SELAMAT DATANG KE SIMULASI BOLA BALING TAHUN 5")
    print("      Topik: Kemahiran Menghantar & Menerima Bola")
    garisan()
    print("Arahan: Buat keputusan taktikal yang betul berdasarkan prinsip mekanik PJK.")
    print()
    
    skor = 0
    pusingan = 1
    
    # Rawakkan situasi
    soalan_soalan = list(SITUASI_LATIHAN)
    random.shuffle(soalan_soalan)
    
    for item in soalan_soalan:
        garisan()
        print(f"PUSINGAN {pusingan} / 4")
        garisan()
        print(f"Situasi: {item['situasi']}")
        print(f"Kedudukan Lawan: {item['lawan']}")
        print("\nPilih Jenis Hantaran Yang Paling Tepat:")
        for k, v in JENIS_HANTARAN.items():
            print(f"  [{k}] {v['nama']}")
        
        pilihan = input("\nMasukkan pilihan anda (1/2/3/4): ").strip()
        
        if pilihan == item["jawapan_betul"]:
            print(f"\n[BETUL!] {item['ulasan']} (+20 Markah)")
            skor += 20
            # Seterusnya uji kemahiran menerima balasan bola
            skor += uji_menerima_bola()
        else:
            betul_key = item["jawapan_betul"]
            nama_sebenar = JENIS_HANTARAN[betul_key]["nama"]
            print(f"\n[KURANG TEPAT] Hantaran tersebut mudah dipintas atau kurang efisien.")
            print(f"Jawapan terbaik ialah: [{betul_key}] {nama_sebenar}")
            print(f"Penjelasan: {item['ulasan']}")
        
        pusingan += 1
        time.sleep(1.2)
        print()
    
    garisan()
    print(f"TAMAT LATIHAN! JUMLAH SKOR ANDA: {skor} / 180 MATA")
    garisan()
    if skor >= 150:
        print("Gred: TAHAP PENGUASAAN 6 (CEMERLANG) 🏆")
        print("Anda menguasai semua jenis hantaran dan teknik serap daya tangan 'W'!")
    elif skor >= 100:
        print("Gred: TAHAP PENGUASAAN 4-5 (SANGAT BAIK) 🥇")
        print("Kemahiran asas anda mantap! Teruskan latihan untuk reaksi lebih pantas.")
    else:
        print("Gred: TAHAP PENGUASAAN 3 (USAHA LAGI) 🥈")
        print("Ulang kaji semula bila waktu terbaik guna Hantaran Lantul, Dada, Bahu & Lob.")
    garisan()

if __name__ == "__main__":
    main_simulasi()
