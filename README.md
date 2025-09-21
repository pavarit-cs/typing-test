# Typing Test CLI & Streamlit

โปรแกรม **Typing Test CLI & Web App** สำหรับวัดความเร็ว (WPM) และความแม่นยำในการพิมพ์  
- **CLI version**: รันบน Command Line  
- **Streamlit version**: รันเป็นเว็บแอปใช้งานง่าย  

โปรเจกต์นี้เป็นงาน **Mini Project** ของรายวิชา **CP352301 Script Programming** ภาคเรียนที่ 1 ปีการศึกษา 2568  

---

## 📌 ฟีเจอร์ (Features)
- สุ่มประโยคจาก `textbank.py` หรือ `prompts.json`
- จับเวลาตั้งแต่เริ่มพิมพ์จนจบ
- คำนวณ **Words Per Minute (WPM)**
- คำนวณ **Accuracy (%)**
- ตรวจสอบความถูกต้องแบบตัวอักษรต่ออักษร
- รองรับ `Ctrl + C` ใน CLI เพื่อกลับเมนูหลัก
- (Streamlit) รองรับกด **Enter** เพื่อส่งข้อความทันที  

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```bash
Typing-Test-CLI/
├── docs/                   # เอกสารประกอบ
│   ├── PLAN.md             # แผนงาน
│   └── PROGRESS.md         # บันทึกความคืบหน้า
│
├── src/typing_test/        # Source code หลัก (package)
│   ├── __init__.py
│   ├── main.py             # CLI entry point
│   ├── prompt_source.py    # ดึงข้อความจาก JSON
│   ├── textbank.py         # ข้อความตัวอย่าง
│   └── typing_calculate.py # ฟังก์ชันคำนวณ accuracy, WPM
│
├── App/
│   └── main_app.py         # Streamlit web app
│
├── requirements.txt        # dependencies
├── pyproject.toml          # project config (editable install)
├── Dockerfile              # ใช้ build image สำหรับ deploy
├── .gitignore
└── README.md
```

---

## ⚙️ วิธีการติดตั้งและใช้งาน (Installation & Usage)
1. Clone project
```bash
git clone https://github.com/pavarit548x/Typing-Test-CLI.git
cd Typing-Test-CLI
```
2. (แนะนำ) สร้าง virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```
3. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```
ถ้าอยากให้โค้ด import ได้ทุกที่ ใช้ editable mode:
```bash
pip install -e .
```

---

## ▶️ Run CLI version
```bash
python src/typing_test/main.py
```
เมนู:

* กด 1 → เริ่มทดสอบ
* กด 2 → ออกจากโปรแกรม

---

## 🌐 Run Streamlit version
```bash
streamlit run App/main_app.py
```
เปิดเบราว์เซอร์ที่ http://localhost:8501

---

## 🐳 Run with Docker
1. Build image
```bash
docker build -t typing-test .
```
2. Run container
```bash
docker run -p 8501:8501 typing-test
```
เปิดเบราว์เซอร์: http://localhost:8501

```
Typing-Test-CLI
├─ App
│  └─ main_app.py
├─ docs
│  ├─ PLAN.md
│  └─ PROGRESS.md
├─ pyproject.toml
├─ README.md
└─ src
   ├─ typing_test
   │  ├─ data
   │  │  ├─ prompts.json
   │  │  └─ script_sort_jsonPrompts.py
   │  ├─ main.py
   │  ├─ prompt_source.py
   │  ├─ textbank.py
   │  └─ typing_calculate.py
   └─ typing_test.egg-info
      ├─ dependency_links.txt
      ├─ entry_points.txt
      ├─ PKG-INFO
      ├─ SOURCES.txt
      └─ top_level.txt

```