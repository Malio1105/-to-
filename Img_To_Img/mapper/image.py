from model.models import Image as modelsImage
from model.models import db


#数据库账号信息
class Image():
    def add_image(image):
        db.session.add(image)
        db.session.commit()
        return {'添加成功'}

    def get_image(excludeId=[]):
        images = modelsImage.query.filter(modelsImage.id.notin_(excludeId)).all()
        return images

    def find_imageUrl(imageId):
        img = modelsImage.query.filter_by(id=imageId).first()
        return img.image
