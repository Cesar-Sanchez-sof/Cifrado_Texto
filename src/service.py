"""
=============================================================================
Capa de Servicios: src/service.py
Fachada y Orquestador de Operaciones Criptográficas y Simulación de Fallas
=============================================================================
"""

from typing import List, Dict, Any
from Crypto.Util.Padding import unpad

from src.models import ResultadoOperacion
from src.strategies import EstrategiaCifrado, CifradorDES, Cifrador3DES, CifradorAES


class ServicioCriptografico:
    """
    Servicio principal que expone los casos de uso del sistema criptográfico:
    - Cifrado y descifrado individual.
    - Comparativa simultánea de los tres algoritmos.
    - Simulación didáctica de corrupción de clave y vector de inicialización (IV).
    """

    _estrategias: Dict[str, EstrategiaCifrado] = {
        "DES": CifradorDES(),
        "3DES": Cifrador3DES(),
        "AES": CifradorAES(256),
        "AES-128": CifradorAES(128),
        "AES-192": CifradorAES(192),
        "AES-256": CifradorAES(256),
    }

    @classmethod
    def obtener_estrategia(cls, nombre: str) -> EstrategiaCifrado:
        """Obtiene la estrategia correspondiente o lanza ValueError."""
        clave = nombre.upper().strip()
        if clave in cls._estrategias:
            return cls._estrategias[clave]
        raise ValueError(f"Algoritmo '{nombre}' no reconocido. Opciones válidas: DES, 3DES, AES")

    @classmethod
    def cifrar_y_descifrar(cls, texto: str, algoritmo: str) -> ResultadoOperacion:
        """Ejecuta el ciclo de cifrado y descifrado para un algoritmo específico."""
        estrategia = cls.obtener_estrategia(algoritmo)
        return estrategia.procesar(texto)

    @classmethod
    def comparar_todos(cls, texto: str) -> List[ResultadoOperacion]:
        """Ejecuta DES, 3DES y AES consecutivamente para generar la comparativa."""
        return [
            cls.cifrar_y_descifrar(texto, "DES"),
            cls.cifrar_y_descifrar(texto, "3DES"),
            cls.cifrar_y_descifrar(texto, "AES")
        ]

    @classmethod
    def simular_fallos_seguridad(cls, resultado_original: ResultadoOperacion) -> Dict[str, Any]:
        """
        Simula las dos condiciones de falla de la Sección 6:
        1. Descifrado con clave secreta incorrecta.
        2. Descifrado con Vector de Inicialización (IV) alterado.
        """
        estrategia = cls.obtener_estrategia(resultado_original.algoritmo)
        tamano_bloque = estrategia.tamano_bloque_bytes

        # Caso 1: Clave Incorrecta
        clave_falsa = estrategia.generar_clave()
        descifrador_clave_falsa = estrategia.crear_cifrador(clave_falsa, resultado_original.iv)

        detalle_clave = {}
        try:
            bytes_desc = descifrador_clave_falsa.decrypt(resultado_original.texto_cifrado)
            unpad(bytes_desc, tamano_bloque)
            detalle_clave["error"] = "Sin excepción de padding (caso fortuito raro)"
            detalle_clave["mensaje"] = "El texto resultante es ruido pseudoaleatorio ininteligible."
        except ValueError as err:
            detalle_clave["error"] = f"ValueError: {err}"
            detalle_clave["mensaje"] = (
                "Al usar una clave incorrecta, el descifrador genera bytes pseudoaleatorios. "
                "La función unpad rechaza el bloque final porque los bytes de relleno no cumplen PKCS#7."
            )

        # Caso 2: IV Incorrecto (con Clave Correcta)
        iv_falso = estrategia.generar_iv()
        descifrador_iv_falso = estrategia.crear_cifrador(resultado_original.clave, iv_falso)

        detalle_iv = {}
        try:
            bytes_desc_iv = descifrador_iv_falso.decrypt(resultado_original.texto_cifrado)
            texto_recuperado_bytes = unpad(bytes_desc_iv, tamano_bloque)
            texto_recuperado = texto_recuperado_bytes.decode('utf-8', errors='replace')
            detalle_iv["error"] = None
            detalle_iv["mensaje"] = (
                "En modo CBC: P1 = D(C1) ⊕ IV. Al cambiar el IV, ÚNICAMENTE el primer bloque queda destruido. "
                "Todos los bloques posteriores (bloque 2 en adelante) se recuperan con 100% de exactitud."
            )
            detalle_iv["texto_corrupto"] = texto_recuperado
        except ValueError as err:
            detalle_iv["error"] = f"ValueError: {err}"
            detalle_iv["mensaje"] = "Si el mensaje ocupa solo un bloque, el fallo del IV altera el relleno PKCS#7."
            detalle_iv["texto_corrupto"] = None

        return {
            "clave_erronea": detalle_clave,
            "iv_erroneo": detalle_iv
        }
