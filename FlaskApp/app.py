import os
from flask import Flask, render_template, request

import ocr_core
import translator
import object_detect

# upload and object detection output folders
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'

# configure the folders to the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# home page routing
@app.route('/')
def home_page():
    return render_template('index.html')


# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected',
                                   target_languages=translator.TARGET_LANGUAGE_OPTIONS)
        file = request.files['file']
        # lang = request.form.get('source_languages')
        target_lang = request.form.get('target_languages')

        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected',
                                   target_languages=translator.TARGET_LANGUAGE_OPTIONS)

        if file and ocr_core.allowed_file(file.filename):
            # call the OCR function on it
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            just_fname = file.filename.split(".")[0]
            extracted_text, lang = ocr_core.auto_detect_text(file)
            objects_detected = object_detect.object_detect(file.filename)

            if lang == 'XX':
                return render_template('upload.html', msg='Language not '
                                                          'recognised or '
                                                          'Image does not '
                                                          'have text',
                                   target_languages=translator.TARGET_LANGUAGE_OPTIONS,
                                    img_src=os.path.join(app.config[
                                                                'UPLOAD_FOLDER'],
                                                            file.filename),
                                       obj_det=os.path.join(app.config[
                                                                'OUTPUT_FOLDER'],
                                                            just_fname + '.png'),
                                       objects_detected=objects_detected
                                       )

            # lang = ocr_core.format_language(lang)
            # extracted_text = ocr_core.ocr_detect(file, lang)

            if target_lang != 'None':
                target_lang = translator.format_language(target_lang)
                extracted_text = translator.translate(extracted_text, target_lang)

            # text extraction
            return render_template('upload.html',
                                   msg='Successfully processed...',
                                   extracted_text=extracted_text,
                                   target_languages=translator.TARGET_LANGUAGE_OPTIONS,
                                   img_src=os.path.join(app.config[
                                                            'UPLOAD_FOLDER'],
                                                        file.filename),
                                   obj_det=os.path.join(app.config[
                                                            'OUTPUT_FOLDER'],
                                                        just_fname + '.png'),
                                   objects_detected = objects_detected
                                   )

            # return render_template('upload.html',
            #                        msg='Successfully processed...',
            #                        extracted_text=extracted_text,
            #                        target_languages=translator.TARGET_LANGUAGE_OPTIONS,
            #                        img_src=os.path.join(app.config[
            #                                                 'UPLOAD_FOLDER'],
            #                                             file.filename),
            #                        )

        else:
            return render_template('upload.html', msg='Only jpg, jpeg and png images allowed',
                                   target_languages=translator.TARGET_LANGUAGE_OPTIONS)

    elif request.method == 'GET':
        return render_template('upload.html', target_languages=translator.TARGET_LANGUAGE_OPTIONS)


if __name__ == '__main__':
    app.run(debug=True)
