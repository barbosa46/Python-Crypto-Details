from ast import Bytes

import imageio
import PIL.Image as Image
import random
import numpy as np
from random import randint

class ImageMixer(object):
    def __init__(self, *args):
        pass

    def createRandomImage(imageFilePath, width, height):
        imageArray = np.zeros((height, width, 4), dtype=np.uint8)

        image = ImageMixer.getImageFromArray(imageArray, width, height)
        image.save(imageFilePath)


    def getImageFromArray(imageArray, width, height):
        for x in range(width):
            for y in range(height):
                randomnumber = randint(0,1)
                if randomnumber == 1:
                    imageArray[x, y] = [0, 0, 0, 255]
                else:
                    imageArray[x, y] = [0,0,0,0]
        img = Image.fromarray(imageArray, 'RGBA')
        return img;

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