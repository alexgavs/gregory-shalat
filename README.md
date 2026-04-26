# gregory-shalat

Multi-gate 433 MHz remote replay firmware for a Digispark (ATtiny85) board — opens several different gates (named after their owners) by replaying captured RF on/off timings.

## What it does

On power-up the device cycles through a series of pre-recorded RF key patterns and transmits each one several times via a 433 MHz transmitter wired to `PB2`, blinking an LED on `PB1` between groups so the operator can tell which key is being sent.

Replayed keys (declared in `src/main.cpp`):

| Key   | Comment in source    |
|-------|----------------------|
| Key1  | "butt1 offer universal" |
| Key2  | "butt2 universal"       |
| Key3  | "butt3 universal"       |
| Key4  | "gregory universal"     |
| Key5  | "leonid big key 1" (open) |
| Key6  | "leonid small key 2" (close) |
| Key7  | "yohav"                  |

`KeySend()` walks the timing array, toggling the TX pin for each entry — negative values are treated as `delay()` in milliseconds, positive values as `delayMicroseconds()`.

## Stack

- Language: C++ (Arduino framework)
- Target board: `digispark-tiny` (ATtiny85) — see `platformio.ini`
- Build system: PlatformIO (`platform = atmelavr`, `framework = arduino`)
- Conversion helper: `cnv/s2p.py` — Python script (kept alongside the firmware, presumably for converting captured signal data into the C arrays).

## Build / Run

```bash
pio run                # build
pio run -t upload      # flash to the Digispark
```

(Requires PlatformIO Core. The Digispark uses the micronucleus bootloader for upload.)

## Wiring

| Pin  | Function                     |
|------|------------------------------|
| PB2  | 433 MHz transmitter data in  |
| PB1  | Status LED                   |

## Layout

```
gregory-shalat/
├── platformio.ini
├── src/main.cpp        — key arrays + transmit/blink loop
├── cnv/s2p.py          — capture-to-array conversion helper
├── include/, lib/, test/  — PlatformIO standard folders (placeholder READMEs)
├── .travis.yml
└── .vscode/
```

## Status

Maintenance.
