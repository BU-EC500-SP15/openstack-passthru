import os
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/jj/flask_upload'        # needs to be changed according to the own system(server)
ALLOWED_EXTENSIONS = set(['txt'])             #can add more file types currently working on txt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):				#to check if file is of allowed extension
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploaded/<filename>')
def uploaded_file(filename):				#see uploaded file
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/', methods = ['GET', 'POST'])
def upload():					  	#upload file
	if request.method == 'POST':
		#print "HERE"
		file = request.files['filename']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print "reached"
			return redirect(url_for('uploaded_file', filename = filename))
	return '''
	<!doctype html>
	<title>UPLOAD NEW FILE</title>
	<h1>upload new file</h1>
	<form action = "" method = post enctype = multipart/form-data>
		<p><input type=file name = filename>
		   <input type=submit value=Upload>
	</form>
	'''

if __name__ == '__main__':
	app.run(None,5001,True)
