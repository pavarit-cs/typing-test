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
├── .git/                   # git repo ของคุณ
├── .gitignore              # กำหนดไฟล์ที่ไม่ต้องการ track
├── App/
│   └── main_app.py         # Streamlit app
│
├── docs/                   # เอกสารประกอบ
│   ├── PLAN.md
│   └── PROGRESS.md
│
├── src/typing_test/        # source code (package)
│   ├── __init__.py         # ทำให้เป็น package
│   ├── data/
│   │   ├── prompts.json
│   │   └── script_sort_jsonPrompts.py
│   ├── main.py             # CLI entry point
│   ├── prompt_source.py
│   ├── textbank.py
│   └── typing_calculate.py
│
├── requirements.txt        # dependencies (เช่น streamlit)
├── pyproject.toml          # project config (pip install -e .)
├── Dockerfile              # build docker image
└── README.md               # คู่มือโปรเจกต์

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