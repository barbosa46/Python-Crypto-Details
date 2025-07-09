import base64
import sys

class base64_encode_decode:
    def encode(data):
        return base64.b64encode(data)

    def decode(data):
        return base64.b64decode(data)


def encode_file(input_path, output_path):
    with open(input_path, "rb") as f_in:
        data = f_in.read()
        encoded = base64.b64encode(data)
    with open(output_path, "wb") as f_out:
        f_out.write(encoded)

def decode_file(input_path, output_path):
    with open(input_path, "rb") as f_in:
        data = f_in.read()
        decoded = base64.b64decode(data)
    with open(output_path, "wb") as f_out:
        f_out.write(decoded)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python base64_encode_decode.py <encode|decode> <input_file> <output_file>")
        sys.exit(1)
    
    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == "encode":
        encode_file(input_file, output_file)
    elif mode == "decode":
        decode_file(input_file, output_file)
    else:
        print("Modo inválido. Use 'encode' ou 'decode'.")
        sys.exit(1)
