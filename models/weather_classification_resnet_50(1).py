# -*- coding: utf-8 -*-
"""weather_classification_resnet-50(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oSFmhD-dFmCkm3oApTH4pl60OooMTGhg
"""

from  google.colab import drive
import zipfile
drive.mount("/content/gdrive")

cd /content/gdrive/My\ Drive/

z=zipfile.ZipFile("Multi-class_Weather_Dataset.zip","r")
z.extractall("/tmp/")
z.close()

ls

ls/tmp/

ls/tmp/Multi-class_Weather_Dataset/Cloudy/cloudy1.jpg

#dependencies
import numpy as np
import cv2
import os
from imutils import paths
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
import tensorflow
from keras.applications.resnet50 import ResNet50, preprocess_input
import tensorflow.keras as keras
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D,Activation, MaxPooling3D, GlobalAveragePooling2D, GlobalAveragePooling3D, BatchNormalization
from keras.preprocessing import image
from keras.preprocessing.image import  ImageDataGenerator
from keras.layers import merge, Input
import random
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.optimizers import SGD,Adam
import numpy as np
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D,Activation
import time
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import  ImageDataGenerator
from keras.layers import merge, Input
from keras import regularizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import optimizers

path= "/tmp/Multi-class_Weather_Dataset/"

#global constants


num_classes = 4


channels = 3

image_resize = 224
resnet_50_pooling_avg = 'avg'
dense_layer_activation = 'softmax'
objective_function = 'categorical_crossentropy'
LOSS_METRICS = ['accuracy']
NUM_EPOCHS = 50
STEPS_PER_EPOCH_TRAINING = 10
STEPS_PER_EPOCH_VALIDATION = 10
BATCH_SIZE_TRAINING = 64
BATCH_SIZE_VALIDATION = 64

"""building model"""

model = Sequential()

# 1st layer as the lumpsum weights from resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5
# NOTE that this layer will be set below as NOT TRAINABLE, i.e., use it as is
model.add(ResNet50(include_top = False, pooling = resnet_50_pooling_avg ,weights='imagenet'))

# 2nd layer as Dense for 2-class classification, i.e., dog or cat using SoftMax activation
model.add(Dense(num_classes, activation = dense_layer_activation))

# Say not to train first layer (ResNet) model as it is already trained
model.layers[0].trainable = False

"""model summary"""

model.summary()

"""compile"""

model.compile(optimizer = 'sgd', loss =objective_function, metrics = LOSS_METRICS)

from keras.applications.resnet50 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator

image_size = image_resize

data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

"""train and validation data"""

train_generator = data_generator.flow_from_directory(path,
        target_size=(image_size, image_size),
        batch_size=BATCH_SIZE_TRAINING,
        class_mode='categorical')

validation_generator = data_generator.flow_from_directory(path,
        target_size=(image_size, image_size),
        batch_size=BATCH_SIZE_VALIDATION,
        class_mode='categorical')

"""checkpoint"""

from tensorflow.python.keras.callbacks import  ModelCheckpoint


cb_checkpointer = ModelCheckpoint(filepath = 'resnet_50.hdf5', monitor = 'val_loss', save_best_only = True, mode = 'auto')

"""training """

fit_history = model.fit_generator(
        train_generator,
        steps_per_epoch=STEPS_PER_EPOCH_TRAINING,
        epochs = NUM_EPOCHS,
        validation_data=validation_generator,
        validation_steps=STEPS_PER_EPOCH_VALIDATION,
        callbacks=[cb_checkpointer]
)
model.load_weights("resnet_50.hdf5")

"""accuracy and loss plots"""

import matplotlib.pyplot as plt
def show_history(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train_accuracy', 'test_accuracy'], loc='best')
    plt.show()

show_history(fit_history)

def show_history(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train_loss', 'test_loss'], loc='best')
    plt.show()

show_history(fit_history)

import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics import confusion_matrix

import numpy as np
from keras.models import load_model
from keras.preprocessing import image

ls/tmp/Multi-class_Weather_Dataset/

"""testing predictions"""

test_image = image.load_img(r'/tmp/Multi-class_Weather_Dataset/Sun_shine/shine109.jpg', target_size = (224, 224))

test_image = image.img_to_array(test_image)

test_image = np.expand_dims(test_image, axis = 0) #flattening
model=load_model('resnet_50.hdf5') #sending data to the model for preditiopn
result = model.predict(test_image)
print(result)

print('{:.4f}%'.format(result[0][0]*100 ))
print('{:.4f}%'.format(result[0][1]*100 ))
print('{:.4f}%'.format(result[0][2]*100 ))
print('{:.4f}%'.format(result[0][3]*100 ))

print(train_generator.class_indices)

if (result[0][0]*100) >= 50:
    prediction = 'Cloudy'
    print(prediction)
elif (result[0][1]*100) >= 50:
    prediction = 'Rain'
    print(prediction)
elif (result[0][2]*100) >= 50:
    prediction = 'Sun_shine'
    print(prediction)
elif (result[0][3]*100) >= 50:
    prediction = 'Sunrise'
    print(prediction)























