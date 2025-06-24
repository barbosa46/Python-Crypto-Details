from sys import argv
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64_encode_decode import base64_encode_decode

class RSAKeyGenerator:

    def write(priv_keypath, pub_keypath):

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024,)

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        private_key_encoded = base64_encode_decode.encode(private_pem)

        with open(priv_keypath, 'wb') as f:
            f.write(private_key_encoded)

        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
        with open(pub_keypath, 'wb') as f:
            f.write(public_pem)

    def read(priv_keyPath, pub_keyPath):
        f = open(priv_keyPath, "rb")
        key_encoded = f.read()
        private_key_decoded = base64_encode_decode.decode(key_encoded)
        print("Private RSA Key:")
        print(private_key_decoded)

        print("\n")

        print("Public RSA Key:")
        f = open(pub_keyPath, "rb")
        pub_key = f.read()
        print(pub_key)


def main(argv):
    if (len(argv) != 4):
        print("Usage: RSAKeyGenerator.py [r|w] <priv-key-file>.pem <pub-key-file>.pem")
        print("Do not ever share your private keys.")
        return

    mode = argv[1]
    priv_keyPath = argv[2]
    pub_keyPath = argv[3]

    if (mode.lower() == "w"):
        print("Generating and saving keys")
        RSAKeyGenerator.write(priv_keyPath, pub_keyPath)
    else:
        RSAKeyGenerator.read(priv_keyPath, pub_keyPath)

    print("Done.")

if __name__ == '__main__':
    main(argv)
