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
        <h2 class="table-title details-title" style="color: black;">会话特征</h2>
        <table class="details-table">
          <thead>
            <tr>
              <th>绘画ID</th>
              <th>会话名称</th>
              <th>源IP</th>
              <th>目的IP</th>
              <th>源端口</th>
              <th>目的端口</th>
              <th>TLS版本</th>
              <th>恶意概率</th>
              <!-- <th>Feature</th> -->
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
              <!-- <td>{{ detail.feature }}</td> -->
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
        { id: 51, name: '2022-11-25_09:47:20_pcap_TCP_189.194.23.241_443_198.168.3.7_443_1' },
        { id: 52, name: '2022-11-25_09:47:20_pcap_TCP_189.233.20.243_443_198.168.3.7_443_1' },
        { id: 53, name: '2022-11-25_09:47:20_pcap_TCP_189.194.23.241_443_198.168.3.7_443_1' },
        { id: 54, name: '2022-11-25_09:47:20_pcap_TCP_189.233.20.243_443_198.168.3.7_443_1' },
        { id: 55, name: '2022-11-25_09:47:20_pcap_TCP_189.194.23.241_443_198.168.3.7_443_1' },
        { id: 56, name: '2022-11-25_09:47:20_pcap_TCP_189.233.20.243_443_198.168.3.7_443_1' },
        // ...更多数据
      ],
      results: [
        { sessionId: 1, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        { sessionId: 2, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        { sessionId: 3, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        { sessionId: 4, label: 'normal', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443 },
        // ...更多数据
      ],
      details: [
        { sessionId: 1, sessionName: '2022-11-25_09:47:20_pcap_TCP_14', sourceIp: '142.251.43.10', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '86.95%'},
        { sessionId: 2, sessionName: '2022-11-25_09:47:20_pcap_TCP_15', sourceIp: '142.251.43.11', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '75.65%'},
        { sessionId: 3, sessionName: '2022-11-25_09:47:20_pcap_TCP_16', sourceIp: '142.251.43.12', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '65.13%'},
        { sessionId: 4, sessionName: '2022-11-25_09:47:20_pcap_TCP_19', sourceIp: '142.251.43.13', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '84.16%'},
        { sessionId: 5, sessionName: '2022-11-25_09:47:20_pcap_TCP_21', sourceIp: '142.251.43.14', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '65.17%'},
        { sessionId: 6, sessionName: '2022-11-25_09:47:20_pcap_TCP_25', sourceIp: '142.251.43.15', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '65.59%'},
        { sessionId: 7, sessionName: '2022-11-25_09:47:20_pcap_TCP_31', sourceIp: '142.251.43.16', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '86.56%'},
        { sessionId: 8, sessionName: '2022-11-25_09:47:20_pcap_TCP_32', sourceIp: '142.251.43.17', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '19.55%'},
        { sessionId: 9, sessionName: '2022-11-25_09:47:20_pcap_TCP_33', sourceIp: '142.251.43.18', destIp: '192.168.3.7', sourcePort: 443, destPort: 45214, version: 'TLS 1.2', imageFeature: '22.99%'},
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
  font-weight: bold;
}

.start-button {
  background-color: #228200;
}

.pause-button {
  background-color: #e42222;
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
  font-weight: bold;;
}

.packets-title {
  background-color: #154ec1;
}

.results-title {
  background-color: #228200;
}

.details-title {
  background-color: #ffd43a;
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
