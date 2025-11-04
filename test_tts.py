#!/usr/bin/env python3
"""Test TTS tren Raspberry Pi"""

import sys
import os

print("=" * 60)
print("TEST TEXT-TO-SPEECH")
print("=" * 60)

# Test 1: espeak command line
print("\n1. Test espeak command line...")
import subprocess
try:
    result = subprocess.run(
        ["espeak", "-v", "vi", "Xin chào, đây là test giọng nói"],
        capture_output=True,
        timeout=5
    )
    if result.returncode == 0:
        print("   ✅ espeak hoạt động")
    else:
        print(f"   ❌ espeak lỗi: {result.stderr.decode()}")
except FileNotFoundError:
    print("   ❌ espeak chưa cài đặt")
    print("   💡 Cài: sudo apt-get install espeak")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 2: pyttsx3
print("\n2. Test pyttsx3...")
try:
    import pyttsx3
    print("   ✅ pyttsx3 đã cài đặt")
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        # Get voices
        voices = engine.getProperty('voices')
        print(f"   Có {len(voices)} giọng nói available")
        
        print("   🔊 Đang phát test...")
        engine.say("Xin chào, đây là giọng nói AI")
        engine.runAndWait()
        print("   ✅ pyttsx3 hoạt động")
        
    except Exception as e:
        print(f"   ❌ Lỗi khi chạy pyttsx3: {e}")
        
except ImportError:
    print("   ❌ pyttsx3 chưa cài đặt")
    print("   💡 Cài: pip install pyttsx3")

# Test 3: TTSManager
print("\n3. Test TTSManager...")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps/visionmin'))

try:
    from tts_manager import TTSManager
    print("   ✅ TTSManager module found")
    
    try:
        tts = TTSManager()
        print("   ✅ TTSManager khởi tạo thành công")
        
        print("   🔊 Đang phát test...")
        tts.speak("Hệ thống giám sát tư thế đang hoạt động", block=True)
        print("   ✅ TTSManager hoạt động")
        
    except Exception as e:
        print(f"   ❌ Lỗi TTSManager: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"   ❌ Không tìm thấy TTSManager: {e}")

# Test 4: Audio output
print("\n4. Kiểm tra audio output...")
try:
    result = subprocess.run(
        ["aplay", "-l"],
        capture_output=True,
        text=True
    )
    print("   Audio devices:")
    for line in result.stdout.split('\n'):
        if 'card' in line.lower() or 'device' in line.lower():
            print(f"   {line}")
            
    # Check default
    result = subprocess.run(
        ["wpctl", "status"],
        capture_output=True,
        text=True
    )
    print("\n   Default audio:")
    in_audio = False
    for line in result.stdout.split('\n'):
        if 'Audio' in line:
            in_audio = True
        if in_audio and ('Sinks:' in line or 'Default' in line):
            print(f"   {line}")
        if in_audio and 'Video' in line:
            break
            
except Exception as e:
    print(f"   ⚠️ Lỗi: {e}")

print("\n" + "=" * 60)
print("KẾT LUẬN")
print("=" * 60)
print("Nếu không nghe thấy âm thanh:")
print("1. Kiểm tra speaker/headphone đã cắm đúng port")
print("2. Tăng volume: alsamixer")
print("3. Set default audio output:")
print("   wpctl status  # xem ID của output device")
print("   wpctl set-default <ID>")
print("4. Test: speaker-test -t wav -c 2 -l 1")
print("=" * 60)
