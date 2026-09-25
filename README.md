# Trabajo Práctico: Cifrado de Texto con Python (DES, 3DES y AES)
## Arquitectura de Software Modular (Clean Architecture) • Interfaz Web CryptoLab

Este repositorio contiene la solución completa al trabajo práctico sobre algoritmos de cifrado simétrico por bloques (**DES**, **3DES** y **AES** en modo **CBC** con relleno **PKCS#7**), diseñada bajo los estándares de la ingeniería de software moderna con separación estricta de capas (*Separation of Concerns*).

---

## 1. Arquitectura y Jerarquía del Proyecto

```text
cifrado_texto/
├── run.py                     # Punto de entrada principal (Lanza la App Web y abre el navegador)
├── requirements.txt           # Dependencias oficiales del proyecto
├── Informe_Cifrado.md         # Informe técnico formal (Resolución de la Sección 6)
├── Informe_Cifrado.html       # Informe técnico maquetado con estilos para imprimir a PDF (Ctrl+P)
├── empaquetar_entregable.py   # Script de empaquetado para generar el archivo ZIP de entrega
├── README.md                  # Manual técnico de arquitectura y fundamentación teórica
│
├── app/                       # CAPA DE PRESENTACIÓN (Flask Web Dashboard)
│   ├── __init__.py            # Fábrica de la aplicación (Application Factory Pattern)
│   ├── routes.py              # Controladores y endpoints de la API REST (/api/cifrar, /api/comparar)
│   ├── templates/
│   │   └── index.html         # Plantilla HTML5 reactiva con Tailwind CSS y Chart.js
│   └── static/
│       ├── css/
│       │   └── styles.css     # Estilos visuales del tema oscuro de ciberseguridad
│       └── js/
│           └── app.js         # Lógica frontend (eventos, llamadas API y visualizador de bloques)
│
├── src/                       # CAPA DE DOMINIO Y MOTOR CRIPTOGRÁFICO
│   ├── __init__.py            # Inicializador del paquete de dominio
│   ├── models.py              # Entidades inmutables y estructuras de datos (Dataclasses & Enums)
│   ├── strategies.py          # Patrón Strategy (CifradorDES, Cifrador3DES, CifradorAES)
│   ├── service.py             # Fachada de Servicios y orquestador criptográfico
│   └── utils.py               # Utilidades de Entropía de Shannon y análisis de bloques PKCS#7
│
├── tests/                     # CAPA DE PRUEBAS AUTOMATIZADAS Y BENCHMARKS
│   ├── __init__.py            # Inicializador del paquete de pruebas
│   └── test_cifrado.py        # Suite de pruebas unitarias, benchmark (100 iteraciones) y fallas
│
├── data/                      # PERSISTENCIA DE RESULTADOS Y EVIDENCIAS
│   ├── resultados_pruebas.json # Datos completos serializados de las pruebas ejecutadas
│   ├── resultados_pruebas.txt  # Reporte legible en texto plano de las métricas
│   ├── grafico_rendimiento.png # Gráfico comparativo de tiempos (100 iteraciones)
│   ├── captura_ejecucion_1.png # Evidencia visual de Ejecución #1 (Texto estándar)
│   └── captura_ejecucion_2.png # Evidencia visual de Ejecución #2 (Caracteres especiales)
│
└── Sanchez_Cesar_TrabajoCifrado.zip # Archivo comprimido final para entrega en el Aula Virtual
```

---

## 2. Requisitos e Instalación

- **Python**: Versión 3.8 o superior (verificado y optimizado en Python 3.9+).
- **Instalación de paquetes:**
```bash
pip install -r requirements.txt
```

---

## 3. Modo de Uso

### A. Iniciar la Aplicación Web Interactiva
Ejecute el comando principal en la raíz del proyecto:
```bash
python run.py
```
> El script iniciará el servidor Flask local y **abrirá de manera automática su navegador web** en `http://127.0.0.1:5000`.

**Características de la Aplicación Web:**
- **Contador en tiempo real de caracteres:** Valida que el texto ingresado tenga un mínimo de 20 caracteres (alerta en rojo y cambia a verde al ser válido).
- **Botones de texto rápido:** Carga con un solo clic textos de prueba (básico, caracteres especiales en español con tildes/ñ, y párrafo multi-bloque).
- **Tarjetas de resultados completas:** Muestra Clave HEX, IV HEX, Criptograma HEX y Texto recuperado con botones individuales de copia al portapapeles 📋.
- **Gráfico dinámico de velocidad (Chart.js):** Al seleccionar *"⚡ Comparar Todos"*, despliega un gráfico interactivo comparando los microsegundos de cada algoritmo.
- **Inspector didáctico de bloques CBC y PKCS#7:** Muestra cómo el texto plano se divide en bloques y resalta los bytes de relleno agregados.
- **Laboratorio de Ataques:** Permite simular qué ocurre al descifrar con una clave falsa o un IV alterado (Sección 6, Pregunta 3).

### B. Ejecutar las Pruebas Automatizadas y Benchmarks
```bash
python tests/test_cifrado.py
```
Este comando ejecuta la batería de pruebas, realiza 100 iteraciones estadísticas por algoritmo y actualiza automáticamente los archivos en `data/`.

### C. Generar el Archivo ZIP de Entrega
```bash
python empaquetar_entregable.py [Apellido] [Nombre]
```
*(Por defecto genera `Sanchez_Cesar_TrabajoCifrado.zip`).*

---

## 4. Respuestas Técnicas a la Sección 6 (Preguntas del Informe)

### Pregunta 1: ¿Qué algoritmo resultó más rápido al cifrar? ¿Y al descifrar? Sustenten con los tiempos obtenidos.

**Métricas Promedio Obtenidas (100 Iteraciones):**

| Algoritmo | Clave | Bloque | T. Cifrado Promedio | T. Descifrado Promedio | Tiempo Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **AES-256** | **256 bits** | **128 bits** | **2.93 µs** | **4.01 µs** | **6.94 µs** *(Más Rápido)* |
| **DES** | 64 bits (56 efect.) | 64 bits | 5.83 µs | 7.05 µs | 12.88 µs |
| **3DES** | 192 bits (168 efect.) | 64 bits | 10.03 µs | 10.52 µs | 20.55 µs *(Más Lento)* |

**Sustentación Técnica:**
- **AES-256** fue el más veloz tanto al cifrar como al descifrar, siendo **casi 3 veces más rápido que 3DES**.
- **AES** utiliza una Red de Sustitución-Permutación (SPN) optimizada para procesadores modernos de 32 y 64 bits con soporte de aceleración por hardware (AES-NI). Además, al procesar bloques de 128 bits (el doble de DES/3DES), requiere la mitad de operaciones de encadenamiento CBC para los mismos datos.
- **3DES** resultó el más lento debido a que ejecuta tres pasadas completas de cifrado/descifrado DES por cada bloque de 64 bits.

---

### Pregunta 2: ¿Por qué la clave y el IV deben generarse aleatoriamente en cada ejecución, y no dejarse fijos en el código?
- **Claves fijas (*hardcoded*):** Infringen el *Principio de Kerckhoffs*. Una clave incrustada en el código fuente puede extraerse fácilmente mediante ingeniería inversa o descompilación (`.pyc`), comprometiendo todos los mensajes pasados, presentes y futuros.
- **IV fijo:** En CBC ($C_1 = E_K(P_1 \oplus IV)$), el IV asegura que textos planos idénticos produzcan criptogramas distintos. Si el IV y la clave fuesen estáticos, un atacante detectaría patrones de inicio comunes y podría lanzar ataques de repetición y de oráculo de relleno (*Padding Oracle*).

---

### Pregunta 3: ¿Qué ocurre si se intenta descifrar el texto cifrado usando una clave o un IV distintos a los que se usaron para cifrar?
- **Con Clave errónea:** El descifrado genera ruido pseudoaleatorio. Al remover el relleno PKCS#7 (`unpad`), la estructura de relleno falla en el 99.6% de los casos lanzando la excepción `ValueError: Padding is incorrect`.
- **Con IV erróneo (y Clave correcta):** En CBC, $P_1 = D_K(C_1) \oplus IV$ y $P_i = D_K(C_i) \oplus C_{i-1}$ para $i \ge 2$. Por lo tanto, **solo el primer bloque ($P_1$) queda destruido e ilegible**; a partir del segundo bloque en adelante, todos los datos se descifran con un 100% de exactitud.

---

### Pregunta 4: ¿Por qué DES ya no se recomienda para proteger información sensible en la actualidad, a pesar de que sigue siendo válido usarlo con fines educativos?
- **Vulnerabilidad por fuerza bruta:** DES ofrece solo **56 bits efectivos de clave** ($2^{56} \approx 7.2 \times 10^{16}$ combinaciones), un espacio que hoy se rompe en **menos de 24 horas por menos de $25 USD** usando clústeres de GPUs o hardware especializado (como el histórico *Deep Crack* de la EFF).
- **Vulnerabilidad de bloque (Sweet32):** Su bloque de 64 bits sufre colisiones estadísticas tras cifrar solo $2^{32}$ bloques (~32 GB).
- **Valor educativo:** Sigue siendo el pilar didáctico fundamental para comprender la Red de Feistel, las cajas de sustitución (S-Boxes) y la difusión y confusión de Shannon.

---

### Pregunta 5: Entre 3DES y AES, ¿cuál elegirían para un sistema nuevo? Justifiquen su respuesta.
Se debe elegir **AES** indiscutiblemente:
1. **Seguridad Robusta:** Bloques de 128 bits (inmune a Sweet32) y claves de hasta 256 bits, frente a los 112 bits de seguridad efectiva de 3DES vulnerables al ataque *Meet-in-the-Middle*.
2. **Rendimiento:** AES es hasta 3 veces más veloz en software y dispone de soporte nativo en el silicio de procesadores modernos (AES-NI).
3. **Estatus Regulatorio:** El **NIST (SP 800-131A Rev. 2)** retiró y prohibió formalmente el uso de 3DES para nuevas aplicaciones a partir del **31 de diciembre de 2023**, catalogándolo como obsoleto e inseguro.

---

## 5. Buenas Prácticas de Ingeniería de Software Aplicadas
- **Arquitectura en Capas:** Clara separación entre Dominio/Criptografía (`src/`), Presentación Web (`app/`), Pruebas (`tests/`) y Datos Persistidos (`data/`).
- **Patrón Strategy:** Algoritmos intercambiables y desacoplados bajo interfaces abstractas.
- **Tipado Estático:** Uso riguroso de *Type Hints* de Python para robustez y legibilidad.
- **Persistencia Abierta:** Los resultados de las pruebas se exportan tanto en formato estructurado JSON como en reportes legibles en texto plano.
