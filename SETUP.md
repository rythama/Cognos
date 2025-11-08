# Setup Guide - Avoiding Dependency Conflicts

## Understanding the Warnings

The dependency warnings you're seeing are from existing packages in your environment (spyder, tensorflow), not from the Cognos application. These warnings won't prevent the Flask app from running, but they indicate potential conflicts.

## Recommended Solution: Use a Virtual Environment

Using a virtual environment isolates the Cognos dependencies from your other projects, preventing conflicts.

### Option 1: Using venv (Built-in Python)

```bash
# Create a virtual environment
python3 -m venv cognos_env

# Activate it (macOS/Linux)
source cognos_env/bin/activate

# Activate it (Windows)
cognos_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# When done, deactivate
deactivate
```

### Option 2: Using conda (If you use Anaconda/Miniconda)

```bash
# Create a new conda environment
conda create -n cognos python=3.9

# Activate it
conda activate cognos

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# When done, deactivate
conda deactivate
```

## Alternative: Install Without Conflicts

If you prefer not to use a virtual environment, you can install with `--no-deps` and then install only what's needed:

```bash
# Install Flask and Flask-CORS directly
pip install flask>=3.0.0 flask-cors>=4.0.0

# Install OpenAI (if using LLM mode)
pip install openai>=1.0.0

# Install python-dotenv (optional)
pip install python-dotenv>=1.0.0
```

## Minimal Requirements (If You Have Conflicts)

If you want to run the app with minimal dependencies and avoid conflicts:

```bash
# Core Flask dependencies
pip install flask flask-cors

# Optional: OpenAI for LLM mode
pip install openai

# Optional: Environment variables
pip install python-dotenv
```

The app will work in rule-based mode without OpenAI if you don't set the `OPENAI_API_KEY`.

## Verifying Installation

After installation, verify everything works:

```bash
# Check Flask installation
python -c "import flask; print(flask.__version__)"

# Check if app can start (will show error if dependencies missing)
python app.py
```

## Troubleshooting

### If Flask doesn't work:
```bash
pip install --upgrade flask flask-cors
```

### If you get import errors:
Make sure you're in the correct directory and have activated your virtual environment (if using one).

### If you want to ignore the warnings:
The warnings are informational. The app should still run. However, using a virtual environment is strongly recommended for clean dependency management.

