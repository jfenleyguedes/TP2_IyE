import sys
import pickle
import numpy as np
from PIL import Image
from funciones_auxiliares_tp2 import huffman_decode


def descomprimir(ruta_entrada, ruta_salida_png=None):
    with open(ruta_entrada, "rb") as f:
        encabezado = pickle.load(f) 
        datos_comprimidos = f.read()

    filas = encabezado["filas"]
    columnas = encabezado["columnas"]
    primera_columna = encabezado["primera_columna"]
    codigo = encabezado["codigo"]
    relleno = encabezado["relleno"]

    #Bytes -> cadena de bits, sacando el relleno agregado al comprimir
    bits = "".join(f"{byte:08b}" for byte in datos_comprimidos)
    if relleno:
        bits = bits[:-relleno]

    #Decodificar Huffman: bits -> lista de residuos
    residuos = huffman_decode(bits, codigo)
    residuos = np.array(residuos).reshape(filas, columnas - 1)

    #Reconstruir cada fila sumando los residuos: x[i,j] = x[i,j-1] + y[i,j]
    X = np.zeros((filas, columnas), dtype=int)
    X[:, 0] = primera_columna
    X[:, 1:] = np.array(primera_columna)[:, None] + np.cumsum(residuos, axis=1)

    imagen = Image.fromarray(X.astype(np.uint8), mode="L")

    if ruta_salida_png:
        imagen.save(ruta_salida_png)
        print(f"Imagen guardada en {ruta_salida_png}")
    else:
        imagen.show()


if __name__ == "__main__":
    #Si se pasan menos de 2 parámetros por la terminal (sys.argv es una lista con los armugentos pasados por terminal) muestra como se deberia utilizar el programa y termina
    if len(sys.argv) < 2:
        print("Uso: python descomprimir_tp2.py <archivo.tp2> [salida.png]")
        #El programa termina: el 1 es para indicar qe terminó con un error
        sys.exit(1)
    #Si se le pasó correctamente llama a la función y le pasa los parámetros correspondientes.
    descomprimir(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
