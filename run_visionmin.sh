#!/bin/bash
# Script chay VisionMin.AI tren Raspberry Pi
# Cach dung: ./run_visionmin.sh

echo "=========================================="
echo "VisionMin.AI - Raspberry Pi Startup"
echo "=========================================="
echo ""

# 1. Fix audio system
echo "1. Fix audio system..."
systemctl --user stop pipewire pipewire-pulse wireplumber 2>/dev/null
killall pipewire pipewire-pulse wireplumber 2>/dev/null
systemctl --user start pipewire pipewire-pulse wireplumber 2>/dev/null
sleep 3

# 2. Set USB microphone as default
echo "2. Set USB microphone as default..."
USB_MIC_ID=$(wpctl status | grep "AB13X.*Source" | grep -oP '^\s*\K\d+' | head -1)
if [ -n "$USB_MIC_ID" ]; then
    wpctl set-default "$USB_MIC_ID"
    echo "   USB microphone ID: $USB_MIC_ID set as default"
else
    echo "   Warning: USB microphone not found"
fi

# 3. Check Python venv
echo "3. Check Python environment..."
if [ ! -d ~/visionmin-venv ]; then
    echo "   Creating venv..."
    python3 -m venv ~/visionmin-venv --system-site-packages
fi

# 4. Activate venv
echo "4. Activate venv..."
source ~/visionmin-venv/bin/activate

# 5. Install dependencies if needed
echo "5. Check dependencies..."
pip list | grep -q SpeechRecognition || pip install -q SpeechRecognition
pip list | grep -q pyaudio || pip install -q pyaudio

# 6. Set DISPLAY for camera preview
echo "6. Set DISPLAY..."
export DISPLAY=:0

# 7. Run app
echo ""
echo "=========================================="
echo "Starting VisionMin.AI..."
echo "=========================================="
echo ""

cd ~/picamera2/apps
python3 app_visionmin_standalone.py
