from flask import Flask, render_template, request, flash, redirect, url_for
import os
import boto3
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights='imagenet')
img_path = 'elephant.jpg'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
s3 = boto3.resource('s3')

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_cat(classification, confidence) -> str:
    if classification in ["tabby", "tiger_cat", "Persian_cat", "Siamese_cat", "Egyptian_cat"]:
        print("Classification " + classification + " matches a cat!")
        if float(confidence) > 0.15:
            return "Yes, definitely a cat in this picture"
        else:
            return "There's probably a cat in this picture"
    else:
        print("Classification " + classification + " does not match a cat!")
        return "No, not a cat"

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/classify/")
@app.route("/classify/<filename>")
def classify(filename=None):
    if filename is None:
        return "<p>No picture to found to classify</p>"
    img = image.load_img(os.path.join('/tmp', filename), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    dpred = decode_predictions(preds, top=1)[0]
    predClass = str(dpred[0][1])
    predConfidence = str(dpred[0][2])

    cat = is_cat(predClass, predConfidence)
    return "<p>"+cat+"</p>" + "<p>Class: " + predClass + "</p><p>Confidence: " + predConfidence + "</p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'potential-cat-pic' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['potential-cat-pic']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/tmp', filename))
            s3.Bucket('cat-image-bucket').put_object(Key=filename, Body=file)
            return redirect(url_for('classify', filename=filename))
