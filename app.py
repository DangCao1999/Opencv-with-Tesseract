from flask import Flask, request, send_file
import sys
import pytesseract
import os
app = Flask(__name__)


@app.route("/")
def hello():
    print(pytesseract.get_tesseract_version(), file=sys.stderr)
    return 'OK'
    
@app.route('/upload-image', methods = ['POST'] )
def upload_image():
    if request.method == 'POST':
        f = request.files['image']
        f.save(os.path.join("Image-input", f.filename))
        return "OK"



if __name__ == "__main__":
    app.run()
