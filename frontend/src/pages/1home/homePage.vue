<template>
  <div>
    <!-- 网络图 -->
    <div id="networkGraph" class="chart" style="width: 100%; height: 400px; margin-top: 20px;"></div>

    <!-- 图表 -->
    <div class="charts" style="display: flex; justify-content: space-between; margin-top: 20px;">
      <div class="chart" id="attackSourceChart" style="width: 32%; height: 300px;"></div>
      <div class="chart" id="attackTargetChart" style="width: 32%; height: 300px;"></div>
      <div class="chart" id="attackPortChart" style="width: 32%; height: 300px;"></div>
    </div>
    <div class="charts" style="display: flex; justify-content: space-between; margin-top: 20px;">
      <div class="chart" id="trainLossChart" style="width: 49%; height: 300px;"></div>
      <div class="chart" id="trainAccuracyChart" style="width: 49%; height: 300px;"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'HomePage',
  mounted() {
    this.initCharts();
  },
  activated() {
    this.initCharts();
  },
  methods: {
    initCharts() {
      this.initEncryptedTrafficGraph();
      this.initAttackSourceChart();
      this.initAttackTargetChart();
      this.initAttackPortChart();
      this.initTrainLossChart();
      this.initTrainAccuracyChart();
    },
    initEncryptedTrafficGraph() {
      var chartDom = document.getElementById('networkGraph');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '加密流量图',
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            data: this.getEncryptedTrafficData(),
            links: this.getEncryptedTrafficLinks(),
            roam: true,
            label: {
              show: true,
              position: 'right',
              formatter: '{b}'
            },
            force: {
              repulsion: 500, // 增加排斥力，避免节点过度聚集
              gravity: 0.1,  // 调整引力，使节点向中心靠拢
              edgeLength: [50, 100],  // 线的长度范围，控制节点间距离的松紧
              layoutAnimation: true
            },
            lineStyle: {
              width: 2,  // 线条宽度
              curveness: 0.3  // 线条的弯曲度
            }
          },
        ],
      };
      myChart.setOption(option);
    },
    initAttackSourceChart() {
      var chartDom = document.getElementById('attackSourceChart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '攻击来源IP分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: 'bottom'
        },
        series: [
          {
            name: '攻击来源',
            type: 'pie',
            radius: '50%',
            data: this.getAttackSourceData(),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    initAttackTargetChart() {
      var chartDom = document.getElementById('attackTargetChart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '被攻击目标IP分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: 'bottom'
        },
        series: [
          {
            name: '攻击目标',
            type: 'pie',
            radius: '50%',
            data: this.getAttackTargetData(),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    initAttackPortChart() {
      var chartDom = document.getElementById('attackPortChart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '被攻击端口分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: 'bottom'
        },
        series: [
          {
            name: '攻击端口',
            type: 'pie',
            radius: '50%',
            data: this.getAttackPortData(),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    initTrainLossChart() {
      var chartDom = document.getElementById('trainLossChart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '模型训练损失',
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: this.getTrainEpochs()
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'train',
            data: this.getTrainLossData(),
            type: 'line'
          },
          {
            name: 'val',
            data: this.getValLossData(),
            type: 'line'
          }
        ]
      };
      myChart.setOption(option);
    },
    initTrainAccuracyChart() {
      var chartDom = document.getElementById('trainAccuracyChart');
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: '模型训练准确率',
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: this.getTrainEpochs()
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'train',
            data: this.getTrainAccuracyData(),
            type: 'line'
          },
          {
            name: 'val',
            data: this.getValAccuracyData(),
            type: 'line'
          }
        ]
      };
      myChart.setOption(option);
    },
    getEncryptedTrafficData() {
      // 返回加密流量图的节点数据
      return [
        { name: '节点1', value: 25 },
        { name: '节点2', value: 58 },
        { name: '节点3', value: 12 },
        { name: '节点4', value: 97 },
        { name: '节点5', value: 3 },
        { name: '节点6', value: 32 },
        { name: '节点7', value: 10 },
        { name: '节点8', value: 84 },
        { name: '节点9', value: 87 },
        { name: '节点10', value: 99 },
        // 更多节点数据
      ];
    },
    getEncryptedTrafficLinks() {
      // 返回加密流量图的连接数据
      return [
        { source: '节点1', target: '节点9' },
        { source: '节点1', target: '节点8' },
        { source: '节点1', target: '节点2' },
        { source: '节点1', target: '节点6' },
        { source: '节点1', target: '节点3' },
        { source: '节点1', target: '节点4' },
        { source: '节点1', target: '节点5' },
        { source: '节点1', target: '节点7' },
        { source: '节点1', target: '节点10' },
        // 更多连接数据
      ];
    },
    getAttackSourceData() {
      // 返回攻击来源IP的数据
      return [
        { value: 1048, name: '192.168.1.1' },
        { value: 735, name: '192.168.1.2' },
        // ...
      ];
    },
    getAttackTargetData() {
      // 返回被攻击目标IP的数据
      return [
        { value: 1048, name: '192.168.1.3' },
        { value: 735, name: '192.168.1.4' },
        // ...
      ];
    },
    getAttackPortData() {
      // 返回被攻击端口的数据
      return [
        { value: 1048, name: '80' },
        { value: 735, name: '443' },
        // ...
      ];
    },
    getTrainEpochs() {
      // 返回训练的epoch
      return ['Epoch 1', 'Epoch 2', 'Epoch 3', // ...
      ];
    },
    getTrainLossData() {
      // 返回训练损失数据
      return [0.6, 0.4, 0.3, // ...
      ];
    },
    getValLossData() {
      // 返回验证损失数据
      return [0.7, 0.5, 0.4, // ...
      ];
    },
    getTrainAccuracyData() {
      // 返回训练准确率数据
      return [0.6, 0.7, 0.8, // ...
      ];
    },
    getValAccuracyData() {
      // 返回验证准确率数据
      return [0.5, 0.6, 0.7, // ...
      ];
    }
  }
}
</script>

<style scoped>
/* 整体布局风格 */
body {
  font-family: 'Arial', sans-serif; /* 设置字体 */
}

/* 图表外层容器风格 */
.charts {
  display: flex;
  justify-content: space-between;
  margin: 20px 0; /* 调整图表与图表之间的垂直间距 */
}

/* 单个图表的风格 */
.chart {
  width: 32%;
  height: 300px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* 添加阴影 */
  border: 1px solid #ccc; /* 边框颜色 */
  border-radius: 8px; /* 圆角边框 */
  padding: 10px; /* 内边距 */
  background-color: #fff; /* 背景色 */
}

/* 特别处理网络图的样式 */
#networkGraph {
  width: 100%;
  height: 400px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* 添加阴影 */
  border: 1px solid #ccc; /* 边框颜色 */
  border-radius: 8px; /* 圆角边框 */
  padding: 10px; /* 内边距 */
  background-color: #fff; /* 背景色 */
}

/* 标题样式 */
.echarts-title {
  color: #333; /* 字体颜色 */
  font-size: 16px; /* 字体大小 */
  font-weight: bold; /* 字体加粗 */
  text-align: center; /* 标题居中 */
}

/* Tooltip样式 */
.echarts-tooltip {
  background-color: #f4f4f4; /* 背景颜色 */
  border: 1px solid #ddd; /* 边框颜色 */
  border-radius: 4px; /* 边框圆角 */
  padding: 5px; /* 内边距 */
  color: #333; /* 文本颜色 */
  font-size: 14px; /* 字体大小 */
}
</style>
