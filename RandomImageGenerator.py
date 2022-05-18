from sys import argv
from ImageMixer import ImageMixer

class RandomImageGenerator:
    def run(argv):
        ImageMixer.createRandomImage(argv[1], int(argv[2]), int(argv[3]));

def main(argv):
    if (len(argv) != 4):
        print("This program generates a 1-bit image file with randomized pixels");
        print("Usage: randomImageGenerator <file.png> <height> <width>");
        return;
    RandomImageGenerator.run(argv);

if __name__ == '__main__':
    main(argv)