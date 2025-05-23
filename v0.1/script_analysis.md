# Script Analysis

Los siguientes son los pasos que se deben ejecutar en el presente proyecto para
que los expedientes judiciales cumplan las condiciones para migración al
**SISTEMA DE GESTIÓN DE DOCUMENTOS ELECTRÓNICOS DE ARCHIVO**, dispuesto para la
administración de documentos por el Consejo Superior de la Judicatura.

Los expedientes a migrar deben cumplir con el protocolo para la gestión de
documentos electrónicos. Para ello, seguiremos los siguientes pasos:

---

## 0. Eliminar carpetas vacías e índices electrónicos

1. **Listar en un archivo CSV** todos los nombres de archivos que cumplan las
siguientes condiciones:
   - Que sean archivos de Excel.
   - Que contengan la palabra *índice* en el nombre.

2. **Eliminar** todas las carpetas vacías y todos los índices electrónicos
existentes en la ruta a organizar que
cumplan que contengan la palabra indice en su nombre ya sea con mayusculas o
minusculas y sean excel

---

## 1. Organización de carpetas

### a. Renombrar carpeta electrónica del proceso judicial

1. Verifica si el nombre de La carpeta electrónica del proceso judicial tiene
23 dígitos números an principio del nombre
   No Cumple Ejemplo: 2023-00234 Ejecutivo Singular
   Cumple Ejemplo: `1001750302520200234501`

2. Se debe contar con los **primeros 12 dígitos del despacho judicial**.
   Nombre original Ejemplo: 2023-00234 Ejecutivo Singular
   Nombre nuevo Ejemplo: 0538040890012023-00234 Ejecutivo Singular

3. Los siguientes **9 dígitos** corresponden al número del proceso judicial.
   El número del proceso judicial es: 2023-00234

4. Los **últimos 2 dígitos serán 00** después del número del proceso judicial.
   Nombre original Ejemplo: 2023-00234 Ejecutivo Singular
   Nombre nuevo Ejemplo: 0538040890012023-0023400 Ejecutivo Singular

5. Contar en el nombre de la carpeta todos los caracteres que haya después de
los números del nombre original:
    Ejemplo: 0538040890012023-0009400 Ejecutivo Singular Minima Seguir Ejecución

6. Modificar el nombre de la carpeta electronica lo siguiente:
   - No queden espacios ni caracteres especiales.
   - El nombre no exceda los **39 caracteres**.

   Ejemplo: "05380408900120230009400EjecutivoSingular"

7. El número del proceso debe ir separado con un espacio de las palabras.
   05380408900120230009400 EjecutivoSingula

8. si hay una carpeta con el mismo nombre genere un reporte csv con el nombre
y la ruta y no cambie el nombre

9. Generar reporte con los nombres de carpeta que cambio, nombre original,
nombre nuevo y ruta

## 2. Organización de subcarpetas

### a. Estructura por instancia

La carpeta electrónica del proceso puede subdividirse en otras carpetas para
contemplar las etapas procesales y permitir la participación de todos los
despachos y personas intervinientes:

- `01PrimeraInstancia` (ó `01UnicaInstancia`)
- `02SegundaInstancia`
- `03RecursosExtraordinarios`
- `04Ejecucion`

Pasos:

1. Iterar en todas las carpetas cuyo nombre inicia con los
**5 primeros dígitos del radicado del despacho**.

2. Si no existe la carpeta `01PrimeraInstancia` y no existe una carpeta
`01UnicaInstancia`, **crear** la carpeta
`01PrimeraInstancia`

3. Crear reporte con las rutas de las carpetas nuevas, nombre y ruta

### b. Subcarpetas dentro de cada instancia

Ejemplo:

- 05380408900120230009400 EjecutivoSingula/
-- 01PrimeraInstancia/
-- ...

Dentro de cada carpeta electrónica se debe crear una carpeta principal
(identificada como `C01Principal`) para almacenar los documentos del trámite
de la instancia. También se podrán crear carpetas para incidentes, medidas
cautelares, acumulaciones, etc., identificadas como `C02`, `C03`, `C04`, etc.

Pasos:

1. Iterar recursivamente en todas las carpetas con los **5 primeros dígitos del
radicado del despacho**

2. Omitir carpetas que ya tengan los nombres C0

3. Si no empieza con C0, Verificar si el nombre contiene una palabra clave como:
    palabras_principal = ['principal', 'Principal', 'ppal', 'PPAL', 'Ppal',
'PRINCIPAL', 'CuadernoUnico',
'01.Expediente Restitutucion 056314089001201800150  ST', '01 Unica Instancia']
    palabras_medidas = ['medida', 'Medida', 'MEDIDA', 'M.C', 'M. Cautelar',
'Media Cautelar', 'MS', 'Medias Cautelares',
'MEDIDA CAUTELAR']
    palabras_acumulacion = ['acumulacion', 'ACUMULACION', 'Acumulacion']
    palabras_titulos = ['deposito', 'titulo', 'TITULO' 'Deposito' 'DEPOSITOS'
'Titulo', 'DJ04']
palabras_indicentes = ['indidente', 'incidentes', 'INCIDENTE', ' Incidente',
'Incidentes', 'INCIDENTES']
**NOTA**: Revisar estas palabras basado en el reporte de nombres de carpetas.

4. Si se detecta, **renombrar** la carpeta.
    palabras_principal -> C01Principal
    palabras_medidas -> C05MedidasCautelares
    palabras_acumulacion -> C03AcumulacionProcesos
    palabras_titulos -> C04DepositosJudiciales
    palabras_incidentes -> C02Incidentes

5. Si no existen carpetas que inicien con C0, y solo archivos y solo una carpeta
llamada 01PrimeraInstancia entonces
**crear una carpeta llamada `C01Principal`**.

6. crear reporte con las carpetas que se renombraron, nombre original, nombre
nuevo y ruta.

7. crear un reporte con las carpetas nuevas, nombre y ruta.

---

## 3. Organización de subcarpetas (reubicación)

Estructura de carpetas hasta ahora:

- 05380408900120230009400 EjecutivoSingula/
-- 01PrimeraInstancia/
-- C01Principal/
-- C05MedidasCautelares/
-- archivo1.jpg
-- subsanacion/

1. Iterar recursivamente en todas las carpetas que comienzan por los primeros
5 dígitos del despacho judicial.
ejm: 05380

2. Si existe `01PrimeraInstancia`, mover las subcarpetas de la carpeta padre
que inicien por C0 a la
carpeta `01PrimeraInstancia`

3. Verificar si existe la carpeta `01PrimeraInstancia/C01Principal`.

4. Mover archivos de la carpeta `056314` a `01PrimeraInstancia/C01Principal/`.

Resultado:

- 05380408900120230009400 EjecutivoSingula/
-- 01PrimeraInstancia/
--- C01Principal/
---- archivo1.jpg
--- C05MedidasCautelares/
-- subsanacion/

---

## 4. Organización de archivos

1. Recorrer todas las carpetas y subcarpetas recursivamente.

2. Validar si todos los archivos empiezan por números

3. Si todos empiezan por numeros, Ordenar los archivos de forma descendente,
si hay más de 100 archivos, ordenar por
los primeros 3 caracteres, si no, por los primeros 2.
Ejemplo:
   - 01 archivo1.jpg
   - 02 prueba.jpg

4. Si no todos los archivos tienen numero, ordenar por la fecha de creación de
forma ascendente, es decir la más
antigua primero.

5. Cargar el orden en que están los archivos organizados en la carpeta en un
arreglo

6. Eliminamos todos los numeros antes de la primera letra de izquierda a derecha
    Nombre Original: 02 2023-00094 2023-07-14 Memorial
    Nombre nuevo: Memorial

7. Crear un nuevo nombre **manteniendo la extensión**, eliminando: Caracteres
especiales, espacios y limitandolo a 35 caracteres y validar si no existe un
archivo con ese nombre, si existe, añadirle un contador al final del
nuevo nombre de ese archivo
    Nombre Anterior: Memorial-admisión
    Nombre nuevo: Memorialadmision

    Ejemplo Nombre duplicado: Memorialadmision 01

8. Renombrar el archivo colocandole el numero al principio de la posición en
que se encuentra ordenado en el arreglo,
ejm: 01, 02 ...
   Nombre Final: 01 Memorialadmision
                 02 Memorialadmision 01

9. Generar reporte csv con el nombre original, nombre final y ruta, ordenado
por(Numero/Fechas).

---

## 5. Elaboración de índice electrónico

El índice electrónico del expediente es el mecanismo para identificar la
**totalidad de documentos** que componen el expediente judicial electrónico
o híbrido, debidamente ordenados, respetando su orden cronológico secuencial.

1. Crear el archivo `00IndiceElectronicoC0{numero-carpeta-padre}.xlsm` en
todas las carpetas que empiecen con C0

2. Usar de plantilla el archivo: "FormatoIndiceElectronico.xlsm"

3. Usar la base de datos para obtener el radicado

---

## Recomendaciones de identificación de archivos

- Máximo **40 caracteres** en el nombre.
- No incluir **guiones ni espacios**.
- Usar solo **caracteres alfanuméricos**, sin caracteres especiales
(`/#%&:<>().¿?`) ni tildes.
- Utilizar **mayúscula inicial**. Si el nombre es compuesto, usar
mayúscula al inicio de cada palabra.
- Evitar el uso de:
  - Pronombres (ej. *el, la, los*).
  - Preposiciones (ej. *de, por, para*).
  - Abreviaturas.
- Si el nombre contiene un número de un solo dígito, debe estar
antecedido por **0**.
- Fechas deben ir en formato `AAAAMMDD` (ej. 20250508 para 8 de mayo de 2025).
