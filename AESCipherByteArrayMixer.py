import sys
import traceback

from AESKeyGenerator import AESKeyGenerator
from Crypto.Cipher import AES


# import javax.crypto.Cipher;
# import javax.crypto.spec.IvParameterSpec;
# import java.security.Key;

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
        iv = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
        try:
            key = AESKeyGenerator.read(self.keyFile)

            match self.mode:
                case 'ECB':
                    cipher = AES.new(key, AES.MODE_ECB)
                case 'CBC':
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                case 'OFB':
                    cipher = AES.new(key, AES.MODE_OFB, iv)

            print("Ciphering ...")

            match self.opmode:
                case 'Cipher.ENCRYPT_MODE':
                    return cipher.encrypt(byteArray)
                case 'Cipher.DECRYPT_MODE':
                    return cipher.decrypt(byteArray)

        except Exception:
            traceback.print_exc(file=sys.stdout)
        return None

