package com.lattice.service;

import com.lattice.bridge.PythonClient;
import com.lattice.minecraft.MinecraftActions;

/**
 * Servicio principal del puente.
 *
 * ¿Por qué existe?
 * - Une las piezas sin que cada clase tenga demasiadas responsabilidades.
 * - Sirve como capa intermedia entre Python y Minecraft.
 *
 * ¿Para qué sirve ahora?
 * - Mostrar cómo se conectarán los componentes en el futuro.
 * - Hacer visible el flujo: Python -> Java -> Minecraft.
 *
 * ¿Qué podrías cambiar en el futuro?
 * - Leer una petición del usuario.
 * - Consultar Python.
 * - Traducir la respuesta a una acción de Minecraft.
 */
public class BridgeService {
    private final PythonClient pythonClient;
    private final MinecraftActions minecraftActions;

    public BridgeService(PythonClient pythonClient, MinecraftActions minecraftActions) {
        this.pythonClient = pythonClient;
        this.minecraftActions = minecraftActions;
    }

    public void start() {
        System.out.println("BridgeService preparado: aquí irá la orquestación del puente.");
        System.out.println("Futuro flujo: obtener dato de Python y enviar acción a Minecraft.");
    }
}

