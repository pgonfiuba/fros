## Clase 3 - Sistemas de referencia y TF2

En esta clase se introducen los conceptos básicos de sistemas de referencia y transformaciones en ROS2 utilizando TF2.

Se trabaja sobre un modelo simplificado de doble péndulo, acompañado por un launch mínimo para visualizar el robot en RViz y explorar el árbol de transformaciones generado por `robot_state_publisher`.

En esta etapa del curso los modelos URDF y los launch files se utilizan únicamente como soporte para estudiar TF2, sin profundizar todavía en la descripción detallada de robots.

### Contenido incluido

* Modelo URDF simplificado de un doble péndulo
* Launch básico para visualización en RViz
* Ejemplos de transformaciones dinámicas y estáticas mediante TF2

### Scripts y notebooks (`src/clase3/scripts/`)

Se incluyen distintos ejemplos en Python para explorar el uso de transformaciones:

* Notebook con ejercicios básicos utilizando ángulos Euler RPY
* Nodo ROS2 que publica una transformación estática adicional respecto de `tool0`
* Nodo ROS2 que adquiere durante un intervalo de tiempo la traslación de `tool0` respecto de `base_link` y grafica su evolución

El objetivo es introducir:

* sistemas de referencia,
* representación de poses,
* árboles TF2,
* y consulta de transformaciones desde Python.


## Clase 4 - Modelado de robots: URDF, XACRO y cinemática en ROS2

En esta clase se trabaja sobre la descripción de robots mediante URDF y XACRO, incorporando además herramientas básicas para visualización en RViz y publicación de estados articulares desde Python.

### Launch files

Se incluyen tres versiones de launch para analizar progresivamente distintas estrategias de configuración:

* **Launch básico**
  Implementación completamente hardcodeada para visualizar un robot en RViz utilizando `robot_state_publisher` y `joint_state_publisher_gui`.

* **Launch con soporte XACRO**
  Variante mínima del launch anterior adaptada para procesar archivos `.xacro`.

* **Launch parametrizable**
  Versión más flexible que permite seleccionar el robot a cargar mediante parámetros de launch.

---

### Modelos incluidos (`robots/`)

La carpeta `robots` contiene distintos modelos y variantes utilizadas durante la clase y los trabajos prácticos:

* Modelo básico del robot **MyCobot 320**
* Mallas (`meshes`) y URDF del MyCobot
* Modelo de una **pinza adaptativa** para integrar como TP
* Modelo básico de un **doble péndulo**
* Variante del doble péndulo utilizando **XACRO** y parametrizaciones simples

---

### Scripts y notebooks (`scripts/`)

Se incluye una notebook en Python donde:

* Se implementa la cinemática directa (FK) e inversa (IK) de un doble péndulo
* Se analiza el comportamiento de distintas configuraciones cinemáticas y singularidades
* Se genera una trayectoria cartesiana en línea recta
* Se publican variables articulares mediante ROS2 para actualizar el movimiento del robot en RViz

El objetivo es practicar:

* cinemática geométrica,
* publicación de tópicos desde Python,
* e interacción entre notebooks y ROS2.
