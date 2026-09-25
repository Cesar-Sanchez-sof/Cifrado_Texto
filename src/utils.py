"""
=============================================================================
Capa de Utilidades: src/utils.py
Cálculo de Entropía de Shannon y Análisis Estructural de Bloques PKCS#7
=============================================================================
"""

import math
from typing import List
from src.models import DetalleBloque, AnalisisCriptografico


def calcular_entropia_shannon(datos: bytes) -> float:
    """
    Calcula la entropía de Shannon (en bits por byte).
    Una distribución perfectamente aleatoria e incompresible alcanza ~8.0 bits/byte.
    """
    if not datos:
        return 0.0

    frecuencias = {}
    for byte in datos:
        frecuencias[byte] = frecuencias.get(byte, 0) + 1

    entropia = 0.0
    longitud = len(datos)
    for conteo in frecuencias.values():
        probabilidad = conteo / longitud
        entropia -= probabilidad * math.log2(probabilidad)

    return entropia


def analizar_bloques_pkcs7(datos_originales: bytes, datos_rellenados: bytes, tamano_bloque: int) -> AnalisisCriptografico:
    """
    Desglosa el flujo de bytes rellenados con PKCS#7 en bloques individuales,
    identificando los bytes de información útil y los de relleno.
    """
    total_bloques = len(datos_rellenados) // tamano_bloque
    bytes_relleno_total = len(datos_rellenados) - len(datos_originales)
    bloques_detalle: List[DetalleBloque] = []

    for i in range(total_bloques):
        inicio = i * tamano_bloque
        fin = inicio + tamano_bloque
        fragmento = datos_rellenados[inicio:fin]

        # Determinar bytes originales vs bytes de relleno en este bloque
        if fin <= len(datos_originales):
            b_orig = tamano_bloque
            b_pad = 0
            es_pad = False
        elif inicio < len(datos_originales) < fin:
            b_orig = len(datos_originales) - inicio
            b_pad = tamano_bloque - b_orig
            es_pad = True
        else:
            b_orig = 0
            b_pad = tamano_bloque
            es_pad = True

        ascii_rep = "".join(chr(b) if 32 <= b <= 126 else "." for b in fragmento)

        bloques_detalle.append(DetalleBloque(
            indice=i + 1,
            bytes_hex=fragmento.hex().upper(),
            es_relleno_pkcs7=es_pad,
            bytes_originales=b_orig,
            bytes_relleno=b_pad,
            contenido_ascii=ascii_rep
        ))

    return AnalisisCriptografico(
        longitud_original_caracteres=len(datos_originales.decode('utf-8', errors='replace')),
        longitud_original_bytes=len(datos_originales),
        tamano_bloque_bytes=tamano_bloque,
        total_bloques=total_bloques,
        bytes_relleno_agregados=bytes_relleno_total,
        entropia_texto_plano=calcular_entropia_shannon(datos_originales),
        entropia_criptograma=0.0,
        desglose_bloques=bloques_detalle
    )
