# lattice-bridge

Puente en Java para conectar tu modelo en Python con Minecraft Java.

## Idea general
Este subproyecto será el intermediario entre:
- tu modelo en Python, que vive en el directorio raíz `Lattice`
- Java, que recibe la respuesta del modelo y decide qué hacer
- Minecraft Java, que ejecuta acciones, mensajes o comandos

## Estado actual
El proyecto está en una fase muy inicial. Por ahora tienes:
- `src/main/java/App.java` como prueba mínima
- una estructura base bajo `src/main/java/com/tuproyecto`

La idea es que primero entiendas la forma del proyecto, y después vayamos creciendo sin mezclar demasiadas responsabilidades en una sola clase.

## Estructura inicial del subproyecto
```text
src/main/java/
├── App.java
└── com/tuproyecto/
    ├── App.java
    ├── bridge/
    │   └── PythonClient.java
    ├── service/
    │   └── BridgeService.java
    ├── minecraft/
    │   └── MinecraftActions.java
    └── model/
        └── ModelResponse.java
```

## Para qué sirve cada parte

### `src/main/java/App.java`
Prueba inicial muy simple.

**Motivo:**
- sirve para comprobar que el proyecto compila y ejecuta sin complicarte

**Para qué ahora:**
- validar que Java funciona correctamente

**Futuro posible:**
- puede dejar de usarse cuando todo el arranque quede dentro del paquete `com.lattice`

### `src/main/java/com/tuproyecto/App.java`
Punto de entrada recomendado para el subproyecto.

**Motivo:**
- centraliza el arranque de la aplicación
- evita que la lógica principal quede en el archivo de prueba

**Para qué ahora:**
- mostrar la estructura base del proyecto

**Futuro posible:**
- iniciar el servicio principal
- cargar configuración
- arrancar el cliente hacia Python o el módulo de Minecraft

### `bridge/PythonClient.java`
Cliente que hablará con Python.

**Motivo:**
- la comunicación con el modelo debe vivir separada del resto

**Para qué ahora:**
- reservar el lugar donde irá la llamada a la API local de Python

**Futuro posible:**
- usar `HttpClient`
- manejar timeouts, reintentos y errores
- enviar prompts y leer JSON

### `service/BridgeService.java`
Capa que coordina el flujo general.

**Motivo:**
- une los componentes sin mezclar demasiadas responsabilidades

**Para qué ahora:**
- dejar visible el flujo general: Python -> Java -> Minecraft

**Futuro posible:**
- transformar respuestas del modelo en acciones reales
- decidir cuándo llamar a Python y cuándo ejecutar algo en Minecraft

### `minecraft/MinecraftActions.java`
Acciones del mundo Minecraft.

**Motivo:**
- la lógica de juego debe estar aislada del cliente Python

**Para qué ahora:**
- reservar el lugar donde irán mensajes, comandos o eventos

**Futuro posible:**
- enviar mensajes al chat
- ejecutar comandos en Paper/Spigot
- responder a eventos del jugador o del mundo

### `model/ModelResponse.java`
Modelo de datos para representar la respuesta de Python.

**Motivo:**
- tener una estructura clara para los datos que devolverá el modelo

**Para qué ahora:**
- preparar el proyecto para cuando Python empiece a devolver JSON

**Futuro posible:**
- añadir campos como confianza, tipo de acción o metadata
- validar la respuesta antes de usarla

## Build system
Este proyecto usa Gradle con Groovy DSL.

- Archivo: `build.gradle`
- No se usa `build.gradle.kts`

## Cómo ejecutar la prueba actual
### Con Gradle
```bash
./gradlew test
```

### Ejecutando `App.java` directamente
```bash
cd src/main/java
javac App.java
java App
```

## Cómo crecer sin perderte
Te recomiendo avanzar en este orden:
1. probar Java solo
2. crear el cliente hacia Python
3. devolver JSON simple
4. traducir la respuesta en Java
5. conectar esa respuesta con Minecraft

## Siguiente paso sugerido
La siguiente mejora natural sería crear un endpoint local en Python y hacer que `PythonClient` lo consulte. Así ya tendrías el primer puente real.
