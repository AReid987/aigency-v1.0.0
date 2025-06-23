
from pytube import YouTube

def test_youtube_extraction(url):
    try:
        yt = YouTube(url)
        print(f"Title: {yt.title}")
        print("Author:", yt.author)
        print("Duration:", yt.length, "seconds")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Test with a known working video
if test_youtube_extraction('https://www.youtube.com/watch?v=jNQXAC9IVRw'):
    print("\nYouTube extraction test successful!")
else:
    print("\nYouTube extraction test failed.")
