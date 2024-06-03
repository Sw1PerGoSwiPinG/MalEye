<template>
  <div class="container">
    <div class="header">
      <button @click="showGroupModal = true" class="add-button">新增组</button>
      <button @click="deleteData" class="delete-button">删除</button>
      <input v-model="search" type="text" placeholder="Search" class="search-input" />
      <select v-model="filter" class="filter-select">
        <option value="">所有类别</option>
        <option value="malicious">恶意流量</option>
        <option value="normal">正常流量</option>
      </select>
      <button @click="searchData" class="search-button">搜索</button>
    </div>
    <div v-for="group in filteredDataset" :key="group.name" class="group-container">
      <div class="group-header">
        <span class="group-name">名称： {{ group.name }}</span>
        <span class="group-description">描述： {{ group.description }}</span>
      </div>
      <div class="category-container" v-for="category in group.categories" :key="category">
        <span class="category-name">{{ category }}</span>
        <div class="images-container">
          <div v-for="image in group.images[category]" :key="image" class="image-box">
            <img :src="image" class="image-feature" />
          </div>
        </div>
        <button @click="selectCategory(group.name, category)" class="upload-button">上传</button>
      </div>
    </div>

    <!-- 新增组的模态框 -->
    <div v-if="showGroupModal" class="modal">
      <div class="modal-content">
        <span @click="closeGroupModal" class="close">&times;</span>
        <h2>添加组和分类</h2>
        <div class="modal-body">
          <input v-model="newGroupName" type="text" placeholder="组名" class="input-field" />
          <input v-model="newGroupDescription" type="text" placeholder="描述" class="input-field" />
          <div v-for="(category, index) in newCategories" :key="index" class="input-group">
            <input v-model="newCategories[index]" type="text" placeholder="分类名称" class="input-field" />
            <button @click="removeCategory(index)" class="remove-button">删除</button>
          </div>
          <button @click="addCategory" class="add-button">添加分类</button>
          <button @click="createGroup" class="create-button">创建组</button>
        </div>
      </div>
    </div>

    <!-- 上传文件的模态框 -->
    <div v-if="showUploadModal" class="modal">
      <div class="modal-content">
        <span @click="closeUploadModal" class="close">&times;</span>
        <h2>上传流量数据</h2>
        <div class="modal-body">
          <input type="file" @change="handleFileUpload" />
          <button @click="uploadFile" class="upload-button">上传</button>
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
      showGroupModal: false,
      newGroupName: '',
      newGroupDescription: '', // 添加描述字段
      newCategories: [''],
      showUploadModal: false,
      selectedFile: null,
      selectedGroup: '',
      selectedCategory: '',
    };
  },
  computed: {
    filteredDataset() {
      let result = this.dataset;
      if (this.search) {
        result = result.filter(group => group.name.includes(this.search) || group.categories.some(category => category.includes(this.search)));
      }
      if (this.filter) {
        result = result.filter(group => group.label === this.filter);
      }
      return result;
    }
  },
  methods: {
    addCategory() {
      this.newCategories.push('');
    },
    removeCategory(index) {
      this.newCategories.splice(index, 1);
    },
    async createGroup() {
      if (!this.newGroupName || this.newCategories.length === 0 || this.newCategories.some(category => !category)) {
        alert('请填写完整的组名和分类');
        return;
      }
      const newGroup = {
        name: this.newGroupName,
        description: this.newGroupDescription, // 添加描述
        categories: [...this.newCategories],
        images: {} // Initialize images object
      };
      try {
        const response = await axios.post('http://127.0.0.1:5000/create_group', newGroup);
        if (response.status === 200) {
          this.dataset.unshift(newGroup); // 将新创建的组插入到数组的最前面
          alert('组创建成功');
          this.closeGroupModal();
        }
      } catch (error) {
        console.error('创建组失败:', error);
        alert('创建组失败');
      }
    },
    selectCategory(group, category) {
      this.selectedGroup = group;
      this.selectedCategory = category;
      this.showUploadModal = true;
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert('请先选择一个文件');
        return;
      }
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('group', this.selectedGroup);
      formData.append('category', this.selectedCategory);

      try {
        const response = await axios.post('http://127.0.0.1:5000/get_image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.status === 200) {
          alert('文件上传成功');
          this.updateAllImages(response.data.images);
          this.closeUploadModal();
        }
      } catch (error) {
        console.error('文件上传失败:', error);
        alert('文件上传失败');
      }
    },
    updateAllImages(allImages) {
      for (const groupName in allImages) {
        let group = this.dataset.find(g => g.name === groupName);
        if (!group) {
          group = {
            name: groupName,
            categories: [],
            images: {}
          };
          this.dataset.unshift(group); // 将新的组插入到数组的最前面
        }
        for (const category in allImages[groupName]) {
          if (!group.categories.includes(category)) {
            group.categories.push(category);
          }
          if (!group.images) {
            group.images = {};
          }
          group.images[category] = allImages[groupName][category].map(img => `data:image/png;base64,${img}`);
        }
      }
    },
    closeGroupModal() {
      this.showGroupModal = false;
      this.newGroupName = '';
      this.newGroupDescription = ''; // 重置描述字段
      this.newCategories = [''];
    },
    closeUploadModal() {
      this.showUploadModal = false;
      this.selectedFile = null;
      this.selectedGroup = '';
      this.selectedCategory = '';
    },
    searchData() {
      // Implement search logic if needed
    },
    deleteData() {
      console.log('删除数据');
      // Implement delete logic if needed
    },
    async fetchAllImages() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_all_images');
        if (response.status === 200) {
          this.updateAllImages(response.data.images);
        }
      } catch (error) {
        console.error('获取所有图片失败:', error);
        alert('获取所有图片失败');
      }
    }
  },
  async mounted() {
    await this.fetchAllImages(); // Fetch initial data here
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
.delete-button,
.upload-button {
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

.upload-button {
  background-color: #2196f3;
}

.search-input,
.filter-select,
.search-button {
  margin-right: 10px;
}

.search-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
}

.filter-select {
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

.group-container {
  margin-bottom: 20px;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}

.group-header {
  display: flex;
  justify-content: space-between;
  font-size: 16px;
  margin-bottom: 10px;
}

.category-container {
  margin-bottom: 10px;
  background-color: #e3f2fd;
  padding: 10px;
  border-radius: 5px;
}

.category-name {
  display: block;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

.images-container {
  display: flex;
  flex-wrap: wrap;
}

.image-box {
  margin: 5px;
  padding: 5px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.image-feature {
  width: 50px;
  height: 50px;
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

.input-field {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: calc(100% - 20px);
}

.input-group {
  display: flex;
  align-items: center;
}

.remove-button {
  margin-left: 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.remove-button:hover {
  background-color: #d32f2f;
}

.image-container {
  display: inline-block;
  margin: 5px;
}
</style>
