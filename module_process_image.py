from google.cloud import vision
import io
import json
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def detect_text(path):
    client = vision.ImageAnnotatorClient()
    vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    bounding = []

    for text in texts:
        

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        bounding.append(vertices)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts, bounding


def visualize(image_name, texts):
  image = cv2.imread(image_name)
  name_tags = []
  hasTag = False
  for text in texts:
    pts = np.array([[v.x,v.y] for v in text.bounding_poly.vertices ], np.int32)
    pts = pts.reshape((-1,1,2))
  
    cv2.polylines(image,[pts],True,(0,255,255),thickness=3)
    if hasTag == True:
      name_tags.append({
          "text":text.description,
          "pos": (text.bounding_poly.vertices[0].x,text.bounding_poly.vertices[0].y-20)
      })
    if hasTag == False:
      hasTag = True

  fontpath = "font/Roboto-Regular.ttf"     
  font = ImageFont.truetype(fontpath, 30)
  img_pil = Image.fromarray(image)
  draw = ImageDraw.Draw(img_pil)
  

  for tag in name_tags:
    draw.text(tag['pos'], tag['text'], font = font, fill = (0, 0, 255))
  img = np.array(img_pil)

  #print("Image: "+image_name+" -------------------------------------")
  save_path = "Image-output/" + image_name.split(".")[0][12:] + "result." + image_name.split(".")[1]
  #print(save_path+"---------------------------")
  cv2.imwrite(save_path,img)
  #print("Raw data --------------------------")
  #print(name_tags)
  return save_path