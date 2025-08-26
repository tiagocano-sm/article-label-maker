#!/bin/bash

# Update package list and install curl
apt-get update
apt-get install -y curl

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -f http://localhost:11434/api/tags > /dev/null 2>&1; do
    echo "Waiting for Ollama API..."
    sleep 2
done

echo "Ollama is ready, checking if model exists..."
# Check if model already exists
if ollama list | grep -q "llama3.1:8b"; then
    echo "Model llama3.1:8b already exists, skipping download"
else
    echo "Pulling model llama3.1:8b..."
    ollama pull llama3.1:8b
    echo "Model pulled successfully"
fi

echo "Ollama service is ready and model is available"
# Keep the container running
wait
