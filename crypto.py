import sys
import argparse
from cryptography.fernet import Fernet

#Function for generating an encryption keyFunction for generating an encryption key
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    print("key generated")

# Function to load the encryption key from a file
def load_key():
    try:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
            return key
    except FileNotFoundError:
        print("first you need a key please use the command 'generate-key'")
        sys.exit(1)

# Function to encrypt a file
def encrypt_file(filename, key):
    cipher_suite = Fernet(key)

    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            encrypted_data = cipher_suite.encrypt(file_data)

        with open(filename + '.enc', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print("successfully encrypted file: {}.enc".format(filename))
    except FileNotFoundError:
        print("no file found: {}".format(filename))
        sys.exit(1)

# Function to decrypt a file
def decrypt_file(filename, key):
    cipher_suite = Fernet(key)

    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            decrypted_data = cipher_suite.decrypt(file_data)

        with open(filename[:-4], 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print("successfully decrypted file: {}".format(filename[:-4]))
    except FileNotFoundError:
        print("no file found: {}".format(filename))
        sys.exit(1)

# Command handling
if len(sys.argv) == 1:
    print("python script.py <comand> <file>")
    print("generate-key, encrypt <file>, decrypt <file>")
    sys.exit(1)


parser = argparse.ArgumentParser(description="Script for encrypting and decrypting files")
subparsers = parser.add_subparsers(dest="command")


command = sys.argv[1]

if command == "generate-key":
    generate_key()
elif command == "encrypt":
    key = load_key()
    filename = sys.argv[2]
    encrypt_file(filename, key)
elif command == "decrypt":
    key = load_key()
    filename = sys.argv[2]
    decrypt_file(filename, key)
else:
    print("invalid command. Available commands: generate-key, encrypt <file>, decrypt <file>")
