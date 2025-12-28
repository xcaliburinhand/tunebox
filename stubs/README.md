# RPi.GPIO Stub Package

This is a development stub package that provides the same interface as `RPi.GPIO` 
but without actual hardware control. It's designed for development environments 
where the actual RPi.GPIO library is not available (e.g., on non-Raspberry Pi systems).

## Installation

```bash
pip install -e ./stubs
```

## Usage

After installation, you can import `RPi.GPIO` as normal:

```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
```

All functions are stubs that log their calls but don't perform actual hardware operations.

## Production

On a Raspberry Pi, install the real package:
```bash
pip install RPi.GPIO
```

The stub package will be automatically overridden by the real package if both are installed.

