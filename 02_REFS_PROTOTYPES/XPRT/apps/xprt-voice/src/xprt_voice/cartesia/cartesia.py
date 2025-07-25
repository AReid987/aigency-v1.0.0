import argparse

import mlx.core as mx

import cartesia_mlx as cmx

parser = argparse.ArgumentParser(
    description="Test script for run Cartesia MLX Model"
)

parser.add_argument("--model", default="cartesia-ai/Llamba-1B-4bit-mlx", help="The model name.")
parser.add_argument("--prompt", default="Rene Descartes was")
parser.add_argument(
    "--max-tokens", type=int, default=500, 
    help="The maximum number of tokens to generate."
)
parser.add_argument(
    "--top-p",
    type=float,
    default=0.99,
    help="Top-p sampling (a value of 1 is equal to standard sampling).",    
)
parser.add_argument(
    "--temperature",
    type=float,
    default=0.85,
    help="Temperature scaling parameter",
)
args = parser.parse_args()

model = cmx.from_pretrained(args.model)
model.set_dtype(mx.float32)

prompt = args.prompt

print(prompt, end="", flush=True)
for text in model.generate(
    prompt,
    max_tokens=args.max_tokens,
    eval_every_n=1,
    verbose=True,
    top_p=args.top_p,
    temperature=args.temperature
):
    print(text, end="", flush=True) 