from PIL import Image
from io import BytesIO

import base64
import numpy as np
import cv2

class painter(object):
    def __init__(self):
        pass

    def change_str(self, input_str):


        # convert it to a pil image
        input_img = self.base64_to_pil_image(input_str)

        ################## where the hard work is done ############
        # output_img is an PIL image
        output_img = self.transpose(input_img)

        # output_str is a base64 string in ascii
        output_str = self.pil_image_to_base64(output_img)

        #nparr = np.array(input_img)
        #img_np = cv2.cvtColor(nparr, cv2.COLOR_RGB2BGR)
        #print(img_np)

        return output_str

    def transpose(self, img):
        return img.transpose(Image.FLIP_LEFT_RIGHT)

    def pil_image_to_base64(self, pil_image):
        buf = BytesIO()
        pil_image.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue())


    def base64_to_pil_image(self, base64_img):
        return Image.open(BytesIO(base64.b64decode(base64_img)))
