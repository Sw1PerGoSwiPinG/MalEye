<template>
  <div class="container">
    <div class="steps">
      <div :class="['step', { completed: currentStep >= 1 }]" @click="setStep(1)">
        <div class="circle">1</div>
        <div class="label">步骤1<br>开始检测数据</div>
      </div>
      <div :class="['step', { completed: currentStep >= 2 }]" @click="setStep(2)">
        <div class="circle">2</div>
        <div class="label">步骤2<br>数据预处理</div>
      </div>
      <div :class="['step', { completed: currentStep >= 3 }]" @click="setStep(3)">
        <div class="circle">3</div>
        <div class="label">步骤3<br>特征提取</div>
      </div>
      <div :class="['step', { completed: currentStep >= 4 }]" @click="setStep(4)">
        <div class="circle">4</div>
        <div class="label">步骤4<br>获取结果并展示</div>
      </div>
    </div>

    <div v-if="currentStep === 1" class="step-content">
      <h3>步骤1: 开始检测数据</h3>
      <p>请上传并开始检测数据...</p>
    </div>

    <div v-if="currentStep === 2" class="step-content">
      <h3>步骤2: 数据预处理</h3>
      <p>正在进行数据预处理...</p>
    </div>

    <div v-if="currentStep === 3" class="step-content">
      <h3>步骤3: 特征提取</h3>
      <p>正在提取数据特征...</p>
    </div>

    <div v-if="currentStep === 4" class="step-content">
      <h3>步骤4: 获取结果并展示</h3>
      <div class="result-data">
        <h3>测试数据</h3>
        <table>
          <thead>
            <tr>
              <th>名称</th>
              <th>label</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>2022-11-08_11-11-15.pcap_TCP_10-128-214-124_30107_120-253-253-169_443</td>
              <td class="label-malicious">malicious</td>
            </tr>
          </tbody>
        </table>
      </div>
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
export default {
  name: 'DectPage',
  data() {
    return {
      currentStep: 4
    };
  },
  methods: {
    retest() {
      console.log('重新测试');
      this.currentStep = 1;
    },
    setStep(step) {
      this.currentStep = step;
    }
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
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #ddd;
  color: white;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.step.completed .circle {
  background-color: #4caf50;
}

.step .label {
  font-size: 14px;
}

.step-content {
  margin-bottom: 20px;
}

.result-data {
  margin-bottom: 20px;
}

.result-data h3 {
  margin-bottom: 10px;
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
