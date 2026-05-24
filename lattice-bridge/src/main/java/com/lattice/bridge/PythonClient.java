package com.lattice.bridge;

/**
 * Cliente que en el futuro hablará con Python.
 *
 * ¿Por qué existe?
 * - La comunicación con el modelo debe vivir en una clase propia.
 * - Así no mezclas red, parseo JSON y reglas del dominio.
 *
 * ¿Para qué sirve ahora?
 * - Dejar preparado el lugar donde irá la llamada al API local de Python.
 *
 * ¿Qué podrías cambiar en el futuro?
 * - Usar HttpClient de Java.
 * - Añadir timeouts, reintentos y manejo de errores.
 * - Enviar prompts y leer respuestas JSON.
 */
public class PythonClient {
    public String sendPrompt(String prompt) {
        throw new UnsupportedOperationException("PythonClient todavía no está implementado.");
    }
}

