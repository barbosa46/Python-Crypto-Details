from ast import Bytes
import io
import random
import PIL.Image as Image
from click import File


class ImageMixer(object):
    def __init__(self, *args):
        pass

    def createRandomImage(imageFilePath, width, height):
        imageArray = Bytes(width*height);
        # generate random pixels on array
        # (we multiply by 2^8=256 because one byte equals 8 pixels)
        for i in range(0, width*height):
            imageArray = (Bytes)(random.random()*256)
        
        image = ImageMixer.getImageFromArray(imageArray, width, height)
        ImageMixer.writeImagetoFile(image, imageFilePath)
    
    
    def getImageFromArray(imageArray, width, height):        
        image = Image.open(io.BytesIO(imageArray))

       
    def writeImagetoFile(image, imageFilePath):
        outputFile = File(imageFilePath);     
        image.write(image, "png", outputFile)    