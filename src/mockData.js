// src/mockData.js
// DADOS MOCKADOS GERADOS POR IA POIS TIVE DIFICULDADE EM INTEGRAR COM O BACKEND
export const mockVms = [
    {
      id: 'vm-linux-1',
      name: 'Linux Server 1 (Ubuntu)',
      ip: '192.168.1.101',
      metrics: {
        cpuUsage: 75, // %
        memoryUsage: 88, // %
        diskUsage: 60, // %
        networkActivity: { in: '1.2 MB/s', out: '0.8 MB/s' },
        alert: true, // Simula um alerta de memória alta
      },
      os: 'Linux',
    },
    {
      id: 'vm-linux-2',
      name: 'Linux Server 2 (Debian)',
      ip: '192.168.1.102',
      metrics: {
        cpuUsage: 30,
        memoryUsage: 45,
        diskUsage: 78, // Simula disco quase cheio
        networkActivity: { in: '0.5 MB/s', out: '0.3 MB/s' },
        alert: false,
      },
      os: 'Linux',
    },
    {
      id: 'vm-windows-1',
      name: 'Windows Server 1',
      ip: '192.168.1.103',
      metrics: {
        cpuUsage: 55,
        memoryUsage: 70,
        diskUsage: 35,
        networkActivity: { in: '2.1 MB/s', out: '1.5 MB/s' },
        alert: false,
      },
      os: 'Windows',
    },
  ];
  
  export const mockPdfs = [
    {
      id: 'pdf-1',
      filename: 'Relatorio_Anual_2023.pdf',
      location: '/home/ubuntu/docs/financeiro/',
      topic: 'Análise de Desempenho Financeiro de 2023 e Projeções',
    },
    {
      id: 'pdf-2',
      filename: 'Especificacoes_Tecnicas_Projeto_Alpha.pdf',
      location: '/mnt/windows_share/projetos/',
      topic: 'Detalhes Técnicos e Requisitos do Projeto Alpha',
    },
    {
      id: 'pdf-3',
      filename: 'Manual_Usuario_Sistema_CRM.pdf',
      location: '/var/www/html/docs/',
      topic: 'Guia Completo de Uso do Sistema CRM para Novos Operadores',
    },
    {
      id: 'pdf-4',
      filename: 'Politica_de_Seguranca_Interna.pdf',
      location: '/home/admin/config/',
      topic: 'Diretrizes e Procedimentos de Segurança da Informação na Empresa',
    },
  ];