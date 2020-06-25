from flask import Flask, request, send_file, send_from_directory
import sys
import pytesseract
import os
import module_process_image
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vision-key.json"
app = Flask(__name__, static_url_path='/Image-output')

app.config['CLIENT_IMAGE'] = "./Image-output"

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
        return save_path


@app.route('/image/<name_image>', methods=['GET'])
def get_image(name_image):
    if(request).method == 'GET':
        #filename = f"{name_image}"
        return send_from_directory(app.config['CLIENT_IMAGE'], filename= name_image, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
