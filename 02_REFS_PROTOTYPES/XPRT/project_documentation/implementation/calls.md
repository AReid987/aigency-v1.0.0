# Calls & Voice

<img class="md" src="../images/calls.png" alt="switchboard operator" /> 

## Linux Calls

<div class="bg">

### Hypothesis

#### What?

- Docker containers can be used as a virtual environment for enabling Agents to make phone calls

#### How?

- Docker running Linux
- Installing Calls onto Linux
  - Calls typically requires a GUI environment
  - Running a GUI in Linux requires X11 forwarding or VNC server
- Calls uses Sofia SIP

</div>

---

### Calls

<div class="bg">

- <a href="https://gitlab.gnome.org/GNOME/calls">Calls</a>

- A Phone Dialer and Call Handler
- A Phone and VoIP (SIP) Handler

</div>

---

### SIP

<div class="bg">

- <a href="https://github.com/BelledonneCommunications/sofia-sip">
    Sofia SIP
</a>

- Open Source SIP user-agent Library
- Building block for SIP Client Software
- VoIP, IM, Real-Time, Person to Person Services

</div>

---

### Voice

<div class="bg">

- A combination of voice models are implemented for the experiment

#### Cartesia

- Repository
  - <a href="https://github.com/cartesia-ai/edge">
    Cartesia Edge
</a>

**Use Case**

Fast, Free, On Device Real Time Speech

**Overview**

- Open Source Library supporting the research of efficient state space models (SSMs)
- More efficient, high quality over Transformers models
- On device real-time, streaming
- Llamba 1B, 3B, & 8B in Pytorch & MLX
- Rene-v0.1 in Pytorch & MLX
- <a href="https://github.com/cartesia-ai/edge/blob/main/cartesia-pytorch">Cartesia Pytorch</a>
- <a href="https://github.com/cartesia-ai/edge/blob/main/cartesia-metal">Cartesia Metal</a>
- <a href="https://github.com/cartesia-ai/edge/blob/main/cartesia-mlx">Cartesia MLX</a>

#### F5-TTS & E2 TTS

**Use Case**

- Excellent Voice Cloning
- Fast, Performant, realistic Speech

<a href="https://arxiv.org/abs/2410.06885">Arxiv Paper</a>

- Fairytaler that Fakes Fluent & Faithful Speech with Flowmatching
- Diffusion Transformer with ConvNeXt V2
- Faster Training and Inference
- Flat-UNet Transformer
- Sway Sampler -> Infrence Time flow step sampling -> Performance Optimization
- Voice Chat, Multi Style, Multi Speaker
- Training and Finetuning: 
  - <a href="https://github.com/SWivid/F5-TTS/blob/main/src/f5_tts/train">Training & Finetuning Guidance</a>

---

#### CSM

- Conversational Speech Model 

**Use Case**

- Best yet, most realistic speech

**Overview**

- Generates RVQ Audio codes from text and audio inputs
- Provide model with context for best performance
- Pair with LLM for generating Text

#### Kokoro TTS

#### Kokoro.js

</div>
