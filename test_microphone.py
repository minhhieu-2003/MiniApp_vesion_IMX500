#!/usr/bin/env python3
"""
Test microphone và audio input trên Raspberry Pi
Chạy trước khi dùng app_visionmin_standalone.py
"""

import sys

def test_pyaudio():
    """Test PyAudio có hoạt động không"""
    print("=" * 60)
    print("1️⃣ KIỂM TRA PYAUDIO")
    print("=" * 60)
    
    try:
        import pyaudio
        print("✅ PyAudio đã cài đặt")
        
        # List all audio devices
        p = pyaudio.PyAudio()
        print(f"\n📋 Tìm thấy {p.get_device_count()} thiết bị audio:\n")
        
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"Device {i}: {info['name']}")
            print(f"  - Input channels: {info['maxInputChannels']}")
            print(f"  - Output channels: {info['maxOutputChannels']}")
            print(f"  - Sample rate: {int(info['defaultSampleRate'])} Hz")
            print()
        
        # Get default input device
        try:
            default_input = p.get_default_input_device_info()
            print(f"✅ Default input device: {default_input['name']}")
            print(f"   Channels: {default_input['maxInputChannels']}")
        except Exception as e:
            print(f"❌ Không tìm thấy default input device: {e}")
        
        p.terminate()
        return True
        
    except ImportError:
        print("❌ PyAudio chưa cài đặt")
        print("💡 Cài đặt: pip install pyaudio")
        return False
    except Exception as e:
        print(f"❌ Lỗi PyAudio: {e}")
        return False


def test_speech_recognition():
    """Test SpeechRecognition"""
    print("\n" + "=" * 60)
    print("2️⃣ KIỂM TRA SPEECH RECOGNITION")
    print("=" * 60)
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition đã cài đặt")
        
        recognizer = sr.Recognizer()
        
        # List microphones
        print("\n📋 Danh sách microphones:")
        mics = sr.Microphone.list_microphone_names()
        for i, mic in enumerate(mics):
            print(f"  [{i}] {mic}")
        
        if not mics:
            print("❌ Không tìm thấy microphone nào!")
            return False
        
        # Test với default microphone
        print("\n🎤 Test microphone (ambient noise adjustment)...")
        try:
            with sr.Microphone() as source:
                print("   Đang điều chỉnh ambient noise (3 giây)...")
                recognizer.adjust_for_ambient_noise(source, duration=3)
                print(f"   ✅ Energy threshold: {recognizer.energy_threshold}")
                
                # Test ngắn - timeout nhanh để không chờ lâu
                print("   🎤 Nói gì đó (3 giây)...")
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    print(f"   ✅ Đã ghi âm {len(audio.frame_data)} bytes")
                    return True
                except sr.WaitTimeoutError:
                    print("   ⚠️ Timeout - không nghe thấy âm thanh")
                    print("   💡 Microphone có thể bị tắt hoặc âm lượng quá thấp")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Lỗi khi test microphone: {e}")
            return False
            
    except ImportError:
        print("❌ SpeechRecognition chưa cài đặt")
        print("💡 Cài đặt: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False


def test_audio_system():
    """Test ALSA/PulseAudio system"""
    print("\n" + "=" * 60)
    print("3️⃣ KIỂM TRA AUDIO SYSTEM")
    print("=" * 60)
    
    import subprocess
    
    # Check arecord (ALSA record tool)
    try:
        result = subprocess.run(
            ["arecord", "-l"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("📋 ALSA recording devices:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️ arecord error: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Không chạy được arecord: {e}")
    
    # Check PulseAudio
    try:
        result = subprocess.run(
            ["pactl", "list", "sources", "short"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("\n📋 PulseAudio sources:")
            print(result.stdout)
        else:
            print(f"⚠️ PulseAudio không chạy hoặc không cài đặt")
    except Exception as e:
        print(f"⚠️ Không chạy được pactl: {e}")


def main():
    print("\n🔍 KIỂM TRA MICROPHONE & AUDIO INPUT")
    print("=" * 60 + "\n")
    
    # Test các component
    pyaudio_ok = test_pyaudio()
    sr_ok = test_speech_recognition()
    test_audio_system()
    
    # Kết luận
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ KIỂM TRA")
    print("=" * 60)
    
    if pyaudio_ok and sr_ok:
        print("✅ Microphone và audio input hoạt động tốt!")
        print("💡 Bạn có thể chạy app_visionmin_standalone.py")
    else:
        print("❌ Có vấn đề với microphone/audio input")
        print("\n🔧 HƯỚNG DẪN FIX:")
        print("1. Kiểm tra microphone đã cắm đúng USB port")
        print("2. Kiểm tra âm lượng: alsamixer")
        print("3. Set microphone làm default:")
        print("   pactl set-default-source <source_name>")
        print("4. Test ghi âm:")
        print("   arecord -d 5 test.wav && aplay test.wav")
        print("5. Nếu vẫn lỗi, restart audio:")
        print("   pulseaudio -k && pulseaudio --start")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
