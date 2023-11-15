Instituto Superior Técnico, Universidade de Lisboa

**Network and Computer Security**

# Lab guide: Python Cryptographic Subtleties

## Goals

- Use the cryptographic mechanisms available in the Python platform.
- See the difference between Python and Java in terms of cryptography.

## Introduction

This laboratory assignment uses Python version 3 or later running on Linux or Windows (wsl2) and it is a rebuild of a Java cryptography assignment but using the Python language and its mechanisms.

The Python language includes a large set of libraries that provide tools that can be used for the implementation of security, mechanisms and protocols. So, by using these types of libraries we can easily implement many things we can think in the cryptography world.

Throughout this assignment we can see these libraries in action for random number generation and key generation. The second one generates keys that can be used to create certificates and to make digital signatures or to simply encrypt files using asymmetric keys or symmetric keys depending on the situation.

## Setup

Before starting this assignment you will need a few steps to be able to investigate the cryptography mechanisms in the Python language:

- At first you will need to install python:

```bash
$ sudo apt-get install python3
```

- Then you will need to clone this repository into your workspace

```bash
$ git clone https://github.com/tecnico-sec/Python-Crypto.git
```

or via SSH

```bash
$ git clone git@github.com:tecnico-sec/Python-Crypto.git
```

In order to continue this assignment using native *Windows* python you need to install the following packages using "pip". To install "pip" in *Windows* follow these steps:

```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
```

After that you will need to install a few libraries.

- Libraries that need to be installed (Windows or Linux):

The Python Imaging Library adds image processing capabilities to your Python interpreter.
This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.
The core image library is designed for fast access to data stored in a few basic pixel formats. It should provide a solid foundation for a general image processing tool.

```bash
$ pip install Pillow
```

Imageio is a Python library that provides an easy interface to read and write a wide range of image data, including animated images, volumetric data, and scientific formats. It is cross-platform, runs on Python 3.5+, and it is easy to install.

```bash
$ pip install imageio
```

Numpy provides a powerful N-dimensional array object, sophisticated (broadcasting) functions, useful linear algebra, Fourier transform, and random number capabilities, and much more.

```bash
$ pip install numpy
```

Cryptography is a package which provides cryptographic recipes and primitives to Python developers.
Cryptography includes both high level recipes and low level interfaces to common cryptographic algorithms such as symmetric ciphers, message digests, and key derivation functions.

```bash
$ pip install cryptography
```

PyCryptodome is a self-contained Python package of low-level cryptographic primitives. Avoid having pycrypto and pycryptodome installed at the same time, as they will interfere with each other.

```bash
$ pip install pycryptodome
```

## Image Files

The cryptographic operations will be applied to image files, so that its results can be "seen". In the directory intro/inputs, you can find three different images:

- Tecnico: *.png, the IST logo
- Tux: *.png, Tux, the Linux penguin
- Glider: *.png, the hacker emblem (http://www.catb.org/hacker-emblem/)

Each one is presented with three different dimensions: 480x480, 960x960, and 2400x2400. The resolution number is part of the file name. The ImageMixer class is available to facilitate the operations on images. Different code examples are available, such as the RandomImageGenerator, ImageXor, and ImageAESCipher classes.

Create a folder named intro/outputs:

```bash
$ mkdir /intro/outputs
```

### One-Time Pads (Symmetric stream cipher)

If they could be correctly used in practice, one-time pads would provide perfect security.
One of the constraints to make them work as expected is that the key stream must never be reused.
The following steps visually illustrate what happens if they are reused, even if just once:

Generate a new 480x480 random image:

```bash
$ python3 RandomImageGenerator.py intro/outputs/otp.png 480 480
```

Perform the bitwise eXclusive OR operation (XOR) with the generated key:

```bash
$ python3 ImageXor.py intro/inputs/tecnico-0480.png intro/outputs/otp.png intro/outputs/encrypted-tecnico.png
```

XOR tux-0480.png with the same generated key:
```bash
$ python3 ImageXor.py intro/inputs/tux-0480.png intro/outputs/otp.png intro/outputs/encrypted-tux.png
```

Watch the images `encrypted-tecnico.png` and `encrypted-tux.png`.
Switch between them and see the differences.

To make the differences obvious, XOR them together:

```bash
$ python3 ImageXor.py intro/outputs/encrypted-tecnico.png intro/outputs/encrypted-tux.png intro/outputs/tecnico-tux.png
```

You can see that the reuse of a one-time pad (or any stream cipher key at all) considerably weakens (or completely breaks) the security of the information.
The reason is the following:         

```
C1 = M1 ⊕ K

C2 = M2 ⊕ K

C1 ⊕ C2 = M1 ⊕ M2
```

Legend: C stands for cipher-text, M for plain-text, K for key, ⊕ for XOR

The result you get is the XOR of the images. 
You can experiment with other images and sizes.


### Block cipher modes

Now that you know that keys should never be reused, remember that the way you use them is also important. 

We will use a symmetric-key encryption algorithm working in blocks to encrypt the pixels from an image.
We will use different modes, namely:
ECB (Electronic Code Book), CBC (Cipher Block Chaining) and OFB (Output FeedBack).


#### ECB (Electronic Code Book)

In the ECB mode, each block is independently encrypted with the key:

```
C[i] = E_k(M[i])
```

![ECB](ECB.png)

Begin by generating a new AES Key:

```bash
$ python3 AESKeyGenerator.py w intro/outputs/aes.key
```

Then, encrypt the glider image with it:

```bash
$ python3 ImageAESCipher.py intro/inputs/glider-0480.png intro/outputs/aes.key ECB intro/outputs/glider-aes-ecb.png
```

Watch the output image. 
Remember what you have just done: encrypted the image with AES, using ECB mode, and a key you generated yourself.

Try the same thing with the other images (especially with other sizes).

Try to generate a new AES key.
What is necessary to change in the code for that to happen?
<!-- Since we use a random function you only need to delete the previous AES key and run the code again. -->

Repeat all the previous steps for the new key.

Compare the results obtained using ECB mode with AES with the previous ones. 
What are the differences between them?
<!-- Each new ECB block is different from the previous one since the key is different -->


#### CBC (Cipher Block Chaining)

In CBC mode, each block M[i] is XORed with the ciphertext from the previous block, and then encrypted with key k: 

```
C[i] = E_k (M[i] ⊕ C[i-1])
```

![CBC](CBC.png)

The encryption of the first block can be performed by means of a random and unique value known as the _Initialization Vector_ (IV). 

The AES key will be the same from the previous step.

Encrypt the glider image with it, this time replacing ECB with CBC:

```bash
$ python3 ImageAESCipher.py intro/inputs/glider-0480.png intro/outputs/aes.key CBC intro/outputs/glider-aes-cbc.png
```

Watch the file glider-aes-cbc.png. 
See the difference made by changing only the mode of operation.

Still in the CBC mode, you might have wondered why the IV is needed in the first block. 
Consider what happens when you encrypt two different images with similar beginnings, and with the same key: the initial cipher text blocks would also be similar!

The ImageAESCipher class provided has been deliberately weakened: instead of randomizing the IV, it is always the same.

This time, encrypt the other two images with AES/CBC, still using the same AES key:

```bash
$ python3 ImageAESCipher.py intro/inputs/tux-0480.png intro/outputs/aes.key CBC intro/outputs/tux-aes-cbc.png

$ python3 ImageAESCipher.py intro/inputs/tecnico-0480.png intro/outputs/aes.key CBC intro/outputs/tecnico-aes-cbc.png
```

Now watch the images glider-aes-cbc.png, tux-aes-cbc.png, and tecnico-aes-cbc.png.
Look to the first lines of pixels. 
Can you see what is going on?

<!-- The first lines of pixels are equal due to the initialization block being equal to both -->

#### OFB

In the OFB mode, the IV is encrypted with the key to make a keystream that is then XORed with the plaintext to make the cipher text.

![OFB](OFB.png)

In practice, the keystream of the OFB mode can be seen as the one-time pad that is used to encrypt a message. 
This implies that in OFB mode, if the key and the IV are both reused, there is no security.

Encrypt the images with OFB:

```bash
$ python3 ImageAESCipher.py intro/inputs/glider-0480.png intro/outputs/aes.key OFB intro/outputs/glider-aes-ofb.png

$ python3 ImageAESCipher.py intro/inputs/tux-0480.png intro/outputs/aes.key OFB intro/outputs/tux-aes-ofb.png

$ python3 ImageAESCipher.py intro/inputs/tecnico-0480.png intro/outputs/aes.key OFB intro/outputs/tecnico-aes-ofb.png
```

Remember that the ImageAESCipher implementation has been weakened, by having a null IV, and you are reusing the same AES key. 
Watch the generated images and switch quickly between them.

Take two images (e.g., image1 and image2) and cipher them both. 
XOR image1 with the ciphered image2. 
What did you obtain? 
Why?

What is more secure to use: CBC or OFB?

<!-- OFB because it is ciphering the initial vector -->

### Asymmetric ciphers

The goal now is to use asymmetric ciphers, with separate private and public keys.
RSA is the most well known of these algorithms.

#### Generating a pair of keys with OpenSSL

Generate the key pair:

```bash
$ openssl genrsa -out intro/outputs/server.key
```

Save the public key:

```bash
$ openssl rsa -in intro/outputs/server.key -pubout > intro/outputs/public.key
```


#### Generating a self-signed certificate

Create a Certificate Signing Request, using same key:

```bash
$ openssl req -new -key intro/outputs/server.key -out intro/outputs/server.csr
```

Self-sign:

```bash
$ openssl x509 -req -days 365 -in intro/outputs/server.csr -signkey intro/outputs/server.key -out intro/outputs/server.crt
```

For our certificate to be able to sign other certificates, OpenSSL requires that a database exists (a .srl file). 
Create it:

```bash
$ echo 01 > intro/outputs/server.srl
```


Then, generating a key for a user is basically repeating the same steps (see commands above), except that the self-sign no longer happens and is replaced by:

```bash
$ openssl x509 -req -days 365 -in intro/outputs/user.csr -CA intro/outputs/server.crt -CAkey intro/outputs/server.key -out intro/outputs/user.crt
```

Sign the file grades.txt with the user certificate:

```bash
$ openssl dgst -sha256 grades/inputs/grades.txt > intro/outputs/grades.sha256

$ openssl rsautl -sign -inkey intro/outputs/user.key -keyform PEM -in intro/outputs/grades.sha256 > intro/outputs/grades.sig
```


Verify the signature with the user key:

```bash
$ openssl rsautl -verify -in intro/outputs/grades.sig -inkey intro/outputs/user.key

SHA256(/tmp/sirs/grades/inputs/grades.txt)= 770ddfe97cd0e6d279b9ce780ff060554d8ccbe4b8eccaed364a8fc6e89fd34d
```

and should always match this:

```bash
$ openssl dgst -sha256 grades/inputs/grades.txt

SHA256(/tmp/sirs/grades/inputs/grades.txt)= 770ddfe97cd0e6d279b9ce780ff060554d8ccbe4b8eccaed364a8fc6e89fd34d
```

user.crt: OK



#### Reading the generated pair of keys with Python

To read the generated keys in Python it is necessary to convert them to the right format.

Convert server.key to .pem

```bash
$ openssl rsa -in intro/outputs/server.key -text > private_key.pem
```

Convert private Key to PKCS#8 format (so Python can read it)

```bash
$ openssl pkcs8 -topk8 -inform PEM -outform DER -in private_key.pem -out private_key.der -nocrypt
```

Output public key portion in DER format (so Python can read it)

```bash
$ openssl rsa -in private_key.pem -pubout -outform DER -out public_key.der
```

Read the key files using the following command:

```bash
$ python3 RSAKeyGenerator.py r private_key.der public_key.der
```

#### Generating a pair of keys with Python

Generate a new pair of RSA Keys.

```bash
$ python3 RSAKeyGenerator.py w intro/outputs/private_key.key intro/outputs/public_key.key
```

Based on the ImageAESCipher class create ImageRSACipher and ImageRSADecipher classes.

Encrypt the image with the public key and then decrypt it with the private key.
Try the same thing with the other images - especially with other sizes.

Please consider that the RSA cipher, as implemented by Python, can only be applied to one block of data at a time, and its size depends on the size of the key. 
For a 1024-bit key the block size is 117 bytes or 60 bytes, depending on the padding options. 
This is acceptable because the RSA cipher is mostly used to cipher keys or hashes that are small. 
For large data, hybrid cipher is most suited (combining RSA with AES, for example). 
For this exercise you can cipher one block at a time.


### Additional exercise (file tampering)

In the directory grades/inputs, you can find the file grades.txt, the plaintext of a file with the grades of a course.
This flat-file database has a rigid structure: 64 bytes for name, and 16 bytes for each of the other fields, number, age and grade. Unfortunately, you happen to be _Mr. Thomas S. Cook_, and your grade was not on par with the rest of your class because you studied for a different exam...

Begin by encrypting this file into ecb.aes. 
For this example, we will still reuse the AES key generated above and ECB mode.

```bash
$ python3 FileAESCipher.py grades/inputs/grades.txt intro/outputs/aes.key ECB intro/outputs/grades.ecb.aes
```

Keeping in mind how the mode operations work, and without using the secret key, try to change your grade to 21 in the encrypted files or give everyone in class a 20.
(Why 21 or all 20s? Because you are an _ethical hacker_ using your skills to show that the system is vulnerable, not perform actual cheating.)

Did you succeed? 
Did your changes have side effects?

Now try to attack cbc.aes and ofb.aes. For this example, we will still reuse the AES key generated above but use the CBC and OFB modes.

```bash
$ python3 FileAESCipher.py grades/inputs/grades.txt intro/outputs/aes.key CBC intro/outputs/grades.cbc.aes

$ python3 FileAESCipher.py grades/inputs/grades.txt intro/outputs/aes.key OFB intro/outputs/grades.ofb.aes
```

How do you compare the results with ECB?

Since the inputs and outputs of cryptographic mechanisms are byte arrays, in many occasions it is necessary to represent encrypted data in text files. 
A possibility is to use base 64 encoding that, for every binary sequence of 6 bits, assigns a predefined ASCII character.
Execute the following to create a base 64 representation of files previously generated.

MP - error - python.exe: can't open file 'C:\\dev\\SIRS\\Python-Crypto\\Base64Encode.py': [Errno 2] No such file or directory

```bash
$ python3 Base64Encode.py grades/outputs/grades.cbc.aes grades/outputs/grades.cbc.aes.b64
```

Decode them:

```bash
$ python3 Base64Decode.py grades/outputs/grades.cbc.aes.b64 grades/outputs/grades.cbc.aes.b64.decoded
```

Check if they are similar using the diff command (or fc /b command on Windows):

```bash
$ diff grades/outputs/grades.cbc.aes grades/outputs/grades.cbc.aes.b64.decoded
```

It should not return anything.

Check the difference on the file sizes. 
Can you explain it? 
In percentage, how much is it?

Does base 64 provide any kind of security? 
If so, how?

----
