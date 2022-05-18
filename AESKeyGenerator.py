import base64
from sys import argv
from Crypto.Cipher import AES
from secrets import token_bytes

import keyring

class AESKeyGenerator:
    def write(keypath):
        ##get an AES private key
        print("Generating AES key ...")
        key = token_bytes(128)
        encoded = base64.b64encode(key);
        print( "Finish generating AES key" )
        f = open(keypath, "w+")
        print(key)
        print(encoded)
        f.write(str(encoded))
        f.close

    def read(keypath):
        print("Reading key from file " + keypath + " ...")
        f = open(keypath, "r")
        key_string = f.read()
        print(key_string)
        key = base64.b64decode(key_string)
        f.close
        print(key)
        return key
 
def main(argv):
    if (len(argv) != 3):
        print("Usage: AESKeyGenerator [r|w] <key-file>")
        return

    mode = argv[1]
    keyPath = argv[2]

    if (mode.lower() == "w"):
        print("Generate and save keys")
        AESKeyGenerator.write(keyPath)
    else:
        print("Load keys")
        AESKeyGenerator.read(keyPath)

    print("Done.")


if name == '__main__':
    main(argv)