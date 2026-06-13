# Clase 2

Ejemplos de cogigo de ROS 2

## Compilación

```bash
colcon build --packages-select clase2 --symlink-install
source install/setup.bash
```

## Nodos

### Counter Publisher
El nodo counter_publisher maneja un contador incremental en ROS.

#### Topicos

- `counter_topic` (Publisher)
  - Tipo de mensajes: `std_msgs/Int32`
  - Publica el numero que esta contando

#### Parametros

- `counter_max` (integer, default: 10)
  - Maximo valor del contador antes que pare.
  - Puede ser configurado via el launchfile o la linea de comandos.
  - Ejemplo: `ros2 run clase2 counter_publisher counter_max:=5`

- `timer_period` (float, default: 1.0)
  - Tiempo para incrementar el contador.
  - Puede ser configurado via el launchfile o la linea de comandos.
  - Ejemplo: `ros2 run clase2 counter_publisher timer_period:=0.5`

#### Servicios

- `reset_counter` (std_srvs/Trigger)
  - rsetea el contador de vuelta a 0
  - Devuelve success cuando es llamado.

To run:
```bash
# Default configuración (cuenta a 10, publica cada 1 second)
ros2 run clase2 counter_publisher

# Custom configuración (cuenta a 5, publica cada 0.5 second)
ros2 run clase2 counter_publisher --ros-args -p counter_max:=5 -p timer_period:=0.5

# Resetea el contador
ros2 service call /reset_counter std_srvs/srv/Trigger "{}"
```

### Counter Subscriber
El nodo counter_subscriber recive el contador de los valores del publisher en ROS.

#### Topico

- `counter_topic` (Subscriber)
- Tipo de mensajes: `std_msgs/Int32`
- Receive los valores del publisher

Para ejecutarlo:
```bash
ros2 run clase2 counter_subscriber
```

## Uso

1. Abrir la terminal para iniciar el contador:
```bash
ros2 run clase2 counter_publisher
```

2. En la tarminal, para abrir un contador:
```bash
ros2 run clase2 counter_subscriber
```

El subscriber imprime los valores que recive del publisher.

## Launch File

Un launch file nos permite ejecutar ambos simultaneamente:

```bash
ros2 launch clase2 clase2.launch.py
```

Este launch file:
- Comienza ambos nodos en la misma terminal con un contador hasta 5 una frecuencia de 1 segundo.
- Configura ambos nodos para imprimir los resultados en la pantalla.

## Testing

El paquete que incluye tests basicos:
```bash
colcon test --packages-select clase2 --event-handlers console_direct+ --pytest-args
```

