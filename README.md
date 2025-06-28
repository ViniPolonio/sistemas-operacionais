MiniOS - Sistema Operacional Minimalista em Assembly
💡 Sobre o Projeto

Desenvolvi esse sistema operacional minimalista em Assembly x86 como projeto acadêmico, explorando os fundamentos da computação de baixo nível. Ele demonstra:

    Inicialização completa de um PC a partir do zero

    Gerenciamento básico de cadastros

    Persistência de dados em disco

    Interface de menu simples porém funcional

Tudo isso em menos de 5KB de código, mostrando como sistemas operacionais podem ser eficientes!
🛠️ Componentes Principais
Boot Loader (O Inicializador)

    Desenvolvido em Assembly x86 puro

    Compacto (512 bytes exatos)

    Localizado no setor 0 do disco

    Responsável por carregar o kernel na memória

Kernel (O Núcleo)

    Opera em modo real 16-bit

    Ocupa apenas 4.5KB

    Funcionalidades essenciais:

        Sistema de menu interativo

        Gerenciamento básico de memória

        Controle de entrada/saída via BIOS

Armazenamento de Dados

    Estrutura simples:

        Pessoa: 64 bytes (32 chars para nome + idade)

        Produto: 64 bytes (32 chars para nome + preço)

    Capacidade: 10 registros de cada tipo

    Persistência em setores dedicados do disco

🚀 Guia Rápido
Pré-requisitos
bash

# Ubuntu/Debian
sudo apt install nasm qemu-system-x86

# Fedora
sudo dnf install nasm qemu-system-x86

# Arch Linux
sudo pacman -S nasm qemu

Compilação e Execução
bash

make all   # Compila o sistema
make run   # Executa no QEMU

🎮 Como Utilizar
Menu Principal

    ➕ Adicionar Pessoa (nome e idade)

    🛒 Adicionar Produto (nome e preço)

    👥 Listar Pessoas Cadastradas

    📦 Listar Produtos Cadastrados

    💾 Salvar Dados no Disco

    📥 Carregar Dados do Disco

    ❌ Sair do Sistema

🧠 Detalhes Técnicos
Organização da Memória
Endereço	Conteúdo
0x0000:0x7C00	Boot Loader
0x1000:0x0000	Kernel
0x1000:0x1200	Dados de Pessoas
0x1000:0x1340	Dados de Produtos
Estrutura do Disco
Setores	Conteúdo
0	Boot Loader
2-10	Kernel
11-12	Dados de Pessoas
13-14	Dados de Produtos
⚠️ Limitações Atuais

    Opera apenas em modo 16-bit

    Capacidade máxima de 10 registros por tipo

    Nomes limitados a 32 caracteres

    Valores numéricos até 999

    Sistema de arquivos básico

📝 Considerações Finais

Este projeto foi desenvolvido com fins educacionais, demonstrando os princípios fundamentais de sistemas operacionais. Sinta-se à vontade para utilizá-lo como base para seus próprios experimentos em desenvolvimento de sistemas de baixo nível.

viniciuspolober@gmail.com