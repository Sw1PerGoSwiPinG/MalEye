<template>
  <div class="container">
    <div class="steps">
      <div :class="['step', { completed: currentStep >= 1 }]" @click="setStep(1)">
        <div class="circle" 
          :style="{backgroundColor: isFinished(1) ? '#228200' : '#e6e9ef', 
                  color: isFinished(1) ? 'white' : 'black'}">1
        </div>
        <div class="label">步骤1-PCAP包处理</div>
      </div>
      <div :class="['step', { completed: currentStep >= 2 }]" @click="setStep(2)">
        <div class="circle" 
          :style="{backgroundColor: isFinished(2) ? '#228200' : '#e6e9ef', 
                  color: isFinished(2) ? 'white' : 'black'}">2
        </div>
        <div class="label">步骤2-MFR矩阵生成</div>
      </div>
      <div :class="['step', { completed: currentStep >= 3 }]" @click="setStep(3)">
        <div class="circle" 
          :style="{backgroundColor: isFinished(3) ? '#228200' : '#e6e9ef', 
                  color: isFinished(3) ? 'white' : 'black'}">3
        </div>
        <div class="label">步骤3-模型特征提取</div>
      </div>
      <div :class="['step', { completed: currentStep >= 4 }]" @click="setStep(4)">
        <div class="circle" 
          :style="{backgroundColor: isFinished(4) ? '#228200' : '#e6e9ef', 
                  color: isFinished(4) ? 'white' : 'black'}">4
        </div>
        <div class="label">步骤4-流量检测结果</div>
      </div>
    </div>

    <div v-if="start === false" style="display: flex; flex-direction: column; align-items: center;">
      <div class="upload-box">
        <VaFileUpload v-model="uploadPcap">
          <div class="upload-slot">
            <VaIcon name="cloud_upload" style="font-size: 80px; color: #a8abb2;"/>
            <span style="margin-top: 10%;">点击或将Pcap文件拖拽至此上传点</span>
          </div>
        </VaFileUpload>
      </div>
      <div style="width: 50%; display: flex; justify-content: space-between; margin-top: 5%;">
        <VaSelect v-model="slectedModel" label="🤖选择模型" :options="models" style="max-width: 350px"/>
        <VaButton color="info" class="start-button" @click="startDetecting">
          开始检测
        </VaButton>
      </div>
    </div>

    <div v-if="currentStep === 1" class="step-content">
      <h3>步骤1: 开始检测数据</h3>
      <table class="dataset-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>SourceIP</th>
            <th>DestIP</th>
            <th>SourcePort</th>
            <th>DestPort</th>
            <th>Protocol</th>
            <th>raw</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in trafficData" :key="data.id">
            <td>{{ data.id }}</td>
            <td>{{ data.src_ip }}</td>
            <td>{{ data.dst_ip }}</td>
            <td>{{ data.src_port }}</td>
            <td>{{ data.dst_port }}</td>
            <td>{{ data.protocol }}</td>
            <td>{{ data.raw }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="currentStep === 2" class="step-content">
      <h3>步骤2: 数据预处理</h3>
        <VaDataTable :items="mfrs" :columns="mfrsColumns">
          <template #cell(id)="{ value }">
            <VaChip size="small">{{ value }}</VaChip>
          </template>
          <template #cell(org)="{ rowData }">
            <div>
              <img :src="rowData.org" alt="Image" style="margin: 0px 10px">
            </div>
          </template>
          <template #cell(trans)="{ rowData }">
            <div>
              <img :src="rowData.trans" alt="Image" style="margin: 0px 10px">
            </div>
          </template>
        </VaDataTable>
    </div>

    <div v-if="currentStep === 3" class="step-content">
      <h3>步骤3: 特征提取</h3>
    </div>

    <div v-if="currentStep === 4" class="step-content">
      <h3>步骤4: 获取结果并展示</h3>
      <div class="result-confirmation">
        <div class="checkmark">✔</div>
        <div class="confirmation-text">测试正确</div>
        <div class="confirmation-subtext">该数据被判定为风险数据</div>
        <button @click="retest" class="retest-button">重新测试</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vuestic-ui'
const { init } = useToast();

export default {
  name: 'DectPage',
  data() {
    return {
      start: false,
      currentStep: 0,
      uploadPcap: [],
      slectedModel: "YaTC-FineTuned-ISCXVPN2016",
      models: ["YaTC-FineTuned-ISCXVPN2016", "YaTC-FineTuned-ISCXTor2016", "YaTC-FineTuned-CICIoT2022", "YaTC-FineTuned-USTC-TFC2016"],
      trafficData: {},
      finishedSteps: [],
      mfrs: [],
      mfrsColumns: [
        { key: "org", label: "原MFR" },
        { key: "trans", label: "处理后的MFR" },
      ],
    };
  },
  methods: {
    retest() {
      this.currentStep = 0;
    },
    setStep(step) {
      this.currentStep = step;
    },
    startDetecting() {
      this.start = true;
      this.currentStep = 1;
      this.readPcap();
    },
    async readPcap() {
      const formData = new FormData();
      formData.append('file', this.uploadPcap[0]);
      try {
        const response = await axios.post('http://localhost:5000/read_pcap', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const csvData = response.data;
        var index = 1;
        this.trafficData = csvData.split('\n').map(row => {
          const rowData = row.split(',');
          return {
            id: index++,
            src_ip: rowData[0],
            src_port: rowData[1],
            dst_ip: rowData[2],
            dst_port: rowData[3],
            protocol: rowData[4],
            raw: rowData[5] ? rowData[5].trim() : '', 
          }
        }).slice(1, -1);
      } catch (error) { console.error('解析pcap文件错误', error); }
      console.log('第一步：', this.trafficData);
      this.selectStep(1);
      this.getMFRImg();
    },
    async getMFRImg() {
      const formData = new FormData();
      formData.append('fileName', this.uploadPcap[0].name);
      try {
        const response = await axios.post('http://localhost:5000/gen_mfr', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.data.message == "success") {
          console.log('第二步：', response.data);
          const data = response.data.data;
          // 接收数据
          if (Array.isArray(data.mfrs_org) && Array.isArray(data.mfrs_trans)) {
            this.mfrs_org = data.mfrs_org.map((imageStr, index) => {
              return {
                id: Math.random(),
                src: 'data:image/png;base64,' + imageStr,
              };
            });
            this.mfrs_trans = data.mfrs_trans.map((imageStr, index) => {
              return {
                id: Math.random(),
                src: 'data:image/png;base64,' + imageStr,
              };
            });
          }
          this.updateMfrs();
        } else { return; }
      } catch (error) { console.error('第二步失败', error); }
      this.selectStep(2);
      this.detectByModel();
    },
    async detectByModel() {      
      // try {
      //   const response = await axios.get('http://localhost:5000/detect_upload');
      //   if (response.data.message == "success") {
      //     console.log('第三步：', response.data);
      //     this.model = response.data.data.model;
      //     this.optimizer = response.data.data.optimizer;
      //   } else { return; }
      // } catch (error) { console.error('第三步失败', error); }
      console.log("模型检测中")
      this.selectStep(3);
      this.showResult();
    },
    async showResult() {
      this.selectStep(4);
      init({ message: "检测完成 :)", color: 'success' });
    },
    updateMfrs() {
      for (let i = 0; i < this.mfrs_org.length; i++) {
        const newMfr = {
          id: i+1,
          org: this.mfrs_org[i].src,
          trans: this.mfrs_trans[i].src,
        };
        this.mfrs.push(newMfr);
      }
    },
    selectStep(index) {
      if (!this.finishedSteps.includes(index)) {
        this.finishedSteps.push(index);
      }
    },
    isFinished(index) {
      return this.finishedSteps.includes(index);
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.step {
  text-align: center;
  width: 23%;
  cursor: pointer;
}

.step .circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  font-size: x-large;
  font-weight: bold;
  margin-bottom: 8%;
}

.step.completed .circle {
  background-color: #154ec1;
}

.step .label {
  font-size: 16px;
  font-weight: bold;
}

.step-content {
  margin-bottom: 20px;
}

.upload-box {
  display: flex; 
  justify-content: center;
  height: 350px;
  padding: 1rem;
  margin-top: 2%;
}

.upload-slot {
  width: 750px;
  height: 100%; 
  padding-top: 15%; 
  border: 3px dashed #cccccc;
  text-align: center;
  background-color: white;

  display: flex;
  flex-direction: column;
}

.start-button {
  width: 30%;
  height: 30px;
  margin-top: 18px;
  padding: 0 0;
  background-color: #4caf50;
  color: white;
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

.label-malicious {
  color: red;
}

.result-confirmation {
  text-align: center;
}

.checkmark {
  font-size: 50px;
  color: green;
  margin-bottom: 10px;
}

.confirmation-text {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.confirmation-subtext {
  font-size: 16px;
  color: #777;
  margin-bottom: 20px;
}

.retest-button {
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
