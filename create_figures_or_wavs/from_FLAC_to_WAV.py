import soundfile as sf
from pathlib import Path

def convert_all_flac_to_wav(root_path: str):
    """
    Recursively converts all .flac files under root_path to .wav
    """
    root = Path(root_path)

    if not root.exists():
        raise ValueError(f"Path does not exist: {root_path}")

    # Walk all files recursively
    for flac_file in root.rglob("*.flac"):
        wav_file = flac_file.with_suffix(".wav")
        try:
            data, sr = sf.read(flac_file)
            sf.write(wav_file, data, sr, format="WAV")
            print(f"Converted: {flac_file} → {wav_file}")
        except Exception as e:
            print(f"Failed to convert {flac_file}: {e}")

# Example usage
convert_all_flac_to_wav(r"D:\USERS\wout.decrop\environments\UC5\AIS_annotator\create_figures_or_wavs")
