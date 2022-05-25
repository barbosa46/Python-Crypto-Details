from sys import argv
import base64

class base64_encode_decode:
    def encode(key):
        key = base64.b64encode(key)
        return key
    
    def decode(key):
        key = base64.b64decode(key)
        return key
