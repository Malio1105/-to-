from flask import Blueprint, jsonify, request
from model.models import Image as modelsImage
from mapper.image import Image as mapperImage
import utils.faiss_utils as search
from werkzeug.utils import secure_filename
import os.path
import numpy as np
import faiss

image_api=Blueprint('image',__name__)

@image_api.route('/add',methods=['POST'])
def add_image(): #增加图片到数据库中
    data=request.get_json() #获取数据库前端图片
    print(data)

    if not data.get('image'):
        return jsonify({'message': '图片为空'}), 400

    if len(data)>1024:
        return jsonify({'message':'图片URL过长'}),400

    image=modelsImage(
        image=data.get('image')
    )

    mapperImage.add_image(image)
    return jsonify({'message':'Image adds successfully'}),200

@image_api.route('/get', methods=['GET'])
def get_image(): #获取图片
    all_images=mapperImage.get_image([]); #获取所有图片

    image_list=[{
        'id':pic.id,
        'pictrue':pic.image,
    } for pic in all_images]  #将图片变成字典

    return jsonify({'message': image_list}),200  #向前端输出数据

@image_api.route('/search', methods=['GET','POST']) # API接口：提交查询招聘，终端使用的是POST方法
def search_image():
    # 加载预计算的特征
    data = np.load('image_features.npz', allow_pickle=True)  # 加载训练结果.npz文件
    paths = data['paths']  # 从文件中得出图片路径
    vectors = data['vectors']  # 从文件中得出图片向量
    # 3.构建Faiss索引
    d = 2048  # 特征向量的维度（ResNet-50提取的特征向量维度为 2048）
    index = faiss.IndexFlatL2(d)  # 我也不知道，反正就是创造一个索引对象进行相似性搜索
    index.add(vectors)

    if 'image' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 获取安全的文件名并提取扩展名
    original_filename = secure_filename(image.filename)
    _, ext = os.path.splitext(original_filename)
    # 生成动态文件名（保留原扩展名）
    query_filename = f"query{ext}"
    query_path = os.path.join('.', query_filename)
    image.save(query_path)

    # 执行搜索
    try:
        results = search.search_topk(query_path, index, paths, k=3)  #index.add(vectors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # 构建响应
    # 将p的值(原本是id),通过数据库查询找到相应的URL
    response = [{'path': mapperImage.find_imageUrl(p), 'distance': d} for p, d in results]
    return jsonify({'results': response})



