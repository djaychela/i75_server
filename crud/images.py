from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models


def get_all_images(db: Session):
    return db.query(models.ImageData).all()


def get_random_image_filename(db: Session):
    image = db.query(models.ImageData).order_by(func.random()).first()
    print(f"***  {image.id=}, {image.filename=} ***")
    return f"{image.filename}"


def get_image_filename(db: Session, image_id):
    image = db.query(models.ImageData).filter(models.ImageData.id == image_id).first()
    return image.filename


def store_new_image(db: Session, text, filename):
    new_image = models.ImageData()
    new_image.text = text
    new_image.filename = filename
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

def store_new_wifi_image(db: Session, ssid, password, filename):
    wifi_image = db.query(models.WifiImageData).filter(models.WifiImageData.id == 1).first()
    wifi_image.ssid = ssid
    wifi_image.password = password
    wifi_image.filename = filename
    db.add(wifi_image)
    db.commit()
    db.refresh(wifi_image)
    return wifi_image

def get_wifi_image_data(db: Session):
    wifi_image = db.query(models.WifiImageData).filter(models.WifiImageData.id == 1).first()
    return wifi_image


def delete_image_by_id(db: Session, image_id: int):
    to_delete = (
        db.query(models.ImageData).filter(models.ImageData.id == image_id).delete()
    )
    if to_delete:
        db.commit()
        return True
    return False
