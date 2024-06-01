<template>
  <div class="container">
    <div class="top-section">
      <div class="form-container">
        <div style="display: flex;">
          <VaIcon name="display_settings" style="font-size: 30px; margin-right: 2%; color: #158de3"/>
          <div style="font-size: x-large; font-weight: bold; margin-bottom: 20px">超参数设置</div>
        </div>
        <form @submit.prevent="submitForm">
          <!-- 表单输入项 -->
          <div class="form-group" v-for="input in formInputs" :key="input.label">
            <label :for="input.model">{{ input.label }}</label>
            <input v-model="form[input.model]" :type="input.type" :step="input.step || '1'" />
          </div>
          <div class="form-group">
            <label>请选择MFR数据集</label>
            <select v-model="form.dataset">
              <option value="UbuntuTraffic">UbuntuTraffic</option>
              <option value="ISCXVPN2016">ISCXVPN2016</option>
              <option value="ISCXTor2016">ISCXTor2016</option>
              <option value="USTC-TFC2016">USTC-TFC2016</option>
              <option value="CICIoT2022">CICIoT2022</option>
            </select>
          </div>
          <div class="gauge-buttons">
            <VaButton color="info" class="start-button" @click="startTraining" style="height: 30px; padding: 0 0;">
              训练
            </VaButton>
            <VaButton color="danger" class="start-button" @click="stopTraining" style="height: 30px; padding: 0 0;">
              停止
            </VaButton>
            <VaButton color="warning" class="stop-button" @click="resetForm" style="height: 30px; padding: 0 0;">
              重置
            </VaButton>
          </div>
        </form>
      </div>
      <div class="gauge-container">
        <iframe class="pdf" src="../../MAE.pdf"></iframe>
        <!-- <MAEpdf></MAEpdf> -->
      </div>
      <div class="info_container">
        <VaDataTable :items="argsList" :columns="columns" >
          <template #cell(var)="{ value }">
            <strong>{{ value }}</strong>
          </template>
          <template #cell(info)="{ row }">
            <VaButton icon="info" preset="plainOpacity" @click="row.toggleRowDetails()" ></VaButton>
          </template>
          <template #expandableRow="{ rowData }">
              <div class="tip-bar" >{{ rowData.description }}</div>
          </template>
        </VaDataTable>
      </div>
    </div>
    <div class="bottom-section">
      <div class="training-steps-container">
        <div style="display: flex;">
          <VaIcon name="account_tree" style="font-size: 30px; margin-right: 2%; color: #158de3"/>
          <div style="font-size: x-large; font-weight: bold; margin-bottom: 20px">训练流程</div>
        </div>
        <ul>
          <li class="step" v-for="(step, index) in trainingSteps" :key="index" @click="selectStep(step, index)">
            {{ step.name }}
          </li>
        </ul>
      </div>
      <div class="chart-display-container">
        <div style="font-size: large; font-weight: bold;">{{ selectedStep.name }}</div>
        <div :id="selectedStep.chartId" class="chart" v-if="selectedStep.chartId"></div>
        <div v-else>选择一个流程以显示详细信息。</div>
        <div v-if="curStep == 1" style="display: flex; flex-direction: column;">
          <div class="mfr-container">
            <div v-for="mfr in mfrs_org" :key="mfr.id">
              <img :src="mfr.src" alt="Image" style="margin-right: 10px">
            </div>
          </div>
          <div v-if="mfrs_org.length != 0" class="transform">👇经过Torchvision.Transform过程👇</div>
          <div class="mfr-container">
            <div v-for="mfr in mfrs_trans" :key="mfr.id">
              <img :src="mfr.src" alt="Image" style="margin-right: 10px">
            </div>
          </div>
        </div>
        <div v-else-if="curStep == 2">
          <pre>{{ model }}</pre>
          <pre>{{ optimizer }}</pre>
        </div>
        <div v-else-if="curStep == 3">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

import MAEpdf from  '../../components/MAEpdf.vue'

export default {
  components: { 
    MAEpdf,
  },
  name: 'ModelPage',
  data() {
    const argsList = [
    {
        "var": "batch_size",
        "name": "批处理大小",
        "type": "int",
        "default": 128,
        "description": "每个GPU的批处理大小",
    },
    {
        "var": "steps",
        "name": "步骤数",
        "type": "int",
        "default": 150000,
        "description": "预训练的总步骤数，每一步代表一次编码解码过程"
    },
    {
        "var": "model",
        "name": "模型名称",
        "type": "str",
        "default": "MAE_YaTC",
        "description": "要训练的模型名称，默认为掩码自编码器"
    },
    {
        "var": "input_size",
        "name": "输入大小",
        "type": "int",
        "default": "40*40",
        "description": "输入的MFR图像样本的大小"
    },
    {
        "var": "mask_ratio",
        "name": "掩码比例",
        "type": "float",
        "default": 0.90,
        "description": "掩码比例，预训练时对于样本的遮挡比例，一般取较大的值"
    },
    {
        "var": "norm_pix_loss",
        "name": "归一化像素损失",
        "type": "bool",
        "default": false,
        "description": "使用（每个补丁的）归一化像素作为计算损失的目标"
    },
    {
        "var": "weight_decay",
        "name": "权重衰减",
        "type": "float",
        "default": 0.05,
        "description": "权重衰减，用于防止模型过拟合（默认：0.05）"
    },
    {
        "var": "blr",
        "name": "基础学习率",
        "type": "float",
        "default": 1e-3,
        "description": "基础学习率：绝对学习率 = 基础学习率 * 总批处理大小 / 256"
    },
    {
        "var": "warmup_epochs",
        "name": "预热轮数",
        "type": "int",
        "default": 25,
        "description": "学习率预热阶段所需要的轮数"
    },
    {
        "var": "data_path",
        "name": "数据集路径",
        "type": "str",
        "default": "ISCXVPN2016",
        "description": "数据集存放的路径"
    },
    {
        "var": "device",
        "name": "设备",
        "type": "str",
        "default": "cuda",
        "description": "训练/测试使用的设备，默认使用GPU加速"
    },
    {
        "var": "seed",
        "name": "随机种子",
        "type": "int",
        "default": 0,
        "description": "随机种子，用于初始化模型参数"
    },
    {
        "var": "num_workers",
        "name": "工作线程数",
        "type": "int",
        "default": 10,
        "description": "工作线程数"
    },
    {
        "var": "pin_mem",
        "name": "固定内存",
        "type": "bool",
        "default": true,
        "description": "在DataLoader中固定CPU内存以更有效地传输到GPU（有时）"
    },
    {
        "var": "dist_on_itp",
        "name": "在ITP上分布",
        "type": "bool",
        "default": false,
        "description": "是否在在ITP上进行分布式训练"
    },
    {
        "var": "dist_url",
        "name": "分布式URL",
        "type": "str",
        "default": "env://",
        "description": "设置分布式训练的URL"
    }
    ];
    const columns = [
      { key: "var", label: "参数" },
      { key: "name", label: "名称" },
      { key: "type", label: "类型" },
      { key: "default", label: "默认值" },
      { key: "info", label: "含义"},
    ];
    return {
      form: {
        epochs: 100,
        warmupEpochs: 0,
        batchSize: 64,
        learningRate: 0.001,
        maskRatio: 0.9,
        weightDecay: 0.05,
        seed: 0,
        dataset: "UbuntuTraffic"
      },
      formInputs: [
        { label: '训练轮数', model: 'epochs', type: 'number' },
        { label: '预热轮数', model: 'warmupEpochs', type: 'number' },
        { label: 'Batch大小', model: 'batchSize', type: 'number' },
        { label: '基础学习率', model: 'learningRate', type: 'number', step: '0.001' },
        { label: '掩码比例', model: 'maskRatio', type: 'number', step: '0.01', max: '1'},
        { label: '权重衰减系数', model: 'weightDecay', type: 'number', step: '0.01'},
        { label: '随机数种子', model: 'seed', type: 'number' },
      ],
      trainingSteps: [
        { name: 'Step 1: 数据预处理', chartId: 'preprocessingChart' },
        { name: 'Step 2: 模型及优化器', chartId: 'trainingChart' },
        { name: 'Step 3: 模型训练', chartId: 'evaluationChart' },
        { name: 'Step 4: 训练结果', chartId: 'tuningChart' },
      ],
      selectedStep: {},
      curStep: 0,
      argsList,
      columns,
      // 下面数据是展示训练过程时候用的
      mfrs_org: [],
      mfrs_trans: [],
      model: "",
      optimizer: "",
      trainLog: Object(),
    };
  },
  methods: {
    startTraining() {
      this.stepOne(); 
    },
    stopTraining() {
      console.log('停止训练');
      // 触发停止训练的逻辑
    },
    submitForm() {
      console.log('提交表单', this.form);
      // 处理表单提交
    },
    async stepOne() {
      try {
        const response = await axios.post('http://localhost:5000/pre-train-step1', this.form);
        if (response.data.message == "success") {
          console.log('第一步：', response.data);
          const data = response.data.data
          if (Array.isArray(data.mfrs_org) && Array.isArray(data.mfrs_trans)) {
            console.log("here")
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
          this.curStep = 1;
          this.selectStep(this.trainingSteps[0]);
          this.stepTwo();
        } else {
          alert(`在第一步时训练出错`);
          return;
        }
      } catch (error) { console.error('第一步失败', error); }
    },
    async stepTwo() {      
      try {
        const response = await axios.get('http://localhost:5000/pre-train-step2');
        if (response.data.message == "success") {
          console.log('第二步：', response.data);
          this.model = response.data.data.model;
          this.optimizer = response.data.data.optimizer;
          this.curStep = 2;
          this.selectStep(this.trainingSteps[1]);
          // this.stepThree();
        } else {
          alert(`在第二步时训练出错`);
          return;
        }
      } catch (error) { console.error('第二步失败', error); }
    },
    async stepThree() {      
      try {
        const response = await axios.get('http://localhost:5000/pre-train-step3');
        if (response.data.message == "success") {
          console.log('第三步：', response.data);
        } else {
          alert(`在第三步时训练出错`);
          return;
        }
      } catch (error) { console.error('第三步失败', error); }
      this.curStep = 3;
      this.selectStep(this.trainingSteps[2]);
      alert("完成整个训练过程")
    },
    // stepFour() {

    // },
    resetForm() {
      this.form = {
        epochs: 100,
        warmupEpochs: 0,
        batchSize: 64,
        learningRate: 0.001,
        maskRatio: 0.9,
        weightDecay: 0.05,
        seed: 0,
        dataset: "UbuntuTraffic"
      };
    },
    selectStep(step, index) {
      this.selectedStep = step;
      this.initChart(step.chartId);
      this.curStep = index + 1;
    },
    initChart(chartId) {
      if (!chartId) return; // 如果没有chartId则直接返回
      const chartDom = document.getElementById(chartId);
      if (!chartDom) return; // 如果DOM元素不存在也返回
      const myChart = echarts.init(chartDom);
      const option = {
        // 根据图表类型设置不同的option配置
      };
      myChart.setOption(option);
    },
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.top-section {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  max-height: 732px;
}

.gauge-container {
  width: 36%;
  background-color: #f0f4f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: scroll;
}

.gauge-container::-webkit-scrollbar {
  display: none;  /* Safari and Chrome */
}

.gauge-chart {
  width: 100%;
  height: 85%;
}

.gauge-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.gauge-buttons button {
  width: 45%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.start-button {
  background-color: #4caf50;
  color: white;
}

.stop-button {
  background-color: #f44336;
  color: white;
}

.form-container {
  width: 20%;
  background-color: #f0f4f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
}

.pdf {
  width: 450px;
  height: 900px;
  margin-top: -90px;
  margin-right: -10px;
  border: none;
  overflow: hidden;
}

.pdf::-webkit-scrollbar {
  display: none;
}

.info_container {
  width: 40%;
  background-color: #f0f4f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.submit-button {
  background-color: #2196f3;
  color: white;
}

.reset-button {
  background-color: #ff9800;
  color: white;
}

.bottom-section {
  display: flex;
  justify-content: space-around;
}

/* .step {
  margin-bottom: 25px;
} */

.training-steps-container {
  width: 32%;
}
.chart-display-container {
  width: 65%;
}

.training-steps-container,
.chart-display-container {
  background-color: #f0f4f8; /* 浅蓝色背景 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.training-steps-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.training-steps-container li {
  cursor: pointer;
  padding: 10px;
  border-radius: 20px;
  margin-bottom: 10px;
  background: linear-gradient(145deg, #e6e9ef, #ffffff);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.training-steps-container li:hover {
  background: #d2e1ec; /* 鼠标悬停时的背景色 */
  color: #333;
}

.chart {
  width: 100%;
  height: 300px; /* 根据需要调整高度 */
}

.mfr-container {
  display: flex;
}

.transform {
  font-size: large;
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  color: #333; /* 深色文字 */
}

.va-data-table__table-tr--expanded td {
  background: var(--va-background-border);
}

.va-data-table__table-expanded-content td {
  background-color: var(--va-background-element);
}

.tip-bar {
  text-align: center; 
  padding: 10px 20px; 
  background-color: white; 
  border-radius: 20px;
}

pre {
  white-space: pre-wrap;
  padding-left: 20%;
}
</style>
