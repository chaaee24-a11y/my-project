"""
=============================================================================
HANDBALL PASSING & RECEIVING SKILLS GAME - YEAR 5 PRIMARY SCHOOL
AKADEMI BOLA BALING TAHUN 5 (KSSR SEMAKAN PJK SEKOLAH RENDAH)
=============================================================================
Zero dependencies required! Runs in any standard Python terminal:
   python3 game_terminal_pjk.py
Supports both English and Bahasa Melayu.
=============================================================================
"""

import time
import random
import sys

def garisan():
    print("=" * 68)

def teks_perlahan(ayat, kelajuan=0.015):
    for aksara in ayat:
        sys.stdout.write(aksara)
        sys.stdout.flush()
        time.sleep(kelajuan)
    print()

DATA_TEKS = {
    "en": {
        "title": "YEAR 5 HANDBALL SKILLS SIMULATION: PASSING & RECEIVING",
        "subtitle": "Physical Education (PE) Primary School - Ball Control & Tactics",
        "instructions": "Instructions: Make smart tactical passing decisions and react fast to absorb force when catching!",
        "pass_title": "Choose the best pass type:",
        "passes": {
            "1": {
                "name": "Chest Pass",
                "desc": "Quick push from chest level with both hands. Best for short-medium open spaces."
            },
            "2": {
                "name": "Shoulder / Overarm Pass",
                "desc": "Strongest, fastest pass using shoulder torque. Best for long distance & fast-breaks."
            },
            "3": {
                "name": "Bounce Pass",
                "desc": "Bounces off the floor ~2/3 distance to teammate. Best against tall upright defenders."
            },
            "4": {
                "name": "Overhead / Lob Pass",
                "desc": "High arcing trajectory. Best over tight defenders crouched low or pressing close."
            }
        },
        "scenarios": [
            {
                "sit": "Your teammate (Aidan) is sprinting fast towards the goal 15 meters away!",
                "def": "Defenders are chasing from behind but there is an open long-distance lane ahead.",
                "ans": "2",
                "exp": "Spot on! The Shoulder/Overarm Pass provides maximum power and velocity for long-distance fast-breaks."
            },
            {
                "sit": "A tall defender stands right in front of you with both arms raised high to block chest-high passes.",
                "def": "Defender's arms and hands are held high in the air.",
                "ans": "3",
                "exp": "Brilliant! The Bounce Pass stays low and skips beneath the defender's raised arms."
            },
            {
                "sit": "Your teammate is 4 meters to your side in open space without any opponent nearby.",
                "def": "Clear open passing lane, short distance.",
                "ans": "1",
                "exp": "Great choice! The Chest Pass is the quickest, most accurate pass for short distances and open teammates."
            },
            {
                "sit": "An opponent marks you tightly and crouches low with outstretched arms to block ground and chest passes.",
                "def": "Defender is crouched low and pressing close to your body.",
                "ans": "4",
                "exp": "Excellent! An Overhead / Lob Pass arcs smoothly over the low-crouching defender."
            }
        ],
        "catch_header": ">> CATCHING CHALLENGE: ABSORBING FORCE ('W' HAND POSITION) <<",
        "catch_tip": "Year 5 PE Tip: Form a 'W' shape with thumbs & index fingers, and bend your elbows towards your chest to absorb ball momentum!",
        "ready_prompt": "Press [ENTER] when you are ready to receive...",
        "released": "\nBall has been released by your teammate! Flying towards you...",
        "catch_action": ">>> CATCH NOW! (Press [ENTER] as fast as possible!) <<< ",
        "reaction_time": "\nYour reaction time: {:.3f} seconds",
        "reaction_grades": [
            (0.25, "⚡ LIGHTNING FAST! Clean catch with textbook force absorption!", "Strong 'W' hand grip effortlessly absorbed the ball's momentum! (+25 Points)", 25),
            (0.55, "👏 SOLID CATCH! Safe and controlled ball reception. (+15 Points)", "Good elbow flexion cushioned the ball nicely.", 15),
            (0.90, "⚠️ A bit slow, but you managed to secure the ball! (+8 Points)", "Remember to move towards the ball rather than waiting for it.", 8),
            (999.0, "❌ OOPS! The ball slipped through because your reaction was too late! (0 Points)", "Keep your eyes on the ball at all times!", 0)
        ],
        "round_label": "ROUND {} / 4",
        "input_choice": "\nEnter your choice (1/2/3/4): ",
        "correct_alert": "\n[CORRECT!] {} (+20 Points)",
        "wrong_alert": "\n[NOT QUITE] That pass is easily intercepted in this situation.",
        "best_was": "Best option was: [{}] {}",
        "explanation": "Explanation: {}",
        "game_over": "TRAINING SESSION COMPLETE! YOUR TOTAL SCORE: {} / 180 POINTS",
        "grade_mastery": [
            (150, "Grade: MASTERY LEVEL 6 (OUTSTANDING) 🏆", "You have mastered all passing techniques and the 'W' force-absorption catch!"),
            (100, "Grade: MASTERY LEVEL 4-5 (VERY GOOD) 🥇", "Solid fundamental skills! Practice reaction time for even quicker ball releases."),
            (0, "Grade: MASTERY LEVEL 3 (KEEP PRACTICING) 🥈", "Review when to use Bounce, Chest, Shoulder, and Lob passes against different defensive postures.")
        ]
    },
    "bm": {
        "title": "SIMULASI BOLA BALING TAHUN 5: KEMAHIRAN HANTAR & TERIMA",
        "subtitle": "Pendidikan Jasmani & Kesihatan (PJK) KSSR Semakan Sekolah Rendah",
        "instructions": "Arahan: Buat keputusan taktikal hantaran yang tepat dan uji kepantasan serap daya semasa menangkap bola!",
        "pass_title": "Pilih jenis hantaran yang paling sesuai:",
        "passes": {
            "1": {
                "name": "Hantaran Aras Dada (Chest Pass)",
                "desc": "Tolakan kuat dari paras dada. Terbaik untuk jarak dekat/sederhana dan ruang terbuka."
            },
            "2": {
                "name": "Hantaran Atas Bahu (Overarm / Shoulder Pass)",
                "desc": "Hantaran paling kuat dan laju. Terbaik untuk jarak jauh & serangan pantas (fast-break)."
            },
            "3": {
                "name": "Hantaran Lantul (Bounce Pass)",
                "desc": "Bola dilantun kira-kira 2/3 perjalanan ke rakan. Terbaik melepasi penghadang lawan yang tinggi."
            },
            "4": {
                "name": "Hantaran Atas Kepala / Lob (Overhead Pass)",
                "desc": "Melayangkan bola melengkung tinggi. Terbaik melepasi lawan yang mengawal ketat atau membongkok."
            }
        },
        "scenarios": [
            {
                "sit": "Rakan anda (Aiman) sedang membuat larian pantas ke arah gol lawan sejauh 15 meter!",
                "def": "Penghadang lawan mengejar dari belakang tetapi terdapat ruang hantaran jauh di hadapan.",
                "ans": "2",
                "exp": "Tepat sekali! Hantaran Atas Bahu memberi daya tolakan paling kuat dan laju untuk jarak jauh."
            },
            {
                "sit": "Pemain pertahanan lawan yang berbadan tinggi berdiri tegak tepat di hadapan anda sambil mengangkat kedua-dua tangan ke atas.",
                "def": "Tangan lawan terangkat tinggi menghadang laluan aras dada.",
                "ans": "3",
                "exp": "Hebat! Hantaran Lantul melantun rendah di bawah jangkauan tangan lawan yang terangkat tinggi."
            },
            {
                "sit": "Rakan anda berada 4 meter di sebelah anda dalam posisi terbuka tanpa sebarang halangan lawan.",
                "def": "Laluan bola bebas dan jarak dekat.",
                "ans": "1",
                "exp": "Bagus! Hantaran Aras Dada adalah yang paling pantas dan tepat untuk jarak dekat dan ruang terbuka."
            },
            {
                "sit": "Penghadang lawan mengawal sangat rapat dan membongkokkan badan untuk menyekat hantaran rendah.",
                "def": "Lawan membongkokkan badan dan mendepangkan tangan ke bawah.",
                "ans": "4",
                "exp": "Cemerlang! Hantaran Atas Kepala (Lob) melengkung melepasi atas kepala lawan yang rendah."
            }
        ],
        "catch_header": ">> CABARAN KEMAHIRAN MENERIMA BOLA (SERAP DAYA) <<",
        "catch_tip": "Tip PJK Tahun 5: Buka jari membentuk huruf 'W' dan serap daya dengan membengkokkan siku ke arah dada!",
        "ready_prompt": "Tekan [ENTER] apabila anda bersedia menyambut bola...",
        "released": "\nBola dilepaskan oleh rakan! Sedang melayang laju ke arah anda...",
        "catch_action": ">>> TANGKAP SEKARANG! (Tekan [ENTER] secepat mungkin!) <<< ",
        "reaction_time": "\nMasa reaksi anda: {:.3f} saat",
        "reaction_grades": [
            (0.25, "⚡ LUAR BIASA PANTAS! Tangkapan kemas dengan serap daya sempurna!", "Kedudukan tangan 'W' yang kukuh menyerap momentum hentaman bola! (+25 Markah)", 25),
            (0.55, "👏 TANGKAPAN BAIK! Bola berjaya ditangkap dengan selamat. (+15 Markah)", "Siku dibengkokkan dengan baik menyerap impak bola.", 15),
            (0.90, "⚠️ Tangkapan sedikit lambat, tetapi bola masih dapat dikawal. (+8 Markah)", "Ingat: Sentiasa bergerak ke hadapan menyambut bola, jangan tunggu setempat.", 8),
            (999.0, "❌ ALAMAK! Bola terlepas daripada tangan kerana lambat bertindak! (0 Markah)", "Fokus mata pada arah ketibaan bola setiap masa!", 0)
        ],
        "round_label": "PUSINGAN {} / 4",
        "input_choice": "\nMasukkan pilihan anda (1/2/3/4): ",
        "correct_alert": "\n[BETUL!] {} (+20 Markah)",
        "wrong_alert": "\n[KURANG TEPAT] Hantaran tersebut mudah dipintas atau kurang efisien.",
        "best_was": "Jawapan terbaik ialah: [{}] {}",
        "explanation": "Penjelasan: {}",
        "game_over": "TAMAT LATIHAN! JUMLAH SKOR ANDA: {} / 180 MATA",
        "grade_mastery": [
            (150, "Gred: TAHAP PENGUASAAN 6 (CEMERLANG) 🏆", "Anda menguasai semua jenis hantaran dan mekanik serap daya tangan 'W'!"),
            (100, "Gred: TAHAP PENGUASAAN 4-5 (SANGAT BAIK) 🥇", "Kemahiran asas mantap! Teruskan latihan untuk reaksi tangkapan lebih pantas."),
            (0, "Gred: TAHAP PENGUASAAN 3 (USAHA LAGI) 🥈", "Ulang kaji bila waktu terbaik menggunakan Hantaran Lantul, Dada, Bahu & Lob.")
        ]
    }
}

def uji_menerima_bola(lang_dict):
    garisan()
    print(lang_dict["catch_header"])
    garisan()
    print(lang_dict["catch_tip"])
    print()
    
    input(lang_dict["ready_prompt"])
    
    print(lang_dict["released"])
    time.sleep(random.uniform(1.2, 2.5))
    
    mula = time.time()
    input(lang_dict["catch_action"])
    tamat = time.time()
    
    masa_reaksi = tamat - mula
    print(lang_dict["reaction_time"].format(masa_reaksi))
    
    for had, pujian, ulasan, markah in lang_dict["reaction_grades"]:
        if masa_reaksi < had:
            print(pujian)
            print(ulasan)
            return markah
    return 0

def main_simulasi():
    garisan()
    print("   YEAR 5 HANDBALL SKILLS SIMULATION / AKADEMI BOLA BALING")
    print("       Passing (Menghantar) & Receiving / Force Absorption")
    garisan()
    print("Select Language / Pilih Bahasa:")
    print("  [1] English (Default)")
    print("  [2] Bahasa Melayu (PJK Tahun 5)")
    pilih_bahasa = input("Pilihan / Selection (1/2, default 1): ").strip()
    
    lang_code = "bm" if pilih_bahasa == "2" else "en"
    L = DATA_TEKS[lang_code]
    
    garisan()
    print(f"   {L['title']}")
    print(f"      {L['subtitle']}")
    garisan()
    print(L["instructions"])
    print()
    
    skor = 0
    pusingan = 1
    
    senarai_soalan = list(L["scenarios"])
    random.shuffle(senarai_soalan)
    
    for item in senarai_soalan:
        garisan()
        print(L["round_label"].format(pusingan))
        garisan()
        print(f"• {item['sit']}")
        print(f"• {item['def']}")
        print(f"\n{L['pass_title']}")
        for k, v in L["passes"].items():
            print(f"  [{k}] {v['name']} - {v['desc']}")
        
        pilihan = input(L["input_choice"]).strip()
        
        if pilihan == item["ans"]:
            print(L["correct_alert"].format(item["exp"]))
            skor += 20
            # Ujian menangkap bola (serap daya)
            skor += uji_menerima_bola(L)
        else:
            betul_k = item["ans"]
            nama_b = L["passes"][betul_k]["name"]
            print(L["wrong_alert"])
            print(L["best_was"].format(betul_k, nama_b))
            print(L["explanation"].format(item["exp"]))
        
        pusingan += 1
        time.sleep(1.2)
        print()
    
    garisan()
    print(L["game_over"].format(skor))
    garisan()
    for had_min, tajuk_gred, huraian in L["grade_mastery"]:
        if skor >= had_min:
            print(tajuk_gred)
            print(huraian)
            break
    garisan()

if __name__ == "__main__":
    main_simulasi()
