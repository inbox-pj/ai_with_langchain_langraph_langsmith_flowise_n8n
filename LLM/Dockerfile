FROM ollama/ollama:latest

RUN ollama serve & \
    sleep 10 && \
    ollama pull gemma3:1b && \
    ollama pull nomic-embed-text:latest && \
    echo 'Models ready: gemma3:1b, nomic-embed-text'