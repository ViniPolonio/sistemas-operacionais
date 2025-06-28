// src/App.js
import React, { useState } from 'react';
import MonitorDashboard from './MonitorDashboard';
import PDFCollector from './PDFCollector';
import './App.css'; // Importa estilos

function App() {
  const [currentView, setCurrentView] = useState('monitor'); // 'monitor' ou 'pdf'

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Sistema Integrado de Monitoramento e Análise</h1>
        <nav className="app-nav">
          <button
            className={currentView === 'monitor' ? 'active' : ''}
            onClick={() => setCurrentView('monitor')}
          >
            Monitoramento de VMs
          </button>
          <button
            className={currentView === 'pdf' ? 'active' : ''}
            onClick={() => setCurrentView('pdf')}
          >
            Coleta e Análise de PDFs
          </button>
        </nav>
      </header>

      <main className="app-main-content">
        {currentView === 'monitor' && <MonitorDashboard />}
        {currentView === 'pdf' && <PDFCollector />}
      </main>
    </div>
  );
}

export default App;
