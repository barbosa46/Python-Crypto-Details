from sys import argv
from PIL import Image
import imageio.v2 as imageio
import numpy as np
class ImageXor:
    def R_to_RGBA(image, imagedesc):
        imageArray = np.zeros((imagedesc.width, imagedesc.height, 4), dtype=np.uint8)

        for i in range(imagedesc.width):
            for e in range(imagedesc.height):
                if (image[i][e]==0):
                    imageArray[i, e] = [0, 0, 0, 0]
                else:
                    imageArray[i, e] = [0, 0 , 0 , 255]
        return imageArray
        
    def run(argv):
        imagedesc = Image.open(argv[1])        
        image = imageio.imread(argv[1])
        image2desc = Image.open(argv[2])
        image2 = imageio.imread(argv[2])     
        
        if image[0][0].size == 1:
            image = ImageXor.R_to_RGBA(image, imagedesc)
        if image2[0][0].size == 1:    
            image2 = ImageXor.R_to_RGBA(image2, image2desc)

        outputImageArray = np.zeros((imagedesc.width, imagedesc.height, 4), dtype=np.uint8)
        for i in range(imagedesc.width):
            for e in range(imagedesc.height):
                if (image[i][e] == image2[i][e]).all():
                    outputImageArray[i][e] = [0, 0, 0, 0]
                else:
                    outputImageArray[i][e] = [0, 0 , 0 , 255]
        
        img = Image.fromarray(outputImageArray, 'RGBA')
        image = imageio.imwrite(argv[3], img)

def main(argv):
    if (len(argv) != 4):
        print("This program XORs two b/w image files.");
        print("Usage: imageXOR <inputFile1.png> <inputFile2.png> <outputFile.png>");
        return;
    ImageXor.run(argv);

if __name__ == '__main__':
    main(argv)