from PIL import Image
# from vietocr.tool.predictor import Predictor
# from vietocr.tool.config import Cfg
from CommonAssit.FileManager import *
import cv2 as cv

class Viet_OCR:

    def __init__(self, model="seq2seq",
                 weight_file=r"D:\Working\Code\Vision_Base\Modules\Viet_OCR\viet_ocr_wieght_origin\transformerocr.pth",
                 pretrained=False, device="cpu", beamsearch=False, vocab_file_path=""):
        self.detector = self.create_detector(model=model, weight_file=weight_file, vocab_file_path =vocab_file_path,
                                        pretrained=pretrained, device=device, beamsearch=beamsearch)

    def create_detector(self, model="vgg_seq2seq", weight_file="", pretrained=False, device="cpu", beamsearch=False,
                        vocab_file_path=""):

        config = Cfg.load_config_from_name(model)
        if vocab_file_path != "":
            vocab_file = TextFile(vocab_file_path)
            try:
                vocab = vocab_file.readFile()[0] + "\r\n"
                config["vocab"] = vocab
            except:
                vocab = ""
        config['weights'] = weight_file
        # config['weights'] = 'https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA'
        config['cnn']['pretrained'] = pretrained
        config['device'] = device
        config['predictor']['beamsearch'] = beamsearch

        try:
            detector = Predictor(config)
            return detector
        except Exception as error:
            print(error)
            return None

    def read_from_image(self, image):
        text = self.detector.predict(image)
        return text

if __name__ == '__main__':
    viet_ocr = Viet_OCR(model="vgg_transformer",
                        weight_file=r"D:\Working\Code\Vision_Base\Modules\Viet_OCR\viet_ocr_wieght_origin\transformerocr.pth",
                        pretrained=False, device="cpu", beamsearch=False)
    image_path = r"D:\Working\Code\Viet_OCR_Study\ink_dataset\train_image\20151111_0049_25439_1_tg_5_7.png"
    image = cv.imread(image_path)
    print(viet_ocr.read_from_image(Image.fromarray(image)))