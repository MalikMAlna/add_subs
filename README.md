# Whisper API Stuff

## Set Up

_Please note: I've only set this up on a Linux terminal with Python 3.8+. So these instructions might not be entirely right if you're using a non Unix-based operating system (AKA Windows. MacOS should be fine)._

### Virtual Environment
```
python -m venv ./venv

source absolute/path/to/activate_file

pip install -r requirements.txt
```
### Environment Variables
```
cp env-template .env
```
Then paste in your `OPENAI_API_KEY` within the double quotes.
