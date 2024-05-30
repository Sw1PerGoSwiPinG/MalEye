from flask import Flask, request, jsonify
from flask_cors import CORS
from nfstream import NFStreamer
import os
import pymysql
import requests
import json

app = Flask(__name__)
CORS(app)

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


if __name__ == '__main__':
    app.run(port=5000, debug=True)