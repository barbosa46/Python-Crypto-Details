from ast import Bytes
import imageio
import PIL.Image as Image
import numpy as np
from random import randint

class ImageMixer(object):
    def __init__(self, *args):
        pass
    
    @staticmethod
    def createRandomImage(imageFilePath, width, height):
        imageArray = np.zeros((height, width, 4), dtype=np.uint8)
        image = ImageMixer.getImageFromArray(imageArray, width, height)
        image.save(imageFilePath)
    
    @staticmethod
    def getImageFromArray(imageArray, width, height):
        for y in range(height):  # Corrigido: y para altura
            for x in range(width):  # Corrigido: x para largura
                randomnumber = randint(0, 1)
                if randomnumber == 1:
                    imageArray[y, x] = [0, 0, 0, 255]  # Preto opaco
                else:
                    imageArray[y, x] = [255, 255, 255, 0]  # Branco transparente
        img = Image.fromarray(imageArray, 'RGBA')
        return img
    
    @staticmethod
    def mix(inputFile, outputFile, manipulationFunction):
        # Abre a imagem original
        imagedesc = Image.open(inputFile)
        
        # Converte para RGBA se não estiver já
        if imagedesc.mode != 'RGBA':
            imagedesc = imagedesc.convert('RGBA')
        
        # Converte para array numpy
        image_array = np.array(imagedesc)
        
        # Converte para bytes
        imageBytes = image_array.tobytes()
        
        # Aplica a função de manipulação
        outputBytes = manipulationFunction.mix(imageBytes, None)
        
        # Reconstrói a imagem RGBA
        output_array = np.frombuffer(outputBytes, dtype=np.uint8)
        
        # Calcula o tamanho esperado da imagem
        expected_size = imagedesc.height * imagedesc.width * 4  # RGBA = 4 canais
        
        # Remove padding se necessário (comum em criptografia AES)
        if len(output_array) > expected_size:
            output_array = output_array[:expected_size]
        elif len(output_array) < expected_size:
            # Se for menor, pode ser que não tenha canal alpha, tenta como RGB
            expected_rgb_size = imagedesc.height * imagedesc.width * 3
            if len(output_array) == expected_rgb_size:
                output_array = output_array.reshape((imagedesc.height, imagedesc.width, 3))
                # Adiciona canal alpha (opacidade total)
                alpha_channel = np.full((imagedesc.height, imagedesc.width, 1), 255, dtype=np.uint8)
                output_array = np.concatenate([output_array, alpha_channel], axis=2)
                img = Image.fromarray(output_array, 'RGBA')
                img.save(outputFile)
                return img
        
        # Reshape para as dimensões corretas (altura, largura, 4 canais RGBA)
        try:
            output_array = output_array.reshape((imagedesc.height, imagedesc.width, 4))
            img = Image.fromarray(output_array, 'RGBA')
        except ValueError as e:
            print(f"Erro no reshape: {e}")
            print(f"Tamanho do array: {len(output_array)}, esperado: {expected_size}")
            print(f"Dimensões da imagem: {imagedesc.width}x{imagedesc.height}")
            
            # Última tentativa: trata como grayscale
            grayscale_size = imagedesc.height * imagedesc.width
            if len(output_array) >= grayscale_size:
                print("Tentando como grayscale...")
                gray_array = output_array[:grayscale_size].reshape((imagedesc.height, imagedesc.width))
                # Converte grayscale para RGBA
                output_array = np.stack([gray_array, gray_array, gray_array, 
                                       np.full_like(gray_array, 255)], axis=-1)
                img = Image.fromarray(output_array, 'RGBA')
            else:
                raise ValueError(f"Não foi possível processar o array de tamanho {len(output_array)}")
        
        # Salva a imagem
        img.save(outputFile)
        
        return img

# Exemplo de uso:
# ImageMixer.createRandomImage("random_image.png", 100, 100)
