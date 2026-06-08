import os
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template
from markitdown import MarkItDown
import markdown
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

md = MarkItDown()

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    results = []
    for f in files:
        original_name = Path(f.filename).stem
        suffix = Path(f.filename).suffix
        out_name = original_name + ".md"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            f.save(tmp.name)
            tmp_path = tmp.name

        try:
            if suffix.lower() in IMAGE_EXTENSIONS:
                img = Image.open(tmp_path)
                text = pytesseract.image_to_string(img, lang="eng+ind")
                md_content = f"# {original_name}\n\n{text.strip()}"
            else:
                result = md.convert(tmp_path)
                md_content = result.text_content

            out_path = OUTPUT_DIR / out_name
            counter = 1
            while out_path.exists():
                out_path = OUTPUT_DIR / f"{original_name}_{counter}.md"
                counter += 1
            out_path.write_text(md_content, encoding="utf-8")
            results.append({"name": f.filename, "output": out_path.name, "status": "ok"})
        except Exception as e:
            results.append({"name": f.filename, "output": None, "status": f"error: {e}"})
        finally:
            os.unlink(tmp_path)

    return jsonify(results)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route("/view/<filename>")
def view(filename):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        return "File tidak ditemukan", 404
    raw = file_path.read_text(encoding="utf-8")
    html_content = markdown.markdown(raw, extensions=["tables", "fenced_code", "nl2br"])
    return render_template("viewer.html", filename=filename, content=html_content)


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:5000")
    app.run(debug=False)
