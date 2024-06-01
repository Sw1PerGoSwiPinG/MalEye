from flask import Flask, request, jsonify
from flask_cors import CORS
from nfstream import NFStreamer
from YaTC.pre_train import step_data, step_model, step_train
from PIL import Image, ImageOps
import numpy as np

import base64
import io

# import os
# import pymysql
# import requests
# import json

app = Flask(__name__)
CORS(app)

args = None
data_loader_train = None
model, model_without_ddp, optimizer, device = None, None, None, None
train_stat = None


@app.route("/upload_pcap", methods=['POST'])
def upload_pcap():
    """
    上传pcap文件
    :return: id, src_ip, src_port, dst_ip, dst_port, protocol, application_name
    """
    # 从请求中获取文件
    file = request.files['file']
    label = request.form['label']
    print(label)
    # 保存文件
    save_path = "uploadPcap/" + label + "/" + file.filename
    print(save_path)
    file.save(save_path)
    output_path = "uploadPcapToCsv/" + label + "/" + file.filename.replace('.pcap', '.pcap.csv')
    my_streamer = NFStreamer(source=save_path)
    my_streamer.to_csv(path=output_path, columns_to_anonymize=[], flows_per_file=0, rotate_files=0)
    df = my_streamer.to_pandas()[["id", "src_ip", "src_port", "dst_ip", "dst_port", "protocol", "application_name"]]
    df["label"] = label
    json_data = df.to_json(orient='records')
    print(json_data)
    return json_data


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
        mfrs_org = []
        mfrs_trans = []
        for mfr in dataset_train:
            mfr = Image.fromarray(np.uint8(mfr[0][0].numpy()))
            mfr_org = ImageOps.invert(mfr)
            # 将图片转换为Base64字符串
            buffered_org = io.BytesIO()
            mfr_org.save(buffered_org, format="PNG")
            mfrs_org.append(base64.b64encode(buffered_org.getvalue()).decode('utf-8'))

            buffered_trans = io.BytesIO()
            mfr.save(buffered_trans, format="PNG")
            mfrs_trans.append(base64.b64encode(buffered_trans.getvalue()).decode('utf-8'))
            # mfrs_org.append(base64.b64encode(mfr_org.tobytes()).decode('utf-8'))
            # mfrs_trans.append(base64.b64encode(mfr.tobytes()).decode('utf-8'))
        return jsonify({
            'message': 'success', 
            'data': {'mfrs_org': mfrs_org, 'mfrs_trans': mfrs_trans}
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
    global train_stat
    status, train_stat = step_train(args, data_loader_train, model, model_without_ddp, optimizer, device)
    if status == "success":
        return jsonify({'message': 'success', 'data': train_stat})
    else:
        return jsonify({'message': 'error'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)