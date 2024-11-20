import base64
import os
import time
from plotly import graph_objs as go
import io

class ImageService:
    # def __init__(self):
    #     self.output_folder = os.path.join(os.path.dirname(__file__), "../graph_images")
    #     os.makedirs(self.output_folder, exist_ok=True)

    # def save_fig_to_image(self, fig, filename):
    #     image_path = os.path.join(self.output_folder, filename)
    #     fig_object = go.Figure(fig)
    #     fig_object.write_image(image_path)
    #     time.sleep(1)
    #     return image_path

    @staticmethod
    def save_fig_to_image(fig):
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        base64_image = base64.b64encode(img_bytes.read()).decode('utf-8')
        return base64_image

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')