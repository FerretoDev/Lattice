# CLAUDE.md

## Objetivo del proyecto
Este proyecto es el puente Java entre tu modelo en Python y Minecraft Java.

La idea es avanzar poco a poco:
1. Python contiene el modelo.
2. Java actúa como intermediario.
3. Minecraft Java recibe acciones o comandos.

## Contexto importante
En tu workspace existe el directorio raíz `Lattice`, donde está el modelo en Python.
Este proyecto `lattice-bridge` se encarga de la parte Java del puente.

## Estado actual
- Existe una prueba mínima en `src/main/java/App.java`.
- Ya existe una estructura base en `src/main/java/com/tuproyecto`.
- La build usa Gradle.

## Build system
- Gradle con Groovy DSL
- Archivo: `build.gradle`
- No se usa `build.gradle.kts`

## Estructura inicial creada
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

## Motivo de esta estructura
- `App.java` en raíz: prueba mínima para empezar sin complicarse.
- `com/tuproyecto/App.java`: punto de entrada real recomendado para crecer ordenadamente.
- `bridge`: todo lo relacionado con comunicación con Python.
- `service`: coordinación entre componentes.
- `minecraft`: acciones que terminan en el juego.
- `model`: objetos de datos que representarán respuestas del modelo.

## Estrategia de trabajo
### Fase 1: base Java
- Mantener el arranque simple.
- Aprender la estructura mínima del proyecto.
- Entender cómo compilar y ejecutar.

### Fase 2: comunicación con Python
- Crear un cliente Java.
- Llamar a un API local en Python.
- Recibir y parsear JSON.

### Fase 3: acciones de Minecraft
- Traducir la respuesta del modelo a comandos o eventos.
- Integrar con un servidor o plugin de Minecraft Java.

## Reglas simples para no complicarse
- Empezar siempre por lo mínimo funcional.
- Un archivo = una responsabilidad.
- Primero imprimir o probar datos, después conectar Minecraft.
- Evitar mezclar lógica de red, lógica de modelo y lógica de Minecraft en la misma clase.

## Próximo paso recomendado
Crear una prueba muy pequeña:
- Python expone un endpoint local.
- Java lo consulta.
- Java imprime la respuesta.

## Comandos útiles
Compilar y probar:
```bash
./gradlew test
```

Ejecutar una clase Java simple:
```bash
cd src/main/java
javac App.java
java App
```

## Notas para futuras mejoras
Cuando el puente ya funcione, se puede añadir:
- un paquete de configuración
- pruebas unitarias
- cliente HTTP más robusto para Python
- integración con Paper/Spigot
- logging más claro
- mapeo de respuestas del modelo a acciones concretas
