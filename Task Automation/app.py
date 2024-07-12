from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename
import file_organizer
import data_cleaner
import system_maintenance

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# HTML content
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        .section {
            margin-bottom: 20px;
        }
        input[type="file"], input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 15px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #upload-result, #organize-result, #clean-result, #system-result {
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Automation with Python</h1>

        <div class="section">
            <h2>Upload File</h2>
            <form id="upload-form" enctype="multipart/form-data">
                <input type="file" id="file" name="file">
                <button type="submit">Upload</button>
            </form>
            <div id="upload-result"></div>
        </div>

        <div class="section">
            <h2>Organize Files</h2>
            <button id="organize-files-btn">Organize Files</button>
            <div id="organize-result"></div>
        </div>

        <div class="section">
            <h2>Clean Data</h2>
            <input type="text" id="data-file" placeholder="Enter filename">
            <button id="clean-data-btn">Clean Data</button>
            <div id="clean-result"></div>
        </div>

        <div class="section">
            <h2>System Maintenance</h2>
            <button id="disk-usage-btn">Check Disk Usage</button>
            <div id="system-result"></div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#upload-form').submit(function(e) {
                e.preventDefault();
                var formData = new FormData(this);
                $.ajax({
                    url: '/upload_file',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        $('#upload-result').text(response.success || response.error);
                    }
                });
            });

            $('#organize-files-btn').click(function() {
                $.ajax({
                    url: '/organize_files',
                    type: 'POST',
                    success: function(response) {
                        $('#organize-result').text(response.success);
                    }
                });
            });

            $('#clean-data-btn').click(function() {
                var filename = $('#data-file').val();
                $.ajax({
                    url: '/clean_data',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ filename: filename }),
                    success: function(response) {
                        $('#clean-result').text(response.success + ': ' + response.cleaned_file);
                    }
                });
            });

            $('#disk-usage-btn').click(function() {
                $.ajax({
                    url: '/system_maintenance',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ task: 'disk_usage' }),
                    success: function(response) {
                        $('#system-result').text(response.result);
                    }
                });
            });
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': 'File uploaded successfully', 'filename': filename})


@app.route('/organize_files', methods=['POST'])
def organize_files():
    directory = app.config['UPLOAD_FOLDER']
    file_organizer.organize_files(directory)
    return jsonify({'success': 'Files organized successfully'})


@app.route('/clean_data', methods=['POST'])
def clean_data():
    filename = request.json.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'})
    cleaned_file_path = data_cleaner.clean_csv(file_path)
    return jsonify({'success': 'Data cleaned successfully', 'cleaned_file': os.path.basename(cleaned_file_path)})


@app.route('/system_maintenance', methods=['POST'])
def system_maintenance_task():
    task = request.json.get('task')
    result = system_maintenance.perform_task(task)
    return jsonify({'result': result})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
