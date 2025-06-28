; boot.asm - Boot Loader
; Compila com: nasm -f bin boot.asm -o boot.bin

[BITS 16]
[ORG 0x7C00]

start:
    ; Configurar segmentos
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov sp, 0x7BFF
    sti

    ; Limpar tela
    call clear_screen
    
    ; Mostrar mensagem de boot
    mov si, boot_msg
    call print_string
    
    ; Carregar kernel do setor 2
    call load_kernel
    
    ; Pular para o kernel
    jmp 0x1000:0x0000

clear_screen:
    mov ah, 0x00    ; Função set video mode
    mov al, 0x03    ; Modo texto 80x25
    int 0x10
    ret

print_string:
    pusha
.loop:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0E
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    jmp .loop
.done:
    popa
    ret

load_kernel:
    pusha
    mov si, loading_msg
    call print_string
    
    ; Resetar drive
    mov ah, 0x00
    mov dl, 0x00
    int 0x13
    
    ; Carregar setores 2-10 (kernel) para 0x1000:0x0000
    mov ah, 0x02    ; Função read sectors
    mov al, 9       ; 9 setores
    mov ch, 0       ; Cilindro 0
    mov cl, 2       ; Setor 2
    mov dh, 0       ; Cabeça 0
    mov dl, 0x00    ; Drive A
    mov bx, 0x1000  ; Segmento destino
    mov es, bx
    mov bx, 0x0000  ; Offset destino
    int 0x13
    
    jc disk_error
    
    mov si, success_msg
    call print_string
    popa
    ret

disk_error:
    mov si, error_msg
    call print_string
    hlt

; Mensagens
boot_msg db 'MiniOS Boot Loader v1.0', 0x0D, 0x0A, 0
loading_msg db 'Carregando kernel...', 0x0D, 0x0A, 0
success_msg db 'Kernel carregado com sucesso!', 0x0D, 0x0A, 0
error_msg db 'Erro ao carregar kernel!', 0x0D, 0x0A, 0

; Boot signature
times 510-($-$$) db 0
dw 0xAA55

; ==================== KERNEL (SETOR 2+) ====================
[ORG 0x0000]

kernel_start:
    ; Configurar stack
    mov ax, 0x1000
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov sp, 0xFFFF
    
    ; Mostrar mensagem do kernel
    mov si, kernel_msg
    call print_string
    
    ; Inicializar sistema de arquivos
    call init_filesystem
    
    ; Menu principal
    call main_menu

init_filesystem:
    ; Inicializar área de dados na memória
    mov word [pessoa_count], 0
    mov word [produto_count], 0
    ret

main_menu:
.loop:
    call clear_screen
    mov si, menu_msg
    call print_string
    
    ; Ler opção do usuário
    call read_char
    
    cmp al, '1'
    je add_pessoa
    cmp al, '2' 
    je add_produto
    cmp al, '3'
    je list_pessoas
    cmp al, '4'
    je list_produtos
    cmp al, '5'
    je save_data
    cmp al, '6'
    je load_data
    cmp al, '0'
    je exit_system
    
    jmp .loop

add_pessoa:
    call clear_screen
    mov si, add_pessoa_msg
    call print_string
    
    ; Verificar se há espaço
    mov ax, [pessoa_count]
    cmp ax, 10
    jb .tem_espaco
    mov si, max_pessoas_msg
    call print_string
    call wait_key
    jmp main_menu
    
.tem_espaco:
    ; Ler nome (32 bytes)
    mov di, temp_buffer
    mov cx, 32
    call read_string
    
    ; Copiar para área de pessoas
    mov ax, [pessoa_count]
    mov bx, 64
    mul bx
    mov di, ax
    add di, pessoas_data
    mov si, temp_buffer
    mov cx, 32
    rep movsb
    
    ; Ler idade
    mov si, idade_msg
    call print_string
    call read_number
    mov [di], al
    
    ; Incrementar contador
    inc word [pessoa_count]
    
    mov si, success_add_msg
    call print_string
    call wait_key
    jmp main_menu

add_produto:
    call clear_screen
    mov si, add_produto_msg
    call print_string
    
    ; Verificar se há espaço
    mov ax, [produto_count]
    cmp ax, 10
    jb .tem_espaco
    mov si, max_produtos_msg
    call print_string
    call wait_key
    jmp main_menu
    
.tem_espaco:
    ; Ler nome (32 bytes)
    mov di, temp_buffer
    mov cx, 32
    call read_string
    
    ; Copiar para área de produtos
    mov ax, [produto_count]
    mov bx, 64
    mul bx
    mov di, ax
    add di, produtos_data
    mov si, temp_buffer
    mov cx, 32
    rep movsb
    
    ; Ler preço
    mov si, preco_msg
    call print_string
    call read_number
    mov [di+32], al
    
    ; Incrementar contador
    inc word [produto_count]
    
    mov si, success_add_msg
    call print_string
    call wait_key
    jmp main_menu

list_pessoas:
    call clear_screen
    mov si, list_pessoas_msg
    call print_string
    
    mov cx, [pessoa_count]
    or cx, cx
    jz .empty
    
    mov si, pessoas_data
.loop_pessoa:
    push cx
    push si
    
    ; Mostrar nome
    call print_string
    
    ; Mostrar idade
    mov si, idade_prefix
    call print_string
    add word [esp], 32  ; Avança para o campo idade
    mov si, [esp]
    lodsb
    call print_number
    
    mov si, newline
    call print_string
    
    pop si
    add si, 64
    pop cx
    loop .loop_pessoa
    jmp .done
    
.empty:
    mov si, empty_msg
    call print_string
    
.done:
    call wait_key
    jmp main_menu

list_produtos:
    call clear_screen
    mov si, list_produtos_msg
    call print_string
    
    mov cx, [produto_count]
    or cx, cx
    jz .empty
    
    mov si, produtos_data
.loop_produto:
    push cx
    push si
    
    ; Mostrar nome
    call print_string
    
    ; Mostrar preço
    mov si, preco_prefix
    call print_string
    add word [esp], 32  ; Avança para o campo preço
    mov si, [esp]
    lodsb
    call print_number
    
    mov si, newline
    call print_string
    
    pop si
    add si, 64
    pop cx
    loop .loop_produto
    jmp .done
    
.empty:
    mov si, empty_msg
    call print_string
    
.done:
    call wait_key
    jmp main_menu

save_data:
    mov si, saving_msg
    call print_string
    
    ; Salvar contadores primeiro
    mov bx, 0x1000
    mov es, bx
    mov bx, pessoa_count
    mov ah, 0x03
    mov al, 1
    mov ch, 0
    mov cl, 11      ; Setor 11 - contadores
    mov dh, 0
    mov dl, 0x00
    int 0x13
    jc disk_error
    
    ; Salvar pessoas
    mov bx, pessoas_data
    mov ah, 0x03
    mov al, 4       ; 4 setores para 10 registros
    mov cl, 12      ; Setor 12-15
    int 0x13
    jc disk_error
    
    ; Salvar produtos
    mov bx, produtos_data
    mov ah, 0x03
    mov al, 4       ; 4 setores para 10 registros
    mov cl, 16      ; Setor 16-19
    int 0x13
    jc disk_error
    
    mov si, save_success_msg
    call print_string
    call wait_key
    jmp main_menu

load_data:
    mov si, loading_data_msg
    call print_string
    
    ; Carregar contadores
    mov bx, 0x1000
    mov es, bx
    mov bx, pessoa_count
    mov ah, 0x02
    mov al, 1
    mov ch, 0
    mov cl, 11      ; Setor 11 - contadores
    mov dh, 0
    mov dl, 0x00
    int 0x13
    jc disk_error
    
    ; Carregar pessoas
    mov bx, pessoas_data
    mov ah, 0x02
    mov al, 4       ; 4 setores
    mov cl, 12      ; Setor 12-15
    int 0x13
    jc disk_error
    
    ; Carregar produtos
    mov bx, produtos_data
    mov ah, 0x02
    mov al, 4       ; 4 setores
    mov cl, 16      ; Setor 16-19
    int 0x13
    jc disk_error
    
    mov si, load_success_msg
    call print_string
    call wait_key
    jmp main_menu

exit_system:
    call clear_screen
    mov si, goodbye_msg
    call print_string
    hlt

; Funções auxiliares
print_number:
    pusha
    xor cx, cx
    mov bl, 10
    
.divide:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz .divide
    
.print:
    pop ax
    add al, '0'
    mov ah, 0x0E
    int 0x10
    loop .print
    
    popa
    ret

read_char:
    mov ah, 0x00
    int 0x16
    ret

read_string:
    pusha
    mov bx, di
.loop:
    call read_char
    cmp al, 0x0D    ; Enter
    je .done
    cmp al, 0x08    ; Backspace
    je .backspace
    
    stosb
    mov ah, 0x0E
    int 0x10
    dec cx
    jnz .loop
    jmp .done
    
.backspace:
    cmp di, bx
    je .loop
    dec di
    mov ah, 0x0E
    mov al, 0x08
    int 0x10
    mov al, ' '
    int 0x10
    mov al, 0x08
    int 0x10
    inc cx
    jmp .loop
    
.done:
    mov al, 0
    stosb
    popa
    ret

read_number:
    push bx
    push cx
    xor bx, bx  ; Armazenará o número resultante
    xor cx, cx  ; Contador de dígitos
    
.read_loop:
    call read_char
    cmp al, 0x0D    ; Enter - finalizar
    je .done
    cmp al, '0'
    jb .read_loop   ; Ignorar caracteres não numéricos
    cmp al, '9'
    ja .read_loop
    
    ; Mostrar o dígito
    mov ah, 0x0E
    int 0x10
    
    ; Converter para valor e acumular
    sub al, '0'
    push ax
    mov ax, bx
    mov dx, 10
    mul dx          ; Multiplica o acumulador por 10
    mov bx, ax
    pop ax
    add bl, al
    adc bh, 0
    
    inc cx
    cmp cx, 3       ; Máximo de 3 dígitos
    jb .read_loop
    
.done:
    mov ax, bx      ; Retorna o número em AX
    pop cx
    pop bx
    ret

wait_key:
    mov si, press_key_msg
    call print_string
    call read_char
    ret

; Mensagens do kernel
kernel_msg db 'MiniOS Kernel v1.0 - Sistema de Mainframe', 0x0D, 0x0A, 0
menu_msg db 0x0D, 0x0A, '=== SISTEMA DE MAINFRAME ===', 0x0D, 0x0A
         db '1. Adicionar Pessoa', 0x0D, 0x0A
         db '2. Adicionar Produto', 0x0D, 0x0A
         db '3. Listar Pessoas', 0x0D, 0x0A
         db '4. Listar Produtos', 0x0D, 0x0A
         db '5. Salvar Dados', 0x0D, 0x0A
         db '6. Carregar Dados', 0x0D, 0x0A
         db '0. Sair', 0x0D, 0x0A
         db 'Escolha uma opcao: ', 0

add_pessoa_msg db 'Digite o nome da pessoa: ', 0
add_produto_msg db 'Digite o nome do produto: ', 0
idade_msg db 0x0D, 0x0A, 'Digite a idade: ', 0
preco_msg db 0x0D, 0x0A, 'Digite o preco: ', 0
list_pessoas_msg db '=== LISTA DE PESSOAS ===', 0x0D, 0x0A, 0
list_produtos_msg db '=== LISTA DE PRODUTOS ===', 0x0D, 0x0A, 0
empty_msg db 'Nenhum registro encontrado!', 0x0D, 0x0A, 0
success_add_msg db 0x0D, 0x0A, 'Registro adicionado com sucesso!', 0x0D, 0x0A, 0
saving_msg db 'Salvando dados...', 0x0D, 0x0A, 0
loading_data_msg db 'Carregando dados...', 0x0D, 0x0A, 0
save_success_msg db 'Dados salvos com sucesso!', 0x0D, 0x0A, 0
load_success_msg db 'Dados carregados com sucesso!', 0x0D, 0x0A, 0
press_key_msg db 'Pressione qualquer tecla...', 0
goodbye_msg db 'Encerrando sistema...', 0x0D, 0x0A, 0
newline db 0x0D, 0x0A, 0
max_pessoas_msg db 'Capacidade maxima de pessoas atingida!', 0x0D, 0x0A, 0
max_produtos_msg db 'Capacidade maxima de produtos atingida!', 0x0D, 0x0A, 0
idade_prefix db ' - Idade: ', 0
preco_prefix db ' - Preco: ', 0

; Variáveis
pessoa_count dw 0
produto_count dw 0
temp_buffer times 64 db 0

; Áreas de dados (cada registro = 64 bytes)
pessoas_data times 640 db 0    ; 10 pessoas max
produtos_data times 640 db 0   ; 10 produtos max

; Preencher resto do kernel
times 4608-($-kernel_start) db 0