"""
=============================================================================
Capa de Controladores y Rutas: app/routes.py
Endpoints HTTP y API REST para la Interfaz Web de Cifrado Simétrico
=============================================================================
"""

from flask import Blueprint, render_template, request, jsonify
from src.service import ServicioCriptografico

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def index():
    """Ruta principal que sirve la interfaz web de usuario."""
    return render_template("index.html")


@bp_main.route("/api/cifrar", methods=["POST"])
def api_cifrar():
    """Endpoint API para cifrar y descifrar con un algoritmo individual."""
    datos = request.get_json() or {}
    texto = datos.get("texto", "").strip()
    algoritmo = datos.get("algoritmo", "AES")

    if len(texto) < 20:
        return jsonify({
            "error": f"El texto debe contener al menos 20 caracteres (actualmente tiene {len(texto)})."
        }), 400

    try:
        resultado = ServicioCriptografico.cifrar_y_descifrar(texto, algoritmo)
        return jsonify(resultado.a_diccionario()), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar el cifrado: {str(e)}"}), 500


@bp_main.route("/api/comparar", methods=["POST"])
def api_comparar():
    """Endpoint API para ejecutar y comparar DES, 3DES y AES simultáneamente."""
    datos = request.get_json() or {}
    texto = datos.get("texto", "").strip()

    if len(texto) < 20:
        return jsonify({
            "error": f"El texto debe contener al menos 20 caracteres (actualmente tiene {len(texto)})."
        }), 400

    try:
        resultados = ServicioCriptografico.comparar_todos(texto)
        return jsonify([r.a_diccionario() for r in resultados]), 200
    except Exception as e:
        return jsonify({"error": f"Error al ejecutar la comparativa: {str(e)}"}), 500


@bp_main.route("/api/simular_fallo", methods=["POST"])
def api_simular_fallo():
    """Endpoint API para la prueba didáctica de descifrado con clave e IV erróneos."""
    datos = request.get_json() or {}
    texto = datos.get("texto", "").strip()
    algoritmo = datos.get("algoritmo", "AES")

    if not texto:
        return jsonify({"error": "Texto plano no provisto."}), 400

    try:
        res_original = ServicioCriptografico.cifrar_y_descifrar(texto, algoritmo)
        fallas = ServicioCriptografico.simular_fallos_seguridad(res_original)
        return jsonify(fallas), 200
    except Exception as e:
        return jsonify({"error": f"Error al simular fallas: {str(e)}"}), 500
