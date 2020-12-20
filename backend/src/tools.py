import os
import urllib
import urllib.request
import random
import string
import base64
import shutil

from mimetypes import guess_extension, guess_type
import tempfile

from keras.models import Sequential,Model
from keras.applications import ResNet50, ResNet152V2
from keras.applications.resnet50 import preprocess_input,decode_predictions
from keras.layers import GlobalAveragePooling2D, Dense,Dropout
from enum import Enum

class Helper:
    @staticmethod
    def get_base64_image_by_urls(image_urls):
        images_result = {}
        for image_url in image_urls:
            images_result[image_url] = Helper.get_base64_image_by_url(image_url)
        return images_result

    @staticmethod
    def get_base64_image_by_url(image_url):
        #NamedTemporaryFile  has not been used because of a problem with access rights.
        temp_file = os.path.join(os.getcwd(), Helper.generate_name() + "/" + Helper.generate_name())
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)
        urllib.request.urlretrieve(image_url, temp_file)
        with open(temp_file, 'rb') as read_file:
                image_string = base64.b64encode(read_file.read())
        shutil.rmtree(os.path.dirname(temp_file))
        return image_string.decode("utf-8")

    @staticmethod
    def get_fixed_base64_images_by_dict(base64_images):
        images_to_predict = {}
        for img_key, img_data in base64_images.items():
            ext = guess_extension(guess_type(img_data)[0])
            with tempfile.TemporaryDirectory() as dir:
                local_full_path_file = os.path.join(dir, "{0}{1}".format(Helper.generate_name(), ext))
                exts = ["jpeg", "jpg", "png", "gif", "tiff"]
                for ext in exts:
                    img_data = img_data.replace("data:image/{0};base64,".format(ext), "")
                with open(local_full_path_file, "wb") as fh:
                    fh.write(base64.decodestring(img_data.encode()))
                
                with open(local_full_path_file, 'rb') as read_file:
                    image_string = base64.b64encode(read_file.read())

            image_string = image_string.decode("utf-8")
            images_to_predict[img_key] = image_string
        return images_to_predict



    @staticmethod
    def generate(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    @staticmethod
    def generate_name(size=6, chars=string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))
    

class ModelType(Enum):
    RESNET50 = 1
    RESNET150 = 2

class ModelLoader(object):
    def load(self, model_path, number_classes = 3, resnet_type = ModelType.RESNET50):

        if not os.path.isfile(model_path):
            raise Exception("model with '{0}'  path not found".format(model_path))

        base_model = None
        
        if resnet_type == ModelType.RESNET150:
            base_model = ResNet152V2(weights="imagenet",include_top=False)
        elif resnet_type == ModelType.RESNET50:
            base_model = ResNet50(weights="imagenet",include_top=False)

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1000,activation="relu")(x)
        x = Dropout(0.5)(x)
        pred = Dense(number_classes,activation="softmax")(x)
        model = Model(inputs=base_model.input, outputs=pred)
        model.load_weights(model_path)
        return model


