from flask import Flask, render_template, request, jsonify
import requests
import json
import re

app = Flask(__name__)

# Enhanced language mappings
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'pl': 'Polish',
    'nl': 'Dutch',
    'te': 'Telugu',
    'ta': 'Tamil',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'ur': 'Urdu',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'tl': 'Filipino',
    'sw': 'Swahili',
    'fa': 'Persian',
    'he': 'Hebrew',
    'uk': 'Ukrainian'
}

def clean_translation_result(text):
    """Clean up translation artifacts and errors"""
    if not text:
        return text
    
    # Remove common translation service warnings
    text = re.sub(r'MYMEMORY WARNING:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Translation by.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[.*?\]', '', text)  # Remove bracketed text
    
    # Clean up extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def translate_with_google_translate_free(text, source_lang, target_lang):
    """Use a free Google Translate alternative endpoint"""
    try:
        # Using a public Google Translate endpoint that doesn't require API key
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0 and len(result[0]) > 0:
                translated_text = ''.join([item[0] for item in result[0] if item[0]])
                return clean_translation_result(translated_text)
    except Exception as e:
        print(f"Google Translate free API error: {e}")
    return None

def translate_with_mymemory_improved(text, source_lang, target_lang):
    """Improved MyMemory translation with better parameters"""
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text.strip(),
            "langpair": f"{source_lang}|{target_lang}",
            "de": "translator@example.com",  # Better identification
            "mt": "1"  # Enable machine translation
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Translation Tool)'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=12)
        if response.status_code == 200:
            result = response.json()
            if (result.get("responseData") and 
                result["responseData"].get("translatedText") and
                not result["responseData"]["translatedText"].startswith("MYMEMORY WARNING")):
                
                translated = result["responseData"]["translatedText"]
                return clean_translation_result(translated)
    except Exception as e:
        print(f"MyMemory improved API error: {e}")
    return None

def translate_with_libretranslate_improved(text, source_lang, target_lang):
    """Improved LibreTranslate with better endpoints"""
    endpoints = [
        "https://libretranslate.com/translate",
        "https://translate.argosopentech.com/translate",
        "https://translate.astian.org/translate"
    ]
    
    for endpoint in endpoints:
        try:
            payload = {
                "q": text.strip(),
                "source": source_lang,
                "target": target_lang,
                "format": "text",
                "alternatives": 1
            }
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Translation Tool'
            }
            
            response = requests.post(endpoint, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if result.get("translatedText"):
                    return clean_translation_result(result["translatedText"])
                    
        except Exception as e:
            print(f"LibreTranslate improved error ({endpoint}): {e}")
            continue
    return None

def get_best_translation(text, source_lang, target_lang):
    """Try multiple APIs and return the best result"""
    translations = []
    
    # Try Google Translate free first (usually most accurate)
    google_result = translate_with_google_translate_free(text, source_lang, target_lang)
    if google_result and len(google_result) > 0:
        translations.append(("Google", google_result))
    
    # Try improved MyMemory
    mymemory_result = translate_with_mymemory_improved(text, source_lang, target_lang)
    if mymemory_result and len(mymemory_result) > 0:
        translations.append(("MyMemory", mymemory_result))
    
    # Try improved LibreTranslate
    libretranslate_result = translate_with_libretranslate_improved(text, source_lang, target_lang)
    if libretranslate_result and len(libretranslate_result) > 0:
        translations.append(("LibreTranslate", libretranslate_result))
    
    if translations:
        # Prefer Google Translate result if available
        for service, translation in translations:
            if service == "Google":
                print(f"Using Google Translate: {translation}")
                return translation
        
        # Otherwise return the first successful translation
        service, translation = translations[0]
        print(f"Using {service}: {translation}")
        return translation
    
    return None

def translate_text(text, source_lang, target_lang):
    """Main translation function with improved logic"""
    if not text or not text.strip():
        return "Please enter text to translate"
    
    if source_lang == target_lang:
        return text
    
    # Clean and validate input
    cleaned_text = text.strip()
    if len(cleaned_text) > 5000:
        return "Text is too long. Please limit to 5000 characters."
    
    print(f"Translating: '{cleaned_text}' from {source_lang} to {target_lang}")
    
    # Get the best available translation
    result = get_best_translation(cleaned_text, source_lang, target_lang)
    
    if result and len(result.strip()) > 0:
        return result
    
    return "Translation failed. Please check your internet connection and try again."

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ''
    original_text = ''
    source_lang = 'en'
    target_lang = 'te'  # Default to Telugu as shown in your screenshot
    
    if request.method == 'POST':
        original_text = request.form.get('text', '').strip()
        source_lang = request.form.get('source', 'en')
        target_lang = request.form.get('target', 'te')
        
        if original_text:
            translated_text = translate_text(original_text, source_lang, target_lang)
    
    return render_template('index.html',
                         languages=LANGUAGES,
                         translated_text=translated_text,
                         source_lang=source_lang,
                         target_lang=target_lang,
                         text=original_text)

if __name__ == '__main__':
    app.run(debug=True)
