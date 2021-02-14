from googletrans import Translator

TARGET_LANGUAGE_OPTIONS = ['None', 'English', 'Spanish', 'French', 'Hindi']


# Translate text to selected destination language
def translate(text, dest):
    translator = Translator()
    return translator.translate(text, dest=dest).text


# Format language string to be used by google translator
def format_language(lang):
    if lang == TARGET_LANGUAGE_OPTIONS[1]:
        return 'en'
    elif lang == TARGET_LANGUAGE_OPTIONS[2]:
        return 'es'
    elif lang == TARGET_LANGUAGE_OPTIONS[3]:
        return 'fr'
    elif lang == TARGET_LANGUAGE_OPTIONS[4]:
        return 'hi'
