import re
import os


class ErrorCompilacion(Exception):
    pass


class CompiladorKimo:
    def __init__(self):
        self.linea_actual = 1

        self.macros_asm = []
        self.data_asm = []
        self.code_asm = []

        self.tabla_simbolos = {}
        self.errores_detectados = []

        self.en_bloque_variables = False
        self.inicio_encontrado = False

        self.pila_bloques = []
        self.contador_ciclos = 0
        self.contador_mensajes = 0
        self.contador_elevacion = 0

        self.definir_tabla_errores()
        self.definir_regex()
        self.preparar_estructura_base()

    def definir_tabla_errores(self):
        self.tabla_errores = {
            "E000": "El archivo fuente no existe.",
            "E001": "Instrucción desconocida.",
            "E002": "Falta la instrucción INICIO:.",
            "E003": "Falta cerrar el bloque de variables con FIN_VAR.",
            "E004": "Existe un bloque SI o MIENTRAS sin cerrar.",
            "E005": "Declaración inválida. Use la forma: ID : TIPO;",
            "E006": "Variable ya declarada.",
            "E007": "Variable no declarada.",
            "E008": "Sintaxis inválida en IMPRIMIR.",
            "E009": "Sintaxis inválida en LEER.",
            "E010": "Sintaxis inválida en SI.",
            "E011": "Sintaxis inválida en MIENTRAS.",
            "E012": "FIN encontrado sin bloque SI abierto.",
            "E013": "FINM encontrado sin ciclo MIENTRAS abierto.",
            "E014": "Asignación inválida.",
            "E015": "Tipo incompatible en asignación.",
            "E016": "Expresión aritmética inválida. Use una operación simple: A = B + 5;",
            "E017": "Operador aritmético inválido.",
            "E018": "INICIO: ya fue declarado.",
            "E019": "No se permiten instrucciones antes de INICIO:.",
            "E020": "La declaración de variables debe estar dentro de INI_VAR y FIN_VAR."
        }

    def registrar_error(self, codigo):
        self.errores_detectados.append({
            "codigo": codigo,
            "linea": self.linea_actual
        })
        raise ErrorCompilacion

    def reportar_errores(self):
        print("\n[REPORTE DE ERRORES]")

        for error in self.errores_detectados:
            codigo = error["codigo"]
            linea = error["linea"]
            descripcion = self.tabla_errores.get(codigo, "Error no registrado.")
            print(f"Línea {linea} | {codigo} | {descripcion}")

    def definir_regex(self):
        self.ID = r"[A-Z0-9_-]+"
        self.ENTERO = r"[+-]?[0-9]+"
        self.FLOAT = r"[+-]?[0-9]+\.[0-9]+"
        self.CADENA = r'"[A-Z0-9\s+\-*/%^=><!;:,._@#$&]*"'

        self.TIPO = r"(?:ENT|FLOAT|CAD)"
        self.OP_REL = r"(?:>=|<=|==|!=|>|<)"
        self.OP_ARIT = r"(?:\+|-|\*|/|%|\^)"

        self.ESP = r"\s*"
        self.ESP_OBL = r"\s+"

        self.PA = r"\("
        self.PC = r"\)"
        self.PYC = r";"
        self.DOSP = r":"
        self.IGUAL = r"="
        #Lenguaje
        self.PR_INICIO = r"INICIO:"
        self.PR_INI_VAR = r"INI_VAR"
        self.PR_FIN_VAR = r"FIN_VAR"
        self.PR_LEER = r"LEER"
        self.PR_IMPRIMIR = r"IMPRIMIR"
        self.PR_SI = r"SI"
        self.PR_SINO = r"SINO"
        self.PR_ENTONCES = r"ENTONCES"
        self.PR_FIN = r"FIN"
        self.PR_MIENTRAS = r"MIENTRAS"
        self.PR_HACER = r"HACER"
        self.PR_FINM = r"FINM"
        self.PR_DESDE = r"DESDE"
        self.PR_HASTA = r"HASTA"

        self.OPERANDO_NUM = rf"(?:{self.ID}|{self.ENTERO})"
        self.EXP_IMPRIMIBLE = rf"(?:{self.ID}|{self.ENTERO}|{self.CADENA})"
        self.EXP_NUM_FOR = rf"(?:{self.OPERANDO_NUM}(?:{self.ESP}{self.OP_ARIT}{self.ESP}{self.OPERANDO_NUM})?)"

        self.regex_id = re.compile(rf"^{self.ID}$")
        self.regex_entero = re.compile(rf"^{self.ENTERO}$")
        self.regex_float = re.compile(rf"^{self.FLOAT}$")
        self.regex_cadena = re.compile(rf"^{self.CADENA}$")

        # Producciones de Kimo
        # <DECL> ::= <ID> : <TIPO> ;
        self.regex_declaracion = re.compile(
            rf"^{self.ESP}({self.ID}){self.ESP}{self.DOSP}{self.ESP}({self.TIPO}){self.ESP}{self.PYC}$"
        )
        # <ENTRADA> ::= LEER ( <ID> ) ;
        self.regex_leer = re.compile(
            rf"^{self.ESP}{self.PR_LEER}{self.ESP}{self.PA}{self.ESP}({self.ID}){self.ESP}{self.PC}{self.ESP}{self.PYC}$"
        )
        #<SALIDA> ::= IMPRIMIR ( <EXPRESION> ) ;
        self.regex_imprimir = re.compile(
            rf"^{self.ESP}{self.PR_IMPRIMIR}{self.ESP}{self.PA}{self.ESP}({self.EXP_IMPRIMIBLE}){self.ESP}{self.PC}{self.ESP}{self.PYC}$"
        )
        # <CONDICIONAL> ::= SI <EXPRESION> <OP_REL> <EXPRESION> ENTONCES
        self.regex_si = re.compile(
            rf"^{self.ESP}{self.PR_SI}{self.ESP_OBL}"
            rf"({self.OPERANDO_NUM}){self.ESP}({self.OP_REL}){self.ESP}({self.OPERANDO_NUM})"
            rf"{self.ESP_OBL}{self.PR_ENTONCES}$"
        )
        # <WHILE> ::= MIENTRAS <EXPRESION> <OP_REL> <EXPRESION> HACER
        self.regex_mientras = re.compile(
            rf"^{self.ESP}{self.PR_MIENTRAS}{self.ESP_OBL}"
            rf"({self.OPERANDO_NUM}){self.ESP}({self.OP_REL}){self.ESP}({self.OPERANDO_NUM})"
            rf"{self.ESP_OBL}{self.PR_HACER}$"
        )
        # <FOR> ::= DESDE <ID> = <EXPRESION> HASTA <EXPRESION> HACER
        self.regex_for = re.compile(
            rf"^{self.ESP}{self.PR_DESDE}{self.ESP_OBL}"
            rf"({self.ID}){self.ESP}{self.IGUAL}{self.ESP}({self.EXP_NUM_FOR})"
            rf"{self.ESP_OBL}{self.PR_HASTA}{self.ESP_OBL}({self.EXP_NUM_FOR})"
            rf"{self.ESP_OBL}{self.PR_HACER}$"
        )

        # <ASIGNACION> ::= <ID> = <EXPRESION> ;
        self.regex_asignacion = re.compile(
            rf"^{self.ESP}({self.ID}){self.ESP}{self.IGUAL}{self.ESP}(.+?){self.ESP}{self.PYC}$"
        )

        self.regex_exp_num_simple = re.compile(
            rf"^({self.OPERANDO_NUM})(?:{self.ESP}({self.OP_ARIT}){self.ESP}({self.OPERANDO_NUM}))?$"
        )

        self.saltos_inversos = {
            ">": "JLE",
            "<": "JGE",
            ">=": "JL",
            "<=": "JG",
            "==": "JNE",
            "!=": "JE"
        }

    def preparar_estructura_base(self):
        self.macros_asm = [
            "IMPRIMIR Macro Mensaje",
            "   mov Ah, 09h",
            "   mov Dx, offset Mensaje",
            "   int 21h",
            "EndM",
            "",
            "LEER Macro Entrada",
            "   mov Ah, 0Ah",
            "   mov Dx, offset Entrada",
            "   int 21h",
            "EndM",
            ""
        ]

        self.data_asm = [
            ".DATA",
            "salto db 10,13,24h"
        ]

    def es_id_valido(self, valor):
        return valor != "" and self.regex_id.match(valor) is not None

    def es_entero(self, valor):
        return self.regex_entero.match(valor) is not None

    def es_float(self, valor):
        return self.regex_float.match(valor) is not None

    def es_cadena(self, valor):
        return self.regex_cadena.match(valor) is not None

    def existe_variable(self, nombre):
        return nombre in self.tabla_simbolos

    def validar_variable(self, nombre):
        if not self.existe_variable(nombre):
            self.registrar_error("E007")

    def tipo_variable(self, nombre):
        self.validar_variable(nombre)
        return self.tabla_simbolos[nombre]

    def nombre_asm(self, nombre):
        return f"V_{nombre}"

    def nombre_txt(self, nombre):
        return f"TXT_{nombre}"

    def operando_asm(self, valor):
        if self.es_entero(valor):
            return valor

        self.validar_variable(valor)
        return self.nombre_asm(valor)

    def agregar_inicio(self):
        if self.inicio_encontrado:
            self.registrar_error("E018")

        self.inicio_encontrado = True

    def declarar_variable(self, linea):
        match = self.regex_declaracion.match(linea)

        if not match:
            self.registrar_error("E005")

        nombre = match.group(1)
        tipo = match.group(2)

        if not self.es_id_valido(nombre):
            self.registrar_error("E005")

        if self.existe_variable(nombre):
            self.registrar_error("E006")

        self.tabla_simbolos[nombre] = tipo

        if tipo == "ENT":
            self.data_asm.append(f"{self.nombre_asm(nombre)} dw 0")
            self.data_asm.append(f"{self.nombre_txt(nombre)} db 6, ?, 7 dup(24h)")

        elif tipo == "FLOAT":
            # FLOAT se conserva a nivel de palabra entera por limitaciones del objetivo 8086 sin FPU.
            self.data_asm.append(f"{self.nombre_asm(nombre)} dw 0 ; FLOAT limitado")
            self.data_asm.append(f"{self.nombre_txt(nombre)} db 6, ?, 7 dup(24h)")

        elif tipo == "CAD":
            self.data_asm.append(f"{self.nombre_asm(nombre)} db 100, ?, 100 dup(24h)")

    def generar_imprimir(self, linea):
        match = self.regex_imprimir.match(linea)

        if not match:
            self.registrar_error("E008")

        expresion = match.group(1).strip()

        if self.es_cadena(expresion):
            nombre_msg = f"MSJ_{self.contador_mensajes}"
            self.data_asm.append(f"{nombre_msg} db {expresion},24h")
            self.code_asm.append(f"\tIMPRIMIR {nombre_msg}")
            self.code_asm.append("\tIMPRIMIR salto")
            self.contador_mensajes += 1

        elif self.es_entero(expresion):
            nombre_msg = f"MSJ_{self.contador_mensajes}"
            self.data_asm.append(f'{nombre_msg} db "{expresion}",24h')
            self.code_asm.append(f"\tIMPRIMIR {nombre_msg}")
            self.code_asm.append("\tIMPRIMIR salto")
            self.contador_mensajes += 1

        elif self.es_id_valido(expresion):
            self.validar_variable(expresion)
            tipo = self.tipo_variable(expresion)

            if tipo == "CAD":
                self.code_asm.append(f"\tIMPRIMIR {self.nombre_asm(expresion)}+2")
            else:
                self.generar_conversion_dinamica(
                    self.nombre_asm(expresion),
                    self.nombre_txt(expresion)
                )
                self.code_asm.append(f"\tIMPRIMIR {self.nombre_txt(expresion)}+2")

            self.code_asm.append("\tIMPRIMIR salto")

        else:
            self.registrar_error("E008")

    def generar_leer(self, linea):
        match = self.regex_leer.match(linea)

        if not match:
            self.registrar_error("E009")

        nombre = match.group(1)

        if not self.es_id_valido(nombre):
            self.registrar_error("E009")

        self.validar_variable(nombre)
        tipo = self.tipo_variable(nombre)

        if tipo == "CAD":
            self.code_asm.append(f"\tLEER {self.nombre_asm(nombre)}")
            self.code_asm.append("\tIMPRIMIR salto")
        else:
            nombre_txt = self.nombre_txt(nombre)
            nombre_var = self.nombre_asm(nombre)
            etiqueta = self.contador_mensajes
            self.contador_mensajes += 1

            self.code_asm.append(f"\tLEER {nombre_txt}")

            self.code_asm.append("\txor ax, ax")
            self.code_asm.append("\txor cx, cx")
            self.code_asm.append(f"\tmov cl, {nombre_txt}[1]")
            self.code_asm.append(f"\tmov si, offset {nombre_txt}")
            self.code_asm.append("\tadd si, 2")

            self.code_asm.append(f"LEER_NUM_{etiqueta}:")
            self.code_asm.append("\tcmp cl, 0")
            self.code_asm.append(f"\tje FIN_LEER_NUM_{etiqueta}")
            self.code_asm.append("\tmov bx, 10")
            self.code_asm.append("\tmul bx")
            self.code_asm.append("\tmov bl, [si]")
            self.code_asm.append("\tsub bl, 30h")
            self.code_asm.append("\tmov bh, 0")
            self.code_asm.append("\tadd ax, bx")
            self.code_asm.append("\tinc si")
            self.code_asm.append("\tdec cl")
            self.code_asm.append(f"\tjmp LEER_NUM_{etiqueta}")

            self.code_asm.append(f"FIN_LEER_NUM_{etiqueta}:")
            self.code_asm.append(f"\tmov {nombre_var}, ax")

            self.generar_conversion_dinamica(nombre_var, nombre_txt)
            self.code_asm.append("\tIMPRIMIR salto")

    def generar_conversion_dinamica(self, nombre_var, nombre_txt):
        etiqueta = self.contador_mensajes
        self.contador_mensajes += 1

        self.code_asm.append(f"\tmov ax, {nombre_var}")
        self.code_asm.append(f"\tmov di, offset {nombre_txt}")
        self.code_asm.append("\tadd di, 2")
        self.code_asm.append("\tcmp ax, 0")
        self.code_asm.append(f"\tjne CONV_{etiqueta}")

        self.code_asm.append("\tmov byte ptr [di], '0'")
        self.code_asm.append("\tinc di")
        self.code_asm.append("\tmov byte ptr [di], 24h")
        self.code_asm.append(f"\tjmp FIN_CONV_{etiqueta}")

        self.code_asm.append(f"CONV_{etiqueta}:")
        self.code_asm.append("\txor cx, cx")
        self.code_asm.append("\tmov bx, 10")

        self.code_asm.append(f"APILAR_DIG_{etiqueta}:")
        self.code_asm.append("\txor dx, dx")
        self.code_asm.append("\tdiv bx")
        self.code_asm.append("\tpush dx")
        self.code_asm.append("\tinc cx")
        self.code_asm.append("\tcmp ax, 0")
        self.code_asm.append(f"\tjne APILAR_DIG_{etiqueta}")

        self.code_asm.append(f"ESCRIBIR_DIG_{etiqueta}:")
        self.code_asm.append("\tpop dx")
        self.code_asm.append("\tadd dl, 30h")
        self.code_asm.append("\tmov [di], dl")
        self.code_asm.append("\tinc di")
        self.code_asm.append(f"\tloop ESCRIBIR_DIG_{etiqueta}")

        self.code_asm.append("\tmov byte ptr [di], 24h")
        self.code_asm.append(f"FIN_CONV_{etiqueta}:")

    def generar_comparacion(self, izq, operador, der, etiqueta_salida):
        self.code_asm.append(f"\tmov ax, {self.operando_asm(izq)}")
        self.code_asm.append(f"\tcmp ax, {self.operando_asm(der)}")
        self.code_asm.append(f"\t{self.saltos_inversos[operador]} {etiqueta_salida}")

    def generar_si(self, linea):
        match = self.regex_si.match(linea)

        if not match:
            self.registrar_error("E010")

        izq = match.group(1)
        operador = match.group(2)
        der = match.group(3)

        etiqueta_sino = f"SINO_{self.contador_ciclos}"
        etiqueta_fin = f"FIN_SI_{self.contador_ciclos}"
        self.contador_ciclos += 1

        self.generar_comparacion(izq, operador, der, etiqueta_sino)

        self.pila_bloques.append({
            "tipo": "SI",
            "sino": etiqueta_sino,
            "fin": etiqueta_fin,
            "tiene_sino": False
        })


    def generar_sino(self):
        if not self.pila_bloques:
            self.registrar_error("E012")

        bloque = self.pila_bloques.pop()

        if bloque["tipo"] != "SI" or bloque.get("tiene_sino"):
            self.registrar_error("E012")

        self.code_asm.append(f"\tjmp {bloque['fin']}")
        self.code_asm.append(f"{bloque['sino']}:")

        bloque["tiene_sino"] = True
        self.pila_bloques.append(bloque)

    def cerrar_fin(self):
        if not self.pila_bloques:
            self.registrar_error("E012")

        bloque = self.pila_bloques.pop()

        if bloque["tipo"] != "SI":
            self.registrar_error("E012")

        if not bloque.get("tiene_sino"):
            self.code_asm.append(f"{bloque['sino']}:")

        self.code_asm.append(f"{bloque['fin']}:")

    def generar_mientras(self, linea):
        match = self.regex_mientras.match(linea)

        if not match:
            self.registrar_error("E011")

        izq = match.group(1)
        operador = match.group(2)
        der = match.group(3)

        etiqueta_inicio = f"MIENTRAS_{self.contador_ciclos}"
        etiqueta_fin = f"FIN_MIENTRAS_{self.contador_ciclos}"
        self.contador_ciclos += 1

        self.code_asm.append(f"{etiqueta_inicio}:")
        self.generar_comparacion(izq, operador, der, etiqueta_fin)

        self.pila_bloques.append({
            "tipo": "MIENTRAS",
            "inicio": etiqueta_inicio,
            "fin": etiqueta_fin
        })

    def generar_for(self, linea):
        match = self.regex_for.match(linea)

        if not match:
            self.registrar_error("E001")

        variable_control = match.group(1)
        expresion_inicio = match.group(2)
        expresion_fin = match.group(3)

        self.validar_variable(variable_control)

        if not self.regex_exp_num_simple.match(expresion_inicio):
            self.registrar_error("E016")

        if not self.regex_exp_num_simple.match(expresion_fin):
            self.registrar_error("E016")

        self.pila_bloques.append({
            "tipo": "FOR"
        })

    def cerrar_finm(self):
        if not self.pila_bloques:
            self.registrar_error("E013")

        bloque = self.pila_bloques.pop()

        if bloque["tipo"] == "MIENTRAS":
            self.code_asm.append(f"\tjmp {bloque['inicio']}")
            self.code_asm.append(f"{bloque['fin']}:")
        elif bloque["tipo"] == "FOR":
            pass
        else:
            self.registrar_error("E013")

    def generar_asignacion(self, linea):
        match = self.regex_asignacion.match(linea)

        if not match:
            self.registrar_error("E014")

        destino = match.group(1)
        expresion = match.group(2).strip()

        if not self.es_id_valido(destino):
            self.registrar_error("E014")

        self.validar_variable(destino)

        tipo_destino = self.tipo_variable(destino)

        if tipo_destino == "CAD":
            if not self.es_cadena(expresion):
                self.registrar_error("E015")

            nombre_temp = f"CAD_TEMP_{self.contador_mensajes}"
            etiqueta = f"COPIAR_CAD_{self.contador_mensajes}"
            self.contador_mensajes += 1

            self.data_asm.append(f"{nombre_temp} db {expresion},24h")

            self.code_asm.append(f"\tlea si, {nombre_temp}")
            self.code_asm.append(f"\tlea di, {self.nombre_asm(destino)}+2")
            self.code_asm.append(f"{etiqueta}:")
            self.code_asm.append("\tmov al, [si]")
            self.code_asm.append("\tmov [di], al")
            self.code_asm.append("\tinc si")
            self.code_asm.append("\tinc di")
            self.code_asm.append("\tcmp al, 24h")
            self.code_asm.append(f"\tjne {etiqueta}")
            return

        match_exp = self.regex_exp_num_simple.match(expresion)

        if not match_exp:
            self.registrar_error("E016")

        op1 = match_exp.group(1)
        operador = match_exp.group(2)
        op2 = match_exp.group(3)

        self.code_asm.append(f"\tmov ax, {self.operando_asm(op1)}")

        if operador is not None:
            if operador == "+":
                self.code_asm.append(f"\tadd ax, {self.operando_asm(op2)}")

            elif operador == "-":
                self.code_asm.append(f"\tsub ax, {self.operando_asm(op2)}")

            elif operador == "*":
                self.code_asm.append(f"\tmov bx, {self.operando_asm(op2)}")
                self.code_asm.append("\tmul bx")

            elif operador == "/":
                self.code_asm.append(f"\tmov bx, {self.operando_asm(op2)}")
                self.code_asm.append("\txor dx, dx")
                self.code_asm.append("\tdiv bx")

            elif operador == "%":
                self.code_asm.append(f"\tmov bx, {self.operando_asm(op2)}")
                self.code_asm.append("\txor dx, dx")
                self.code_asm.append("\tdiv bx")
                self.code_asm.append("\tmov ax, dx")

            elif operador == "^":
                etiqueta = self.contador_elevacion
                self.contador_elevacion += 1

                self.code_asm.append("\tmov bx, ax")
                self.code_asm.append(f"\tmov cx, {self.operando_asm(op2)}")
                self.code_asm.append("\tmov ax, 1")
                self.code_asm.append(f"elevar_{etiqueta}:")
                self.code_asm.append("\tcmp cx, 0")
                self.code_asm.append(f"\tje fin_elevar_{etiqueta}")
                self.code_asm.append("\tmul bx")
                self.code_asm.append("\tdec cx")
                self.code_asm.append(f"\tjmp elevar_{etiqueta}")
                self.code_asm.append(f"fin_elevar_{etiqueta}:")

            else:
                self.registrar_error("E017")

        self.code_asm.append(f"\tmov {self.nombre_asm(destino)}, ax")
        self.generar_conversion_dinamica(
            self.nombre_asm(destino),
            self.nombre_txt(destino)
        )

    def compilar(self, ruta_fuente, ruta_salida):
        try:
            if not os.path.exists(ruta_fuente):
                self.registrar_error("E000")

            with open(ruta_fuente, "r", encoding="utf-8") as archivo:
                lineas = [linea.rstrip("\n") for linea in archivo.readlines()]

            for linea in lineas:
                linea_limpia = linea.strip()

                if not linea_limpia or linea_limpia.startswith("//"):
                    self.linea_actual += 1
                    continue

                partes = linea_limpia.split()
                token_inicial = partes[0] if partes else ""

                if token_inicial == "INICIO:":
                    self.agregar_inicio()

                elif not self.inicio_encontrado:
                    self.registrar_error("E019")

                elif token_inicial == "INI_VAR":
                    self.en_bloque_variables = True

                elif token_inicial == "FIN_VAR":
                    self.en_bloque_variables = False

                elif self.regex_declaracion.match(linea_limpia):
                    if not self.en_bloque_variables:
                        self.registrar_error("E020")
                    self.declarar_variable(linea_limpia)

                elif self.en_bloque_variables:
                    self.registrar_error("E005")

                elif self.regex_imprimir.match(linea_limpia):
                    self.generar_imprimir(linea_limpia)

                elif self.regex_leer.match(linea_limpia):
                    self.generar_leer(linea_limpia)

                elif self.regex_si.match(linea_limpia):
                    self.generar_si(linea_limpia)

                elif token_inicial == "SINO":
                    self.generar_sino()

                elif token_inicial == "FIN":
                    self.cerrar_fin()

                elif self.regex_mientras.match(linea_limpia):
                    self.generar_mientras(linea_limpia)

                elif self.regex_for.match(linea_limpia):
                    self.generar_for(linea_limpia)

                elif token_inicial == "FINM":
                    self.cerrar_finm()

                elif self.regex_asignacion.match(linea_limpia):
                    self.generar_asignacion(linea_limpia)

                else:
                    self.registrar_error("E001")

                self.linea_actual += 1

            if not self.inicio_encontrado:
                self.registrar_error("E002")

            if self.en_bloque_variables:
                self.registrar_error("E003")

            if self.pila_bloques:
                self.registrar_error("E004")

            self.escribir_asm(ruta_salida)

        except ErrorCompilacion:
            self.reportar_errores()

    def escribir_asm(self, ruta_salida):
        asm_final = []

        asm_final.extend(self.macros_asm)
        asm_final.append(".MODEL SMALL")
        asm_final.append(".CODE")
        asm_final.append("Inicio:")
        asm_final.append("	mov Ax, @Data")
        asm_final.append("	mov Ds, Ax")
        asm_final.extend(self.code_asm)
        asm_final.append("	mov ax, 4C00h")
        asm_final.append("	int 21h")
        asm_final.extend(self.data_asm)
        asm_final.append(".STACK")
        asm_final.append("END Inicio")

        with open(ruta_salida, "w", encoding="utf-8") as salida:
            salida.write("\n".join(asm_final))

        print(f"\n[ÉXITO] Archivo generado en: {os.path.abspath(ruta_salida)}")


if __name__ == "__main__":
    comp = CompiladorKimo()

    ruta_origen = r"C:\Users\jimen\Documents\Codigos 6to\Automatas ll\Kimo\Compilador Kimo\programa.kimo"
    ruta_destino = r"C:\Users\jimen\Documents\Codigos 6to\Automatas ll\Kimo\Compilador Kimo\salida.asm"

    comp.compilar(ruta_origen, ruta_destino)
