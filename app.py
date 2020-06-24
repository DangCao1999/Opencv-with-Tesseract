from flask import Flask, request, send_file
import sys
import pytesseract
import os
import module_process_image
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vision-key.json"
app = Flask(__name__)


@app.route("/")
def hello():
    print("hello")
    return 'OK'
    
@app.route('/upload-image', methods = ['POST'] )
def upload_image():
    if request.method == 'POST':
        f = request.files['image']
        f.save(os.path.join("Image-input", f.filename))
        image_path = "Image-input/" + f.filename
        texts, boudingbox = module_process_image.detect_text(image_path)
        save_path = module_process_image.visualize(image_path, texts)
        print("save-path API-"+save_path)
        return send_file(save_path)



if __name__ == "__main__":
    app.run()
