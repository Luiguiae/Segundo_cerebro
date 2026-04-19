# Jarvis — Interfaz de Voz para el Segundo Cerebro

Script Python que actúa como capa de voz sobre Claude Code CLI.
Escucha un comando, lo interpreta, lo ejecuta vía `claude` CLI, y responde en voz alta.

---

## Instalación de dependencias

```bash
pip3 install SpeechRecognition pyttsx3 pyaudio
```

> **macOS:** `pyaudio` requiere PortAudio. Si falla, instala primero:
> ```bash
> brew install portaudio
> pip3 install pyaudio
> ```

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
VOZ → [STT Google] → texto → detectar_intent() → construir_prompt()
                                                       ↓
                                              claude CLI (cwd: Segundo_cerebro/)
                                                       ↓
                                              resumir_output() → [TTS pyttsx3] → VOZ
```

`listar_conceptos` no invoca Claude Code — lee directamente el filesystem con glob recursivo.

---

## Instalación del daemon (wake word — Mejora 002b)

El daemon corre en segundo plano desde el login y responde al decir **"Hey Jarvis"**.

### 1. Instalar dependencias nuevas

```bash
pip3.11 install pvporcupine pvrecorder
```

### 2. Obtener API key de Picovoice

- Crear cuenta gratuita en https://console.picovoice.ai
- Copiar el **AccessKey** del dashboard (el tier gratuito incluye el wake word "Jarvis" built-in)

### 3. Editar el plist con tu API key

```bash
nano ~/Documents/Segundo_cerebro/Prompts/Meta/jarvis/com.segundocerebro.jarvis.plist
```

Reemplaza `[REEMPLAZAR_CON_TU_KEY]` con tu AccessKey de Picovoice.

### 4. Instalar y cargar el LaunchAgent

```bash
cp ~/Documents/Segundo_cerebro/Prompts/Meta/jarvis/com.segundocerebro.jarvis.plist \
   ~/Library/LaunchAgents/

launchctl load ~/Library/LaunchAgents/com.segundocerebro.jarvis.plist
```

### 5. Verificar que está corriendo

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
    ↓ loop infinito
    escucha frames de audio (PvRecorder)
    Pvporcupine.process(frame) → detecta "Hey Jarvis"
    Mónica dice "Dime"
    escuchar() → transcribir() → detectar_intent()
    construir_prompt() → claude CLI → resumir_output()
    Mónica lee respuesta
    ↑ vuelve al loop
```
