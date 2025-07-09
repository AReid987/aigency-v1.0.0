docker run -it \
--user $(id -u):$(id -g) \
--volume $(pwd):/app \
--env-file .env \
paulgauthier/aider-full

# =================================================

## Gemini
# - gemini-2.0-flash
# - gemini-2.0-flash-001
# - gemini-2.0-flash-exp
# - gemini-2.0-flash-lite
# - gemini-2.0-flash-lite-001
# - gemini-2.0-flash-thinking-exp
# - gemini-2.0-flash-thinking-exp-01-21
# - gemini-2.0-pro-exp-02-05
# - gemini-2.5-pro-preview-03-25
# - gemini-flash-experimental
# =================================================

## Groq
# - groq/deepseek-r1-distill-llama-70b
# - groq/gemma-7b-it
# - groq/gemma2-9b-it
# - groq/llama-3.1-405b-reasoning
# - groq/llama-3.1-70b-versatile
# - groq/llama-3.1-8b-instant
# - groq/llama-3.2-11b-text-preview
# - groq/llama-3.2-11b-vision-preview
# - groq/llama-3.2-1b-preview
# - groq/llama-3.2-3b-preview
# - groq/llama-3.2-90b-text-preview
# - groq/llama-3.2-90b-vision-preview
# - groq/llama-3.3-70b-specdec
# - groq/llama2-70b-4096
# - groq/llama3-70b-8192
# - groq/llama3-8b-8192
# - groq/llama3-groq-70b-8192-tool-use-preview
# - groq/llama3-groq-8b-8192-tool-use-preview
# - groq/mixtral-8x7b-32768
# =================================================

## Cerebras
# - cerebras/llama3.1-70b
# - cerebras/llama3.1-8b
# - cerebras/llama3.3-70b
# =================================================

## OpenRouter Free
# - openrouter/deepseek/deepseek-chat-v3-0324:free
# - openrouter/deepseek/deepseek-chat:free
# - openrouter/deepseek/deepseek-r1:free
# - openrouter/google/gemini-2.0-flash-exp:free
# - openrouter/google/gemini-2.5-pro-exp-03-25:free
# - openrouter/meta-llama/llama-3-8b-instruct:free
# - openrouter/mistralai/mistral-7b-instruct:free