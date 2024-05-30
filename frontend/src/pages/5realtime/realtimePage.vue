<template>
  <div class="container">
    <div class="top-buttons">
      <button @click="startDetection" class="start-button">开始检测</button>
      <button @click="pauseDetection" class="pause-button">暂停检测</button>
    </div>
    <div class="top-section">
      <div class="packets-table-container">
        <h2 class="table-title packets-title">待检测包</h2>
        <table class="packets-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="packet in packets" :key="packet.id">
              <td>{{ packet.id }}</td>
              <td>{{ packet.name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="results-table-container">
        <h2 class="table-title results-title">检测结果</h2>
        <table class="results-table">
          <thead>
            <tr>
              <th>SessionID</th>
              <th>Label</th>
              <th>SourceIP</th>
              <th>DestIP</th>
              <th>SourcePort</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in results" :key="result.sessionId">
              <td>{{ result.sessionId }}</td>
              <td :class="{'label-normal': result.label === 'normal', 'label-abnormal': result.label === 'abnormal'}">{{ result.label }}</td>
              <td>{{ result.sourceIp }}</td>
              <td>{{ result.destIp }}</td>
              <td>{{ result.sourcePort }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="bottom-section">
      <div class="details-table-container">
        <h2 class="table-title details-title">会话特征</h2>
        <table class="details-table">
          <thead>
            <tr>
              <th>SessionID</th>
              <th>SessionName</th>
              <th>SourceIP</th>
              <th>DestIP</th>
              <th>SourcePort</th>
              <th>DestPort</th>
              <th>Version</th>
              <th>ImageFeature</th>
              <th>Feature</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="detail in details" :key="detail.sessionId">
              <td>{{ detail.sessionId }}</td>
              <td>{{ detail.sessionName }}</td>
              <td>{{ detail.sourceIp }}</td>
              <td>{{ detail.destIp }}</td>
              <td>{{ detail.sourcePort }}</td>
              <td>{{ detail.destPort }}</td>
              <td>{{ detail.version }}</td>
              <td>{{ detail.imageFeature }}</td>
              <td>{{ detail.feature }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RealtimePage',
  data() {
    return {
      packets: [
        { id: 1379, name: '2022-11-25_09:47:20_pcap_TCP_189.194.23.241_443_198.168.3.7_443_1' },
        { id: 1378, name: '2022-11-25_09:47:20_pcap_TCP_189.233.20.243_443_198.168.3.7_443_1' },
        // ...更多数据
      ],
      results: [
        { sessionId: 1406, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        { sessionId: 1405, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        // ...更多数据
      ],
      details: [
        { sessionId: 1406, sessionName: '2022-11-25_09:47:20_pcap_TCP_14', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '特征1', feature: '特征详情' },
        { sessionId: 1405, sessionName: '2022-11-25_09:47:20_pcap_TCP_14', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '特征2', feature: '特征详情' },
        // ...更多数据
      ]
    };
  },
  methods: {
    startDetection() {
      console.log('开始检测');
      // 触发开始检测的逻辑
    },
    pauseDetection() {
      console.log('暂停检测');
      // 触发暂停检测的逻辑
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.top-buttons {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.start-button,
.pause-button {
  margin-right: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  font-size: 16px;
}

.start-button {
  background-color: #4caf50;
}

.pause-button {
  background-color: #f44336;
}

.top-section, .bottom-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.packets-table-container, .results-table-container, .details-table-container {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.packets-table-container {
  width: 48%;
}

.results-table-container {
  width: 48%;
}

.details-table-container {
  width: 100%;
}

.table-title {
  text-align: center;
  margin-bottom: 10px;
  background-color: #e0e0e0;
  padding: 10px;
  border-radius: 5px;
  color: white;
}

.packets-title {
  background-color: #2196f3;
}

.results-title {
  background-color: #4caf50;
}

.details-title {
  background-color: #ff9800;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #e0e0e0;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.label-normal {
  color: green;
  font-weight: bold;
}

.label-abnormal {
  color: red;
  font-weight: bold;
}

td {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
