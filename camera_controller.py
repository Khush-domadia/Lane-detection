from flask import request, render_template, redirect

from base import app
from base.com.dao.camera_dao import CameraDAO
from base.com.vo.camera_vo import CameraVO


@app.route('/loadCamera')
def load_camera():
    return render_template('admin/addCamera.html')


@app.route('/admin/addCamera', methods=['POST'])
def admin_add_camera():
    camera_name = request.form.get("camera_name")
    camera_code = request.form.get("camera_code")
    select_location = request.form.get("select_location")

    camera_vo = CameraVO()
    camera_dao = CameraDAO()

    camera_vo.camera_name = camera_name
    camera_vo.camera_code = camera_code
    camera_vo.select_location = select_location

    camera_dao.add_camera(camera_vo)
    return redirect('/admin/viewCamera')


@app.route("/admin/viewCamera")
def admin_view_camera():
    camera_dao = CameraDAO()
    camera_vo_list = camera_dao.view_camera()
    return render_template('admin/viewCamera.html',
                           camera_vo_list=camera_vo_list)


@app.route('/admin/deleteCamera')
def admin_delete_camera():
    camera_vo = CameraVO()
    camera_dao = CameraDAO()
    camera_id = request.args.get('camera_id')
    camera_vo.camera_id = camera_id
    camera_dao.delete_camera(camera_vo)
    return redirect('/admin/viewCamera')


@app.route('/admin/editCamera', methods=['GET'])
def admin_edit_camera():
    camera_vo = CameraVO()
    camera_dao = CameraDAO()

    camera_id = request.args.get('camera_id')
    camera_vo.camera_id = camera_id
    camera_vo_list = camera_dao.edit_camera(camera_vo)
    print(">>>>>>>>>", camera_vo_list)
    return render_template('admin/editCamera.html',
                           camera_vo_list=camera_vo_list)


@app.route('/admin/updateCamera', methods=['POST'])
def admin_update_camera():
    camera_id = request.form.get('camera_id')
    camera_name = request.form.get('camera_name')
    camera_code = request.form.get('camera_code')
    select_location = request.form.get('select_location')

    camera_vo = CameraVO()
    camera_dao = CameraDAO()

    camera_vo.camera_id = camera_id
    camera_vo.camera_name = camera_name
    camera_vo.camera_code = camera_code
    camera_vo.select_location = select_location
    camera_dao.update_camera(camera_vo)
    return redirect('/admin/viewCamera')
