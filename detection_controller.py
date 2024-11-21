import os

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from base import app
from base.com.dao.detection_dao import DetectionDAO
from base.com.vo.detection_vo import DetectionVO
from base.service.detect import ai_inference

app.config['input_video_path'] = "base/static/adminResources/input/"
app.config['output_video_path'] = "base/static/adminResources/output/"


@app.route('/loadDetection')
def load_detection():
    return render_template('admin/addDetection.html')


@app.route('/admin/addDetection', methods=['POST'])
def admin_add_detection():
    detection_id = request.form.get('detection_id')
    input_video = request.files.get('filename')

    input_video_name = secure_filename(input_video.filename)

    input_video_path = str(os.path.join(app.config['input_video_path']))
    input_video_file_path = input_video_path + input_video_name
    input_video.save(input_video_file_path)

    output_video_file_name = ai_inference(input_video_file_path)
    print(output_video_file_name)
    output_video_name = output_video_file_name
    output_video_path = os.path.join(app.config['output_video_path'])

    detection_vo = DetectionVO()
    detection_dao = DetectionDAO()

    detection_vo.detection_id = detection_id
    detection_vo.input_video_name = input_video_name
    detection_vo.input_video_path = input_video_path.replace("base", "..")

    detection_vo.detection_id = detection_id
    detection_vo.output_video_name = output_video_name
    detection_vo.output_video_path = output_video_path.replace("base", "..")

    detection_dao.add_detection(detection_vo)
    return redirect('/admin/viewDetection')


@app.route("/admin/viewDetection")
def admin_view_detection():
    try:
        detection_dao = DetectionDAO()
        detection_vo_list = detection_dao.view_detection()
        print("detection_vo_list---->>>>>>>>>>>>>>", detection_vo_list)
        return render_template('admin/viewDetection.html',
                               detection_vo_list=detection_vo_list)
    except Exception as ex:
        print("admin_view_detection route exception>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/deleteDetection')
def admin_delete_detection():
    try:
        detection_vo = DetectionVO()
        detection_dao = DetectionDAO()
        detection_id = request.args.get('detection_id')
        detection_vo.detection_id = detection_id
        detection_vo_list = detection_dao.delete_detection(detection_id)
        file_path = (detection_vo_list.input_video_path.replace("..",
                                                                "base") +
                     detection_vo_list.input_video_name)
        os.remove(file_path)
        file_path1=(detection_vo_list.output_video_path.replace("..","base")
                    + detection_vo_list.output_video_name)
        os.remove(file_path1)
        return redirect(url_for('admin_view_detection'))

        if os.path.exists(input_video_path):
            os.remove(input_video_path)
        if os.path.exists(output_video_path):
            os.remove(output_video_path)

        detection_dao.delete_detection(detection_id)


    except Exception as ex:
        print("admin_delete_detection route exception occured>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)
