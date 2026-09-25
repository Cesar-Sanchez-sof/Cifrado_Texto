"""
=============================================================================
Punto de Entrada Principal del Sistema: run.py
Lanzador de la Aplicación Web CryptoLab (Cifrado Simétrico DES, 3DES y AES)
=============================================================================

Uso:
    python run.py
=============================================================================
"""

import time
import threading
import webbrowser
from app import create_app

app = create_app()


def abrir_navegador_automatico():
    """Abre el navegador predeterminado del sistema operativo automáticamente."""
    time.sleep(1.2)
    url = "http://127.0.0.1:5000"
    print(f"\n[+] Abriendo automáticamente la interfaz web en: {url}\n")
    try:
        webbrowser.open_new(url)
    except Exception as e:
        print(f"[!] No se pudo abrir el navegador automáticamente: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print(" 🚀 INICIANDO CRYPTOLAB: PLATAFORMA WEB DE CIFRADO SIMÉTRICO")
    print(" Algoritmos: DES, 3DES y AES en Modo CBC con Relleno PKCS#7")
    print(" Entorno:    Python 3.9+ | PyCryptodome | Flask")
    print(" URL Local:  http://127.0.0.1:5000")
    print("=" * 80)

    # Iniciar apertura de navegador en hilo secundario
    threading.Thread(target=abrir_navegador_automatico, daemon=True).start()

    # Iniciar servidor Flask
    app.run(host="127.0.0.1", port=5000, debug=False)
