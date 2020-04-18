# RandomTestGenerator

Script para la generación de exámenes aleatorios. 

## Paquetes requeridos
- python3
- pyyaml
- subprocess
- random

Es necesario contar con pdflatex instalado. Los paquetes de latex necesarios se encuentran disponibles en CTAN, por lo que la instalación de pdflatex debería ser suficiente.

## Estructura de archivos
```
- generator.py: Script ejecutable 
- READMY.md : Este documento
- config.yaml : Archivo de configuración
- DefinicionProblemas/ : Carpeta de definición de problemas a seleccionar
  \_ problems-1stprinciples.tex : ejemplo de definición de problemas
- assets/ : Archivos complementarios
  \_logo-utn.png : ejemplo de logo
```

## Modo de uso

1. Establecer los archivos de preguntas utilizando LaTeX según la plantilla provista. 
2. Configurar el archivo config.yaml tal como se detalla debajo.
3. Ejecutar script utilizando python
```
python generator.py
```
4. Los exámenes serán generados en la carpeta output especificada. Los archivos .out, .tex y .log son archivos auxiliares que pueden ser eliminados.

## Archivo de configuración

El archivo de configuración debe ser provisto con la información siguiente:
```
- student_number: entero, cantidad de exámenes a generar
- university: nombre de la universidad, información para el encabezado
- faculty: nombre de la facultad, información para el encabezado
- department: nombre del departamento, información para el encabezado
- subject: nombre de la materia, información para el encabezado
- topic: nombre de la universidad, información para el encabezado
- date: fecha, información para el encabezado
- logo: ruta del logo, generalmente dentro de assets
- question_bases: lista de archivos de base de preguntas.
- questions_per_file: lista de números indicando la cantidad de preguntas a seleccionar de cada archivo de question_bases
```
## Base de preguntas

Archivo .tex en el que se detallan preguntas. Es posible tener varios archivos para cada tema.
El formato es el especificado por el paquete probsoln de latex. 

```
\begin{defproblem}{id}
 \begin{onlyproblem}
    % Definición del problema
 \end{onlyproblem}
 \begin{onlysolution}
    % solución
 \end{onlysolution}
\end{defproblem}
```

Para más información sobre este paquete consultar [probsoln documentation](http://ctan.dcc.uchile.cl/macros/latex/contrib/probsoln/probsoln.pdf).

## Contacto

- Giovanni D. Rottoli: gd.rottoli@gmail.com
- Carlos Casanova: carlos.casanova16@gmail.com
- Gonzalo Gorosito: gonzalogmg09@gmail.com




