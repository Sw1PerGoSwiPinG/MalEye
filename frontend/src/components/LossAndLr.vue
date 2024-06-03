<template>
  <div ref="chart" :style="{ width: '100%', height: '400px' }"></div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'EChartsComponent',
  data() {
  },
  mounted() {
    this.initChart();
  },
  methods: {
    async initChart() {
      try {
        const response = await axios.get(`/life-expectancy-table.json`);
        this.run(response.data);
      } catch (error) {
        console.error('Error fetching data', error);
      }
    },
    run(_rawData) {
      const countries = [
        'Finland',
        'France',
        'Germany',
        'Iceland',
        'Norway',
        'Poland',
        'Russia',
        'United Kingdom',
      ];
      const datasetWithFilters = [];
      const seriesList = [];

      echarts.util.each(countries, (country) => {
        var datasetId = 'dataset_' + country;
        datasetWithFilters.push({
          id: datasetId,
          fromDatasetId: 'dataset_raw',
          transform: {
            type: 'filter',
            config: {
              and: [
                { dimension: 'Year', gte: 1950 },
                { dimension: 'Country', '=': country },
              ],
            },
          },
        });
        seriesList.push({
          type: 'line',
          datasetId: datasetId,
          showSymbol: false,
          name: country,
          endLabel: {
            show: true,
            formatter: function (params) {
              return params.value[3] + ': ' + params.value[0];
            },
          },
          labelLayout: {
            moveOverlap: 'shiftY',
          },
          emphasis: {
            focus: 'series',
          },
          encode: {
            x: 'Year',
            y: 'Income',
            label: ['Country', 'Income'],
            itemName: 'Year',
            tooltip: ['Income'],
          },
        });
      });

      const option = {
        animationDuration: 10000,
        dataset: [
          {
            id: 'dataset_raw',
            source: _rawData,
          },
          ...datasetWithFilters,
        ],
        title: {
          text: 'Income of Germany and France since 1950',
        },
        tooltip: {
          order: 'valueDesc',
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          nameLocation: 'middle',
        },
        yAxis: {
          name: 'Income',
        },
        grid: {
          right: 140,
        },
        series: seriesList,
      };

      const chartDom = this.$refs.chart;
      const myChart = echarts.init(chartDom);
      myChart.setOption(option);
    },
  },
};
</script>

<style scoped>
/* Add any additional styling here */
</style>