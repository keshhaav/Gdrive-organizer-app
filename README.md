# Google Drive File Categorizer and Organizer 📁✨

An intelligent Google Drive organization tool that automatically categorizes and sorts your messy files using AI-powered categorization. Built with Streamlit and powered by the Mixtral-8x7B model through Groq.

## Features 🚀

- **Smart Categorization**: Automatically generates meaningful categories based on file names using AI
- **Google Drive Integration**: Seamlessly connects with your Google Drive account
- **Bulk Organization**: Processes multiple files simultaneously
- **Real-time Progress Tracking**: Shows progress bars and status updates during organization
- **Secure Authentication**: Uses OAuth2 for secure Google Drive access
- **Stop Functionality**: Allows users to safely stop the organization process at any time
- **Clean Interface**: Built with Streamlit for a user-friendly experience

## Technical Stack 💻

- **Frontend**: Streamlit
- **Authentication**: Google OAuth2
- **AI Model**: Mixtral-8x7B (via Groq)
- **APIs**: Google Drive API
- **String Matching**: FuzzyWuzzy for intelligent file categorization
- **Cloud Integration**: Google Cloud Platform

## Prerequisites 📋

- Python 3.12 or higher
- Google Cloud Platform account with Drive API enabled
- Groq API key
- Required Python packages (see `requirements.txt`)

## Installation 🔧

1. Clone the repository:
```bash
git clone <repository-url>
cd google-drive-organizer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```
GROQ_API_KEY=your_groq_api_key
```

4. Configure Google OAuth credentials in your Streamlit secrets:
```toml
[google_oauth]
client_id = "your_client_id"
client_secret = "your_client_secret"
```

## Usage 🎯

1. Run the Streamlit app:
```bash
streamlit run drive_sorter_app.py
```

2. Click the "Click to Authorize" button in the sidebar to connect your Google Drive
3. Wait for the app to fetch your files
4. Review the automatically generated categories
5. Click "Create folders and organize files" to start the organization process

## Project Structure 📂

```
├── drive_sorter_app.py   # Main application file
├── authenticate.py       # Google OAuth authentication
├── categorization.py    # AI-powered file categorization
├── drive_ops.py        # Google Drive operations
└── requirements.txt    # Project dependencies
```

## Features in Detail 🔍

### Authentication
- Secure OAuth2 flow for Google Drive access
- Session state management
- Automatic token refresh

### File Categorization
- AI-powered category generation using Mixtral-8x7B
- Fuzzy string matching for accurate file assignment
- Support for up to 15 unique categories

### Drive Operations
- Batch file moving
- Folder creation
- Error handling and recovery
- Progress tracking

## Error Handling 🛠️

The application includes comprehensive error handling for:
- Authentication failures
- API rate limits
- Network issues
- File permission errors
- Invalid file operations

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.


## Support 💬

For support, contact me on discord (keshav._._.) or my linkedin.
