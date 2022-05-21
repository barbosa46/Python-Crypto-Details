from sys import argv

from AESCipherByteArrayMixer import AESCipherByteArrayMixer
from ImageMixer import ImageMixer

def main(argv):
    if (len(argv) != 5):
        print("This program encrypts an image file with AES.");
        print("Usage: ImageAESCipher [inputFile.png] [AESKeyFile] [ECB|CBC|OFB] [outputFile.png]");
        return

    inputFile = argv[1]
    keyFile = argv[2]
    mode = argv[3]
    outputFile = argv[4]

    if mode != "ECB" and mode != "CBC" and mode != "OFB":
        print("The modes of operation must be ECB, CBC or OFB.");
        return
    
    cipher = AESCipherByteArrayMixer("Cipher.ENCRYPT_MODE")
    cipher.setParameters(keyFile, mode)
    ImageMixer.mix(inputFile, outputFile, cipher);
    
    print("Done.")


if __name__ == '__main__':
    main(argv)