from base import db
from base.com.vo.detection_vo import DetectionVO


class DetectionDAO:
    def add_detection(self, detection_vo):
        db.session.add(detection_vo)
        db.session.commit()

    def view_detection(self) -> object:
        detection_vo_list = DetectionVO.query.all()
        return detection_vo_list

    def delete_detection(self, detection_id):
        detection_vo_list = DetectionVO.query.get(detection_id)
        db.session.delete(detection_vo_list)
        db.session.commit()
        return detection_vo_list
