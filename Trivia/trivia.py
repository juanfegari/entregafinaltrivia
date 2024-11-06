import csv
import random
from functools import reduce
import itertools

class Maybe:
    def __init__(self, valor):
        self.valor = valor

    def bind(self, func):
        if self.valor is not None:
            try:
                return Maybe(func(self.valor))
            except Exception:
                return Maybe(None)
        return Maybe(None)
    
    def get(self, default=None):
        return self.valor if self.valor is not None else default

def leer_preguntas(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        return [(row[0], row[1:4], row[4]) for row in reader]

def generar_preguntas(preguntas, cantidad=5):
    '''
    Del pool de preguntas, selecciona una cantidad de preguntas al azar
    '''
    for pregunta in random.sample(preguntas, cantidad):
        yield pregunta

def add_comillas_final(s):
    '''
    Agrega comillas al final de un string
    '''
    return s + '"'

def add_comillas_inicio(s):
    '''
    Agrega comillas al inicio de un string
    '''
    return '"' + s

def compose(func1, func2):
    '''
    Compone dos funciones
    '''
    return lambda x: func1(func2(x))

composed_comillas = compose(add_comillas_inicio, add_comillas_final)

calcular_puntaje = lambda respuesta, correcta: 10 if respuesta.strip().lower() == correcta.strip().lower() else 0

def procesar_pregunta(pregunta, opciones, correcta):
    '''
    Muestra la pregunta y las 3 opciones posibles, y solicita al usuario que seleccione una respuesta, luego procesa la respuesta y guarde el puntaje
    '''
    print(f"\n{pregunta}\nA) {opciones[0]}\nB) {opciones[1]}\nC) {opciones[2]}")
    respuesta_usuario = input("Selecciona tu respuesta: ")
    respuesta_comillas = composed_comillas(respuesta_usuario)

    respuesta_maybe = Maybe(respuesta_comillas).bind(lambda x: x if x.strip().lower() in [o.strip().lower() for o in opciones] else None)
    return respuesta_maybe.bind(lambda r: calcular_puntaje(r, correcta)).get(0)

def temporizar(func):
    '''
    Decorador de tiempo, calcula cuanto demora uno en responder las preguntas
    '''
    import time
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo total: {fin - inicio} segundos")
        return resultado
    return wrapper

@temporizar
def jugar_trivia(preguntas):
    '''
    Juega la trivia, seleccionando 5 preguntas al azar y procesandolas
    '''
    preguntas_seleccionadas = generar_preguntas(preguntas)
    puntajes = list(itertools.starmap(procesar_pregunta, preguntas_seleccionadas))
    puntaje_final = reduce(lambda x, y: x + y, puntajes, 0)
    print(f"\nPuntaje final: {puntaje_final} puntos")

if __name__ == "__main__":
    preguntas = leer_preguntas('trivia_questions.csv')
    jugar_trivia(preguntas)