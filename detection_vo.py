from base import db


class DetectionVO(db.Model):
    __tablename__ = 'detection_table'
    detection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_video_name = db.Column('input_video_name', db.Text,
                                 nullable=False)
    input_video_path = db.Column('input_video_path', db.Text,
                                 nullable=False)
    output_video_name = db.Column('output_video_name', db.Text, nullable=False)
    output_video_path = db.Column('output_video_path', db.Text, nullable=False)

    def as_dict(self):
        return {
            'detection_id': self.detection_id,
            'input_video_name': self.input_video_name,
            'input_video_path': self.input_video_path,
            'output_video_name': self.output_video_name,
            'output_video_path': self.output_video_path
        }


db.create_all()
