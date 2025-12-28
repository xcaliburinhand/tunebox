#!/bin/bash
# Install development stubs for RPi.GPIO
# This allows IDE/linter to resolve imports without actual hardware

echo "Installing RPi.GPIO stub package..."
pip install -e ./stubs

echo "✓ Development stubs installed successfully!"
echo "  Your IDE should now be able to resolve 'import RPi.GPIO'"

