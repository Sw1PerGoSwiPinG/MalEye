from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import glob
import base64

app = Flask(__name__)
CORS(app)

@app.route("/upload_pcap", methods=['POST'])
def upload_pcap():
    try:
        file = request.files['file']
        label = request.form['label']
        save_path = "uploadPcap/" + label + "/" + file.filename
        file.save(save_path)
        return jsonify({"status": "success", "message": "File uploaded successfully"}), 200
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"status": "error", "message": "Failed to process file"}), 500

@app.route("/create_group", methods=['POST'])
def create_group():
    try:
        data = request.get_json()
        group_name = data['name']
        categories = data['categories']

        base_path = "uploadPcap/" + group_name
        image_base_path = "static/images/" + group_name
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(image_base_path, exist_ok=True)

        for category in categories:
            category_path = os.path.join(base_path, category)
            image_category_test_path = os.path.join(image_base_path, "test", category)
            image_category_train_path = os.path.join(image_base_path, "train", category)
            os.makedirs(category_path, exist_ok=True)
            os.makedirs(image_category_test_path, exist_ok=True)
            os.makedirs(image_category_train_path, exist_ok=True)

        return jsonify({"status": "success", "message": "Group and categories created successfully"}), 200
    except Exception as e:
        print(f"Error creating group: {e}")
        return jsonify({"status": "error", "message": "Failed to create group"}), 500

# MFR矩阵管理页面，创建组后上传文件调用的接口
@app.route("/get_image", methods=['POST'])
def get_image():
    try:
        base_path = "static/images"
        groups = os.listdir(base_path)
        all_images = {}

        # 待添加：生成图片逻辑

        for group in groups:
            group_path = os.path.join(base_path, group, "test")
            if os.path.isdir(group_path):
                categories = os.listdir(group_path)
                all_images[group] = {}
                for category in categories:
                    category_path = os.path.join(group_path, category)
                    image_files = glob.glob(os.path.join(category_path, "*.png"))[:10]
                    images_base64 = []
                    for img_file in image_files:
                        with open(img_file, "rb") as image:
                            images_base64.append(base64.b64encode(image.read()).decode('utf-8'))
                    all_images[group][category] = images_base64

        return jsonify({"status": "success", "images": all_images}), 200
    except Exception as e:
        print(f"Error fetching images: {e}")
        return jsonify({"status": "error", "message": "Failed to fetch images"}), 500

@app.route("/get_all_images", methods=['GET'])
def get_all_images():
    try:
        base_path = "static/images"
        groups = os.listdir(base_path)
        all_images = {}

        for group in groups:
            group_path = os.path.join(base_path, group, "test")
            if os.path.isdir(group_path):
                categories = os.listdir(group_path)
                all_images[group] = {}
                for category in categories:
                    category_path = os.path.join(group_path, category)
                    image_files = glob.glob(os.path.join(category_path, "*.png"))[:10]
                    images_base64 = []
                    for img_file in image_files:
                        with open(img_file, "rb") as image:
                            images_base64.append(base64.b64encode(image.read()).decode('utf-8'))
                    all_images[group][category] = images_base64

        return jsonify({"status": "success", "images": all_images}), 200
    except Exception as e:
        print(f"Error fetching all images: {e}")
        return jsonify({"status": "error", "message": "Failed to fetch all images"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
