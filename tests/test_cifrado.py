"""
=============================================================================
Capa de Pruebas: tests/test_cifrado.py
Batería de Pruebas Automatizadas, Benchmark Estadístico y Registro de Datos
=============================================================================

Descripción:
    Ejecuta pruebas sobre la capa de dominio (src/), mide el rendimiento
    a lo largo de 100 iteraciones y persiste los resultados en la carpeta 'data/':
    - data/resultados_pruebas.json
    - data/resultados_pruebas.txt
    - data/grafico_rendimiento.png
    - data/captura_ejecucion_1.png
    - data/captura_ejecucion_2.png
=============================================================================
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any

# Asegurar que la raíz del proyecto esté en el path de Python
DIR_TESTS = os.path.dirname(os.path.abspath(__file__))
DIR_RAIZ = os.path.dirname(DIR_TESTS)
if DIR_RAIZ not in sys.path:
    sys.path.insert(0, DIR_RAIZ)

# Asegurar codificación UTF-8 en Windows
if sys.platform.startswith('win'):
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from src.service import ServicioCriptografico
from src.models import ResultadoOperacion


def asegurar_directorio_data(ruta_data: str):
    """Crea la carpeta data/ si no existe."""
    os.makedirs(ruta_data, exist_ok=True)


def ejecutar_bateria_pruebas() -> Dict[str, Any]:
    """
    Ejecuta la suite completa de pruebas criptográficas, benchmark y fallas.
    """
    print("\n" + "=" * 80)
    print(" INICIANDO BATERIA DE PRUEBAS AUTOMATIZADAS (SRC/ DOMAIN LAYER)")
    print("=" * 80)

    registro_global = {
        "metadatos": {
            "fecha_ejecucion": datetime.now().isoformat(),
            "version_python": sys.version,
            "sistema_operativo": sys.platform,
            "modo_cifrado": "CBC con relleno PKCS#7"
        },
        "casos_prueba": [],
        "benchmark_promedios": {},
        "pruebas_seguridad": {}
    }

    textos_de_prueba = [
        {
            "id": "TC-01",
            "descripcion": "Texto estándar de longitud mínima requerida",
            "texto": "Criptografia Simetrica en Python 2026 - Proteccion de Datos."
        },
        {
            "id": "TC-02",
            "descripcion": "Texto con caracteres especiales en español (tildes, ñ, signos)",
            "texto": "¡Seguridad Informática Avanzada! Cifrado de contraseñas y mensajes: cañón, árbol, pingüino."
        },
        {
            "id": "TC-03",
            "descripcion": "Texto extenso multi-bloque",
            "texto": (
                "Los algoritmos de cifrado simetrico por bloques como DES, 3DES y AES transforman "
                "bloques de datos usando claves secretas compartidas. El modo CBC (Cipher Block Chaining) "
                "garantiza que bloques identicos de texto plano generen bloques de criptograma totalmente "
                "diferentes gracias al uso de un Vector de Inicializacion (IV) pseudoaleatorio y al encadenamiento."
            )
        }
    ]

    for caso in textos_de_prueba:
        print(f"\n>>> Ejecutando {caso['id']}: {caso['descripcion']}")
        print(f"    Texto: \"{caso['texto'][:60]}...\" ({len(caso['texto'])} caracteres)")

        registro_caso = {
            "caso_id": caso["id"],
            "descripcion": caso["descripcion"],
            "longitud_caracteres": len(caso["texto"]),
            "longitud_bytes_utf8": len(caso["texto"].encode('utf-8')),
            "ejecuciones": []
        }

        for algo in ["DES", "3DES", "AES"]:
            res: ResultadoOperacion = ServicioCriptografico.cifrar_y_descifrar(caso["texto"], algo)

            assert res.coincide, f"Fallo de integridad en {algo} para el caso {caso['id']}"
            assert res.texto_descifrado == caso["texto"], "El texto descifrado difiere del original"

            datos_ej = res.a_diccionario()
            registro_caso["ejecuciones"].append(datos_ej)
            print(f"    [PASS] {algo:6s} | Cifrado: {res.tiempo_cifrado_us:7.2f} us | Descifrado: {res.tiempo_descifrado_us:7.2f} us | Verif: OK")

        registro_global["casos_prueba"].append(registro_caso)

    # Benchmark estadístico de 100 iteraciones
    print("\n" + "=" * 80)
    print(" EJECUTANDO BENCHMARK ESTADISTICO (100 iteraciones por algoritmo)...")
    print("=" * 80)

    texto_bm = "Prueba de rendimiento y latencia para algoritmos simetricos DES, 3DES y AES en modo CBC."
    iteraciones = 100

    tiempos = {
        "DES": {"cifrado": [], "descifrado": []},
        "3DES": {"cifrado": [], "descifrado": []},
        "AES": {"cifrado": [], "descifrado": []}
    }

    for algo in ["DES", "3DES", "AES"]:
        for _ in range(iteraciones):
            r = ServicioCriptografico.cifrar_y_descifrar(texto_bm, algo)
            tiempos[algo]["cifrado"].append(r.tiempo_cifrado_us)
            tiempos[algo]["descifrado"].append(r.tiempo_descifrado_us)

        prom_cif = sum(tiempos[algo]["cifrado"]) / iteraciones
        prom_dec = sum(tiempos[algo]["descifrado"]) / iteraciones
        prom_tot = prom_cif + prom_dec

        registro_global["benchmark_promedios"][algo] = {
            "iteraciones": iteraciones,
            "promedio_cifrado_us": round(prom_cif, 2),
            "promedio_descifrado_us": round(prom_dec, 2),
            "promedio_total_us": round(prom_tot, 2)
        }
        print(f"  * {algo:6s} | Prom. Cifrado: {prom_cif:7.2f} us | Prom. Descifrado: {prom_dec:7.2f} us | Total: {prom_tot:7.2f} us")

    # Pruebas de fallas
    print("\n" + "=" * 80)
    print(" EJECUTANDO PRUEBAS DE SEGURIDAD (Clave e IV incorrectos)...")
    print("=" * 80)
    res_aes = ServicioCriptografico.cifrar_y_descifrar("Texto para verificar resiliencia ante parametros invalidos.", "AES")
    fallas = ServicioCriptografico.simular_fallos_seguridad(res_aes)
    registro_global["pruebas_seguridad"] = fallas
    print(f"  * Caso Clave Errónea: {fallas['clave_erronea']['error']}")
    print(f"  * Caso IV Erróneo:    Corrupción limitada al primer bloque en CBC")

    return registro_global


def guardar_archivos_data(datos: Dict[str, Any], ruta_json: str, ruta_txt: str):
    """Guarda los resultados serializados en JSON y TXT."""
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"\n[+] Resultados serializados guardados en: {ruta_json}")

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE EJECUCION DE PRUEBAS DE CIFRADO SIMETRICO (DES, 3DES, AES)\n")
        f.write(f"Fecha: {datos['metadatos']['fecha_ejecucion']}\n")
        f.write("=" * 80 + "\n\n")

        for c in datos["casos_prueba"]:
            f.write(f"--- CASO {c['caso_id']}: {c['descripcion']} ---\n")
            f.write(f"Longitud: {c['longitud_caracteres']} caracteres\n\n")
            for ej in c["ejecuciones"]:
                f.write(f"  [ALGORITMO]: {ej['algoritmo']} ({ej['tamano_clave_bits']} bits)\n")
                f.write(f"    * Clave (HEX):        {ej['clave_hex']}\n")
                f.write(f"    * IV (HEX):           {ej['iv_hex']}\n")
                f.write(f"    * Texto Original:     {ej['texto_original']}\n")
                f.write(f"    * Criptograma (HEX):  {ej['texto_cifrado_hex']}\n")
                f.write(f"    * Texto Descifrado:   {ej['texto_descifrado']}\n")
                f.write(f"    * Verificacion:       {'EXITOSA [100% IDENTICO]' if ej['coincide'] else 'FALLIDA'}\n")
                f.write(f"    * Tiempo Cifrado:     {ej['tiempo_cifrado_us']} us\n")
                f.write(f"    * Tiempo Descifrado:  {ej['tiempo_descifrado_us']} us\n")
                f.write(f"    * Tiempo Total:       {ej['tiempo_total_us']} us\n\n")
            f.write("-" * 80 + "\n\n")

        f.write("=" * 80 + "\n")
        f.write("RESUMEN DE BENCHMARK ESTADISTICO (100 ITERACIONES)\n")
        f.write("=" * 80 + "\n")
        for algo, v in datos["benchmark_promedios"].items():
            f.write(f"{algo:<10} | Cif: {v['promedio_cifrado_us']:>8.2f} us | Dec: {v['promedio_descifrado_us']:>8.2f} us | Tot: {v['promedio_total_us']:>8.2f} us\n")

    print(f"[+] Informe legible guardado en: {ruta_txt}")


def generar_grafico_rendimiento(datos: Dict[str, Any], ruta_grafico: str):
    """Genera gráfico comparativo de barras."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        algoritmos = list(datos["benchmark_promedios"].keys())
        tiempos_cif = [datos["benchmark_promedios"][a]["promedio_cifrado_us"] for a in algoritmos]
        tiempos_desc = [datos["benchmark_promedios"][a]["promedio_descifrado_us"] for a in algoritmos]

        max_t = max(tiempos_cif + tiempos_desc)
        x = range(len(algoritmos))
        ancho = 0.32

        fig, ax = plt.subplots(figsize=(9.5, 6), dpi=300)
        b1 = ax.bar([i - ancho/2 for i in x], tiempos_cif, ancho, label='Cifrado (us)', color='#0ea5e9', edgecolor='#0369a1')
        b2 = ax.bar([i + ancho/2 for i in x], tiempos_desc, ancho, label='Descifrado (us)', color='#10b981', edgecolor='#047857')

        ax.set_ylabel('Tiempo promedio en microsegundos (us)', fontsize=12, fontweight='bold', labelpad=10)
        ax.set_title('Comparativa de Rendimiento: DES vs 3DES vs AES (Modo CBC + PKCS#7)\nPromedio sobre 100 iteraciones en Python 3.9', fontsize=13, fontweight='bold', pad=20)
        ax.set_xticks(list(x))
        ax.set_xticklabels(algoritmos, fontsize=12, fontweight='bold')
        ax.set_ylim(0, max_t * 1.30)
        ax.legend(fontsize=11, loc='upper right')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        for bar in b1:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + (max_t * 0.02), f'{yval:.2f} us', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0369a1')

        for bar in b2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + (max_t * 0.02), f'{yval:.2f} us', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#047857')

        plt.tight_layout()
        plt.savefig(ruta_grafico)
        plt.close()
        print(f"[+] Gráfico comparativo generado en: {ruta_grafico}")

    except Exception as e:
        print(f"[!] Error generando gráfico: {e}")


def _dividir_en_bloques(cadena: str, tamano: int = 64) -> List[str]:
    return [cadena[i:i+tamano] for i in range(0, len(cadena), tamano)]


def generar_capturas_ejecucion(datos: Dict[str, Any], ruta_img1: str, ruta_img2: str):
    """Genera imágenes legibles de las ejecuciones #1 y #2 para los entregables."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        casos = datos["casos_prueba"][:2]
        rutas = [ruta_img1, ruta_img2]

        for i, (caso, ruta_salida) in enumerate(zip(casos, rutas), 1):
            lineas = []
            lineas.append("=" * 86)
            lineas.append(f"  EJECUCION #{i} DEL SISTEMA DE CIFRADO SIMETRICO (DEMOSTRACION)")
            lineas.append("=" * 86)
            lineas.append(f" Caso ID:        {caso['caso_id']} - {caso['descripcion']}")
            lineas.append(f" Texto Original: \"{caso['ejecuciones'][0]['texto_original']}\"")
            lineas.append(f" Longitud:       {caso['longitud_caracteres']} caracteres ({caso['longitud_bytes_utf8']} bytes UTF-8)")
            lineas.append("-" * 86)

            for ej in caso["ejecuciones"]:
                lineas.append(f" ALGORITMO: {ej['algoritmo']} ({ej['tamano_clave_bits']} bits | Bloque: {ej['tamano_bloque_bits']} bits)")
                lineas.append(f"   * Clave (HEX):        {ej['clave_hex']}")
                lineas.append(f"   * IV (HEX):           {ej['iv_hex']}")

                cripto_hex = ej['texto_cifrado_hex']
                bloques_hex = _dividir_en_bloques(cripto_hex, 64)
                lineas.append(f"   * Criptograma (HEX):  {bloques_hex[0]}")
                for b_extra in bloques_hex[1:]:
                    lineas.append(f"                         {b_extra}")

                lineas.append(f"   * Texto Descifrado:   {ej['texto_descifrado']}")
                lineas.append(f"   * Verificacion:       [OK] IDENTICO AL ORIGINAL (100% COINCIDENCIA)")
                lineas.append(f"   * Metricas de Tiempo: Cifrado: {ej['tiempo_cifrado_us']} us | Descifrado: {ej['tiempo_descifrado_us']} us")
                lineas.append("-" * 86)

            lineas.append("=" * 86)

            ancho_img = 1150
            alto_linea = 24
            alto_img = alto_linea * len(lineas) + 50

            imagen = Image.new("RGB", (ancho_img, alto_img), color="#0f172a")
            draw = ImageDraw.Draw(imagen)

            fuente = None
            for nombre_fuente in ["consola.ttf", "consolas.ttf", "cour.ttf", "Courier"]:
                try:
                    fuente = ImageFont.truetype(nombre_fuente, 15)
                    break
                except Exception:
                    continue
            if fuente is None:
                fuente = ImageFont.load_default()

            y = 25
            for linea in lineas:
                color = "#cbd5e1"
                if "[OK]" in linea:
                    color = "#34d399"
                elif "ALGORITMO:" in linea or "EJECUCION" in linea:
                    color = "#38bdf8"
                elif "=" in linea or "-" in linea:
                    color = "#475569"
                elif "Clave" in linea or "IV" in linea:
                    color = "#fbbf24"
                elif "Criptograma" in linea or "                         " in linea:
                    color = "#f87171"

                draw.text((25, y), linea, fill=color, font=fuente)
                y += alto_linea

            imagen.save(ruta_salida)
            print(f"[+] Captura de ejecución generada en: {ruta_salida}")

    except Exception as e:
        print(f"[!] Error generando capturas con Pillow: {e}")


def main():
    ruta_data = os.path.join(DIR_RAIZ, "data")
    asegurar_directorio_data(ruta_data)

    ruta_json = os.path.join(ruta_data, "resultados_pruebas.json")
    ruta_txt = os.path.join(ruta_data, "resultados_pruebas.txt")
    ruta_grafico = os.path.join(ruta_data, "grafico_rendimiento.png")
    ruta_img1 = os.path.join(ruta_data, "captura_ejecucion_1.png")
    ruta_img2 = os.path.join(ruta_data, "captura_ejecucion_2.png")

    datos = ejecutar_bateria_pruebas()
    guardar_archivos_data(datos, ruta_json, ruta_txt)
    generar_grafico_rendimiento(datos, ruta_grafico)
    generar_capturas_ejecucion(datos, ruta_img1, ruta_img2)

    print("\n" + "=" * 80)
    print(" [OK] BATERIA DE PRUEBAS COMPLETADA. DATOS ALMACENADOS EN 'data/'")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
