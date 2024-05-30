<template>
  <div class="container">
    <div class="header">
      <button @click="addData" class="add-button">新增</button>
      <button @click="deleteData" class="delete-button">删除</button>
      <input v-model="search" type="text" placeholder="Search" class="search-input" />
      <select v-model="filter" class="filter-select">
        <option value="">所有类别</option>
        <option value="malicious">恶意流量</option>
        <option value="normal">正常流量</option>
      </select>
      <button @click="searchData" class="search-button">搜索</button>
    </div>
    <div class="dataset-table-container">
      <table class="dataset-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>SourceIP</th>
            <th>DestIP</th>
            <th>SourcePort</th>
            <th>DestPort</th>
            <th>Protocol</th>
            <th>ApplicationName</th>
            <!-- <th>Version</th>
            <th>ImageFeature</th>
            <th>ThFeature</th>
            <th>Feature</th> -->
            <th>Label</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in dataset" :key="data.id">
            <td>{{ data.id }}</td>
            <td>{{ data.src_ip }}</td>
            <td>{{ data.dst_ip }}</td>
            <td>{{ data.src_port }}</td>
            <td>{{ data.dst_port }}</td>
            <td>{{ data.protocol }}</td>
            <td>{{ data.application_name }}</td>
            <!-- <td>{{ data.version }}</td>
            <td><img :src="data.imageFeature" alt="Image Feature" class="image-feature" /></td>
            <td><img :src="data.thFeature" alt="Th Feature" class="th-feature" /></td>
            <td>{{ data.feature }}</td> -->
            <td :class="{'label-malicious': data.label === 'Benign', 'label-normal': data.label === 'Malware'}">{{ data.label }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span @click="closeModal" class="close">&times;</span>
        <h2>添加流量数据</h2>
        <div class="modal-body">
          <input type="file" @change="handleFileUpload" />
          <select v-model="selectedFlag">
            <option value="" disabled>选择包类型</option>
            <option value="benign">Benign</option>
            <option value="malware">Malware</option>
          </select>
          <button @click="uploadFile" class="upload-button">上传检测流量</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DatasetPage',
  data() {
    return {
      search: '',
      filter: '',
      dataset: [
      ],
      showModal: false,
      selectedFile: null,
      selectedFlag: ''
    };
  },
  methods: {
    addData() {
      this.showModal = true;
    },
    deleteData() {
      console.log('删除数据');
      // 触发删除数据的逻辑
    },
    searchData() {
      console.log('搜索数据');
      // 触发搜索数据的逻辑
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      console.log('文件上传:', this.selectedFile);
      // 处理文件上传
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert('请先选择一个文件');
        return;
      }
      if (!this.selectedFlag) {
        alert('请先选择一个包类型');
        return;
      }
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('label', this.selectedFlag);

      try {
        const response = await axios.post('http://127.0.0.1:5000/upload_pcap', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('文件上传成功:', response.data);
        this.dataset = this.dataset.concat(response.data);
        alert('文件上传成功');
        this.closeModal();
      } catch (error) {
        console.error('文件上传失败:', error);
        alert('文件上传失败');
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedFile = null;
      this.selectedFlag = '';
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.add-button,
.delete-button {
  margin-right: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.add-button {
  background-color: #4caf50;
}

.delete-button {
  background-color: #f44336;
}

.search-input {
  margin-right: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
}

.filter-select {
  margin-right: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.dataset-table-container {
  width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

thead {
  background-color: #e0e0e0;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.image-feature, .th-feature {
  width: 50px;
  height: 50px;
}

.label-malicious {
  color: red;
}

.label-normal {
  color: green;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 50%;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}

.upload-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
