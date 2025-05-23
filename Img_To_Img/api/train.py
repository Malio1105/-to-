from flask import Blueprint, jsonify, request
from model.models import Image as modelsImage

from PIL import Image
from io import BytesIO
import numpy as np

from mapper.image import Image as mapperImage
from utils import train_utils

train_api=Blueprint('train',__name__)

@train_api.route('/get', methods=['GET'])
def get_image(): #获取图片，对搜图训练进行代码优化
    old_data = np.load('image_features.npz', allow_pickle=True)
    old_paths = old_data['paths']  # 旧路径
    old_vectors = old_data['vectors']  # 旧特征向量

    all_images = mapperImage.get_image(old_paths)  # 获取除old_path以外所有图片

    images = [{
        'id':img.id,
        'url': img.image,
    } for img in all_images]  # 将图片变成字典

    new_paths = []  # 存储图像路径
    new_vectors = []# 存储图像向量

    for i in range(len(images)):
        vec = train_utils.extract_vector_from_url(images[i]['url'])
        if vec is not None:
            new_paths.append(images[i]['id'])
            new_vectors.append(vec)
            print(f"Processed: {images[i]['id'],images[i]['url']}")
        else:
             print(f"Failed to extract features from: {images[i]['id'],images[i]['url']}")

    if not new_paths:
        return jsonify({"message": "No valid new images processed"})

    new_vectors=np.array(new_vectors)

    paths = []  # 存储图像路径
    vectors = []# 存储图像向量

    paths = np.concatenate((old_paths,new_paths))

    #转化为numpy数组
    paths = np.array(paths, dtype=object)
    vectors = np.vstack((old_vectors, new_vectors))
    #print(paths, vectors)
    # 保存合并后的数据（覆盖旧文件）
    np.savez_compressed('image_features.npz', paths=paths, vectors=vectors)

    #old_data.close()
    return jsonify({"message":"OK"})

#优化前的代码
# def get_image():  # 获取图片
#     all_images = mapperImage.get_image();  # 获取所有图片
#
#     images = [{
#         'id':img.id,
#         'url': img.image,
#     } for img in all_images]  # 将图片变成字典
#
#     paths = []# 存储图像路径
#     vectors = []# 存储图像向量
#
#     for i in range(len(images)):
#         vec = train_utils.extract_vector_from_url(images[i]['url'])
#         if vec is not None:
#             paths.append(images[i]['id'])
#             vectors.append(vec)
#             print(f"Processed: {images[i]['url']}")
#         else:
#             print(f"Failed to extract features from: {images[i]['url']}")
#
#     print(vectors)
#     #转化为numpy数组
#     paths = np.array(paths, dtype=object)
#     vectors = np.vstack(vectors)
#
#     # 保存为.npz文件
#     np.savez_compressed('image_features.npz', paths=paths, vectors=vectors)
#     return jsonify({
#         "message":f"Saved {len(paths)} feature vectors to image_features.npz",
#         "paths":paths.tolist()
#                     })


