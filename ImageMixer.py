from ast import Bytes

import imageio
import PIL.Image as Image
import random

class ImageMixer(object):
    def __init__(self, *args):
        pass

    def createRandomImage(imageFilePath, width, height):
        imageArray = Bytes(width * height);
        # generate random pixels on array
        # (we multiply by 2^8=256 because one byte equals 8 pixels)
        for i in range(0, width * height):
            imageArray = (Bytes)(random.random() * 256)

        image = ImageMixer.getImageFromArray(imageArray, width, height)
        ImageMixer.writeImagetoFile(image, imageFilePath)


    def getImageFromArray(imageArray, width, height):
        return;

    def writeImagetoFile(image, imageFilePath):
        return;

    def mix(inputFile, outputFile, manipulationFunction):
        imagedesc = Image.open(inputFile)
        image = imageio.imread(inputFile)
        imageBytes = bytes(image)

        outputBytes = manipulationFunction.mix(imageBytes, None)

        img = Image.frombytes("L", (imagedesc.width, imagedesc.height), outputBytes)
        image = imageio.imwrite(outputFile, img)

        '''ImageMixer.getImageFromArray(outputBytes, image.getWidth(), image.getHeight());
        ImageMixer.writeImageToFile(outputImage, outputFile);'''
        return;