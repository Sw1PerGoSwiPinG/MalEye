from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from nfstream import NFStreamer
from PIL import Image, ImageOps
from io import StringIO
import numpy as np
import pandas as pd
import os
import io
import glob
import base64
import socket
import scapy.all as scapy
from scapy.layers.inet6 import IP, TCP, Raw, IPv6

# from YaTC.data_process_new import read_MFR_bytes
from YaTC.data_process import read_MFR_bytes
from YaTC.pre_train import step_data, step_model, step_train
from YaTC.fine_tune import run as FineTuning

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KRY'] = "SW1PERGOSWIPING"
socketio = SocketIO(app, cors_allowed_origins='*')

args = None
data_loader_train = None
model, model_without_ddp, optimizer, device = None, None, None, None
train_stat = None

protocol_dict = {
    0: "HOPOPT",
    1: "ICMP",
    2: "IGMP",
    6: "TCP",
    17: "UDP",
    41: "IPv6",
    47: "GRE",
    50: "ESP",
    51: "AH",
    58: "ICMPv6",
    89: "OSPF",
    132: "SCTP",
}

@app.route("/upload_pcap", methods=['POST'])
def upload_pcap():
    try:
        file = request.files['file']
        label = request.form['label']
        save_path = "uploadPcap/" + label + "/" + file.filename
        file.save(save_path)

        output_path = "uploadPcapToCsv/" + label + "/" + file.filename.replace('.pcap', '.csv')
        my_streamer = NFStreamer(source=save_path)
        df = my_streamer.to_pandas()[["src_ip", "src_port", "dst_ip", "dst_port", "protocol", "application_name"]]
        print(len(df))
        df["label"] = label

        whole_csv_path = "uploadPcapToCsv/whole.csv"
        if os.path.exists(whole_csv_path):
            whole_df = pd.read_csv(whole_csv_path)
            last_id = whole_df["id"].max()
        else:
            whole_df = pd.DataFrame()
            last_id = 0

        df.insert(0, 'id', range(last_id + 1, last_id + 1 + len(df)))
        df.to_csv(output_path, index=False)
        df.to_csv(whole_csv_path, mode='a', header=not os.path.exists(whole_csv_path), index=False)

        return jsonify({"status": "success", "message": "File uploaded and processed successfully"}), 200
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"status": "error", "message": "Failed to process file"}), 500

@app.route("/get_dataset", methods=['GET'])
def get_dataset():
    try:
        page = int(request.args.get('page', 1))
        page_size = 100
        df = pd.read_csv("uploadPcapToCsv/whole.csv")
        df = df[["id", "src_ip", "src_port", "dst_ip", "dst_port", "protocol", "application_name", "label"]]
        df = df.sort_values(by="id", ascending=False)
        start = (page - 1) * page_size
        end = start + page_size
        json_data = df.iloc[start:end].to_json(orient='records')
        return json_data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return jsonify({"error": "Failed to read dataset"}), 500

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
        # base_path = "static/images"
        base_path = "./YaTC/data"
        groups = os.listdir(base_path)
        all_images = {}

        # 待添加：生成图片逻辑

        for group in groups:
            group_path = os.path.join(base_path, group, "train")
            if os.path.isdir(group_path):
                categories = os.listdir(group_path)
                all_images[group] = {}
                for category in categories:
                    category_path = os.path.join(group_path, category)
                    image_files = glob.glob(os.path.join(category_path, "*.png"))[:15]
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
        # base_path = "static/images"
        base_path = "./YaTC/data"
        groups = os.listdir(base_path)
        all_images = {}
        total_number = {}

        for group in groups:
            group_path = os.path.join(base_path, group, "train")
            if os.path.isdir(group_path):
                categories = os.listdir(group_path)
                all_images[group] = {}
                total_number[group] = {}
                for category in categories:
                    category_path = os.path.join(group_path, category)
                    image_files = glob.glob(os.path.join(category_path, "*.png"))
                    show_image = image_files[:15]
                    images_base64 = []
                    for img_file in show_image:
                        with open(img_file, "rb") as image:
                            images_base64.append(base64.b64encode(image.read()).decode('utf-8'))
                    all_images[group][category] = images_base64
                    total_number[group][category] = len(image_files)


        return jsonify({"status": "success", "images": all_images, "total_number": total_number}), 200
    except Exception as e:
        print(f"Error fetching all images: {e}")
        return jsonify({"status": "error", "message": "Failed to fetch all images"}), 500

"""
预训练路由
"""
@app.route('/pre-train-step1', methods=['POST'])
def pre_tain_step1():
    form_data = request.json
    if not form_data:
        return jsonify({'error': 'No data provided'}), 400

    args_dict = {
        'epochs': form_data.get('epochs'),
        'warmup_epochs': form_data.get('warmupEpochs'),
        'batch_size': form_data.get('batchSize'),
        'learning_rate': form_data.get('learningRate'),
        'mask_ratio': form_data.get('maskRatio'),
        'weight_decay': form_data.get('weightDecay'),
        'seed': form_data.get('seed'),
        'dataset': form_data.get('dataset')
    }

    global args, data_loader_train
    status, args, dataset_train, data_loader_train = step_data(args_dict)
    if status == "success":
        mfrs_label = []
        mfrs_org = []
        mfrs_trans = []
        mfrs_feature = []

        # 获取数据集的标签
        data_path = f"./YaTC/data/{args_dict['dataset']}_MFR/train"
        items = os.listdir(data_path)
        labels = [item for item in items if os.path.isdir(os.path.join(data_path, item))]

        for mfr in dataset_train:
            # 标签
            mfrs_label.append(labels[mfr[1]])
            # 特征
            # mfrs_feature.append(str(mfr[0][0]))
            numpy_array = mfr[0][0].numpy()
            row_strings = [np.array2string(row, separator=', ') for row in np.vstack((numpy_array[:3], numpy_array[-1:]))]
            row_strings.insert(3, '...')
            mfrs_feature.append('\n'.join(row_strings))

            # 获取mfr，并将mfr图片转换为Base64字符串
            mfr = Image.fromarray(np.uint8(mfr[0][0].numpy()))
            mfr_org = ImageOps.invert(mfr)

            buffered_org = io.BytesIO()
            mfr_org.save(buffered_org, format="PNG")
            mfrs_org.append(base64.b64encode(buffered_org.getvalue()).decode('utf-8'))
            buffered_trans = io.BytesIO()
            mfr.save(buffered_trans, format="PNG")
            mfrs_trans.append(base64.b64encode(buffered_trans.getvalue()).decode('utf-8'))
        return jsonify({
            'message': 'success', 
            'data': {'mfrs_label': mfrs_label, 'mfrs_org': mfrs_org, 'mfrs_trans': mfrs_trans, 'mfrs_feature': mfrs_feature}
        })
    else:
        return jsonify({'message': 'error'})


@app.route('/pre-train-step2', methods=['GET'])
def pre_tain_step2():
    global model, model_without_ddp, optimizer, device
    status, model, model_without_ddp, optimizer, device = step_model(args, data_loader_train)
    if status == "success":
        return jsonify({
            'message': 'success', 
            'data': {'model': str(model), 'optimizer': str(optimizer)}
        })
    else:
        return jsonify({'message': 'error'})


@app.route('/pre-train-step3', methods=['GET'])
def pre_tain_step3():
    global stats_list
    status, stats_list, token_list = step_train(args, data_loader_train, model, model_without_ddp, optimizer, device)
    if status == "success":
        return jsonify({
            'message': 'success', 
            'data': {'stats_list': stats_list, 'token_list': token_list}
        })
    else:
        return jsonify({'message': 'error'})


"""
微调路由
"""
@socketio.on('connect', namespace='/finetune')
def handle_connect():
    print("Connet Successfully to localhost:8000!")


@app.route('/fine-tuning', methods=['POST'])
def finetune():
    form_data = request.json
    if not form_data:
        return jsonify({'error': 'No data provided'}), 400

    args_dict = {
        'epochs': form_data.get('epochs'),
        'warmup_epochs': form_data.get('warmup_epochs'),
        'batch_size': form_data.get('batch_size'),
        'blr': form_data.get('blr'),
        'drop_path': form_data.get('drop_path'),
        'weight_decay': form_data.get('weight_decay'),
        'seed': form_data.get('seed'),
        'dataset': form_data.get('dataset'),
        'nb_classes': form_data.get('nb_classes')
    }
    FineTuning(args_dict, socketio)
    
    return jsonify({'message': 'success', })

def send_log(log):
    socketio.emit("message", str(log), namespace='/finetune')


"""
流量检测页面
"""
@app.route("/read_pcap", methods=['POST'])
def read_pcap():
    try:
        file = request.files['file']
        save_path = "uploadPcap/unknown/" + file.filename
        file.save(save_path)
        packets = scapy.rdpcap(save_path)
        filtered_packets = []
        for packet in packets:
            if IPv6 in packet:
                continue
            else:
                src_ip = packet[IP].src
                src_port = packet[TCP].sport if TCP in packet else ""
                dst_ip = packet[IP].dst
                dst_port = packet[TCP].dport if TCP in packet else ""
                protocol_id = packet[IP].proto
                protocol = protocol_dict.get(int(protocol_id), "unknown")
                raw = packet[Raw].load if Raw in packet else ""

                filtered_packets.append([src_ip, src_port, dst_ip, dst_port, protocol, raw])

        df = pd.DataFrame(filtered_packets, columns=["src_ip", "src_port", "dst_ip", "dst_port", "protocol", "raw"])
        print(len(df))

        # 将DataFrame转换为字符串IO对，将文件指针移回文件开头
        csv_data = StringIO()
        df.to_csv(csv_data, index=False)
        csv_data.seek(0)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data.csv"}
        )
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"message": "error"}), 500


@app.route("/gen_mfr", methods=['POST'])
def gen_mfr():
    flows_pcap_path = './uploadPcap/unknown/'
    file_name = request.form['fileName']
    flows = glob.glob(flows_pcap_path + file_name)
    mfrs = []
    mfrs_org = []
    mfrs_trans = []
    for flow in flows:
        packets = scapy.rdpcap(flow)
        packet_count = len(packets)
        
        chunk_count = (packet_count + 4) // 5
        for i in range(chunk_count):
            chunk_packets = packets[i * 5: (i + 1) * 5]
            content = read_MFR_bytes(chunk_packets)
            content = np.array([int(content[j:j + 2], 16) for j in range(0, len(content), 2)])
            fh = np.reshape(content, (40, 40))
            fh = np.uint8(fh)
            im = Image.fromarray(fh)
            mfrs.append(im)
    
    for mfr in mfrs:
        # 获取mfr，并将mfr图片转换为Base64字符串
        mfr_trans = ImageOps.invert(mfr)
        buffered_org = io.BytesIO()
        mfr.save(buffered_org, format="PNG")
        mfrs_org.append(base64.b64encode(buffered_org.getvalue()).decode('utf-8'))
        buffered_trans = io.BytesIO()
        mfr_trans.save(buffered_trans, format="PNG")
        mfrs_trans.append(base64.b64encode(buffered_trans.getvalue()).decode('utf-8'))
    return jsonify({
        'message': 'success', 
        'data': {'mfrs_org': mfrs_org, 'mfrs_trans': mfrs_trans}
    })



@app.route("/detect_upload", methods=['POST'])
def detect_upload():
    pass


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
