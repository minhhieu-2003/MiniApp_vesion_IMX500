#!/bin/bash#!/bin/bash

# Script fix audio va microphone cho Raspberry Pi# Fix audio issues on Raspberry Pi



echo "Fix audio & microphone..."echo ' Fixing audio configuration...'

echo "========================================"

# 1. T?t JACK server (kh?ng c?n thi?t)

# 1. Kill tat ca audio processes conflictecho ' Disabling JACK audio server...'

echo "1. Dung JACK server..."systemctl --user stop jack 2>/dev/null || true

systemctl --user stop jack 2>/dev/null || truesystemctl --user disable jack 2>/dev/null || true

systemctl --user disable jack 2>/dev/null || true

killall jackd 2>/dev/null || true# 2. Kh?i ??ng PulseAudio

echo ' Starting PulseAudio...'

# 2. Restart PulseAudiopulseaudio --check || pulseaudio --start

echo "2. Restart PulseAudio..."

pulseaudio -k 2>/dev/null || true# 3. Set default audio output

sleep 2echo ' Setting default audio output...'

pulseaudio --start --log-target=syslog 2>/dev/null || truepactl set-default-sink 0 2>/dev/null || true

sleep 2

# 4. Test audio

# 3. List audio devicesecho ' Testing audio...'

echo ""speaker-test -t sine -f 1000 -l 1 2>/dev/null || echo ' speaker-test failed (this is OK)'

echo "ALSA Recording Devices:"

arecord -lecho ' Audio configuration complete!'

echo ''

echo ""echo ' ?? test TTS, ch?y:'

echo "PulseAudio Sources:"echo '   espeak \"Hello\" 2>/dev/null'

pactl list sources shortecho '   echo \"Hello\" | festival --tts 2>/dev/null'


# 4. Set USB microphone as default
echo ""
echo "3. Tim va set USB microphone lam default..."

# Tim USB audio device
USB_SOURCE=$(pactl list sources short | grep -i "usb" | head -1 | awk '{print $2}')

if [ -n "$USB_SOURCE" ]; then
    echo "Tim thay USB microphone: $USB_SOURCE"
    pactl set-default-source "$USB_SOURCE"
    echo "Da set lam default source"
else
    echo "Khong tim thay USB microphone"
    echo "Hay cam USB mic va chay lai script nay"
fi

# 5. Set microphone volume
echo ""
echo "4. Set microphone volume..."
if [ -n "$USB_SOURCE" ]; then
    pactl set-source-volume "$USB_SOURCE" 85%
    pactl set-source-mute "$USB_SOURCE" 0
    echo "Da set volume = 85%, unmute"
fi

# 6. Test recording
echo ""
echo "5. Test recording (3 giay)..."
echo "Noi gi do..."

arecord -D plughw:1,0 -d 3 -f cd /tmp/test_mic.wav 2>/dev/null && \
    echo "Ghi am thanh cong!" || \
    echo "Ghi am that bai"

# 7. Test playback
if [ -f /tmp/test_mic.wav ]; then
    echo "Phat lai test recording..."
    aplay /tmp/test_mic.wav 2>/dev/null && \
        echo "Phat lai thanh cong!" || \
        echo "Phat lai that bai"
    rm -f /tmp/test_mic.wav
fi

echo ""
echo "========================================"
echo "HOAN TAT!"
echo ""
echo "Chay test lai:"
echo "   python3 test_microphone.py"
echo ""
