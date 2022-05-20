from sys import argv
from AESCipherByteArrayMixer import AESCipherByteArrayMixer
from FileMixer import FileMixer


class FileAESDecipher:
    def run(argv):
        inputFile = argv[1]
        keyFile = argv[2]
        mode = argv[3].upper()
        outputFile = argv[4]
        if not (mode == "ECB" or mode == "CBC" or mode == "OFB"):
            print("The modes of operation must be ECB, CBC or OFB.")
            return

        cipher = AESCipherByteArrayMixer("Cipher.DECRYPT_MODE")
        cipher.setParameters(keyFile, mode)
        FileMixer.mix1(inputFile, outputFile, cipher)


def main(argv):
    if len(argv) != 5:
        print("This program decrypts a file with AES.")
        print("Usage: FileAESDecipher [inputFile] [AESKeyFile] [ECB|CBC|OFB] [outputFile]")
        return
    FileAESDecipher.run(argv)


if __name__ == '__main__':
    main(argv)
