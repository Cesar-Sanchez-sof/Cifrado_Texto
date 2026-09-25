"""
=============================================================================
Script de Empaquetado: empaquetar_entregable.py
Compilador del Archivo ZIP de Entrega Académica según la Jerarquía en Capas
=============================================================================

Uso:
    python empaquetar_entregable.py
    python empaquetar_entregable.py Sanchez Cesar
=============================================================================
"""

import os
import sys
import zipfile


def empaquetar(apellido: str = "Sanchez", nombre: str = "Cesar") -> str:
    """
    Empaqueta el proyecto estructurado en un único archivo comprimido .ZIP
    siguiendo la nomenclatura exigida: Apellido_Nombre_TrabajoCifrado.zip
    """
    dir_raiz = os.path.dirname(os.path.abspath(__file__))
    nombre_zip = f"{apellido}_{nombre}_TrabajoCifrado.zip"
    ruta_zip = os.path.join(dir_raiz, nombre_zip)

    # Carpetas y archivos a incluir
    elementos = [
        "run.py",
        "requirements.txt",
        "README.md",
        "Informe_Cifrado.md",
        "Informe_Cifrado.html",
        "app",
        "src",
        "tests",
        "data"
    ]

    print("=" * 80)
    print(f" GENERANDO EMPAQUETADO DE ENTREGA: {nombre_zip}")
    print("=" * 80)

    conteo = 0
    with zipfile.ZipFile(ruta_zip, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for elemento in elementos:
            ruta_elemento = os.path.join(dir_raiz, elemento)

            if not os.path.exists(ruta_elemento):
                print(f" [!] ALERTA: No se encontró: {elemento}")
                continue

            if os.path.isfile(ruta_elemento):
                zipf.write(ruta_elemento, arcname=elemento)
                tamano_kb = os.path.getsize(ruta_elemento) / 1024.0
                print(f" [+] Archivo: {elemento:<35} ({tamano_kb:6.1f} KB)")
                conteo += 1
            elif os.path.isdir(ruta_elemento):
                for raiz, _, archivos in os.walk(ruta_elemento):
                    # Ignorar carpetas temporales de cache
                    if "__pycache__" in raiz:
                        continue
                    for arch in archivos:
                        ruta_completa = os.path.join(raiz, arch)
                        ruta_relativa = os.path.relpath(ruta_completa, dir_raiz)
                        zipf.write(ruta_completa, arcname=ruta_relativa)
                        tamano_kb = os.path.getsize(ruta_completa) / 1024.0
                        print(f" [+] Paquete: {ruta_relativa:<35} ({tamano_kb:6.1f} KB)")
                        conteo += 1

    tamano_total_kb = os.path.getsize(ruta_zip) / 1024.0
    print("-" * 80)
    print(f"[OK] ARCHIVO ZIP GENERADO EXITOSAMENTE ({conteo} elementos incluidos):")
    print(f"     Ruta:   {ruta_zip}")
    print(f"     Tamano: {tamano_total_kb:.2f} KB")
    print("=" * 80 + "\n")

    return ruta_zip


if __name__ == "__main__":
    apellido = sys.argv[1] if len(sys.argv) > 1 else "Sanchez"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Cesar"
    empaquetar(apellido, nombre)
