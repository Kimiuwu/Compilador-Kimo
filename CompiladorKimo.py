import re
import os


class CompiladorKimo:
    def __init__(self):
        self.linea_actual = 1

        self.macros_asm = []
        self.data_asm = []
        self.code_asm = []

        self.tabla_variables = {}

        self.pila_bloques = []
        self.contador_ciclos = 0
        self.contador_mensajes = 0
        self.contador_elevacion = 0

        self.en_bloque_variables = False
        self.inicio_encontrado = False

        self.regex_id = re.compile(r"^[A-Z][A-Z0-9_]*$")
        self.regex_entero = re.compile(r"^[+-]?[0-9]+$")
        self.regex_cadena = re.compile(r'^"[^"]*"$')

        self.regex_declaracion = re.compile(
            r"^\s*([A-Z][A-Z0-9_]*)\s*:\s*(ENT|FLOAT|CAD)\s*;$"
        )

        self.regex_imprimir = re.compile(
            r"^\s*IMPRIMIR\s*\((.*?)\)\s*;$"
        )

        self.regex_leer = re.compile(
            r"^\s*LEER\s*\(([A-Z][A-Z0-9_]*)\)\s*;$"
        )

        self.regex_si = re.compile(
            r"^\s*SI\s+([A-Z][A-Z0-9_]*|[+-]?[0-9]+)\s*(>|<|!=|==|>=|<=)\s*"
            r"([A-Z][A-Z0-9_]*|[+-]?[0-9]+)\s+ENTONCES$"
        )

        self.regex_mientras = re.compile(
            r"^\s*MIENTRAS\s+([A-Z][A-Z0-9_]*|[+-]?[0-9]+)\s*(>|<|!=|==|>=|<=)\s*"
            r"([A-Z][A-Z0-9_]*|[+-]?[0-9]+)\s+HACER$"
        )

        self.regex_asignacion = re.compile(
            r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*;$"
        )

        self.saltos_inversos = {
            ">": "JLE",
            "<": "JGE",
            ">=": "JL",
            "<=": "JG",
            "==": "JNE",
            "!=": "JE"
        }

        self.preparar_estructura_base()

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

    def compilador_error(self, mensaje):
        print(f"\n[Error] Línea {self.linea_actual}: {mensaje}")
        exit(1)

    def nombre_asm(self, nombre):
        return f"var_{nombre}"

    def nombre_txt(self, nombre):
        return f"txt_{nombre}"

    def existe_variable(self, nombre):
        return nombre in self.tabla_variables

    def validar_variable(self, nombre):
        if not self.existe_variable(nombre):
            self.compilador_error(f"La variable '{nombre}' no ha sido declarada.")

    def es_numero(self, valor):
        return self.regex_entero.match(valor) is not None

    def operando_asm(self, valor):
        if self.es_numero(valor):
            return valor

        self.validar_variable(valor)
        return self.nombre_asm(valor)

    def agregar_inicio(self):
        if self.inicio_encontrado:
            self.compilador_error("INICIO: ya fue declarado.")

        self.inicio_encontrado = True

    def declarar_variable(self, linea):
        match = self.regex_declaracion.match(linea)

        if not match:
            self.compilador_error("Declaración inválida. Use: A : ENT;")

        nombre = match.group(1)
        tipo = match.group(2)

        if self.existe_variable(nombre):
            self.compilador_error(f"La variable '{nombre}' ya fue declarada.")

        self.tabla_variables[nombre] = {
            "tipo": tipo,
            "valor": False
        }

        nombre_var = self.nombre_asm(nombre)
        nombre_txt = self.nombre_txt(nombre)

        if tipo == "ENT":
            self.data_asm.append(f"{nombre_var} dw 0")
            self.data_asm.append(f"{nombre_txt} db 4, ?, 5 dup(24h)")

        elif tipo == "FLOAT":
            self.data_asm.append(f"{nombre_var} dw 0 ; FLOAT limitado en esta versión")
            self.data_asm.append(f"{nombre_txt} db 4, ?, 5 dup(24h)")

        elif tipo == "CAD":
            self.data_asm.append(f"{nombre_var} db 100, ?, 100 dup(24h)")

    def generar_imprimir(self, linea):
        match = self.regex_imprimir.match(linea)

        if not match:
            self.compilador_error("Sintaxis inválida en IMPRIMIR.")

        expresion = match.group(1).strip()

        if self.regex_cadena.match(expresion):
            nombre_msg = f"msg_{self.contador_mensajes}"
            self.data_asm.append(f'{nombre_msg} db {expresion},24h')
            self.code_asm.append(f"\tIMPRIMIR {nombre_msg}")
            self.code_asm.append("\tIMPRIMIR salto")
            self.contador_mensajes += 1

        elif self.regex_id.match(expresion):
            self.validar_variable(expresion)

            tipo = self.tabla_variables[expresion]["tipo"]

            if tipo == "CAD":
                self.code_asm.append(f"\tIMPRIMIR {self.nombre_asm(expresion)}+2")
                self.code_asm.append("\tIMPRIMIR salto")
            else:
                self.code_asm.append(f"\tIMPRIMIR {self.nombre_txt(expresion)}+2")
                self.code_asm.append("\tIMPRIMIR salto")

        elif self.es_numero(expresion):
            nombre_msg = f"msg_{self.contador_mensajes}"
            self.data_asm.append(f'{nombre_msg} db "{expresion}",24h')
            self.code_asm.append(f"\tIMPRIMIR {nombre_msg}")
            self.code_asm.append("\tIMPRIMIR salto")
            self.contador_mensajes += 1

        else:
            self.compilador_error("IMPRIMIR solo acepta cadenas, variables o enteros directos.")

    def generar_leer(self, linea):
        match = self.regex_leer.match(linea)

        if not match:
            self.compilador_error("Sintaxis inválida en LEER.")

        nombre = match.group(1)
        self.validar_variable(nombre)

        tipo = self.tabla_variables[nombre]["tipo"]
        nombre_var = self.nombre_asm(nombre)
        nombre_txt = self.nombre_txt(nombre)

        if tipo == "CAD":
            self.code_asm.append(f"\tLEER {nombre_var}")
            self.code_asm.append("\tIMPRIMIR salto")

        else:
            self.code_asm.append(f"\tLEER {nombre_txt}")
            self.code_asm.append(f"\tmov al, {nombre_txt}[2]")
            self.code_asm.append("\tsub al, 30h")
            self.code_asm.append("\tmov ah, 0")
            self.code_asm.append(f"\tmov {nombre_var}, ax")
            self.generar_conversion_dos_digitos(nombre_var, nombre_txt)
            self.code_asm.append("\tIMPRIMIR salto")

        self.tabla_variables[nombre]["valor"] = True

    def generar_conversion_dos_digitos(self, nombre_var_asm, nombre_txt_asm):
        self.code_asm.append(f"\tmov ax, {nombre_var_asm}")
        self.code_asm.append("\tmov bx, 10")
        self.code_asm.append("\txor dx, dx")
        self.code_asm.append("\tdiv bx")
        self.code_asm.append("\tadd al, '0'")
        self.code_asm.append("\tadd dl, '0'")
        self.code_asm.append(f"\tmov {nombre_txt_asm}[2], al")
        self.code_asm.append(f"\tmov {nombre_txt_asm}[3], dl")
        self.code_asm.append(f"\tmov {nombre_txt_asm}[4], 24h")

    def generar_comparacion(self, izq, operador, der, etiqueta_salida):
        self.code_asm.append(f"\tmov ax, {self.operando_asm(izq)}")
        self.code_asm.append(f"\tcmp ax, {self.operando_asm(der)}")
        self.code_asm.append(f"\t{self.saltos_inversos[operador]} {etiqueta_salida}")

    def generar_si(self, linea):
        match = self.regex_si.match(linea)

        if not match:
            self.compilador_error("Sintaxis inválida en SI.")

        izq = match.group(1)
        operador = match.group(2)
        der = match.group(3)

        etiqueta_fin = f"fin_if_{self.contador_ciclos}"
        self.contador_ciclos += 1

        self.generar_comparacion(izq, operador, der, etiqueta_fin)

        self.pila_bloques.append({
            "tipo": "SI",
            "fin": etiqueta_fin
        })

    def cerrar_fin(self):
        if not self.pila_bloques:
            self.compilador_error("FIN encontrado sin bloque SI abierto.")

        bloque = self.pila_bloques.pop()

        if bloque["tipo"] != "SI":
            self.compilador_error("FIN solo puede cerrar un bloque SI.")

        self.code_asm.append(f"{bloque['fin']}:")

    def generar_mientras(self, linea):
        match = self.regex_mientras.match(linea)

        if not match:
            self.compilador_error("Sintaxis inválida en MIENTRAS.")

        izq = match.group(1)
        operador = match.group(2)
        der = match.group(3)

        etiqueta_inicio = f"while_{self.contador_ciclos}"
        etiqueta_fin = f"fin_while_{self.contador_ciclos}"
        self.contador_ciclos += 1

        self.code_asm.append(f"{etiqueta_inicio}:")
        self.generar_comparacion(izq, operador, der, etiqueta_fin)

        self.pila_bloques.append({
            "tipo": "MIENTRAS",
            "inicio": etiqueta_inicio,
            "fin": etiqueta_fin
        })

    def cerrar_finm(self):
        if not self.pila_bloques:
            self.compilador_error("FINM encontrado sin ciclo abierto.")

        bloque = self.pila_bloques.pop()

        if bloque["tipo"] != "MIENTRAS":
            self.compilador_error("FINM solo puede cerrar un bloque MIENTRAS.")

        self.code_asm.append(f"\tjmp {bloque['inicio']}")
        self.code_asm.append(f"{bloque['fin']}:")

    def generar_asignacion(self, linea):
        match = self.regex_asignacion.match(linea)

        if not match:
            self.compilador_error("Asignación inválida.")

        destino = match.group(1)
        expresion = match.group(2).strip()

        self.validar_variable(destino)

        tipo_destino = self.tabla_variables[destino]["tipo"]
        nombre_destino = self.nombre_asm(destino)

        if tipo_destino == "CAD":
            if not self.regex_cadena.match(expresion):
                self.compilador_error("Una variable CAD solo puede recibir una cadena directa en esta versión.")

            nombre_msg = f"cad_temp_{self.contador_mensajes}"
            etiqueta_copia = f"copiar_cadena_{self.contador_mensajes}"

            self.data_asm.append(f'{nombre_msg} db {expresion},24h')

            self.code_asm.append(f"\tlea si, {nombre_msg}")
            self.code_asm.append(f"\tlea di, {nombre_destino}+2")
            self.code_asm.append(f"{etiqueta_copia}:")
            self.code_asm.append("\tmov al, [si]")
            self.code_asm.append("\tmov [di], al")
            self.code_asm.append("\tinc si")
            self.code_asm.append("\tinc di")
            self.code_asm.append("\tcmp al, 24h")
            self.code_asm.append(f"\tjne {etiqueta_copia}")

            self.contador_mensajes += 1
            self.tabla_variables[destino]["valor"] = True
            return

        tokens = expresion.split()

        if len(tokens) == 0:
            self.compilador_error("Expresión vacía.")

        if len(tokens) % 2 == 0:
            self.compilador_error("Expresión aritmética inválida. Use espacios: A = B + 5;")

        self.code_asm.append(f"\tmov ax, {self.operando_asm(tokens[0])}")

        i = 1
        while i < len(tokens):
            operador = tokens[i]
            operando = tokens[i + 1]
            op_asm = self.operando_asm(operando)

            if operador == "+":
                self.code_asm.append(f"\tadd ax, {op_asm}")

            elif operador == "-":
                self.code_asm.append(f"\tsub ax, {op_asm}")

            elif operador == "*":
                self.code_asm.append(f"\tmov bx, {op_asm}")
                self.code_asm.append("\tmul bx")

            elif operador == "/":
                self.code_asm.append(f"\tmov bx, {op_asm}")
                self.code_asm.append("\txor dx, dx")
                self.code_asm.append("\tdiv bx")

            elif operador == "%":
                self.code_asm.append(f"\tmov bx, {op_asm}")
                self.code_asm.append("\txor dx, dx")
                self.code_asm.append("\tdiv bx")
                self.code_asm.append("\tmov ax, dx")

            elif operador == "^":
                etiqueta = self.contador_elevacion
                self.contador_elevacion += 1

                self.code_asm.append("\tmov bx, ax")
                self.code_asm.append(f"\tmov cx, {op_asm}")
                self.code_asm.append("\tmov ax, 1")
                self.code_asm.append(f"elevar_{etiqueta}:")
                self.code_asm.append("\tcmp cx, 0")
                self.code_asm.append(f"\tje fin_elevar_{etiqueta}")
                self.code_asm.append("\tmul bx")
                self.code_asm.append("\tdec cx")
                self.code_asm.append(f"\tjmp elevar_{etiqueta}")
                self.code_asm.append(f"fin_elevar_{etiqueta}:")

            else:
                self.compilador_error(f"Operador inválido: {operador}")

            i += 2

        self.code_asm.append(f"\tmov {nombre_destino}, ax")
        self.generar_conversion_dos_digitos(nombre_destino, self.nombre_txt(destino))

        self.tabla_variables[destino]["valor"] = True

    def compilar(self, ruta_fuente, ruta_salida):
        if not os.path.exists(ruta_fuente):
            print(f"Error: El archivo {ruta_fuente} no existe.")
            return

        with open(ruta_fuente, "r", encoding="utf-8") as f:
            lineas = [l.rstrip("\n") for l in f.readlines()]

        for linea in lineas:
            linea_limpia = linea.strip()

            if not linea_limpia or linea_limpia.startswith("//"):
                self.linea_actual += 1
                continue

            palabras = linea_limpia.split()
            token_inicial = palabras[0] if palabras else ""

            if token_inicial == "INICIO:":
                self.agregar_inicio()

            elif token_inicial == "INI_VAR":
                self.en_bloque_variables = True

            elif token_inicial == "FIN_VAR":
                self.en_bloque_variables = False

            elif self.en_bloque_variables:
                self.declarar_variable(linea_limpia)

            elif self.regex_imprimir.match(linea_limpia):
                self.generar_imprimir(linea_limpia)

            elif self.regex_leer.match(linea_limpia):
                self.generar_leer(linea_limpia)

            elif self.regex_si.match(linea_limpia):
                self.generar_si(linea_limpia)

            elif token_inicial == "FIN":
                self.cerrar_fin()

            elif self.regex_mientras.match(linea_limpia):
                self.generar_mientras(linea_limpia)

            elif token_inicial == "FINM":
                self.cerrar_finm()

            elif self.regex_asignacion.match(linea_limpia):
                self.generar_asignacion(linea_limpia)

            else:
                self.compilador_error(f"Instrucción desconocida: {linea_limpia}")

            self.linea_actual += 1

        if not self.inicio_encontrado:
            self.compilador_error("Falta INICIO:")

        if self.en_bloque_variables:
            self.compilador_error("Falta FIN_VAR para cerrar el bloque de variables.")

        if self.pila_bloques:
            self.compilador_error("Existen bloques SI o MIENTRAS sin cerrar.")

        asm_final = []
        asm_final.extend(self.macros_asm)
        asm_final.append(".MODEL SMALL")
        asm_final.extend(self.data_asm)
        asm_final.append(".CODE")
        asm_final.append("Inicio:")
        asm_final.append("\tmov Ax, @Data")
        asm_final.append("\tmov Ds, Ax")
        asm_final.extend(self.code_asm)
        asm_final.append("\tmov ax, 4C00h")
        asm_final.append("\tint 21h")
        asm_final.append(".STACK")
        asm_final.append("END Inicio")

        with open(ruta_salida, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(asm_final))

        print(f"\n[ÉXITO] Archivo generado en: {os.path.abspath(ruta_salida)}")


if __name__ == "__main__":
    comp = CompiladorKimo()

    ruta_origen = r"C:\Users\jimen\Documents\Codigos 6to\Automatas ll\Kimo\Compilador Kimo\programa.kimo"
    ruta_destino = r"C:\Users\jimen\Documents\Codigos 6to\Automatas ll\Kimo\Compilador Kimo\salida.asm"

    comp.compilar(ruta_origen, ruta_destino)