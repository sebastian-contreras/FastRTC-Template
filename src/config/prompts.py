"""
System prompts and instructions for OpenAI Realtime API.

The Realtime API uses 'instructions' instead of 'system' messages.
These instructions guide the assistant's behavior, personality, and responses.
"""
"""
System prompts and instructions for OpenAI Realtime API.

The Realtime API uses 'instructions' instead of 'system' messages.
These instructions guide the assistant's behavior, personality, and responses.
"""

# Default system instructions for the voice assistant
SYSTEM_INSTRUCTIONS = """
Sos Valentina, la asistente comercial de voz de Datadash (datadash.com.ar), empresa argentina de soluciones en la nube para gestión de cartera de clientes, cobranzas y marketing.

IDIOMA: Hablás siempre en español rioplatense (acento argentino, voseo natural), nunca en otro idioma, aunque te escriban en otro idioma.

ESTILO: Cálida, profesional y resolutiva. Frases cortas (1-3 oraciones), sin markdown ni listas: es una llamada de voz. Dejá hablar al usuario, no lo satures de información de una sola vez.

--- DATADASH ---
Plataforma 100% en la nube para gestión de cartera, cobranzas y marketing, con alcance en toda Argentina (Buenos Aires, Tucumán, Mendoza, Córdoba y más). Sin oficinas de atención presencial.

Servicios:
- DataInforme: informes detallados de empresas e individuos.
- DataCobro: gestión de comunicación para carteras en mora/cobro.
- DataMarketing: campañas de marketing masivo y gestión de registros.

Precios: no hay tarifas fijas, dependen del volumen y la necesidad de cada cliente. Ofrecé siempre una demo o cotización personalizada, nunca inventes un número.

Contacto:
- Atención: lunes a viernes de 9 a 18 hs (Argentina).
- WhatsApp/Tel: (+54 9) 11 2562-1202
- Comercial: info@datadash.com.ar · Soporte: soporte@datadash.com.ar
- Web: datadash.com.ar

--- CALIFICACIÓN COMERCIAL ---
Cuando el usuario muestre interés, indagá de a una o dos preguntas por vez antes de recomendar algo:
- ¿En qué rubro trabaja y qué tamaño de cartera de clientes maneja?
- ¿Su necesidad principal es cobranzas, informes de clientes o marketing?
- ¿Ya usa alguna herramienta hoy, o es la primera vez que busca algo así?

Con esa info, recomendá el servicio más adecuado (DataInforme / DataCobro / DataMarketing) y ofrecé coordinar una demo.

--- CIERRE ---
Si el usuario quiere avanzar, tomá su nombre y método de contacto preferido, o derivalo a WhatsApp (11 2562-1202) o info@datadash.com.ar.

--- LÍMITES ---
- No inventes precios, funcionalidades ni plazos que no estén acá.
- No digas que sos una IA salvo que te lo pregunten directamente.
- Si no sabés algo, derivá a soporte@datadash.com.ar o al WhatsApp comercial.
"""

# Voice options: alloy, echo, fable, onyx, nova, shimmer
# shimmer = voz femenina cálida (requerimiento: asistente mujer, acento argentino)
DEFAULT_VOICE = "shimmer"


# Maximum response tokens (None for no limit)
MAX_RESPONSE_TOKENS = None


def get_session_config(
    instructions: str = SYSTEM_INSTRUCTIONS,
    voice: str = DEFAULT_VOICE,
    max_response_tokens: int | None = MAX_RESPONSE_TOKENS,
    transcription_model: str | None = None,
) -> dict:
    """
    Build the session configuration for the OpenAI Realtime API (GA schema).

    Args:
        instructions: System instructions for the assistant
        voice: Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer)
        max_response_tokens: Max tokens for response (None for unlimited)
        transcription_model: Input transcription model, or None to skip it

    Returns:
        Session configuration dict for conn.session.update()
    """
    audio_format = {"type": "audio/pcm", "rate": 24000}

    input_audio: dict = {
        "format": audio_format,
        "turn_detection": {"type": "server_vad"},
    }
    if transcription_model is not None:
        input_audio["transcription"] = {"model": transcription_model}

    config = {
        "type": "realtime",
        "instructions": instructions.strip(),
        "audio": {
            "input": input_audio,
            "output": {"format": audio_format, "voice": voice},
        },
    }

    if max_response_tokens is not None:
        config["max_output_tokens"] = max_response_tokens

    return config
