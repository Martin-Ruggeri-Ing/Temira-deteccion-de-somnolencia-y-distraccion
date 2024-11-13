import rsa
import tempfile
import os
from paths import temp_csvs_path, claves_path

def generar_claves():
    clave_publica, clave_privada = rsa.newkeys(2048)
    return clave_publica, clave_privada

def guardar_claves(clave_publica, clave_privada):
    with open('clave_publica.pem', 'wb') as archivo:
        archivo.write(clave_publica.save_pkcs1())
    with open('clave_privada.pem', 'wb') as archivo:
        archivo.write(clave_privada.save_pkcs1())

def leer_clave(tipo):
    clave = None
    archivo_clave = os.path.join(claves_path, f'clave_{tipo}.pem')
    with open(archivo_clave, 'r') as archivo:
        clave = rsa.PrivateKey.load_pkcs1(archivo.read().encode()) if tipo == 'privada' else rsa.PublicKey.load_pkcs1(archivo.read().encode())
    return clave

def get_temp_path_encrypted_file(archivo_encriptado):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(archivo_encriptado.read())
        return temp_file.name

def get_temp_path_file(file_csv):
    temp_dir = os.path.join(os.getcwd(), temp_csvs_path)
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as temp_file:
        temp_file.write(file_csv)
        return temp_file.name

def desencriptar_archivo(clave_privada, archivo_encriptado):
    TAM_BLOQUE = 256  # Tamaño del bloque en bytes

    contenido_desencriptado = b""
    with open(archivo_encriptado, 'rb') as archivo:
        while True:
            bloque_encriptado = archivo.read(TAM_BLOQUE)
            if len(bloque_encriptado) == 0:
                break  # Se llegó al final del archivo encriptado

            bloque_desencriptado = rsa.decrypt(bloque_encriptado, clave_privada)
            contenido_desencriptado += bloque_desencriptado

    return contenido_desencriptado

def encriptar_archivo(clave_publica, file_csv):
    TAM_BLOQUE = 245  # Tamaño del bloque en bytes, ajustado para el padding
    temp_dir = os.path.join(os.getcwd(), 'temp_csvs_encripted')
    os.makedirs(temp_dir, exist_ok=True)
    encrypted_file_path = os.path.join(temp_dir, 'logs_enc.csv')

    with open(file_csv, 'rb') as archivo_csv:
        with open(encrypted_file_path, 'wb') as archivo_encriptado:
            while True:
                bloque = archivo_csv.read(TAM_BLOQUE)
                if len(bloque) == 0:
                    break  # Se llegó al final del archivo

                contenido_encriptado = rsa.encrypt(bloque, clave_publica)
                archivo_encriptado.write(contenido_encriptado)

