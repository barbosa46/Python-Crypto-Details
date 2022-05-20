import sys
import traceback

from AESKeyGenerator import AESKeyGenerator
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

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
        iv = '0000000000000000'
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
                return cipher.encrypt(pad(byteArray.decode("utf-8")).encode("utf-8"))
            elif self.opmode == 'Cipher.DECRYPT_MODE':
                return unpad(cipher.decrypt(byteArray).decode("utf-8"))

        except Exception:
            traceback.print_exc(file=sys.stdout)
        return None
