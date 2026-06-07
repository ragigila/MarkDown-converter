import os
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template
from markitdown import MarkItDown

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

md = MarkItDown()


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
            result = md.convert(tmp_path)
            out_path = OUTPUT_DIR / out_name
            # avoid overwrite collision
            counter = 1
            while out_path.exists():
                out_path = OUTPUT_DIR / f"{original_name}_{counter}.md"
                counter += 1
            out_path.write_text(result.text_content, encoding="utf-8")
            results.append({"name": f.filename, "output": out_path.name, "status": "ok"})
        except Exception as e:
            results.append({"name": f.filename, "output": None, "status": f"error: {e}"})
        finally:
            os.unlink(tmp_path)

    return jsonify(results)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:5000")
    app.run(debug=False)
