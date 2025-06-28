// src/PDFCollector.js
import React, { useState } from 'react';
import { mockPdfs } from './mockData';
import './App.css'; // Importa estilos

const PDFCollector = () => {
  const [collectedPdfs, setCollectedPdfs] = useState([]);
  const [isCollecting, setIsCollecting] = useState(false);

  const handleCollectPdfs = () => {
    setIsCollecting(true);
    setTimeout(() => {
      setCollectedPdfs(mockPdfs);
      setIsCollecting(false);
    }, 1500); // 1.5 segundos de "processamento FIXO "
  };

  return (
    <div className="pdf-collector-container">
      <h2>Coleta e Análise de PDFs</h2>
      <button onClick={handleCollectPdfs} disabled={isCollecting}>
        {isCollecting ? 'Coletando PDFs...' : 'Iniciar Coleta de PDFs'}
      </button>

      {collectedPdfs.length > 0 && (
        <div className="pdf-results">
          <h3>Arquivos PDF Coletados e Analisados:</h3>
          <div className="pdf-list-header">
            <span>Arquivo</span>
            <span>Localização</span>
            <span>Tema (IA Generativa)</span>
          </div>
          {collectedPdfs.map((pdf) => (
            <div key={pdf.id} className="pdf-item">
              <span className="pdf-filename">{pdf.filename}</span>
              <span className="pdf-location">{pdf.location}</span>
              <span className="pdf-topic">{pdf.topic}</span>
            </div>
          ))}
        </div>
      )}

      {collectedPdfs.length === 0 && !isCollecting && (
        <p className="no-data-message">Clique em "Iniciar Coleta de PDFs" para ver os resultados.</p>
      )}
    </div>
  );
};

export default PDFCollector;
