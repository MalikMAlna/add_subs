# Add Subs

Simple script that translates and/or transcribes video audio to English and adds subtitles to said video using the Whisper API and MoviePy.

## Set Up

_Please note: I've only set this up on a Linux terminal with Python 3.8+. So these instructions might not be entirely right if you're using a non-Unix-based operating system (AKA Windows. MacOS should be fine)._

### MacOS

Install [imagemagick](https://imagemagick.org/script/download.php) for MacOS. You can do this with Homebrew:

```
brew install imagemagick
```

### Virtual Environment

```
python -m venv ./venv

source absolute/path/to/activate_file

pip install -r requirements.txt --use-pep517
```

### Environment Variables

```
cp env-template .env
```

Then paste in your `OPENAI_API_KEY` within the double quotes.

### Run the Script

```
python main.py --video <PATH TO TARGET MP4> --type <translate or transcribe> 
```

### Known Issues
The transcribe option doesn't seem to work for certain languages and transcriptions for languages that aren't English aren't as accurate. These are mostly issues with the Whisper API and Moviepy that are outside of our hands.