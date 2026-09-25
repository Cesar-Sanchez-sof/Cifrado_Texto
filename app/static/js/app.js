/**
 * ==============================================================================
 * Lógica Frontend del Cliente: app/static/js/app.js
 * Control de Eventos, Llamadas a la API REST, Renderizado de Bloques y Gráficos
 * ==============================================================================
 */

const ejemplos = {
    1: "Criptografia Simetrica en Python 2026 - Proteccion de Datos.",
    2: "¡Seguridad Informática Avanzada! Cifrado de contraseñas y mensajes: cañón, árbol, pingüino.",
    3: "Los algoritmos de cifrado simetrico por bloques como DES, 3DES y AES transforman bloques de datos usando claves secretas compartidas y modos de operacion como CBC con relleno PKCS7."
};

let chartInstance = null;
let ultimoResultado = null;

// Elementos del DOM
const inputArea = document.getElementById('texto-input');
const charBadge = document.getElementById('char-badge');
const btnProcesar = document.getElementById('btn-procesar');

// Validación reactiva del contador de caracteres
inputArea.addEventListener('input', () => {
    const len = inputArea.value.trim().length;
    if (len >= 20) {
        charBadge.textContent = `${len} caracteres (Válido ✓)`;
        charBadge.className = "text-xs font-mono px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 transition-all";
        btnProcesar.disabled = false;
    } else {
        const faltan = 20 - len;
        charBadge.textContent = `${len} / 20 caracteres (Faltan ${faltan})`;
        charBadge.className = "text-xs font-mono px-3 py-1 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 transition-all";
    }
});

function cargarEjemplo(n) {
    inputArea.value = ejemplos[n];
    inputArea.dispatchEvent(new Event('input'));
}

// Inicializar con el ejemplo 1 por defecto
document.addEventListener("DOMContentLoaded", () => {
    cargarEjemplo(1);
});

async function procesarCifrado() {
    const texto = inputArea.value.trim();
    if (texto.length < 20) {
        alert("Por favor ingrese un texto de al menos 20 caracteres.");
        return;
    }

    const algoritmo = document.querySelector('input[name="algoritmo"]:checked').value;
    const spinner = document.getElementById('loading-spinner');
    spinner.classList.remove('hidden');
    spinner.classList.add('inline-flex');

    try {
        let respuesta;
        if (algoritmo === 'TODOS') {
            respuesta = await fetch('/api/comparar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ texto: texto })
            });
        } else {
            respuesta = await fetch('/api/cifrar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ texto: texto, algoritmo: algoritmo })
            });
        }

        const data = await respuesta.json();
        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        mostrarResultados(data, algoritmo === 'TODOS');
    } catch (err) {
        alert("Error de conexión al servidor: " + err);
    } finally {
        spinner.classList.add('hidden');
        spinner.classList.remove('inline-flex');
    }
}

function copiarTexto(texto, btnId) {
    navigator.clipboard.writeText(texto).then(() => {
        const el = document.getElementById(btnId);
        const txtOrig = el.innerHTML;
        el.innerHTML = "✓ ¡Copiado!";
        setTimeout(() => el.innerHTML = txtOrig, 2000);
    });
}

function renderizarTarjeta(res, index) {
    const uid = `card_${index}_${res.algoritmo}`;
    return `
    <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl relative overflow-hidden card-transition">
        <!-- ENCABEZADO DE TARJETA -->
        <div class="flex flex-wrap items-center justify-between pb-4 mb-4 border-b border-slate-800 gap-3">
            <div class="flex items-center gap-3">
                <span class="text-2xl">${res.algoritmo.includes('AES') ? '🛡️' : (res.algoritmo === '3DES' ? '🔐' : '🔑')}</span>
                <div>
                    <div class="flex items-center gap-2">
                        <h3 class="text-xl font-bold text-white">${res.algoritmo}</h3>
                        <span class="text-xs font-mono px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                            Modo CBC + PKCS#7
                        </span>
                    </div>
                    <p class="text-xs text-slate-400">Clave: ${res.tamano_clave_bits} bits (${res.tamano_clave_bits / 8} bytes) | Bloque: ${res.tamano_bloque_bits} bits</p>
                </div>
            </div>

            <!-- BADGE DE VERIFICACIÓN PROGRAMÁTICA -->
            <div class="flex items-center gap-2">
                ${res.coincide 
                    ? `<div class="px-3.5 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-1.5 shadow-sm glow-green">
                        <span>✓</span> VERIFICACIÓN: 100% IDÉNTICO
                       </div>`
                    : `<div class="px-3.5 py-1.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-400 text-xs font-bold flex items-center gap-1.5">
                        <span>✗</span> VERIFICACIÓN: FALLIDA
                       </div>`
                }
            </div>
        </div>

        <!-- MÉTRICAS DE TIEMPO -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                <span class="text-[11px] text-slate-400 block mb-0.5">Tiempo Cifrado</span>
                <span class="text-sm font-mono font-bold text-cyan-400">${res.tiempo_cifrado_us} µs</span>
                <span class="text-[10px] text-slate-500 block">${(res.tiempo_cifrado_us / 1000).toFixed(4)} ms</span>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                <span class="text-[11px] text-slate-400 block mb-0.5">Tiempo Descifrado</span>
                <span class="text-sm font-mono font-bold text-emerald-400">${res.tiempo_descifrado_us} µs</span>
                <span class="text-[10px] text-slate-500 block">${(res.tiempo_descifrado_us / 1000).toFixed(4)} ms</span>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                <span class="text-[11px] text-slate-400 block mb-0.5">Tiempo Total</span>
                <span class="text-sm font-mono font-bold text-purple-400">${res.tiempo_total_us} µs</span>
                <span class="text-[10px] text-slate-500 block">${(res.tiempo_total_us / 1000).toFixed(4)} ms</span>
            </div>
            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80">
                <span class="text-[11px] text-slate-400 block mb-0.5">Entropía Shannon</span>
                <span class="text-sm font-mono font-bold text-amber-400">${res.analisis ? res.analisis.entropia_criptograma : '7.9'} bits</span>
                <span class="text-[10px] text-slate-500 block">Distribución aleatoria</span>
            </div>
        </div>

        <!-- PARÁMETROS CRIPTOGRÁFICOS -->
        <div class="space-y-3.5 text-xs">
            <!-- CLAVE -->
            <div>
                <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-slate-300">🔑 Clave Secreta Generada (Hexadecimal):</span>
                    <button id="btn_k_${uid}" onclick="copiarTexto('${res.clave_hex}', 'btn_k_${uid}')" class="text-cyan-400 hover:text-cyan-300 transition text-[11px]">
                        Copiar Clave 📋
                    </button>
                </div>
                <div class="code-font bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-amber-300 break-all select-all">
                    ${res.clave_hex}
                </div>
            </div>

            <!-- IV -->
            <div>
                <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-slate-300">🎲 Vector de Inicialización IV (Hexadecimal):</span>
                    <button id="btn_iv_${uid}" onclick="copiarTexto('${res.iv_hex}', 'btn_iv_${uid}')" class="text-cyan-400 hover:text-cyan-300 transition text-[11px]">
                        Copiar IV 📋
                    </button>
                </div>
                <div class="code-font bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-amber-200 break-all select-all">
                    ${res.iv_hex}
                </div>
            </div>

            <!-- CRIPTOGRAMA -->
            <div>
                <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-slate-300">📦 Criptograma / Texto Cifrado (Hexadecimal):</span>
                    <button id="btn_c_${uid}" onclick="copiarTexto('${res.texto_cifrado_hex}', 'btn_c_${uid}')" class="text-cyan-400 hover:text-cyan-300 transition text-[11px]">
                        Copiar Criptograma 📋
                    </button>
                </div>
                <div class="code-font bg-slate-950 p-3 rounded-lg border border-slate-800 text-rose-300 break-all select-all max-h-24 overflow-y-auto scrollbar-custom">
                    ${res.texto_cifrado_hex}
                </div>
            </div>

            <!-- TEXTO DESCIFRADO -->
            <div>
                <span class="font-semibold text-slate-300 block mb-1">🔓 Texto Recuperado (Descifrado):</span>
                <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-emerald-300 select-all">
                    "${res.texto_descifrado}"
                </div>
            </div>
        </div>
    </div>
    `;
}

function renderizarInspectorBloques(analisis, algoritmo) {
    if (!analisis) return;
    const grid = document.getElementById('contenedor-bloques-grid');
    const badge = document.getElementById('resumen-bloques-badge');
    badge.textContent = `${algoritmo} • ${analisis.total_bloques} Bloques de ${analisis.bytes_relleno > 0 ? (analisis.longitud_bytes + analisis.bytes_relleno) / analisis.total_bloques : 16}B • ${analisis.bytes_relleno}B relleno PKCS#7`;

    let html = "";
    analisis.bloques.forEach(b => {
        html += `
        <div class="p-3 bg-slate-950 rounded-xl border ${b.es_relleno ? 'border-amber-500/40 bg-amber-500/5' : 'border-slate-800'} text-xs">
            <div class="flex items-center justify-between mb-1.5">
                <span class="font-bold text-white">Bloque #${b.indice}</span>
                ${b.es_relleno 
                    ? `<span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 text-[10px] font-semibold">Con PKCS#7</span>` 
                    : `<span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">Lleno</span>`}
            </div>
            <div class="code-font text-slate-300 break-all text-[11px] mb-1.5 p-1.5 bg-slate-900 rounded border border-slate-800">
                ${b.hex}
            </div>
            <div class="flex justify-between text-[10px] text-slate-400">
                <span>Texto: "${b.ascii}"</span>
                <span>${b.originales}B texto + ${b.relleno}B pad</span>
            </div>
        </div>
        `;
    });
    grid.innerHTML = html;
}

function mostrarResultados(data, esComparativa) {
    const container = document.getElementById('resultados-container');
    const cardsContainer = document.getElementById('cards-resultados');
    const seccionGrafico = document.getElementById('seccion-grafico');

    container.classList.remove('hidden');

    if (esComparativa) {
        ultimoResultado = data[2]; // Tomar AES para simulación
        cardsContainer.innerHTML = data.map((r, i) => renderizarTarjeta(r, i)).join('');
        seccionGrafico.classList.remove('hidden');
        actualizarGrafico(data);
        renderizarInspectorBloques(data[2].analisis, data[2].algoritmo);
    } else {
        ultimoResultado = data;
        cardsContainer.innerHTML = renderizarTarjeta(data, 0);
        seccionGrafico.classList.add('hidden');
        renderizarInspectorBloques(data.analisis, data.algoritmo);
    }

    container.scrollIntoView({ behavior: 'smooth' });
}

function actualizarGrafico(listaResultados) {
    const ctx = document.getElementById('graficoComparativo').getContext('2d');
    const labels = listaResultados.map(r => r.algoritmo);
    const tiemposCifrado = listaResultados.map(r => r.tiempo_cifrado_us);
    const tiemposDescifrado = listaResultados.map(r => r.tiempo_descifrado_us);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Cifrado (µs)',
                    data: tiemposCifrado,
                    backgroundColor: 'rgba(6, 182, 212, 0.75)',
                    borderColor: 'rgba(6, 182, 212, 1)',
                    borderWidth: 1.5,
                    borderRadius: 6
                },
                {
                    label: 'Descifrado (µs)',
                    data: tiemposDescifrado,
                    backgroundColor: 'rgba(16, 185, 129, 0.75)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 1.5,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                }
            },
            scales: {
                y: {
                    title: { display: true, text: 'Microsegundos (µs)', color: '#64748b' },
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#1e293b' }
                },
                x: {
                    ticks: { color: '#e2e8f0', font: { weight: 'bold' } },
                    grid: { display: false }
                }
            }
        }
    });

    const masRapidoCif = listaResultados.reduce((min, p) => p.tiempo_cifrado_us < min.tiempo_cifrado_us ? p : min, listaResultados[0]);
    const masLentoCif = listaResultados.reduce((max, p) => p.tiempo_cifrado_us > max.tiempo_cifrado_us ? p : max, listaResultados[0]);
    const ratio = (masLentoCif.tiempo_cifrado_us / masRapidoCif.tiempo_cifrado_us).toFixed(1);

    document.getElementById('badge-mas-rapido').textContent = `🏆 ${masRapidoCif.algoritmo} fue el más veloz (${masRapidoCif.tiempo_cifrado_us} µs)`;

    const tablaResumen = document.getElementById('tabla-resumen-comparativo');
    tablaResumen.innerHTML = `
        <div class="text-xs font-semibold text-slate-300 pb-2 border-b border-slate-800">
            💡 Conclusiones del Rendimiento:
        </div>
        <div class="text-xs text-slate-400 space-y-2 pt-1">
            <p>• <strong>${masRapidoCif.algoritmo}</strong> fue el más veloz de todos, siendo <span class="text-cyan-400 font-bold">${ratio}x más rápido</span> que ${masLentoCif.algoritmo}.</p>
            <p>• <strong>3DES</strong> es el más lento debido a que realiza 3 operaciones completas de cifrado por cada bloque de 64 bits.</p>
            <p>• <strong>AES</strong> aprovecha su bloque amplio de 128 bits y optimizaciones nativas de CPU.</p>
        </div>
    `;
}

async function ejecutarSimulacionFalla() {
    if (!ultimoResultado) {
        alert("Primero cifre un texto para poder simular fallas sobre su criptograma.");
        return;
    }

    const boxClave = document.getElementById('falla-clave-box');
    const boxIv = document.getElementById('falla-iv-box');

    boxClave.innerHTML = "<span class='text-cyan-400 animate-pulse'>Simulando ataque con clave falsa...</span>";
    boxIv.innerHTML = "<span class='text-cyan-400 animate-pulse'>Simulando alteración de IV...</span>";

    try {
        const res = await fetch('/api/simular_fallo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                algoritmo: ultimoResultado.algoritmo,
                texto: ultimoResultado.texto_original
            })
        });
        const datos = await res.json();

        // Renderizar Caso 1: Clave errónea
        boxClave.innerHTML = `
            <div class="text-rose-400 font-bold mb-1">🛑 Excepción Capturada:</div>
            <div class="text-slate-300 mb-2">${datos.clave_erronea.error || 'Fallo de integridad'}</div>
            <div class="text-slate-400 text-[11px] leading-relaxed">${datos.clave_erronea.mensaje}</div>
        `;

        // Renderizar Caso 2: IV erróneo
        boxIv.innerHTML = `
            <div class="text-amber-400 font-bold mb-1">⚠️ Comportamiento Matemático CBC:</div>
            <div class="text-slate-400 text-[11px] mb-2 leading-relaxed">${datos.iv_erroneo.mensaje}</div>
            ${datos.iv_erroneo.texto_corrupto ? `
                <div class="text-[11px] text-slate-300">
                    <strong>Texto resultante (Primer bloque dañado):</strong>
                    <div class="p-2 bg-slate-950 rounded border border-amber-500/30 text-amber-200 mt-1 break-all select-all">
                        "${datos.iv_erroneo.texto_corrupto}"
                    </div>
                </div>
            ` : ''}
        `;
    } catch (err) {
        alert("Error al simular fallas: " + err);
    }
}
