FROM tensorflow/tensorflow:latest

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# The pretrained model (ResNet50)
COPY resnet50_weights_tf_dim_ordering_tf_kernels.h5 /root/.keras/models/

# The imagenet classifications
COPY imagenet_class_index.json /root/.keras/models/

# Our application code
COPY app.py .

# Test data
COPY elephant.jpg .

CMD ["flask", "run", "--host=0.0.0.0"]
