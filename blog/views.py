from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import yt_dlp
from .models import BlogPost
from .forms import BlogPostForm
import os
import assemblyai as aai

def download_youtube_audio(url, output_path):
    """Download YouTube audio using yt-dlp"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"YouTube download error: {str(e)}")
        return False

# Create your views here.
def index(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            
            try:
                # Check AssemblyAI API key
                api_key = os.getenv('ASSEMBLYAI_API_KEY')
                print(f"API Key loaded: {'*' * (len(api_key)-4) + api_key[-4:] if api_key else 'None'}")
                
                if not api_key:
                    messages.error(request, 'AssemblyAI API key is not set. Please check your .env file.')
                    return redirect('blog:create_post')

                # Clean the API key
                api_key = api_key.strip().strip('"').strip("'")
                
                # Initialize AssemblyAI
                aai.settings.api_key = api_key
                
                # Create temp directory if it doesn't exist
                temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                
                try:
                    print(f"Attempting to download YouTube video: {youtube_url}")
                    
                    # Fix common YouTube URL issues
                    if 'youtu.be' in youtube_url:
                        video_id = youtube_url.split('/')[-1]
                        youtube_url = f'https://www.youtube.com/watch?v={video_id}'
                    elif 'youtube.com' in youtube_url and 'watch?v=' not in youtube_url:
                        video_id = youtube_url.split('/')[-1]
                        youtube_url = f'https://www.youtube.com/watch?v={video_id}'
                    
                    print(f"Normalized YouTube URL: {youtube_url}")
                    
                    # Generate a unique filename
                    import uuid
                    temp_filename = f"audio_{uuid.uuid4().hex[:8]}"
                    audio_file_path = os.path.join(temp_dir, temp_filename)
                    
                    # Download audio
                    print(f"Downloading audio to: {audio_file_path}")
                    if not download_youtube_audio(youtube_url, audio_file_path):
                        raise Exception("Failed to download audio from YouTube")
                    
                    # The actual file will have .mp3 extension added by yt-dlp
                    audio_file_path = audio_file_path + '.mp3'
                    
                    if not os.path.exists(audio_file_path):
                        raise Exception("Audio file not found after download")
                    
                    file_size = os.path.getsize(audio_file_path)
                    print(f"Download successful: {file_size} bytes")
                    
                    if file_size == 0:
                        raise Exception("Downloaded file is empty")
                    
                    # Create transcriber and check connection
                    print("Testing AssemblyAI connection...")
                    transcriber = aai.Transcriber()
                    
                    # Start transcription
                    print("Starting transcription...")
                    transcript = transcriber.transcribe(audio_file_path)
                    
                    if not transcript or not transcript.text:
                        messages.error(request, 'Failed to transcribe the video.')
                        return redirect('blog:create_post')
                    
                    print("Transcription successful")
                    
                    # Create blog post
                    post = form.save(commit=False)
                    post.author = request.user
                    post.transcription = transcript.text
                    post.save()
                    
                    # Clean up temp file
                    try:
                        if os.path.exists(audio_file_path):
                            os.remove(audio_file_path)
                            print(f"Cleaned up temp file: {audio_file_path}")
                    except Exception as cleanup_error:
                        print(f"Error cleaning up temp file: {cleanup_error}")
                    
                    messages.success(request, 'Blog post created successfully!')
                    return redirect('blog:post_detail', pk=post.pk)
                    
                except Exception as inner_error:
                    print(f"Error during processing: {str(inner_error)}")
                    messages.error(request, f'Error processing video: {str(inner_error)}')
                    return redirect('blog:create_post')
                    
            except Exception as outer_error:
                print(f"Outer error: {str(outer_error)}")
                messages.error(request, f'System error: {str(outer_error)}')
                return redirect('blog:create_post')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})