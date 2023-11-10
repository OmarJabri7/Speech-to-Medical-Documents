# Speech Recognition for Document Interaction

## Overview
The `speech_rec.py` script is an advanced utility for real-time speech recognition, designed to interact with documents by taking notes through voice commands and integrating them into a form. This script uses Google Cloud Speech-to-Text for voice recognition, Tesseract OCR for reading text from images, and custom utility functions for PDF manipulation.

## Features
- Real-time speech recognition with Google Cloud Speech-to-Text.
- Document analysis using Tesseract OCR.
- Note-taking by voice command, integrated directly into document forms.
- Automatic PDF generation from collected notes.
- Environment variable setup for Google Cloud authentication.

## Prerequisites
- Google Cloud account with Speech-to-Text API access.
- Tesseract OCR installed on your system.
- Python with packages: `pytesseract`, `pyaudio`, `google-cloud-speech`, and `nltk`.

## Setup
1. Install the required Python packages:
```bash
pip install pytesseract pyaudio google-cloud-speech nltk
```
2. Set up Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials.json
```
3. Install Tesseract OCR and ensure it's in your system's PATH, or set it in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
## Usage
Run the script from your command line:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
Speak into the microphone to take notes. Say "banana" to integrate notes into the document, and "exit" or "quit" to finish the session and save the output.
## Configuration
Modify the passphrase variable to a keyword that triggers note integration. Update the RATE and CHUNK parameters to match your audio recording preferences.

## Output
The script saves recognized speech as notes, which are then written into a form image and saved as a PDF. Additionally, the raw notes are saved in a text file.

## Note
This script is a prototype and is intended for use in controlled environments. Real-world application may require additional error handling and optimizations.
