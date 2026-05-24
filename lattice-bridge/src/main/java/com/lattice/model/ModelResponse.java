package com.lattice.model;

/**
 * Modelo de datos básico para representar la respuesta de Python.
 *
 * ¿Por qué existe?
 * - El puente necesita una forma estable de representar lo que devuelve el modelo.
 * - Guardar datos en una clase separada facilita probar y mantener el código.
 *
 * ¿Para qué sirve ahora?
 * - Tener una estructura lista para cuando Python devuelva JSON.
 *
 * ¿Qué podrías cambiar en el futuro?
 * - Añadir campos como tipo de acción, confianza o metadata.
 * - Crear validaciones más estrictas.
 */
public class ModelResponse {
    private final String action;
    private final String message;
    private final String payload;

    public ModelResponse(String action, String message, String payload) {
        this.action = action;
        this.message = message;
        this.payload = payload;
    }

    public String getAction() {
        return action;
    }

    public String getMessage() {
        return message;
    }

    public String getPayload() {
        return payload;
    }

    @Override
    public String toString() {
        return "ModelResponse{" +
                "action='" + action + '\'' +
                ", message='" + message + '\'' +
                ", payload='" + payload + '\'' +
                '}';
    }
}

