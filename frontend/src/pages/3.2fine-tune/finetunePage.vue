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
            <label :for="input.model" style="font-weight: bold; color: #154ec1;">{{ input.label }}</label>
            <input v-model="form[input.model]" :type="input.type" :step="input.step || '1'" />
          </div>
          <div class="form-group">
            <label style="font-weight: bold; color: #154ec1;">请选择MFR数据集</label>
            <select v-model="form.dataset">
              <option value="UbuntuTraffic">UbuntuTraffic</option>
              <option value="ISCXVPN2016">ISCXVPN2016</option>
              <option value="ISCXTor2016">ISCXTor2016</option>
              <option value="USTC-TFC2016">USTC-TFC2016</option>
              <option value="CICIoT2022">CICIoT2022</option>
            </select>
          </div>
        </form>
      </div>
      <div class="gauge-container">
        <!-- <iframe class="pdf" src="../../MAE.pdf"></iframe> -->
        <div id="gaugeChart" class="gauge-chart"></div>
        <div class="gauge-buttons">
            <VaButton color="info" class="start-button" @click="startTraining">
              开始微调
            </VaButton>
            <VaButton color="danger" class="start-button" @click="stopTraining">
              停止微调
            </VaButton>
            <VaButton color="warning" class="stop-button" @click="resetForm">
              重置参数
            </VaButton>
          </div>
      </div>
      <div class="info-container">
        <VaDataTable :items="argsHelp" :columns="columns" >
          <template #cell(var)="{ value }">
            <strong style="color: #154ec1;">{{ value }}</strong>
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
          <div style="font-size: x-large; font-weight: bold; margin-bottom: 10%">训练流程</div>
        </div>
        <ul>
          <li class="step" v-for="(step, index) in trainingSteps" :key="index" @click="showStep(step, index)" 
              :style="{backgroundColor: isFinished(index) ? '#228200' : '#e6e9ef', color: isFinished(index) ? 'white' : 'black'}">
            <VaIcon name="check_circle" :style="{marginRight: '5%', color: isFinished(index) ? 'white' : 'black'}"/>
            {{ step.name }}
          </li>
        </ul>
      </div>
      <div class="chart-display-container">
        <div style="font-size: large; font-weight: bold; margin-bottom: 5%;">{{ curStepName }}</div>
        <h2 v-if="curStep == -1" style="text-align: center; margin-top: 10%; font-size: x-large; font-weight: bold;">
          点击训练按钮，开始一次训练🤗
        </h2>
        <div v-else-if="curStep == 0 && start" style="text-align: center">
          <div class="argsTable">
            <VaDataTable :items="argsList" :columns="columnsToPost" >
              <template #header(var)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
              <template #header(name)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
              <template #header(type)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
              <template #header(value)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
              <template #header(default)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
              <template #header(description)="{ label }">
                <VaChip size="small">{{ label }}</VaChip>
              </template>
            </VaDataTable>
          </div>
        </div>
        <div v-else-if="curStep == 1 && start">
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
            <template #cell(feature)="{ rowData }">
              <div style="white-space: initial; overflow-x: auto;">{{ rowData.feature }}</div>
            </template>
          </VaDataTable>
        </div>
        <div v-else-if="curStep == 2 && start">
          <ModelTree></ModelTree>
          <pre>{{ model }}</pre>
          <pre>{{ optimizer }}</pre>
        </div>
        <div v-else-if="curStep == 3 && start">
        </div>
        <div v-else-if="curStep == 4 && start">
          <!-- <div :id="selectedStep[curStep].chartId" class="chart" v-if="selectedStep.chartId"></div> -->
          <Loss></Loss>
          <Lr></Lr>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import Loss from '../../components/Loss.vue';
import Lr from '../../components/Lr.vue';
import ModelTree from '../../components/ModelTree.vue';

export default {
  components: { 
    ModelTree, Loss, Lr
  },
  name: 'ModelPage',
  data() {
    const argsHelp = [
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
    const argsList = [
      {
        "var": "steps",
        "name": "步骤数",
        "type": "int",
        "value": 0,
        "default": 100,
        "description": "预训练的总步骤数，每一步代表一次编码解码过程"
      },
      {
          "var": "warmup",
          "name": "预热轮数",
          "type": "int",
          "value": 0,
          "default": 25,
          "description": "学习率预热阶段所需要的轮数"
      },
      {
        "var": "batch_size",
        "name": "批处理大小",
        "type": "int",
        "value": 0,
        "default": 128,
        "description": "每个GPU的批处理大小",
      },
      {
          "var": "blr",
          "name": "基础学习率",
          "type": "float",
          "value": 0.0,
          "default": 1e-3,
          "description": "绝对学习率 = 基础学习率 * 总批处理大小 / 256"
      },
      {
          "var": "mask_ratio",
          "name": "掩码比例",
          "type": "float",
          "value": 0.0,
          "default": 0.90,
          "description": "掩码比例，即对于样本的遮挡比例，一般取较大的值"
      },
      {
          "var": "weight_decay",
          "name": "权重衰减",
          "type": "float",
          "value": 0.0,
          "default": 0.05,
          "description": "权重衰减，用于防止模型过拟合（默认：0.05）"
      },
      {
          "var": "seed",
          "name": "随机种子",
          "type": "int",
          "value": 0,
          "default": 0,
          "description": "随机种子，用于初始化模型参数"
      },
      {
          "var": "data_path",
          "name": "数据集路径",
          "type": "str",
          "value": "",
          "default": "ISCXVPN2016",
          "description": "数据集，默认为ISCXVPN2016数据集"
      }
    ];
    const mfrs = [];
    const columns = [
      { key: "var", label: "参数" },
      { key: "name", label: "名称" },
      { key: "type", label: "类型" },
      { key: "default", label: "默认值" },
      { key: "info", label: "含义"},
    ];
    const columnsToPost = [
      { key: "var", label: "参数" },
      { key: "name", label: "名称" },
      { key: "type", label: "类型" },
      { key: "value", label: "实际值" },
      { key: "default", label: "默认值" },
      { key: "description", label: "含义"},
    ];
    const mfrsColumns = [
      { key: "id", label: "ID" },
      { key: "label", label: "标签" },
      { key: "org", label: "原MFR" },
      { key: "trans", label: "处理后的MFR" },
      { key: "feature", label: "张量特征" },
    ]
    return {
      form: {
        batch_size: 64,
        epochs: 10,
        accum_iter: 1,
        model: "",
        input_size: "",
        drop_path: 0.1,
        clip_grad: null,
        weight_decay: 0.0,
        lr: 0.001,
        blr: 0.001,
        layer_decay: 0.1,
        min_lr: 0.0,
        warmup_epochs: 0,
        color_jitter: 0.4,
        aa: "",
        smoothing: 0.1,
        reprob: 0.0,
        remode: "",
        recount: 1,
        resplit: false,
        mixup: 0.0,
        cutmix: 0.0,
        cutmix_minmax: null,
        mixup_prob: 1.0,
        mixup_switch_prob: 0.5,
        mixup_mode: "batch",
        finetune: "",
        data_path: "",
        nb_classes: 0,
        output_dir: "",
        log_dir: "",
        device: "",
        seed: 0,
        resume: "",
        start_epoch: 0,
        eval: false,
        dist_eval: false,
        num_workers: 4,
        pin_mem: true,
        world_size: 1,
        local_rank: 0,
        dist_on_itp: false,
        dist_url: ""
      },
      formInputs: [
        { label: '微调轮数', model: 'epochs', type: 'number' },
        { label: 'Batch大小', model: 'batch_size', type: 'number' },
        { label: '梯度累积步数', model: 'accum_iter', type: 'number' },
        { label: '输入图像的尺寸', model: 'input_size', type: 'text' },
        { label: 'Dropout路径的比例', model: 'drop_path', type: 'number', step: '0.01' },
        { label: '剪裁梯度的范数', model: 'clip_grad', type: 'number', step: '0.01' },
        { label: '权重衰减系数', model: 'weight_decay', type: 'number', step: '0.01' },
        { label: '学习率', model: 'lr', type: 'number', step: '0.001' },
        { label: '学习率设置', model: 'blr', type: 'number', step: '0.001' },
        { label: '来自ELECTRA/BEiT的逐层学习率衰减', model: 'layer_decay', type: 'number', step: '0.01' },
        { label: '循环调度器达到0时的最低学习率', model: 'min_lr', type: 'number', step: '0.01' },
        { label: '学习率预热的轮数', model: 'warmup_epochs', type: 'number' },
        { label: '颜色抖动因子', model: 'color_jitter', type: 'number', step: '0.01' },
        { label: '使用的AutoAugment策略', model: 'aa', type: 'text' },
        { label: '标签平滑', model: 'smoothing', type: 'number', step: '0.01' },
        { label: '随机擦除概率', model: 'reprob', type: 'number', step: '0.01' },
        { label: '随机擦除模式', model: 'remode', type: 'text' },
        { label: '随机擦除计数', model: 'recount', type: 'number' },
        { label: '是否对第一个增强数据集进行随机擦除', model: 'resplit', type: 'checkbox' },
        { label: 'mixup的系数', model: 'mixup', type: 'number', step: '0.01' },
        { label: 'cutmix的系数', model: 'cutmix', type: 'number', step: '0.01' },
        { label: 'cutmix的最小/最大比例', model: 'cutmix_minmax', type: 'text' },
        { label: '在启用mixup或cutmix时执行mixup或cutmix的概率', model: 'mixup_prob', type: 'number', step: '0.01' },
        { label: '在同时启用mixup和cutmix时切换到cutmix的概率', model: 'mixup_switch_prob', type: 'number', step: '0.01' },
        { label: '如何应用mixup/cutmix参数', model: 'mixup_mode', type: 'text' },
        { label: '从检查点路径进行微调', model: 'finetune', type: 'text' },
        { label: '数据集路径', model: 'data_path', type: 'text' },
        { label: '分类类型的数量', model: 'nb_classes', type: 'number' },
        { label: '保存模型和结果的路径', model: 'output_dir', type: 'text' },
        { label: '用于训练/测试的设备', model: 'device', type: 'text' },
        { label: '随机种子', model: 'seed', type: 'number' },
        { label: '从检查点路径恢复训练', model: 'resume', type: 'text' },
        { label: '起始轮数', model: 'start_epoch', type: 'number' },
        { label: '仅执行评估', model: 'eval', type: 'checkbox' },
        { label: '启用分布式评估', model: 'dist_eval', type: 'checkbox' },
        { label: '数据加载器的工作进程数', model: 'num_workers', type: 'number' },
        { label: '在DataLoader中固定CPU内存', model: 'pin_mem', type: 'checkbox' },
      ],
      trainingSteps: [
        { name: 'Step 1 - 超参数预览', chartId: 'argsChart' },
        { name: 'Step 2 - 数据预处理', chartId: 'dataChart' },
        { name: 'Step 3 - 模型及优化器', chartId: 'modelChart' },
        { name: 'Step 4 - 模型训练', chartId: 'trainingChart' },
        { name: 'Step 5 - 训练结果', chartId: 'resultChart' },
      ],
      start: false,
      selectedStep: {},
      finishedSteps: [],
      curStep: -1,
      curStepName: "",
      argsHelp,
      columns,
      // 下面数据是展示训练过程时候用的
      argsList,
      columnsToPost,
      mfrs_label: [],
      mfrs_org: [],
      mfrs_trans: [],
      mfrs_feature: [],
      mfrs,
      mfrsColumns,
      model: "",
      optimizer: "",
      statsList: Object(),
      tokenList: Object(),
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
              width: 30
            },
            axisLine: {
              lineStyle: {
                width: 12
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
      this.start = true;
      this.curStep = 0;
      this.curStepName = this.trainingSteps[0].name;
      this.stepZero(); 
    },
    stopTraining() {
      console.log('停止训练');
      // 触发停止训练的逻辑
    },
    submitForm() {
      console.log('提交表单', this.form);
      // 处理表单提交
    },
    async stepZero() {
      try {
        this.updateArgsList();
        this.selectStep(this.trainingSteps[0], 0);
        this.stepOne();
      } catch (error) { console.error('第零步失败', error); }
    },
    async stepOne() {
      try {
        const response = await axios.post('http://localhost:5000/pre-train-step1', this.form);
        if (response.data.message == "success") {
          console.log('第一步：', response.data);
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
          this.mfrs_label = data.mfrs_label;
          this.mfrs_feature = data.mfrs_feature;
          this.updateMfrs();

          this.selectStep(this.trainingSteps[1], 1);
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
          this.selectStep(this.trainingSteps[2], 2);
          this.stepThree();
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
          this.statsList = response.data.data.stats_list;
          this.tokenList = response.data.data.token_list;
          this.selectStep(this.trainingSteps[3], 3);
          this.stepFour();
        } else {
          alert(`在第三步时训练出错`);
          return;
        }
      } catch (error) { console.error('第三步失败', error); }
      
    },
    stepFour() {
      this.initChart(this.trainingSteps[4].chartId);
      this.selectStep(this.trainingSteps[4], 4);
      alert("完成整个训练过程")
    },
    resetForm() {
      this.form = {
        epochs: 10,
        warmupEpochs: 0,
        batchSize: 64,
        learningRate: 0.001,
        maskRatio: 0.9,
        weightDecay: 0.05,
        seed: 0,
        dataset: "UbuntuTraffic"
      };
    },
    showStep(step, index) {
      this.curStep = index;
      this.curStepName = step.name;
    },
    selectStep(step, index) {
      this.selectedStep = step;
      // this.initChart(step.chartId);
      if (!this.finishedSteps.includes(index)) {
        this.finishedSteps.push(index);
      }
    },
    isFinished(index) {
      return this.finishedSteps.includes(index);
    },
    initChart(chartId) {
      if (!chartId) return;
      const chartDom = document.getElementById(chartId);
      if (!chartDom) return;
      const myChart = echarts.init(chartDom);
      const option = {
        // 根据图表类型设置不同的option配置
      };
      myChart.setOption(option);
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    updateArgsList() {
      const formMapping = {
        steps: 'epochs',
        warmup_epochs: 'warmupEpochs',
        batch_size: 'batchSize',
        blr: 'learningRate',
        mask_ratio: 'maskRatio',
        weight_decay: 'weightDecay',
        seed: 'seed',
        data_path: 'dataset'
      };

      this.argsList.forEach(arg => {
        const formKey = formMapping[arg.var];
        if (formKey && this.form.hasOwnProperty(formKey)) {
          arg.value = this.form[formKey];
        }
      });
    },
    updateMfrs() {
      for (let i = 0; i < this.mfrs_label.length; i++) {
        const newMfr = {
          id: i+1,
          label: this.mfrs_label[i],
          org: this.mfrs_org[i].src,
          trans: this.mfrs_trans[i].src,
          feature: this.mfrs_feature[i]
        };
        this.mfrs.push(newMfr);
      }
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
  justify-content: space-around;
  margin-bottom: 20px;
  max-height: 732px;
}

.gauge-container {
  width: 36%;
  background-color: white;
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
  height: 70%;
}

.gauge-buttons {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  margin-top: 2%;
}

.gauge-buttons button {
  width: 80%;
  margin-bottom: 10px;
  padding: 5px;
  border: none;
  border-radius: 50px;
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
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: auto;
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

.info-container {
  width: 40%;
  background-color: white;
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
  background-color: white;
  padding: 20px;
  padding-left: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* .step {
  margin-bottom: 25px;
} */

.training-steps-container {
  width: 25%;
  border-right: 1.5px solid  #154ec1;
  border-top: none;
  border-bottom: none; 
  border-left: none;
}
.chart-display-container {
  width: 72%;
}

.training-steps-container,
.chart-display-container {
  padding: 20px;
  /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
}

.training-steps-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.training-steps-container li {
  cursor: pointer;
  font-size: medium;
  width: 90%;
  padding: 10px 30px;
  border-radius: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.chart {
  width: 100%;
  height: 300px; /* 根据需要调整高度 */
}

.argsTable {
  width: 100%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
  color: white;
  background-color: #154ec1;
  border-radius: 20px;
}

pre {
  font-weight: bold;
  white-space: pre-wrap;
  padding-left: 20%;
}
</style>
