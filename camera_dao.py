from base import db
from base.com.vo.camera_vo import CameraVO


class CameraDAO:
    def add_camera(self, camera_vo):
        db.session.add(camera_vo)
        db.session.commit()

    def view_camera(self) -> object:
        camera_vo_list = CameraVO.query.all()
        return camera_vo_list

    def delete_camera(self, cameravo):
        camera_vo_list = CameraVO.query.get(cameravo.camera_id)
        db.session.delete(camera_vo_list)
        db.session.commit()

    def edit_camera(self, cameravo):
        camera_vo_list = CameraVO.query.filter_by(
            camera_id=cameravo.camera_id).all()
        print(">>>>>", camera_vo_list)
        return camera_vo_list

    def update_camera(self, cameravo):
        db.session.merge(cameravo)
        db.session.commit()
