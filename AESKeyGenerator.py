import base64
import os
from sys import argv

class AESKeyGenerator:
    def write(keypath):
        print("Generating AES key ...")
        key = os.urandom(16)
        print( "Finish generating AES key" )
        f = open(keypath, "wb")
        f.write(key)
        f.close
        
    def read(keypath):
        print("Reading key from file " + keypath + " ...")
        f = open(keypath, "rb")
        key = f.read()
        f.close
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


if __name__ == '__main__':
    main(argv)