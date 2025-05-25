# Google Drive AI File Organizer 🗂️

> **Transform your chaotic Google Drive into a well-organized workspace!** The AI-powered file organizer that categorizes files based on their names and content context, not just file formats.

[![Test it out here](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B.svg)](https://gdrive-organizer.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Drive API](https://img.shields.io/badge/Google%20Drive-API-green.svg)](https://developers.google.com/drive/api)
[![Uses Groq Cloud's Llama 4 Scout LLM](https://img.shields.io/badge/LLM-Groq-purple.svg)](https://console.groq.com/playground)

## 🚀 Features

- **Smart AI Categorization**: Uses Groq's Llama 4 Scout model to analyze file names and create meaningful categories
- **One-Click Organization**: Automatically creates folders and moves files based on AI-generated categories
- **Google Drive Integration**: Seamlessly connects to your Google Drive with secure OAuth2 authentication
- **Streamlit UI**: Clean, responsive interface that runs in your browser
- **Uncategorized File Detection**: Find and organize files sitting in your root directory

## 📋 How It Works

1. **Authenticate** with your Google Drive account
2. **Scan** for files that need organization
3. **Generate** intelligent categories based on file names using AI
4. **Review** the proposed organization structure
5. **Execute** the organization with one click

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/google-drive-ai-organizer.git
cd google-drive-ai-organizer

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Set up a Google Cloud project and enable the Drive API
2. Create OAuth 2.0 credentials
3. Create a `.streamlit/secrets.toml` file with the following:

```toml
[google_oauth]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
project_id = "YOUR_PROJECT_ID"

redirect_uri = "http://localhost:8501"
GROQ_API_KEY = "your-groq-api-key"
```

## 🚀 Usage

```bash
streamlit run drive_sorter_app.py
```

This would automatically open http://localhost:8501 in your browser.

## 🧩 Project Structure

- `drive_sorter_app.py` - Main application entry point
- `authenticate.py` - Handles Google OAuth2 authentication
- `drive_ops.py` - Google Drive API operations
- `categorization.py` - AI-powered file categorization logic

## 🧠 AI Categorization Logic

The app uses Groq's Llama 4 Scout 17b-16e model to analyze file names and group them into logical categories. It looks beyond simple file extensions to understand the context and purpose of your files.

For example, it might create categories like:
- "Project Alpha Documentation"
- "Financial Reports 2024"
- "Marketing Assets"
- "Client Presentations"

## 🔒 Privacy & Security

- Your Google Drive data is accessed only within your local session
- No file content is transmitted to external servers, only file names
- OAuth2 tokens are stored in your local session only

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
