package com.lattice.minecraft;

/**
 * Acciones que, en el futuro, se traducirán a comandos o eventos de Minecraft.
 *
 * ¿Por qué existe?
 * - Minecraft debe tener su propia capa de acciones.
 * - Así no mezclas la lógica del modelo con la lógica del juego.
 *
 * ¿Para qué sirve ahora?
 * - Reservar el lugar donde irán mensajes, comandos o eventos.
 *
 * ¿Qué podrías cambiar en el futuro?
 * - Enviar mensajes al chat.
 * - Ejecutar comandos en un servidor Paper/Spigot.
 * - Responder a eventos del jugador o del mundo.
 */
public class MinecraftActions {
    public void sendChatMessage(String message) {
        throw new UnsupportedOperationException("MinecraftActions todavía no está implementado.");
    }
}

