import sys
import traceback

from AESKeyGenerator import AESKeyGenerator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipherByteArrayMixer:
    def __init__(self, opmode):
        self.opmode = opmode  # ENCRYPT DECRYPT
        self.keyFile = None
        self.mode = None  # CBC OFB ECB

    def setParameters(self, keyfile, mode):
        self.keyFile = keyfile
        self.mode = mode

    def mix(self, byteArray, byteArray2):
        global cipher
        iv = b'0000000000000000'
        try:
            key = AESKeyGenerator.read(self.keyFile)


            if self.mode == 'ECB':
                cipher = AES.new(key, AES.MODE_ECB)
            elif self.mode == 'CBC':
                cipher = AES.new(key, AES.MODE_CBC, iv)
            elif self.mode == 'OFB':
                cipher = AES.new(key, AES.MODE_OFB, iv)

            print("Ciphering ...")

            if self.opmode == 'Cipher.ENCRYPT_MODE':
                return cipher.encrypt(pad(byteArray,16))
            elif self.opmode == 'Cipher.DECRYPT_MODE':
                return unpad(cipher.decrypt(byteArray), 16)

        except Exception:
            traceback.print_exc(file=sys.stdout)
        return None