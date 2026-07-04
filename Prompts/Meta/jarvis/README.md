# Jarvis — Interfaz de Voz para el Segundo Cerebro

Script Python que actúa como capa de voz sobre Claude Code CLI.
Escucha un comando, lo interpreta, lo ejecuta vía `claude` CLI, y responde en voz alta.

---

## Instalación de dependencias

```bash
pip3 install SpeechRecognition pyaudio requests watchdog
```

> **macOS:** `pyaudio` requiere PortAudio. Si falla, instala primero:
> ```bash
> brew install portaudio
> pip3 install pyaudio
> ```

El TTS no usa ninguna librería de Python — `hablar()` invoca el comando nativo
`say -v Mónica` de macOS directamente vía `subprocess`. Nada que instalar para eso.

---

## Cómo ejecutar

Desde la raíz del Segundo Cerebro:

```bash
python3 Prompts/Meta/jarvis/jarvis.py
```

El script escucha **una vez**, procesa el comando y termina.

---

## Comandos de voz disponibles

| Intent | Frase de ejemplo |
|--------|-----------------|
| Crear concepto | *"Crea un concepto sobre diseño especulativo"* |
| Profundizar concepto | *"Profundiza el concepto pit-stop-cognitivo"* |
| Correlacionar | *"Correlaciona capital-de-contexto con feedback-que-escala"* |
| Listar conceptos | *"¿Qué conceptos tengo?"* / *"Lista mis conceptos"* |

---

## Troubleshooting

**"Micrófono no disponible"**
- Verifica que `pyaudio` esté instalado: `pip3 install pyaudio`
- En macOS, ve a Preferencias del Sistema → Privacidad → Micrófono y activa permisos para Terminal

**"Claude Code CLI no está disponible"**
- Verifica que `claude` esté en el PATH: `which claude`
- Si usas la extensión de VSCode, asegúrate de abrir la terminal desde el proyecto

**Error de pyaudio al instalar en macOS (Apple Silicon)**
```bash
brew install portaudio
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip3 install pyaudio
```

**El STT no reconoce el español correctamente**
- Habla despacio y con claridad
- El reconocedor usa `es-ES`; si tu acento es latinoamericano y hay problemas, edita
  `language="es-ES"` → `language="es-419"` en `escuchar()` dentro de `jarvis.py`

---

## Arquitectura

```
VOZ → [STT Google, vía speech_recognition] → texto → detectar_intent()
                                                          ↓
                              Groq (clasificador) — con fallback a keywords si Groq falla
                                                          ↓
                    tres carriles según el intent: Groq directo | mejora_006_filesystem | claude CLI
                                                          ↓
                                 resumir_output() → [TTS `say` nativo de macOS] → VOZ
```

Las operaciones de archivos (`operacion_archivo`) no invocan Claude Code — se resuelven
directamente en `mejora_006_filesystem.py`. Las consultas y el razonamiento sobre el vault
(`consulta_simple`, `razonamiento_profundo`, `conversacion_libre`) tampoco — se resuelven
con Groq. Solo `accion_directa` y los intents de visión que escriben el vault
(`profundizar_pantalla`, `capturar_como_concepto`) invocan `claude` CLI.

---

## Instalación del daemon (wake word — Mejora 002b)

El daemon corre en segundo plano desde el login y responde al decir **"Jarvis"**.
La detección de wake word NO usa un modelo local de wake-word (OpenWakeWord) — usa
el mismo STT de Google vía `speech_recognition` que el resto del sistema: escucha
continuamente en ventanas cortas (`listen(timeout=1)`) y transcribe con
`recognize_google`; si el texto transcrito contiene alguna de las palabras en
`WAKE_WORDS` (`"jarvis"`, `"jarvi"`, `"jarvis!"`, `"oye jarvis"`), se activa. Esto
requiere conexión a internet (la transcripción es un request a la API de Google),
a cambio de no necesitar modelos ni umbrales de score locales.

### 1. Instalar dependencias

```bash
pip3.11 install SpeechRecognition pyaudio requests watchdog
```

> **macOS (Apple Silicon):** si `pyaudio` falla, instala PortAudio primero:
> ```bash
> brew install portaudio
> CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip3.11 install pyaudio
> ```

### 2. Configurar la API key de Groq

El daemon usa Groq (`llama-3.3-70b-versatile`) para clasificar intents y responder
consultas sobre el vault. Exporta `GROQ_API_KEY` en el entorno desde el que arranca
el LaunchAgent (ej. en el `.plist` o en el perfil de shell que lo lanza). Si Groq no
responde, el daemon cae a un clasificador por keywords más limitado — no se cae el
daemon.

### 3. Instalar y cargar el LaunchAgent

```bash
cp ~/Documents/Segundo_cerebro/Prompts/Meta/jarvis/com.segundocerebro.jarvis.plist \
   ~/Library/LaunchAgents/

launchctl load ~/Library/LaunchAgents/com.segundocerebro.jarvis.plist
```

### 4. Verificar que está corriendo

```bash
launchctl list | grep jarvis
```

---

## Comandos de control del daemon

```bash
# Detener
launchctl unload ~/Library/LaunchAgents/com.segundocerebro.jarvis.plist

# Reiniciar
launchctl unload ~/Library/LaunchAgents/com.segundocerebro.jarvis.plist
launchctl load   ~/Library/LaunchAgents/com.segundocerebro.jarvis.plist

# Ver logs en tiempo real
tail -f ~/Documents/Segundo_cerebro/Prompts/Meta/jarvis/jarvis.log
```

---

## Arquitectura del daemon

```
[BOOT] LaunchAgent → jarvis_daemon.py
    ↓ loop_principal()
    esperar_wake_word(): escucha continua (speech_recognition + Google STT),
        ventanas de listen(timeout=1) — sin bloquear, revisa "jarvis" en el texto
    Mónica dice "Dime, Luigui" (TTS via `say`)
    modo_escucha_activo(): ventana de 60s, se reinicia con cada respuesta completa
        procesar_comando() → escuchar() → detectar_intent() (Groq, fallback keywords)
        → despachar_intent() → uno de tres carriles (Groq directo | mejora_006_filesystem | claude CLI)
        → resumir_output_para_voz() → hablar() (TTS via `say`)
    tras MAX_SILENCIAS silencios seguidos o una despedida, vuelve al loop de wake word

En paralelo: un watcher (watchdog) observa Conocimiento/ y notifica por voz
cuando aparece o cambia un concepto/correlación, sin que el usuario lo pida.
```
