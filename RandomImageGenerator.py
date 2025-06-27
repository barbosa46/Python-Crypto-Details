from sys import argv
from PIL import Image
import numpy as np

def create_random_rgb_image(path, width, height):
    # Gera uma imagem RGB com valores aleatórios entre 0 e 255
    random_pixels = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(random_pixels, 'RGB')
    img.save(path)

def main(argv):
    if len(argv) != 4:
        print("Este programa gera uma imagem RGB aleatória (8 bits por canal)")
        print("Uso: python3 RandomImageGenerator.py <ficheiro.png> <largura> <altura>")
        return
    path = argv[1]
    width = int(argv[2])
    height = int(argv[3])
    create_random_rgb_image(path, width, height)

if __name__ == '__main__':
    main(argv)