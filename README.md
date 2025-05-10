# File_Organizer
Project made to organize juzged files to pass the migration process required by the new managemet system

Los siguientes son los pasos que se deben ejecutar en el presente proyecto para que los expedientes judiciales cumplan las condiciones para migración al **SISTEMA DE GESTIÓN DE DOCUMENTOS ELECTRÓNICOS DE ARCHIVO**, dispuesto para la administración de documentos por el Consejo Superior de la Judicatura.

Los expedientes a migrar deben cumplir con el protocolo para la gestión de documentos electrónicos. Para ello, seguiremos los siguientes pasos:

---

## 0. Eliminar carpetas vacías e índices electrónicos

Eliminar todas las carpetas vacías y todos los índices electrónicos existentes en la ruta a organizar.

---

## 1. Organización de carpetas

### a. Renombrar carpeta electrónica del proceso judicial:

1. La carpeta electrónica del proceso judicial debe identificarse con el **Código Único de Identificación (C.U.I)** compuesto por **23 dígitos**.  
   Ejemplo: `1001750302520200234501`
2. Se debe contar con los **primeros 11 dígitos del despacho judicial**.
3. Los siguientes **9 dígitos** corresponden al número del proceso judicial.
4. Los **últimos 2 dígitos serán 00**.
5. Verificar que:
   - No queden espacios ni caracteres especiales.
   - El nombre no exceda los **40 caracteres**.
6. El número del proceso debe ir separado con un espacio de las palabras.

---

## 2. Organización de subcarpetas

### a. Estructura por instancia:

La carpeta electrónica del proceso puede subdividirse en otras carpetas para contemplar las etapas procesales y permitir la participación de todos los despachos y personas intervinientes:

- `01PrimeraInstancia` (ó `01UnicaInstancia`)
- `02SegundaInstancia`
- `03RecursosExtraordinarios`
- `04Ejecucion`

Pasos:

1. Iterar en todas las carpetas cuyo nombre inicia con los **5 primeros dígitos del radicado del despacho**.
2. Si no existe la carpeta `01PrimeraInstancia`, **crear**.
3. Si existe `01UnicaInstancia`, **omitir**.
4. Si `01PrimeraInstancia` ya existe, **omitir**.

### b. Subcarpetas dentro de cada instancia:

Dentro de cada una de estas carpetas se debe crear una carpeta principal (identificada como `C01Principal`) para almacenar los documentos del trámite de la instancia. También se podrán crear carpetas para incidentes, medidas cautelares, acumulaciones, etc., identificadas como `C02`, `C03`, `C04`, etc.

Pasos:

1. Iterar recursivamente en todas las carpetas.
2. Omitir carpetas que ya tengan el nombre correcto.
3. Verificar si el nombre contiene una palabra clave.
4. Si se detecta, **renombrar** la carpeta.
5. Si no existen carpetas, **crear una llamada `C01Principal`**.

---

## 3. Organización de subcarpetas (reubicación)

1. Iterar recursivamente en todas las carpetas que comienzan por los primeros 5 dígitos del despacho judicial.
2. Si existe `01PrimeraInstancia`, mover subcarpetas a esa carpeta.
3. Verificar si existe la carpeta `01PrimeraInstancia/C01Principal`.
4. Mover archivos de la carpeta `056314` a `01PrimeraInstancia/C01Principal`.

---

## 4. Organización de archivos

1. Recorrer todas las carpetas y subcarpetas recursivamente.
2. Procesar nuevos nombres por subcarpeta.
3. Eliminar números al principio del nombre actual.
4. Crear un nuevo nombre **manteniendo la extensión**.
5. Renombrar el archivo.
6. Incrementar el índice.

---

## 5. Elaboración de índice electrónico

El índice electrónico del expediente es el mecanismo para identificar la **totalidad de documentos** que componen el expediente judicial electrónico o híbrido, debidamente ordenados, respetando su orden cronológico secuencial.

---

## Recomendaciones de identificación de archivos:

- Máximo **40 caracteres** en el nombre.
- No incluir **guiones ni espacios**.
- Usar solo **caracteres alfanuméricos**, sin caracteres especiales (`/#%&:<>().¿?`) ni tildes.
- Utilizar **mayúscula inicial**. Si el nombre es compuesto, usar mayúscula al inicio de cada palabra.
- Evitar el uso de:
  - Pronombres (ej. *el, la, los*).
  - Preposiciones (ej. *de, por, para*).
  - Abreviaturas.
- Si el nombre contiene un número de un solo dígito, debe estar antecedido por **0**.
- Fechas deben ir en formato `AAAAMMDD` (ej. 20250508 para 8 de mayo de 2025).