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
.CODE
Inicio:
	mov Ax, @Data
	mov Ds, Ax
	mov ax, 1
	mov V_CONT, ax
	mov ax, V_CONT
	mov di, offset TXT_CONT
	add di, 2
	cmp ax, 0
	jne CONV_0
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_0
CONV_0:
	xor cx, cx
	mov bx, 10
APILAR_DIG_0:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_0
ESCRIBIR_DIG_0:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_0
	mov byte ptr [di], 24h
FIN_CONV_0:
MIENTRAS_0:
	mov ax, V_CONT
	cmp ax, 1
	JNE FIN_MIENTRAS_0
	mov ax, 0
	mov V_VALIDO, ax
	mov ax, V_VALIDO
	mov di, offset TXT_VALIDO
	add di, 2
	cmp ax, 0
	jne CONV_1
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_1
CONV_1:
	xor cx, cx
	mov bx, 10
APILAR_DIG_1:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_1
ESCRIBIR_DIG_1:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_1
	mov byte ptr [di], 24h
FIN_CONV_1:
MIENTRAS_1:
	mov ax, V_VALIDO
	cmp ax, 0
	JNE FIN_MIENTRAS_1
	IMPRIMIR MSJ_2
	IMPRIMIR salto
	LEER TXT_A
	xor ax, ax
	xor cx, cx
	mov cl, TXT_A[1]
	mov si, offset TXT_A
	add si, 2
LEER_NUM_3:
	cmp cl, 0
	je FIN_LEER_NUM_3
	mov bx, 10
	mul bx
	mov bl, [si]
	sub bl, 30h
	mov bh, 0
	add ax, bx
	inc si
	dec cl
	jmp LEER_NUM_3
FIN_LEER_NUM_3:
	mov V_A, ax
	mov ax, V_A
	mov di, offset TXT_A
	add di, 2
	cmp ax, 0
	jne CONV_4
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_4
CONV_4:
	xor cx, cx
	mov bx, 10
APILAR_DIG_4:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_4
ESCRIBIR_DIG_4:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_4
	mov byte ptr [di], 24h
FIN_CONV_4:
	IMPRIMIR salto
	mov ax, V_A
	cmp ax, 9
	JG SINO_2
	mov ax, 1
	mov V_VALIDO, ax
	mov ax, V_VALIDO
	mov di, offset TXT_VALIDO
	add di, 2
	cmp ax, 0
	jne CONV_5
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_5
CONV_5:
	xor cx, cx
	mov bx, 10
APILAR_DIG_5:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_5
ESCRIBIR_DIG_5:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_5
	mov byte ptr [di], 24h
FIN_CONV_5:
SINO_2:
FIN_SI_2:
	mov ax, V_A
	cmp ax, 9
	JLE SINO_3
	IMPRIMIR MSJ_6
	IMPRIMIR salto
SINO_3:
FIN_SI_3:
	jmp MIENTRAS_1
FIN_MIENTRAS_1:
	mov ax, V_A
	cmp ax, 0
	JNE SINO_4
	mov ax, 0
	mov V_CONT, ax
	mov ax, V_CONT
	mov di, offset TXT_CONT
	add di, 2
	cmp ax, 0
	jne CONV_7
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_7
CONV_7:
	xor cx, cx
	mov bx, 10
APILAR_DIG_7:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_7
ESCRIBIR_DIG_7:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_7
	mov byte ptr [di], 24h
FIN_CONV_7:
	IMPRIMIR MSJ_8
	IMPRIMIR salto
SINO_4:
FIN_SI_4:
	mov ax, V_A
	cmp ax, 0
	JE SINO_5
	mov ax, 0
	mov V_VALIDO, ax
	mov ax, V_VALIDO
	mov di, offset TXT_VALIDO
	add di, 2
	cmp ax, 0
	jne CONV_9
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_9
CONV_9:
	xor cx, cx
	mov bx, 10
APILAR_DIG_9:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_9
ESCRIBIR_DIG_9:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_9
	mov byte ptr [di], 24h
FIN_CONV_9:
MIENTRAS_6:
	mov ax, V_VALIDO
	cmp ax, 0
	JNE FIN_MIENTRAS_6
	IMPRIMIR MSJ_10
	IMPRIMIR salto
	LEER TXT_B
	xor ax, ax
	xor cx, cx
	mov cl, TXT_B[1]
	mov si, offset TXT_B
	add si, 2
LEER_NUM_11:
	cmp cl, 0
	je FIN_LEER_NUM_11
	mov bx, 10
	mul bx
	mov bl, [si]
	sub bl, 30h
	mov bh, 0
	add ax, bx
	inc si
	dec cl
	jmp LEER_NUM_11
FIN_LEER_NUM_11:
	mov V_B, ax
	mov ax, V_B
	mov di, offset TXT_B
	add di, 2
	cmp ax, 0
	jne CONV_12
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_12
CONV_12:
	xor cx, cx
	mov bx, 10
APILAR_DIG_12:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_12
ESCRIBIR_DIG_12:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_12
	mov byte ptr [di], 24h
FIN_CONV_12:
	IMPRIMIR salto
	mov ax, V_B
	cmp ax, 9
	JG SINO_7
	mov ax, 1
	mov V_VALIDO, ax
	mov ax, V_VALIDO
	mov di, offset TXT_VALIDO
	add di, 2
	cmp ax, 0
	jne CONV_13
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_13
CONV_13:
	xor cx, cx
	mov bx, 10
APILAR_DIG_13:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_13
ESCRIBIR_DIG_13:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_13
	mov byte ptr [di], 24h
FIN_CONV_13:
SINO_7:
FIN_SI_7:
	mov ax, V_B
	cmp ax, 9
	JLE SINO_8
	IMPRIMIR MSJ_14
	IMPRIMIR salto
SINO_8:
FIN_SI_8:
	jmp MIENTRAS_6
FIN_MIENTRAS_6:
	mov ax, V_B
	cmp ax, 0
	JNE SINO_9
	mov ax, 0
	mov V_CONT, ax
	mov ax, V_CONT
	mov di, offset TXT_CONT
	add di, 2
	cmp ax, 0
	jne CONV_15
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_15
CONV_15:
	xor cx, cx
	mov bx, 10
APILAR_DIG_15:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_15
ESCRIBIR_DIG_15:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_15
	mov byte ptr [di], 24h
FIN_CONV_15:
	IMPRIMIR MSJ_16
	IMPRIMIR salto
SINO_9:
FIN_SI_9:
	mov ax, V_B
	cmp ax, 0
	JE SINO_10
	mov ax, V_A
	cmp ax, V_B
	JLE SINO_11
	IMPRIMIR MSJ_17
	IMPRIMIR salto
	mov ax, 1
	mov V_I, ax
	mov ax, V_I
	mov di, offset TXT_I
	add di, 2
	cmp ax, 0
	jne CONV_18
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_18
CONV_18:
	xor cx, cx
	mov bx, 10
APILAR_DIG_18:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_18
ESCRIBIR_DIG_18:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_18
	mov byte ptr [di], 24h
FIN_CONV_18:
MIENTRAS_12:
	mov ax, V_I
	cmp ax, V_A
	JG FIN_MIENTRAS_12
	mov ax, V_B
	mov bx, ax
	mov cx, V_I
	mov ax, 1
elevar_0:
	cmp cx, 0
	je fin_elevar_0
	mul bx
	dec cx
	jmp elevar_0
fin_elevar_0:
	mov V_P, ax
	mov ax, V_P
	mov di, offset TXT_P
	add di, 2
	cmp ax, 0
	jne CONV_19
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_19
CONV_19:
	xor cx, cx
	mov bx, 10
APILAR_DIG_19:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_19
ESCRIBIR_DIG_19:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_19
	mov byte ptr [di], 24h
FIN_CONV_19:
	mov ax, V_P
	mov di, offset TXT_P
	add di, 2
	cmp ax, 0
	jne CONV_20
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_20
CONV_20:
	xor cx, cx
	mov bx, 10
APILAR_DIG_20:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_20
ESCRIBIR_DIG_20:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_20
	mov byte ptr [di], 24h
FIN_CONV_20:
	IMPRIMIR TXT_P+2
	IMPRIMIR salto
	mov ax, V_I
	add ax, 1
	mov V_I, ax
	mov ax, V_I
	mov di, offset TXT_I
	add di, 2
	cmp ax, 0
	jne CONV_21
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_21
CONV_21:
	xor cx, cx
	mov bx, 10
APILAR_DIG_21:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_21
ESCRIBIR_DIG_21:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_21
	mov byte ptr [di], 24h
FIN_CONV_21:
	jmp MIENTRAS_12
FIN_MIENTRAS_12:
SINO_11:
FIN_SI_11:
	mov ax, V_A
	cmp ax, V_B
	JGE SINO_13
	IMPRIMIR MSJ_22
	IMPRIMIR salto
	mov ax, V_A
	mov V_N, ax
	mov ax, V_N
	mov di, offset TXT_N
	add di, 2
	cmp ax, 0
	jne CONV_23
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_23
CONV_23:
	xor cx, cx
	mov bx, 10
APILAR_DIG_23:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_23
ESCRIBIR_DIG_23:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_23
	mov byte ptr [di], 24h
FIN_CONV_23:
MIENTRAS_14:
	mov ax, V_N
	cmp ax, V_B
	JG FIN_MIENTRAS_14
	mov ax, V_N
	mov bx, ax
	mov cx, 3
	mov ax, 1
elevar_1:
	cmp cx, 0
	je fin_elevar_1
	mul bx
	dec cx
	jmp elevar_1
fin_elevar_1:
	mov V_C, ax
	mov ax, V_C
	mov di, offset TXT_C
	add di, 2
	cmp ax, 0
	jne CONV_24
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_24
CONV_24:
	xor cx, cx
	mov bx, 10
APILAR_DIG_24:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_24
ESCRIBIR_DIG_24:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_24
	mov byte ptr [di], 24h
FIN_CONV_24:
	mov ax, V_C
	mov di, offset TXT_C
	add di, 2
	cmp ax, 0
	jne CONV_25
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_25
CONV_25:
	xor cx, cx
	mov bx, 10
APILAR_DIG_25:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_25
ESCRIBIR_DIG_25:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_25
	mov byte ptr [di], 24h
FIN_CONV_25:
	IMPRIMIR TXT_C+2
	IMPRIMIR salto
	mov ax, V_N
	add ax, 1
	mov V_N, ax
	mov ax, V_N
	mov di, offset TXT_N
	add di, 2
	cmp ax, 0
	jne CONV_26
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_26
CONV_26:
	xor cx, cx
	mov bx, 10
APILAR_DIG_26:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_26
ESCRIBIR_DIG_26:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_26
	mov byte ptr [di], 24h
FIN_CONV_26:
	jmp MIENTRAS_14
FIN_MIENTRAS_14:
SINO_13:
FIN_SI_13:
	mov ax, V_A
	cmp ax, V_B
	JNE SINO_15
	IMPRIMIR MSJ_27
	IMPRIMIR salto
	mov ax, 1
	mov V_I, ax
	mov ax, V_I
	mov di, offset TXT_I
	add di, 2
	cmp ax, 0
	jne CONV_28
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_28
CONV_28:
	xor cx, cx
	mov bx, 10
APILAR_DIG_28:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_28
ESCRIBIR_DIG_28:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_28
	mov byte ptr [di], 24h
FIN_CONV_28:
	mov ax, 1
	mov V_N, ax
	mov ax, V_N
	mov di, offset TXT_N
	add di, 2
	cmp ax, 0
	jne CONV_29
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_29
CONV_29:
	xor cx, cx
	mov bx, 10
APILAR_DIG_29:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_29
ESCRIBIR_DIG_29:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_29
	mov byte ptr [di], 24h
FIN_CONV_29:
MIENTRAS_16:
	mov ax, V_I
	cmp ax, 10
	JG FIN_MIENTRAS_16
	mov ax, V_N
	mov bx, 2
	xor dx, dx
	div bx
	mov ax, dx
	mov V_R, ax
	mov ax, V_R
	mov di, offset TXT_R
	add di, 2
	cmp ax, 0
	jne CONV_30
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_30
CONV_30:
	xor cx, cx
	mov bx, 10
APILAR_DIG_30:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_30
ESCRIBIR_DIG_30:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_30
	mov byte ptr [di], 24h
FIN_CONV_30:
	mov ax, V_R
	cmp ax, 0
	JNE SINO_17
	mov ax, V_N
	mov di, offset TXT_N
	add di, 2
	cmp ax, 0
	jne CONV_31
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_31
CONV_31:
	xor cx, cx
	mov bx, 10
APILAR_DIG_31:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_31
ESCRIBIR_DIG_31:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_31
	mov byte ptr [di], 24h
FIN_CONV_31:
	IMPRIMIR TXT_N+2
	IMPRIMIR salto
	mov ax, V_I
	add ax, 1
	mov V_I, ax
	mov ax, V_I
	mov di, offset TXT_I
	add di, 2
	cmp ax, 0
	jne CONV_32
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_32
CONV_32:
	xor cx, cx
	mov bx, 10
APILAR_DIG_32:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_32
ESCRIBIR_DIG_32:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_32
	mov byte ptr [di], 24h
FIN_CONV_32:
SINO_17:
FIN_SI_17:
	mov ax, V_N
	add ax, 1
	mov V_N, ax
	mov ax, V_N
	mov di, offset TXT_N
	add di, 2
	cmp ax, 0
	jne CONV_33
	mov byte ptr [di], '0'
	inc di
	mov byte ptr [di], 24h
	jmp FIN_CONV_33
CONV_33:
	xor cx, cx
	mov bx, 10
APILAR_DIG_33:
	xor dx, dx
	div bx
	push dx
	inc cx
	cmp ax, 0
	jne APILAR_DIG_33
ESCRIBIR_DIG_33:
	pop dx
	add dl, 30h
	mov [di], dl
	inc di
	loop ESCRIBIR_DIG_33
	mov byte ptr [di], 24h
FIN_CONV_33:
	jmp MIENTRAS_16
FIN_MIENTRAS_16:
SINO_15:
FIN_SI_15:
SINO_10:
FIN_SI_10:
SINO_5:
FIN_SI_5:
	jmp MIENTRAS_0
FIN_MIENTRAS_0:
	mov ax, 4C00h
	int 21h
.DATA
salto db 10,13,24h
V_A dw 0
TXT_A db 6, ?, 7 dup(24h)
V_B dw 0
TXT_B db 6, ?, 7 dup(24h)
V_CONT dw 0
TXT_CONT db 6, ?, 7 dup(24h)
V_VALIDO dw 0
TXT_VALIDO db 6, ?, 7 dup(24h)
V_I dw 0
TXT_I db 6, ?, 7 dup(24h)
V_N dw 0
TXT_N db 6, ?, 7 dup(24h)
V_P dw 0
TXT_P db 6, ?, 7 dup(24h)
V_C dw 0
TXT_C db 6, ?, 7 dup(24h)
V_R dw 0
TXT_R db 6, ?, 7 dup(24h)
MSJ_2 db "INGRESE A",24h
MSJ_6 db "A INVALIDO",24h
MSJ_8 db "FIN",24h
MSJ_10 db "INGRESE B",24h
MSJ_14 db "B INVALIDO",24h
MSJ_16 db "FIN",24h
MSJ_17 db "POTENCIAS DE B",24h
MSJ_22 db "CUBOS ENTRE A Y B",24h
MSJ_27 db "PARES",24h
.STACK
END Inicio
