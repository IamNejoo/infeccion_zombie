# Simulación de Edificio con Zombis

## Descripción

Este proyecto simula la propagación de una infección zombi dentro de un edificio. La simulación permite configurar un edificio con múltiples pisos y habitaciones, observar cómo se propaga la infección de zombis, y tomar acciones para contener la propagación.

## Características principales

- Simulación de propagación de zombis por habitaciones adyacentes
- Sistema de sensores IoT para monitorear el estado de las habitaciones
- Mecanismos de bloqueo para prevenir la propagación
- Funciones para limpiar habitaciones infectadas
- Persistencia del estado mediante archivos JSON
- Interfaz de línea de comandos para controlar la simulación

## Requisitos previos

- Python 3.6 o superior
- Módulos estándar de Python (random, time, json)

## Instalación

No se requiere instalación específica más allá de Python. Simplemente clone el repositorio o descargue el archivo principal.

```bash
git clone https://github.com/tu-usuario/infeccion_zombie.git
cd infeccion_zombie
```

## Ejecución

Para iniciar la simulación, ejecute el siguiente comando en la terminal:

```bash
python simulacion.py
```

## Arquitectura

La aplicación sigue un diseño orientado a objetos con las siguientes clases principales:

### Sensor
Representa el dispositivo que detecta la presencia de zombis en una habitación.
- Estados: 'normal', 'alert'
- Métodos: set_alert(), reset()

### Room (Habitación)
Unidad básica del edificio que contiene un sensor y puede albergar zombis.
- Atributos: número de habitación, sensor, estado de infección, estado de bloqueo
- Métodos: add_zombies(), remove_zombies(), block_room(), unblock_room(), reset_sensor()

### Floor (Piso)
Colección de habitaciones que forman un nivel del edificio.
- Atributos: número de piso, lista de habitaciones
- Métodos: is_fully_infected()

### Building (Edificio)
Estructura completa compuesta por pisos.
- Atributos: lista de pisos
- Métodos: infect_random_room(), is_fully_infected(), save_state(), load_state()

### Simulation (Simulación)
Controla la lógica de la simulación y la interacción con el usuario.
- Atributos: edificio, contador de turnos
- Métodos: setup_building(), show_status(), advance_turn(), clean_room(), reset_sensor(), run_simulation()

## Mecánica de la simulación

### Infección inicial
- Al configurar el edificio, se selecciona aleatoriamente una habitación para ser infectada y se propague la infeccion.

### Propagación de zombis
- En cada turno, los zombis intentan propagarse a las habitaciones adyacentes horizontales (mismo piso).
- Existe un 30% de probabilidad de que los zombis se propaguen verticalmente a pisos superiores o inferiores.

### Contención
- Las habitaciones bloqueadas no pueden ser infectadas ni propagar la infección.
- Las habitaciones infectadas pueden ser limpiadas manualmente, eliminando los zombis.
- Los sensores de las habitaciones limpiadas deben ser reseteados manualmente.

### Persistencia
- El estado de la simulación puede guardarse en un archivo JSON.
- Se puede cargar una simulación previamente guardada, sustituyendo la simulación actual.

## Instrucciones de uso

La aplicación presenta un menú con las siguientes opciones:

1. **Configurar edificio**: Define el número de pisos y habitaciones del edificio y crea una nueva simulación.
2. **Mostrar estado del edificio**: Muestra la situación actual de todas las habitaciones.
3. **Avanzar turno**: Simula el siguiente paso en la propagación de zombis.
4. **Bloquear habitación**: Evita que una habitación específica sea infectada o propague zombis.
5. **Desbloquear habitación**: Permite que una habitación previamente bloqueada pueda ser infectada.
6. **Limpiar habitación**: Elimina los zombis de una habitación infectada.
7. **Resetear sensor**: Restablece el sensor de una habitación limpia a estado normal.
8. **Guardar estado**: Almacena la configuración actual en un archivo.
9. **Cargar estado**: Carga una simulación previamente guardada.
10. **Salir**: Termina la aplicación.

## Ejemplo de uso

1. Inicie la aplicación.
2. Seleccione la opción 1 para configurar un edificio (por ejemplo, 3 pisos con 4 habitaciones cada uno).
3. Use la opción 2 para ver el estado inicial del edificio (una habitación estará infectada aleatoriamente).
4. Seleccione la opción 3 para avanzar un turno y ver cómo se propaga la infección.
5. Utilice las opciones 4-7 para intentar contener la propagación bloqueando y limpiando habitaciones estratégicas.
6. Guarde su progreso con la opción 8 si lo desea.

## Supuestos importantes

- Una habitación bloqueada no puede ser infectada ni propagar zombis.
- La limpieza de habitaciones y el reseteo de sensores deben realizarse manualmente.
- La propagación vertical (entre pisos) tiene una probabilidad del 30%.
- Al cargar un estado guardado, se sustituye completamente la simulación actual.
- Los zombis se propagan en cada turno a las habitaciones adyacentes que no estén bloqueadas.
- Un piso completamente infectado aumenta la probabilidad de infectar los pisos adyacentes.

## Notas adicionales

- Los sensores alertan sobre la presencia de zombis, pero no toman acciones automáticamente.
- Una estrategia efectiva es bloquear habitaciones para crear "zonas seguras" y limpiar sistemáticamente las áreas infectadas.
- La simulación termina cuando todas las habitaciones están infectadas, a menos que se tomen medidas para prevenir la propagación total.