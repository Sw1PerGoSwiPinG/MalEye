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
    <div class="dataset-table-container" @scroll="handleScroll">
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
            <th>Label</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in sortedDataset" :key="data.id">
            <td>{{ data.id }}</td>
            <td>{{ data.src_ip }}</td>
            <td>{{ data.dst_ip }}</td>
            <td>{{ data.src_port }}</td>
            <td>{{ data.dst_port }}</td>
            <td>{{ data.protocol }}</td>
            <td>{{ data.application_name }}</td>
            <td :class="{'label-malicious': data.label === 'Benign', 'label-normal': data.label === 'Malware'}">{{ data.label }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="loadMore" v-if="hasMoreData" class="load-more-button">查看更多数据</button>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span @click="closeModal" class="close">&times;</span>
        <h2>添加流量数据</h2>
        <div class="modal-body">
          <input type="file" @change="handleFileUpload" accept=".pcap" />
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
      dataset: [],
      page: 1,
      hasMoreData: true,
      showModal: false,
      selectedFile: null,
      selectedFlag: ''
    };
  },
  computed: {
    sortedDataset() {
      return this.dataset.sort((a, b) => b.id - a.id);
    }
  },
  methods: {
    async fetchDataset(page = 1) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/get_dataset?page=${page}`);
        const newData = response.data;
        if (newData.length < 100) {
          this.hasMoreData = false;
        }
        if (page === 1) {
          this.dataset = newData;
        } else {
          this.dataset = this.dataset.concat(newData);
        }
        this.page = page;
        console.log('数据集获取成功:', newData);
      } catch (error) {
        console.error('数据集获取失败:', error);
      }
    },
    addData() {
      this.showModal = true;
    },
    deleteData() {
      console.log('删除数据');
    },
    searchData() {
      console.log('搜索数据');
    },
    handleFileUpload(event) {
      const selectedFile = event.target.files[0];
      if (!selectedFile) {
        return;
      }
      // 检查文件类型是否为 pcap
      if (selectedFile.type !== 'application/vnd.tcpdump.pcap' && !selectedFile.name.endsWith('.pcap')) {
        alert('请上传 pcap 文件');
        event.target.value = ''; // 清空文件输入
        return;
      }
      // 保存文件到 selectedFile 状态
      this.selectedFile = selectedFile;
      console.log('文件上传:', this.selectedFile);
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
        alert('文件上传成功');
        this.fetchDataset(1);  // 上传成功后重置并刷新数据集
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
    },
    handleScroll(event) {
      const bottom = event.target.scrollHeight - event.target.scrollTop === event.target.clientHeight;
      if (bottom && this.hasMoreData) {
        this.loadMore();
      }
    },
    loadMore() {
      this.fetchDataset(this.page + 1);
    }
  },
  mounted() {
    this.fetchDataset();
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

.load-more-button {
  margin-top: auto; /* 将按钮推到底部 */
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.load-more-button:hover {
  background-color: #0d8aed;
}
</style>
