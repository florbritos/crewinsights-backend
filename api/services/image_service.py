import base64
import io

class ImageService:
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