try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from langdetect import detect_langs

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# SOURCE_LANGUAGE_OPTIONS = ['English', 'Spanish', 'French', 'Hindi']
ACCEPTED_LANGUAGES = ['en', 'es', 'fr', 'hi']


def allowed_file(filename):
    """
    Checks if file extension is allowed
    :param filename: name of file with extension
    :return: If extension is allowed or not
    """

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def auto_detect_text(filename):
    import platform
    if platform.system() != 'Darwin':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text_eng = pytesseract.image_to_string(Image.open(filename), lang='eng')
    text_spa = pytesseract.image_to_string(Image.open(filename), lang='spa')
    text_fra = pytesseract.image_to_string(Image.open(filename), lang='fra')
    text_hin = pytesseract.image_to_string(Image.open(filename), lang='hin')

    possible_languages = []
    lang_text_map = {}

    if text_eng:
        possible_languages.append(str(detect_langs(text_eng)[0]).split(":"))
        lang_text_map['en'] = text_eng
    if text_spa:
        possible_languages.append(str(detect_langs(text_spa)[0]).split(":"))
        lang_text_map['es'] = text_spa
    if text_fra:
        possible_languages.append(str(detect_langs(text_fra)[0]).split(":"))
        lang_text_map['fr'] = text_fra
    if text_hin:
        possible_languages.append(str(detect_langs(text_hin)[0]).split(":"))
        lang_text_map['hi'] = text_hin

    if possible_languages:
        res = max(possible_languages, key=lambda li: li[1])
        if res[0] not in ACCEPTED_LANGUAGES:
            return 'XX', 'XX'
        else:
            return lang_text_map[res[0]], res[0]

    else:
        return 'XX', 'XX'


def ocr_detect(filename, language):
    """
    This function extracts text from image
    """
    import platform
    if platform.system() != 'Darwin':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename), lang=language)

    if not text:
        return "No text detected in the image"
    return text


def format_language(language):
    """
    This function chooses source language
    :param language: source language
    :return: language chosen
    """

    if language == ACCEPTED_LANGUAGES[0]:
        return 'eng'
    elif language == ACCEPTED_LANGUAGES[1]:
        return 'spa'
    elif language == ACCEPTED_LANGUAGES[2]:
        return 'fra'
    elif language == ACCEPTED_LANGUAGES[3]:
        return 'hin'
