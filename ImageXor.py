from sys import argv
from PIL import Image, ImageChops 
     

class ImageXor:
    def run(argv):
        im1 = Image.open(argv[1]) .convert("1")
        im2 = Image.open(argv[2]) .convert("1")
            
        im3 = ImageChops.logical_xor(im1, im2) 

        im3.save(argv[3])

def main(argv):
    if (len(argv) != 4):
        print("This program XORs two b/w image files.");
        print("Usage: imageXOR <inputFile1.png> <inputFile2.png> <outputFile.png>");
        return;
    ImageXor.run(argv);

if __name__ == '__main__':
    main(argv)









