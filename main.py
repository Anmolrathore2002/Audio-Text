# import os
# import shutil
# import subprocess
# import argparse
# import torch
# import whisper
# from pydub import AudioSegment


# def extract_text_audio(file_path, target_language=None, task="transcribe"):
#     """
#     Converts audio to text or translation using OpenAI Whisper.
#     Returns:
#         str: Transcribed or translated text from the audio.
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Audio file not found: {file_path}")

#     if not shutil.which("ffmpeg"):
#         raise EnvironmentError("FFmpeg is not installed or not found in PATH.")

#     print("🔊 Loading Whisper model...")
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = whisper.load_model("small", device=device)

#     print(f"📥 Processing audio file: {file_path}")
#     audio = whisper.load_audio(file_path)
#     audio = whisper.pad_or_trim(audio)

#     print("🌐 Detecting language...")
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)
#     _, probs = model.detect_language(mel)
#     detected_language = max(probs, key=probs.get)
#     print(f"✅ Detected language: {detected_language} ({probs[detected_language] * 100:.2f}%)")

#     # Determine task and language
#     if task == "translate":
#         if detected_language == "en":
#             raise ValueError("❌ Cannot translate from English. Use transcribe instead.")
#         language = detected_language
#     else:
#         task = "transcribe"
#         language = detected_language

#     print(f"📝 Running task: {task} (Language: {language})")
#     result = model.transcribe(file_path, task=task, language=language)

#     transcription = result.get("text", "").strip()
#     print(f"\n📄 Output Text:\n{transcription}\n")
#     return transcription if transcription else None


# def convert_opus_to_mp3(input_path, output_path):
#     """
#     Converts .opus to .mp3 using FFmpeg.
#     """
#     try:
#         ffmpeg_command = [
#             "ffmpeg",
#             "-i", input_path,
#             "-vn",
#             "-acodec", "libmp3lame",
#             "-q:a", "2",
#             output_path
#         ]
#         print("🎧 Converting OPUS to MP3...")
#         subprocess.run(ffmpeg_command, check=True)
#         print(f"✅ Successfully converted: {input_path} ➡️ {output_path}")
#     except Exception as e:
#         raise RuntimeError(f"❌ Error during conversion: {e}")


# def process_opus_audio(input_path, target_language="en", cleanup=True):
#     """
#     Converts OPUS to MP3 and extracts translated text.
#     """
#     mp3_path = "temp_output.mp3"
#     convert_opus_to_mp3(input_path, mp3_path)
#     text = extract_text_audio(mp3_path, target_language=target_language, task="translate")

#     if cleanup and os.path.exists(mp3_path):
#         os.remove(mp3_path)
#         print("🧹 Cleaned up temporary MP3 file.")

#     return text


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Audio Transcription & Translation using Whisper")
#     parser.add_argument("--input", required=True, help="Path to input audio file (mp3/opus/wav)")
#     parser.add_argument("--target_language", default=None, help="Target language code (e.g., en, hi, es)")
#     parser.add_argument("--task", choices=["transcribe", "translate"], default="transcribe", help="Task to perform")
#     args = parser.parse_args()

#     input_file = args.input
#     file_ext = os.path.splitext(input_file)[1].lower()

#     try:
#         if file_ext == ".opus":
#             text = process_opus_audio(input_file, target_language=args.target_language or "en")
#         else:
#             text = extract_text_audio(input_file, target_language=args.target_language, task=args.task)
#     except Exception as e:
#         print(f"❌ Error: {e}")








import os
import shutil
import subprocess
import argparse
import torch
import whisper


def convert_opus_to_mp3(input_path, output_path):
    """
    Converts .opus to .mp3 using FFmpeg.
    """
    try:
        ffmpeg_command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "2",
            output_path
        ]
        print("🎧 Converting OPUS to MP3...")
        subprocess.run(ffmpeg_command, check=True)
        print(f"✅ Converted: {input_path} ➡️ {output_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Error during OPUS conversion: {e}")


def process_audio(file_path):
    """
    Transcribes and translates audio to English using Whisper.
    Returns a dictionary with language, transcription, and translation.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    if not shutil.which("ffmpeg"):
        raise EnvironmentError("FFmpeg is not installed or not found in PATH.")

    print("🚀 Loading Whisper model (small)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small", device=device)

    print(f"📥 Loading audio: {file_path}")
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    print("🌐 Detecting language...")
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    confidence = probs[detected_language] * 100
    print(f"✅ Language detected: {detected_language} ({confidence:.2f}%)")

    print("📝 Transcribing original audio...")
    result_transcribe = model.transcribe(file_path, task="transcribe", language=detected_language)
    native_text = result_transcribe.get("text", "").strip()
    print("\n📜 Native Transcription:\n", native_text)

    translated_text = native_text
    if detected_language != "en":
        print("\n🌍 Translating to English...")
        result_translate = model.transcribe(file_path, task="translate", language=detected_language)
        translated_text = result_translate.get("text", "").strip()
        print("\n🌐 English Translation:\n", translated_text)
    else:
        print("\n🌐 Translation skipped (already in English)")

    return {
        "language": detected_language,
        "native_text": native_text,
        "translated_text": translated_text
    }


def handle_input(input_file):
    ext = os.path.splitext(input_file)[1].lower()

    if ext == ".opus":
        temp_mp3 = "temp_output.mp3"
        convert_opus_to_mp3(input_file, temp_mp3)
        result = process_audio(temp_mp3)
        os.remove(temp_mp3)
        print("🧹 Cleaned up temporary MP3 file.")
    else:
        result = process_audio(input_file)

    return result
    
file_path = r"C:\Users\Chirag\Desktop\language converter\audio\pashto.mp3"

try:
    output = handle_input(file_path)

    print("\n✅ Final Output Summary:")
    print(f"Detected Language: {output['language']}")
    print("\nOriginal Transcription:\n", output['native_text'])
    print("\nEnglish Translation:\n", output['translated_text'])

    # with open("final_translation.txt", "w", encoding="utf-8") as f:
    #     f.write(output['translated_text'])
    # print("\n💾 Translation saved to final_translation.txt")

except Exception as e:
    print(f"❌ Error: {e}")
