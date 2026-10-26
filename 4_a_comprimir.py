import sys
import pickle
import numpy as np
from PIL import Image
from funciones_auxiliares_tp2 import huffman_code


def comprimir(ruta_entrada, ruta_salida=None):
    if ruta_salida is None:
        ruta_salida = ruta_entrada.rsplit(".", 1)[0] + ".tp2"

    img = Image.open(ruta_entrada).convert("L") #Abrir la imagen en escala de grises
    X = np.array(img, dtype=int)
    filas, columnas = X.shape
    primera_columna = X[:, 0].tolist()
    residuos = (X[:, 1:] - X[:, :-1]).flatten().tolist()

    #Probabilidades de los residuos y codigo de Huffman
    valores, cuentas = np.unique(residuos, return_counts=True)
    probabilidades = {int(v): int(c) / len(residuos) for v, c in zip(valores, cuentas)}
    codigo = huffman_code(probabilidades)
    bits = "".join(codigo[r] for r in residuos) #Codificar todos los residuos como una cadena de bits 0 y 1

    #Completar con ceros hasta un multiplo de 8 y pasar a bytes de a 8 bits
    relleno = (8 - len(bits) % 8) % 8
    bits += "0" * relleno
    datos_comprimidos = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))

    encabezado = {
        "filas": filas,
        "columnas": columnas,
        "primera_columna": primera_columna,
        "codigo": codigo,
        "relleno": relleno,
    }
    with open(ruta_salida, "wb") as f:
        pickle.dump(encabezado, f)   #Guarda el encabezado (incluye el codigo de Huffman)
        f.write(datos_comprimidos)   #Y los residuos ya codificados

    print(f"{ruta_entrada} -> {ruta_salida}  ({filas}x{columnas} px)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python comprimir_tp2.py <imagen.jpg|png> [salida.tp2]")
        sys.exit(1)
    comprimir(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)