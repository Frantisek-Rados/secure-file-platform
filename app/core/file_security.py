from cryptography.fernet import Fernet

# vygenerovaný key
SECRET_FILE_KEY = b'ISLC0mMwj1P-BnNvpsgibi-uDFs0L6CBUv1U8PyjEis='

fernet = Fernet(SECRET_FILE_KEY)


def encrypt_data(data: bytes):
    return fernet.encrypt(data)


def decrypt_data(data: bytes):
    return fernet.decrypt(data)