"""
=============================================================================
Capa de Estrategias Criptográficas: src/strategies.py
Patrón Strategy para Algoritmos Simétricos (DES, 3DES, AES) en Modo CBC
=============================================================================
"""

import time
from abc import ABC, abstractmethod

# Librería oficial
from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from src.models import ResultadoOperacion
from src.utils import analizar_bloques_pkcs7, calcular_entropia_shannon


class EstrategiaCifrado(ABC):
    """Clase base abstracta (Estrategia) para cifrado simétrico en modo CBC."""

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre formal del algoritmo."""
        pass

    @property
    @abstractmethod
    def tamano_clave_bytes(self) -> int:
        """Longitud de clave requerida en bytes."""
        pass

    @property
    @abstractmethod
    def tamano_bloque_bytes(self) -> int:
        """Tamaño de bloque en bytes."""
        pass

    @abstractmethod
    def generar_clave(self) -> bytes:
        """Genera una clave aleatoria segura usando el CSPRNG del sistema operativo."""
        pass

    def generar_iv(self) -> bytes:
        """Genera un Vector de Inicialización (IV) aleatorio de longitud de bloque."""
        return get_random_bytes(self.tamano_bloque_bytes)

    @abstractmethod
    def crear_cifrador(self, clave: bytes, iv: bytes):
        """Instancia el objeto cifrador pycryptodome en modo CBC."""
        pass

    def procesar(self, texto_plano: str, clave_forzada: bytes = None, iv_forzado: bytes = None) -> ResultadoOperacion:
        """
        Ejecuta el ciclo completo de cifrado y descifrado con medición de tiempos,
        verificación de integridad y análisis de bloques.
        """
        clave = clave_forzada if clave_forzada is not None else self.generar_clave()
        iv = iv_forzado if iv_forzado is not None else self.generar_iv()

        datos_bytes = texto_plano.encode('utf-8')
        datos_pad = pad(datos_bytes, self.tamano_bloque_bytes)

        # 1. Cifrado en modo CBC
        cifrador = self.crear_cifrador(clave, iv)
        t0_cif = time.perf_counter_ns()
        texto_cifrado = cifrador.encrypt(datos_pad)
        t1_cif = time.perf_counter_ns()
        tiempo_cifrado_us = (t1_cif - t0_cif) / 1000.0

        # 2. Descifrado en modo CBC
        descifrador = self.crear_cifrador(clave, iv)
        t0_dec = time.perf_counter_ns()
        datos_descifrados_pad = descifrador.decrypt(texto_cifrado)
        datos_descifrados_bytes = unpad(datos_descifrados_pad, self.tamano_bloque_bytes)
        t1_dec = time.perf_counter_ns()
        tiempo_descifrado_us = (t1_dec - t0_dec) / 1000.0

        texto_descifrado = datos_descifrados_bytes.decode('utf-8')
        coincide = (texto_descifrado == texto_plano)

        # 3. Análisis de bloques y cálculo de entropía
        analisis = analizar_bloques_pkcs7(datos_bytes, datos_pad, self.tamano_bloque_bytes)
        analisis.entropia_criptograma = calcular_entropia_shannon(texto_cifrado)

        return ResultadoOperacion(
            algoritmo=self.nombre,
            texto_original=texto_plano,
            clave=clave,
            iv=iv,
            texto_cifrado=texto_cifrado,
            texto_descifrado=texto_descifrado,
            coincide=coincide,
            tiempo_cifrado_us=tiempo_cifrado_us,
            tiempo_descifrado_us=tiempo_descifrado_us,
            tamano_clave_bits=len(clave) * 8,
            tamano_bloque_bits=self.tamano_bloque_bytes * 8,
            analisis=analisis
        )


class CifradorDES(EstrategiaCifrado):
    """Estrategia para Data Encryption Standard (DES)."""

    @property
    def nombre(self) -> str:
        return "DES"

    @property
    def tamano_clave_bytes(self) -> int:
        return 8

    @property
    def tamano_bloque_bytes(self) -> int:
        return DES.block_size

    def generar_clave(self) -> bytes:
        return get_random_bytes(self.tamano_clave_bytes)

    def crear_cifrador(self, clave: bytes, iv: bytes):
        return DES.new(clave, DES.MODE_CBC, iv=iv)


class Cifrador3DES(EstrategiaCifrado):
    """Estrategia para Triple DES (3DES / TDEA) con ajuste de paridad."""

    @property
    def nombre(self) -> str:
        return "3DES"

    @property
    def tamano_clave_bytes(self) -> int:
        return 24

    @property
    def tamano_bloque_bytes(self) -> int:
        return DES3.block_size

    def generar_clave(self) -> bytes:
        clave_cruda = get_random_bytes(self.tamano_clave_bytes)
        return DES3.adjust_key_parity(clave_cruda)

    def crear_cifrador(self, clave: bytes, iv: bytes):
        return DES3.new(clave, DES3.MODE_CBC, iv=iv)


class CifradorAES(EstrategiaCifrado):
    """Estrategia para Advanced Encryption Standard (AES) con soporte para 128, 192 y 256 bits."""

    def __init__(self, tamano_clave_bits: int = 256):
        if tamano_clave_bits not in (128, 192, 256):
            raise ValueError(f"Longitud de clave inválida para AES: {tamano_clave_bits} bits.")
        self._tamano_clave_bits = tamano_clave_bits

    @property
    def nombre(self) -> str:
        return f"AES-{self._tamano_clave_bits}" if self._tamano_clave_bits != 256 else "AES"

    @property
    def tamano_clave_bytes(self) -> int:
        return self._tamano_clave_bits // 8

    @property
    def tamano_bloque_bytes(self) -> int:
        return AES.block_size

    def generar_clave(self) -> bytes:
        return get_random_bytes(self.tamano_clave_bytes)

    def crear_cifrador(self, clave: bytes, iv: bytes):
        return AES.new(clave, AES.MODE_CBC, iv=iv)
