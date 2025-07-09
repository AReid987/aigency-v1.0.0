# Setting Up Nari Labs Dia for BrainCraft

This guide explains how to set up Nari Labs Dia, a high-quality text-to-speech (TTS) model that generates ultra-realistic dialogue in one pass.

## What is Nari Labs Dia?

Dia is a 1.6B parameter text-to-speech model created by Nari Labs that directly generates highly realistic dialogue from a transcript. Key features include:

- Ultra-realistic voice synthesis
- Multiple speaker voices with `[S1]` and `[S2]` tags
- Support for nonverbal communications like laughter, coughing, etc.
- Voice cloning capabilities (with audio prompting)

## Requirements

- Python 3.10 or higher
- CUDA-compatible GPU with at least 10GB VRAM (highly recommended)
- 2GB+ of disk space for model storage

## Installation Options

### Option 1: Using Docker (Recommended)

The BrainCraft Docker setup includes a Dia container that will automatically be configured when you run the application with docker-compose.

```bash
# Simply run BrainCraft with Docker Compose
docker compose -f docker/docker-compose.yml up
```

### Option 2: Local Installation

If you prefer to install Dia locally without Docker:

```bash
# Create a virtual environment (optional but recommended)
python -m venv dia_env
source dia_env/bin/activate  # On Windows: dia_env\Scripts\activate

# Install Dia from GitHub
pip install git+https://github.com/nari-labs/dia.git

# Install additional dependencies for BrainCraft integration
pip install fastapi uvicorn aiohttp
```

## Configuration

### Update BrainCraft Environment Variables

Edit your `.env` file to include these Dia settings:

```
# Text to Speech (Nari Labs Dia)
DIA_ENABLE_LOCAL_TTS=true
DIA_SEED=42  # Optional - for consistent voices (remove for random voices)
DIA_COMPUTE_DTYPE=float16  # Options: float16, bfloat16, float32
DIA_USE_COMPILE=true  # Enable PyTorch compilation for faster inference
```

### Dia Settings Explained

- `DIA_ENABLE_LOCAL_TTS`: Set to `true` to use Dia for speech synthesis
- `DIA_SEED`: (Optional) Set a numeric seed for voice consistency. Same seed = same voice characteristics
- `DIA_COMPUTE_DTYPE`: Computation precision
  - `float16`: Good balance of speed and quality (~10GB VRAM)
  - `bfloat16`: Alternative format, better for some GPUs (~10GB VRAM)
  - `float32`: Highest quality but slower and more memory-intensive (~13GB VRAM)
- `DIA_USE_COMPILE`: Enable PyTorch compilation for faster inference (recommended)

## Using Dia Directly (Optional)

If you want to experiment with Dia directly:

```python
from dia.model import Dia

# Initialize model
model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

# Generate speech with speaker tags
text = "[S1] Hello, this is speaker one. [S2] And this is speaker two."
output = model.generate(text, use_torch_compile=True)

# Save to file
model.save_audio("output.wav", output)
```

## Voice Customization 

### Using Speaker Tags

Dia uses speaker tags to differentiate voices:

```
[S1] Hello, I'm the first speaker!
[S2] And I'm the second speaker with a different voice.
[S1] Back to the first speaker again.
```

### Using Non-Verbal Cues

Dia supports non-verbal expressions:

```
[S1] This is really funny (laughs)
[S2] I agree (clears throat) it's hilarious!
```

Supported non-verbal tags:
- `(laughs)`
- `(clears throat)`
- `(sighs)`
- `(gasps)`
- `(coughs)`
- `(singing)` or `(sings)`
- `(mumbles)`
- `(groans)`
- `(sniffs)`
- `(claps)`
- `(screams)`
- `(inhales)` or `(exhales)`
- `(burps)`
- `(humming)`
- `(sneezes)`
- `(chuckle)`
- `(whistles)`

## Performance Considerations

Dia's performance varies depending on hardware:

| Hardware | Performance (with PyTorch compile) |
|----------|-----------------------------------|
| RTX 4090 | ~2.2x realtime (float16) |
| RTX 3090 | ~1.8x realtime (float16) |
| RTX 3080 | ~1.5x realtime (float16) |
| CPU only | Significantly slower (not recommended) |

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory Error**
   - Try reducing the precision (`DIA_COMPUTE_DTYPE=float16`)
   - Close other GPU-intensive applications
   - Try shorter text inputs (very long inputs require more memory)

2. **Audio Quality Issues**
   - Try different seeds to get different voices
   - Make sure to use speaker tags appropriately
   - Very short inputs (under 5s of speech) may sound unnatural

3. **Model Loading Errors**
   - Ensure you have internet connection for the first run (to download the model)
   - Check you have at least 2GB free disk space
   - Verify your Python version is 3.10+

4. **Slow Generation**
   - Enable PyTorch compilation (`DIA_USE_COMPILE=true`)
   - Use lower precision if possible
   - GPU acceleration is strongly recommended

## Ethical Considerations

Dia can generate highly realistic speech. Please use responsibly:
- Do not create content that impersonates real individuals without permission
- Do not use for generating misleading or deceptive content
- Be aware of the legal implications in your jurisdiction

## Additional Resources

- [Nari Labs Dia GitHub Repository](https://github.com/nari-labs/dia)
- [Dia Documentation](https://github.com/nari-labs/dia/blob/main/README.md)
- [Dia Voice Cloning Examples](https://github.com/nari-labs/dia/blob/main/example/voice_clone.py)