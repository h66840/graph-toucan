# Configuration Guide

## Overview

This directory contains configuration files for the graph-Toucan project. The main configuration file is `config.yaml`.

## Configuration File: config.yaml

### Structure

```yaml
api:
  api_key_env: "DASHSCOPE_API_KEY"  # Environment variable name for API key
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"  # API endpoint

model:
  default: "qwen3-235b-a22b-instruct-2507"  # Default model for most operations
  simulate_api: "qwen3-235b-a22b-instruct-2507"  # Model for simulating external API calls
```

### Usage

1. **API Key**: Set your API key as an environment variable:
   ```bash
   export DASHSCOPE_API_KEY="your-api-key-here"
   ```

2. **Custom API Endpoint**: To use a different API endpoint (e.g., local deployment):
   - Comment out the default configuration
   - Uncomment and modify the alternative configuration:
   ```yaml
   api:
     api_key: "EMPTY"
     base_url: "http://your-endpoint:8000/v1"
   ```

3. **Model Selection**: Change the model names to use different models:
   ```yaml
   model:
     default: "your-preferred-model"
     simulate_api: "your-preferred-model"
   ```

### Files Using This Config

- `backward_to_query.py`: Backward query generation
- `positive_distill.py`: Forward distillation and validation

### Dependencies

Make sure to install required dependencies:
```bash
pip install -r requirements.txt
```
