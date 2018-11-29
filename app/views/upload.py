import os

from flask import request, render_template, Blueprint

from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)


@bp.route('/upload/',methods=["GET","POST"])
def upload_file():
    method = request.method

    if method == "GET":
        return render_template("file_upload.html")

    elif method == "POST":

        file = request.files['fileUpload']

        file_path = os.path.join('/tmp', 'flask_demo')

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path,secure_filename(file.filename))

        file.save(file_path)

        return render_template("file_upload.html")
    else:
        print("不支持%s请求方法\n" % method)

