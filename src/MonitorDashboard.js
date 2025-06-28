// src/MonitorDashboard.js
import React from 'react';
import { mockVms } from './mockData';
import './App.css'; // Importa estilos

const MachineCard = ({ vm }) => {
  const isAlert = vm.metrics.alert;

  return (
    <div className={`machine-card ${isAlert ? 'alert' : ''}`}>
      <h3>{vm.name} ({vm.os})</h3>
      <p>IP: {vm.ip}</p>
      <div className="metrics">
        <div className="metric-item">
          <span>CPU:</span>
          <span className={vm.metrics.cpuUsage > 70 ? 'high' : ''}>
            {vm.metrics.cpuUsage}%
          </span>
        </div>
        <div className="metric-item">
          <span>Memória:</span>
          <span className={vm.metrics.memoryUsage > 85 ? 'high' : ''}>
            {vm.metrics.memoryUsage}%
          </span>
        </div>
        <div className="metric-item">
          <span>Disco:</span>
          <span className={vm.metrics.diskUsage > 80 ? 'high' : ''}>
            {vm.metrics.diskUsage}%
          </span>
        </div>
        <div className="metric-item">
          <span>Rede (In/Out):</span>
          <span>{vm.metrics.networkActivity.in} / {vm.metrics.networkActivity.out}</span>
        </div>
      </div>
      {isAlert && <p className="alert-message">⚠️ ALERTA: Métricas Anormais!</p>}
    </div>
  );
};

const MonitorDashboard = () => {
  const totalAlerts = mockVms.filter(vm => vm.metrics.alert).length;

  return (
    <div className="dashboard-container">
      <h2>Monitoramento de Máquinas Virtuais</h2>
      <p className="dashboard-overview">
        Total de VMs Monitoradas: {mockVms.length} | VMs com Alerta: {totalAlerts}
      </p>
      <div className="machine-cards-grid">
        {mockVms.map((vm) => (
          <MachineCard key={vm.id} vm={vm} />
        ))}
      </div>
    </div>
  );
};

export default MonitorDashboard;