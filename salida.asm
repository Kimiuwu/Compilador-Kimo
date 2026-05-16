IMPRIMIR Macro Mensaje
   mov Ah, 09h
   mov Dx, offset Mensaje
   int 21h
EndM

LEER Macro Entrada
   mov Ah, 0Ah
   mov Dx, offset Entrada
   int 21h
EndM

.MODEL SMALL
.DATA
salto db 10,13,24h
var_A dw 0
txt_A db 4, ?, 5 dup(24h)
var_B dw 0
txt_B db 4, ?, 5 dup(24h)
var_C dw 0
txt_C db 4, ?, 5 dup(24h)
var_I dw 0
txt_I db 4, ?, 5 dup(24h)
var_TEXTO db 100, ?, 100 dup(24h)
cad_temp_0 db "HOLA KIMO",24h
msg_1 db "A ES MAYOR",24h
.CODE
Inicio:
	mov Ax, @Data
	mov Ds, Ax
	mov ax, 5
	mov var_A, ax
	mov ax, var_A
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_A[2], al
	mov txt_A[3], dl
	mov txt_A[4], 24h
	mov ax, 3
	mov var_B, ax
	mov ax, var_B
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_B[2], al
	mov txt_B[3], dl
	mov txt_B[4], 24h
	mov ax, var_A
	add ax, var_B
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	mov ax, var_A
	sub ax, var_B
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	mov ax, var_A
	mov bx, var_B
	mul bx
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	mov ax, var_A
	mov bx, var_B
	xor dx, dx
	div bx
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	mov ax, var_A
	mov bx, var_B
	xor dx, dx
	div bx
	mov ax, dx
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	mov ax, var_A
	mov bx, ax
	mov cx, var_B
	mov ax, 1
elevar_0:
	cmp cx, 0
	je fin_elevar_0
	mul bx
	dec cx
	jmp elevar_0
fin_elevar_0:
	mov var_C, ax
	mov ax, var_C
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_C[2], al
	mov txt_C[3], dl
	mov txt_C[4], 24h
	IMPRIMIR txt_C+2
	IMPRIMIR salto
	lea si, cad_temp_0
	lea di, var_TEXTO+2
copiar_cadena_0:
	mov al, [si]
	mov [di], al
	inc si
	inc di
	cmp al, 24h
	jne copiar_cadena_0
	IMPRIMIR var_TEXTO+2
	IMPRIMIR salto
	LEER txt_A
	mov al, txt_A[2]
	sub al, 30h
	mov ah, 0
	mov var_A, ax
	mov ax, var_A
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_A[2], al
	mov txt_A[3], dl
	mov txt_A[4], 24h
	IMPRIMIR salto
	IMPRIMIR txt_A+2
	IMPRIMIR salto
	mov ax, var_A
	cmp ax, var_B
	JLE fin_if_0
	IMPRIMIR msg_1
	IMPRIMIR salto
	IMPRIMIR txt_A+2
	IMPRIMIR salto
fin_if_0:
while_1:
	mov ax, var_A
	cmp ax, 0
	JLE fin_while_1
	IMPRIMIR txt_A+2
	IMPRIMIR salto
	mov ax, var_A
	sub ax, 1
	mov var_A, ax
	mov ax, var_A
	mov bx, 10
	xor dx, dx
	div bx
	add al, '0'
	add dl, '0'
	mov txt_A[2], al
	mov txt_A[3], dl
	mov txt_A[4], 24h
	jmp while_1
fin_while_1:
	mov ax, 4C00h
	int 21h
.STACK
END Inicio