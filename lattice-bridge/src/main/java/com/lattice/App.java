package com.lattice;

/**
 * Punto de entrada recomendado para el subproyecto.
 *
 * ¿Por qué existe?
 * - Centraliza el arranque del puente Java.
 * - Evita mezclar la lógica de arranque con la lógica de red o Minecraft.
 *
 * ¿Para qué sirve ahora?
 * - Mostrar que la estructura base ya está preparada.
 * - Servir como lugar natural para arrancar el servicio principal.
 *
 * ¿Qué podrías cambiar en el futuro?
 * - Iniciar un cliente HTTP hacia Python.
 * - Cargar configuración desde archivo o variables de entorno.
 * - Conectar con un plugin o servidor de Minecraft.
 */
public class App {
    public static void main(String[] args) {
        System.out.println("lattice-bridge: estructura base lista.");
        System.out.println("Siguiente paso: conectar Python -> Java -> Minecraft.");
    }
}

