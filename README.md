# MD Converter

Convert file apapun ke Markdown — bulk, lokal, offline.

Powered by [markitdown](https://github.com/microsoft/markitdown) dari Microsoft.

## Format yang didukung

PDF, DOCX, PPTX, XLSX, HTML, gambar (JPG/PNG), CSV, XML, ZIP, dan lainnya.

## Cara pakai

### 1. Install Python

Download Python 3.9+ dari [python.org](https://www.python.org/downloads/)

### 2. Clone repo

```bash
git clone https://github.com/ragigila/MarkDown-converter.git
cd MarkDown-converter
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan

**Windows:**
```
run.bat
```

**Mac / Linux:**
```bash
python app.py
```

Browser otomatis terbuka ke `http://localhost:5000`

## Cara pakai app

1. Drag & drop file ke area upload (bisa banyak sekaligus)
2. Klik **Convert Semua**
3. Download hasil `.md` — atau ambil dari folder `output/`

## Struktur folder

```
md-converter/
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
├── run.bat
└── output/        ← hasil konversi (tidak ikut ke GitHub)
```
