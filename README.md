# AI Blog Generator

A Django-based web application that automatically generates blog posts from YouTube videos using AI transcription.

## Features

- **YouTube Video Processing**: Automatically downloads and extracts audio from YouTube videos
- **AI Transcription**: Uses AssemblyAI to convert speech to text with high accuracy
- **User Authentication**: Secure user registration and login system using django-allauth
- **Blog Management**: Create, view, edit, and manage blog posts
- **Modern UI**: Clean and responsive interface built with Django Tailwind

## Prerequisites

- Python 3.8+
- FFmpeg (automatically installed during setup)
- AssemblyAI API Key

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd ai-blog-django
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your AssemblyAI API key:
```
ASSEMBLYAI_API_KEY=your_api_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Usage

1. Register for an account or log in if you already have one
2. Click "Create New Post" to start a new blog post
3. Enter a YouTube URL and post title
4. The system will automatically:
   - Download the video's audio
   - Transcribe it using AssemblyAI
   - Create a blog post with the transcription
5. View and manage your posts from the dashboard

## Technical Details

- **Framework**: Django 5.1.3
- **Authentication**: django-allauth 65.2.0
- **Video Processing**: yt-dlp 2024.11.18
- **Transcription**: AssemblyAI API
- **Frontend**: Django Tailwind
- **Database**: SQLite (default)

## Important Notes

- Make sure the YouTube videos you process are:
  - Publicly accessible
  - Not age-restricted
  - Have clear audio for better transcription results

## Dependencies

Key dependencies include:
- Django
- django-allauth
- assemblyai
- yt-dlp
- python-dotenv
- django-tailwind

For a complete list of dependencies, see `requirements.txt`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Acknowledgments

- AssemblyAI for providing the transcription API
- Django community for the excellent web framework
- yt-dlp maintainers for the reliable YouTube download functionality