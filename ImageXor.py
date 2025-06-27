from sys import argv
from PIL import Image
import numpy as np

class ImageXor:
    @staticmethod
    def run(argv):
        # Abrir ambas as imagens como RGB (3 canais)
        image1 = np.array(Image.open(argv[1]).convert("RGB"), dtype=np.uint8)
        image2 = np.array(Image.open(argv[2]).convert("RGB"), dtype=np.uint8)

        # Verificar se têm a mesma dimensão
        if image1.shape != image2.shape:
            raise ValueError("Erro: As imagens têm dimensões diferentes.")

        # Fazer XOR bit a bit
        xored = np.bitwise_xor(image1, image2)

        # Guardar o resultado como imagem RGB
        result = Image.fromarray(xored, 'RGB')
        result.save(argv[3])
        print(f"Imagem XOR guardada em: {argv[3]}")

def main(argv):
    if len(argv) != 4:
        print("Este programa faz XOR entre duas imagens RGB.")
        print("Uso: python3 ImageXor.py <input1.png> <input2.png> <output.png>")
        return
    ImageXor.run(argv)

if __name__ == '__main__':
    main(argv)