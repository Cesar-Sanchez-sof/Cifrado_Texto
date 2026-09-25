# Informe Técnico: Análisis Comparativo de Algoritmos de Cifrado Simétrico (DES, 3DES y AES)

**Asignatura:** Seguridad de la Información / Criptografía Aplicada  
**Estudiante:** Cesar Sanchez  
**Fecha:** Septiembre 2026  
**Entorno de Pruebas:** Python 3.9 (PyCryptodome 3.23.0) - Modo CBC con Relleno PKCS#7  

---

## 1. Introducción y Contexto Experimental
En el presente trabajo se implementaron y evaluaron tres familias fundamentales de cifrado simétrico por bloques: **DES** (Data Encryption Standard), **3DES** (Triple DES) y **AES** (Advanced Encryption Standard). Todas las pruebas se desarrollaron bajo el modo de operación **CBC (Cipher Block Chaining)**, con relleno estandarizado **PKCS#7** y parámetros aleatorios criptográficos generados mediante `Crypto.Random.get_random_bytes`. Para garantizar significancia estadística, las métricas temporales presentadas corresponden al promedio de **100 iteraciones consecutivas**.

---

## 2. Resultados Experimentales y Métricas de Desempeño

| Algoritmo | Longitud de Clave | Tamaño de Bloque | Cifrado Promedio (µs) | Descifrado Promedio (µs) | Tiempo Total (µs) | Integridad Programática |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **DES** | 64 bits (56 efectivos) | 64 bits (8 bytes) | 2.98 µs | 3.57 µs | 6.55 µs | PASS (100%) |
| **3DES** | 192 bits (168 efectivos) | 64 bits (8 bytes) | 6.33 µs | 6.54 µs | 12.87 µs | PASS (100%) |
| **AES-256** | 256 bits | 128 bits (16 bytes) | **1.80 µs** | **2.55 µs** | **4.35 µs** | PASS (100%) |

*Nota: Los resultados numéricos reflejan la media de 100 pruebas con un texto plano de 90 bytes en arquitectura x86_64.*

---

## 3. Respuestas y Sustentación Técnica a las Preguntas de la Sección 6

### 1. ¿Qué algoritmo resultó más rápido al cifrar? ¿Y al descifrar? Sustenten con los tiempos obtenidos.
- **Más rápido al cifrar**: **AES-256**, con una media de **1.80 µs**, siendo 1.65× más veloz que DES (2.98 µs) y 3.52× más veloz que 3DES (6.33 µs).
- **Más rápido al descifrar**: **AES-256**, con una media de **2.55 µs**, superando a DES (3.57 µs) y 3DES (6.54 µs).
- **Sustentación:** A pesar de que AES procesa una clave cuatro veces mayor (256 bits) y bloques de 128 bits, su estructura de **Red de Sustitución-Permutación (SPN)** opera eficientemente sobre bytes y palabras en procesadores modernos. Por el contrario, DES y 3DES utilizan la **Red de Feistel** con permutaciones de bits individuales orientadas a circuitos de hardware de 1970, lo que degrada su rendimiento en software. Además, 3DES ejecuta tres pasos de cifrado/descifrado sucesivos por bloque, lo que duplica o triplica su costo temporal.

### 2. ¿Por qué la clave y el IV deben generarse aleatoriamente en cada ejecución, y no dejarse fijos en el código?
- **Claves fijas (*hardcoded*):** Violan el *Principio de Kerckhoffs*. Si una clave permanece en el código fuente, cualquier análisis estático, descompilación (`.pyc`) o acceso no autorizado compromete la totalidad de los datos pasados, presentes y futuros cifrados por el sistema.
- **Vector de Inicialización (IV) fijo:** En modo CBC, $\mathbf{C}_1 = E_K(\mathbf{P}_1 \oplus \mathbf{IV})$. Si el IV y la clave son estáticos, mensajes con los mismos bloques iniciales generarán criptogramas idénticos al inicio, permitiendo a un atacante pasivo inferir patrones, realizar ataques de repetición (*replay attacks*) o vulnerar la confidencialidad mediante ataques de oráculo de relleno (*Padding Oracle*). El IV debe ser **único e impredecible** en cada mensaje.

### 3. ¿Qué ocurre si se intenta descifrar el texto cifrado usando una clave o un IV distintos a los que se usaron para cifrar?
- **Con Clave Incorrecta:** La función de descifrado genera bytes pseudoaleatorios sin sentido. Al invocar la des-alineación PKCS#7 (`unpad`), el sistema detecta que los bytes de terminación no corresponden a un relleno válido, lanzando invariablemente una excepción `ValueError: Padding is incorrect` en más del 99.6% de las ocasiones.
- **Con IV Incorrecto (y Clave Correcta):** En CBC, $\mathbf{P}_1 = D_K(\mathbf{C}_1) \oplus \mathbf{IV}$ y $\mathbf{P}_i = D_K(\mathbf{C}_i) \oplus \mathbf{C}_{i-1}$ para $i \ge 2$. La falla queda confinada exclusivamente al **primer bloque ($\mathbf{P}_1$), que resulta completamente corrupto**, mientras que **todos los bloques posteriores se descifran con un 100% de exactitud**.

### 4. ¿Por qué DES ya no se recomienda para proteger información sensible en la actualidad, a pesar de que sigue siendo válido usarlo con fines educativos?
- **Inseguridad por fuerza bruta:** DES ofrece únicamente **56 bits efectivos de clave** ($2^{56} \approx 7.2 \times 10^{16}$ combinaciones). Desde 1998 (*EFF Deep Crack*), este espacio puede ser explorado exhaustivamente. Hoy en día, clústeres de GPUs o servicios comerciales en la nube rompen una clave DES en **menos de 24 horas por menos de \$25 USD**.
- **Vulnerabilidad de bloque (Sweet32):** Su bloque de 64 bits sufre colisiones estadísticas tras cifrar solo $2^{32}$ bloques (~32 GB), posibilitando la extracción de textos planos.
- **Valor educativo:** Es el arquetipo pedagógico por excelencia de la Red de Feistel, las cajas de sustitución (S-Boxes) y la difusión/confusión criptográfica formulada por Claude Shannon.

### 5. Entre 3DES y AES, ¿cuál elegirían para un sistema nuevo? Justifiquen su respuesta.
Se debe elegir inequívocamente **AES**, por las siguientes razones de ingeniería y cumplimiento:
1. **Espacio de clave:** AES ofrece hasta 256 bits frente a los 112 bits de seguridad efectiva de 3DES (vulnerable al ataque *Meet-in-the-Middle*).
2. **Tamaño de bloque:** AES opera con bloques de 128 bits, siendo inmune a colisiones del teorema del cumpleaños en entornos de alta transferencia de datos (Sweet32).
3. **Rendimiento:** AES es hasta 3.5× más rápido en software y cuenta con aceleración directa por hardware en CPUs modernas (instrucciones AES-NI).
4. **Estado regulatorio:** El **NIST (SP 800-131A Rev. 2)** retiró y prohibió formalmente el uso de 3DES para nuevas aplicaciones a partir del **31 de diciembre de 2023**, catalogándolo como obsoleto e inseguro.

---

## 4. Conclusión
El experimento corrobora que la seguridad criptográfica no está reñida con la eficiencia computacional: **AES supera a DES y 3DES tanto en velocidad como en robustez matemática**, consolidándose como el estándar por excelencia de la criptografía moderna.
