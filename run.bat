@echo off
cd /d "%~dp0"

set "TESSERACT_EXE=C:\Program Files\Tesseract-OCR\tesseract.exe"

:: Check if Tesseract exe exists
if not exist "%TESSERACT_EXE%" (
    echo Tesseract tidak ditemukan. Menginstall otomatis via winget...
    winget install --id UB-Mannheim.TesseractOCR -e --silent --accept-package-agreements --accept-source-agreements
    if not exist "%TESSERACT_EXE%" (
        echo Gagal install Tesseract. Coba install manual dari https://github.com/UB-Mannheim/tesseract/wiki
        pause
        exit /b 1
    )
    echo Tesseract berhasil diinstall.
)

:: Add Tesseract to PATH for this session
set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"

:: Download Indonesian language data if not present
if not exist "C:\Program Files\Tesseract-OCR\tessdata\ind.traineddata" (
    echo Mendownload bahasa Indonesia untuk OCR...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata/raw/main/ind.traineddata' -OutFile 'C:\Program Files\Tesseract-OCR\tessdata\ind.traineddata'"
    echo Bahasa Indonesia berhasil didownload.
)

echo Menjalankan MD Converter...
python app.py
pause
