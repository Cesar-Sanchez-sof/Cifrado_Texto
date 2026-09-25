"""
=============================================================================
Capa de Dominio: src/models.py
Modelos de Datos y Entidades Inmutables para Cifrado Simétrico
=============================================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class TipoAlgoritmo(Enum):
    """Enumeración de algoritmos criptográficos simétricos soportados."""
    DES = "DES"
    DES3 = "3DES"
    AES_128 = "AES-128"
    AES_192 = "AES-192"
    AES_256 = "AES-256"


@dataclass
class DetalleBloque:
    """Representa el análisis estructural de un bloque individual."""
    indice: int
    bytes_hex: str
    es_relleno_pkcs7: bool
    bytes_originales: int
    bytes_relleno: int
    contenido_ascii: str


@dataclass
class AnalisisCriptografico:
    """Métricas criptográficas de entropía y estructura de bloques."""
    longitud_original_caracteres: int
    longitud_original_bytes: int
    tamano_bloque_bytes: int
    total_bloques: int
    bytes_relleno_agregados: int
    entropia_texto_plano: float
    entropia_criptograma: float
    desglose_bloques: List[DetalleBloque] = field(default_factory=list)


@dataclass
class ResultadoOperacion:
    """Contenedor de resultados y métricas de una operación de cifrado y descifrado."""
    algoritmo: str
    texto_original: str
    clave: bytes
    iv: bytes
    texto_cifrado: bytes
    texto_descifrado: str
    coincide: bool
    tiempo_cifrado_us: float
    tiempo_descifrado_us: float
    tamano_clave_bits: int
    tamano_bloque_bits: int
    analisis: Optional[AnalisisCriptografico] = None

    @property
    def clave_hex(self) -> str:
        """Clave en formato hexadecimal en mayúsculas."""
        return self.clave.hex().upper()

    @property
    def iv_hex(self) -> str:
        """Vector de Inicialización en formato hexadecimal en mayúsculas."""
        return self.iv.hex().upper()

    @property
    def texto_cifrado_hex(self) -> str:
        """Criptograma en formato hexadecimal en mayúsculas."""
        return self.texto_cifrado.hex().upper()

    @property
    def tiempo_total_us(self) -> float:
        """Tiempo acumulado de cifrado + descifrado en microsegundos."""
        return self.tiempo_cifrado_us + self.tiempo_descifrado_us

    @property
    def tiempo_cifrado_ms(self) -> float:
        """Tiempo de cifrado en milisegundos."""
        return self.tiempo_cifrado_us / 1000.0

    @property
    def tiempo_descifrado_ms(self) -> float:
        """Tiempo de descifrado en milisegundos."""
        return self.tiempo_descifrado_us / 1000.0

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la entidad a diccionario compatible con JSON."""
        datos = {
            "algoritmo": self.algoritmo,
            "texto_original": self.texto_original,
            "clave_hex": self.clave_hex,
            "iv_hex": self.iv_hex,
            "texto_cifrado_hex": self.texto_cifrado_hex,
            "texto_descifrado": self.texto_descifrado,
            "coincide": self.coincide,
            "tamano_clave_bits": self.tamano_clave_bits,
            "tamano_bloque_bits": self.tamano_bloque_bits,
            "tiempo_cifrado_us": round(self.tiempo_cifrado_us, 2),
            "tiempo_descifrado_us": round(self.tiempo_descifrado_us, 2),
            "tiempo_total_us": round(self.tiempo_total_us, 2),
        }
        if self.analisis:
            datos["analisis"] = {
                "longitud_caracteres": self.analisis.longitud_original_caracteres,
                "longitud_bytes": self.analisis.longitud_original_bytes,
                "total_bloques": self.analisis.total_bloques,
                "bytes_relleno": self.analisis.bytes_relleno_agregados,
                "entropia_plano": round(self.analisis.entropia_texto_plano, 3),
                "entropia_criptograma": round(self.analisis.entropia_criptograma, 3),
                "bloques": [
                    {
                        "indice": b.indice,
                        "hex": b.bytes_hex,
                        "es_relleno": b.es_relleno_pkcs7,
                        "originales": b.bytes_originales,
                        "relleno": b.bytes_relleno,
                        "ascii": b.contenido_ascii
                    } for b in self.analisis.desglose_bloques
                ]
            }
        return datos
