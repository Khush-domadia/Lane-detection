from base import db


class CameraVO(db.Model):
    __tablename__ = 'camera_table'
    camera_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_name = db.Column('camera_name', db.Text,
                            nullable=False)
    camera_code = db.Column('camera_code', db.Text,
                            nullable=False)
    select_location = db.Column('select_location', db.Text,
                                nullable=False)

    def as_dict(self):
        return {
            'camera_id': self.camera_id,
            'camera_name': self.camera_name,
            'camera_code': self.camera_code,
            'select_location': self.select_location
        }


db.create_all()
