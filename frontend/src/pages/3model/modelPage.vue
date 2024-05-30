<template>
  <div class="container">
    <div class="top-section">
      <div class="gauge-container">
        <div id="gaugeChart" class="gauge-chart"></div>
        <div class="gauge-buttons">
          <button @click="startTraining" class="start-button">开始训练</button>
          <button @click="stopTraining" class="stop-button">停止训练</button>
        </div>
      </div>
      <div class="form-container">
        <form @submit.prevent="submitForm">
          <!-- 表单输入项 -->
          <div class="form-group" v-for="input in formInputs" :key="input.label">
            <label :for="input.model">{{ input.label }}</label>
            <input v-model="form[input.model]" :type="input.type" :step="input.step || '1'" />
          </div>
          <div class="form-group">
            <label>graphSage</label>
            <select v-model="form.graphSage">
              <option value="mean">mean</option>
              <option value="max">max</option>
            </select>
          </div>
          <div class="form-group">
            <label>启用DGL</label>
            <input v-model="form.enableDGL" type="checkbox" />
          </div>
          <div class="form-buttons">
            <button type="submit" class="submit-button">提交</button>
            <button type="reset" @click="resetForm" class="reset-button">重置</button>
          </div>
        </form>
      </div>
    </div>
    <div class="bottom-section">
      <div class="training-steps-container">
        <h2>训练流程</h2>
        <ul>
          <li v-for="(step, index) in trainingSteps" :key="index" @click="selectStep(step)">
            {{ step.name }}
          </li>
        </ul>
      </div>
      <div class="chart-display-container">
        <h2>{{ selectedStep.name }}</h2>
        <div :id="selectedStep.chartId" class="chart" v-if="selectedStep.chartId"></div>
        <p v-else>选择一个流程以显示详细信息。</p>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'ModelPage',
  data() {
    return {
      form: {
        epochs: 100,
        batchSize: 512,
        learningRate: 0.01,
        firstOrder: 10,
        secondOrder: 5,
        thirdOrder: 0,
        graphSage: 'mean',
        enableDGL: false
      },
      formInputs: [
        { label: '训练轮数', model: 'epochs', type: 'number' },
        { label: 'Batch数量', model: 'batchSize', type: 'number' },
        { label: '学习率', model: 'learningRate', type: 'number', step: '0.01' },
        { label: '一阶邻居数量', model: 'firstOrder', type: 'number' },
        { label: '二阶邻居数量', model: 'secondOrder', type: 'number' },
        { label: '三阶邻居数量', model: 'thirdOrder', type: 'number' }
      ],
      trainingSteps: [
        { name: 'Step 1: 数据预处理', chartId: 'preprocessingChart' },
        { name: 'Step 2: 模型训练', chartId: 'trainingChart' },
        { name: 'Step 3: 模型评估', chartId: 'evaluationChart' },
        { name: 'Step 4: 参数调优', chartId: 'tuningChart' },
        { name: 'Step 5: 结果验证', chartId: 'validationChart' }
      ],
      selectedStep: {}
    };
  },
  mounted() {
    this.initGaugeChart();
  },
  methods: {
    initGaugeChart() {
      var chartDom = document.getElementById('gaugeChart');
      var myChart = echarts.init(chartDom);
      var option = {
        series: [
          {
            type: 'gauge',
            progress: {
              show: true,
              width: 18
            },
            axisLine: {
              lineStyle: {
                width: 18
              }
            },
            pointer: {
              itemStyle: {
                color: 'inherit'
              }
            },
            title: {
              offsetCenter: [0, '70%']
            },
            detail: {
              valueAnimation: true,
              formatter: '{value}%',
              offsetCenter: [0, '90%']
            },
            data: [
              {
                value: 0,
                name: '训练进度'
              }
            ]
          }
        ]
      };
      myChart.setOption(option);
    },
    startTraining() {
      console.log('开始训练');
      // 触发开始训练的逻辑
    },
    stopTraining() {
      console.log('停止训练');
      // 触发停止训练的逻辑
    },
    submitForm() {
      console.log('提交表单', this.form);
      // 处理表单提交
    },
    resetForm() {
      this.form = {
        epochs: 100,
        batchSize: 512,
        learningRate: 0.01,
        firstOrder: 10,
        secondOrder: 5,
        thirdOrder: 0,
        graphSage: 'mean',
        enableDGL: false
      };
    },
    selectStep(step) {
      this.selectedStep = step;
      this.initChart(step.chartId);
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
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.top-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.gauge-container {
  width: 48%;
  background-color: #f0f4f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.gauge-chart {
  width: 100%;
  height: 300px;
}

.gauge-buttons {
  display: flex;
  justify-content: space-between;
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
  width: 48%;
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
  justify-content: space-between;
}

.training-steps-container,
.chart-display-container {
  width: 48%;
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

h2 {
  margin-bottom: 20px;
  color: #333; /* 深色文字 */
}
</style>
