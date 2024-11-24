"""----------------------------------------------------------
Project: Adversarial Caterpillars

Date: 27-Nov-2024
TEAM 13
Authors:
    A01799931 Andrea Doce
    A01750748 Manuel Olmos
----------------------------------------------------------"""
from dagor import JugadorOrugas, TiroInvalido

class JugadorOrugasEquipo13(JugadorOrugas):
    """
    JugadorOrugasEquipo13 is a class representing a player in the Caterpillars game for team 13.
    This class contains methods to evaluate the game board using a heuristic and to make a move.
    \nMethods:
        \theuristica(tablero): Evaluates the given game board and returns a heuristic value.
        \ttira(tablero): Determines the next move based on the current game board and returns the move.
    """

    def heuristic(self, tablero):
        """
        Heuristic function that evaluates the given game board and returns a heuristic value.
        """
        # Número de movimientos posibles para el oponente
        opponent_moves = len(self.posiciones_siguientes((self.contrario.simbolo, tablero)))
        
        # Número de movimientos posibles para ti
        my_moves = len(self.posiciones_siguientes((self.simbolo, tablero)))
        
        # Heurística: maximizar tus movimientos y minimizar los del oponente
        # creo que esta forma de evaluar la heurística es muy simple, pero es un buen punto de partida
        heuristic_value = my_moves - opponent_moves
        
        return heuristic_value

    def es_tiro_valido(self, tablero, movimiento):
        """
        Checks if a move is valid based on the current game board.
        """
        # generar lista de posiciones válidas
        posiciones_validas = [pos[1] for pos in self.posiciones_siguientes((self.simbolo, tablero))]
        #print(f"Posiciones válidas: {posiciones_validas}")  # Imprimir las posiciones válidas
        return movimiento in posiciones_validas # regresar si el movimiento es válido

    def simula_tiro(self, tablero, movimiento):
        """
        Simulates a move on the board and returns the new board state.
        """
        turno_actual = self.simbolo
        turno_siguiente = self.contrario.simbolo
        nuevo_tablero = [list(fila) for fila in tablero]

        for r in range(len(nuevo_tablero)):
            for c in range(len(nuevo_tablero[r])):
                if nuevo_tablero[r][c] == turno_actual:
                    nuevo_tablero[r][c] = turno_actual.lower()
                elif nuevo_tablero[r][c] == turno_actual.lower():
                    nuevo_tablero[r][c] = ' '

        # Esto nos asegura que el movimiento sea una tupla de dos enteros
        # para que no haya errores al intentar acceder a la posición del tablero
        if isinstance(movimiento, tuple) and len(movimiento) == 2:
            nuevo_tablero[movimiento[0]][movimiento[1]] = turno_actual
        else:
            raise TiroInvalido("Movimiento inválido: debe ser una tupla de dos enteros")

        # regresa el nuevo tablero con el movimiento simulado
        # simular el movimiento nos ayuda a evaluar el tablero sin modificar el tablero original
        return (turno_siguiente, tuple(tuple(fila) for fila in nuevo_tablero))

    def tira(self, posicion):
        """
        Determines the next move based on the current game position and returns the move.
        """
        # obtener el tablero de la posición actual
        tablero = posicion[1]
        # obtener los movimientos posibles
        posibles = [(pos[0], pos[1]) for pos in self.posiciones_siguientes((self.simbolo, tablero))]
        if not posibles:
            raise TiroInvalido("No hay movimientos posibles") # si no hay movimientos posibles, lanzar excepción
    
        best_move = posibles[0]
        # Inicializar el mejor valor con el peor valor posible osea negativo infinito
        # usamos negativo infinito para asegurarnos de que cualquier valor heurístico sea mejor
        best_value = float('-inf')
        
        for movimiento in posibles:
            try:
                #print(f"Evaluando movimiento: {movimiento}")  # Imprimir el movimiento que se está evaluando
                if not self.es_tiro_valido(tablero, movimiento):
                    #print(f"Movimiento inválido: {movimiento}")  # Imprimir si el movimiento es inválido
                    continue
                # Simulate the move
                tablero_simulado = self.simula_tiro(tablero, movimiento)
                # Evaluate the move using the heuristic
                # nuevamente, la heurística es muy simple
                value = self.heuristic(tablero_simulado[1])
                #print(f"Valor heurístico para {movimiento}: {value}")  # Imprimir el valor heurístico
                if value > best_value:
                    best_value = value
                    best_move = movimiento
            except TiroInvalido:
                #print(f"Excepción TiroInvalido para el movimiento: {movimiento}")  # Imprimir si se lanza una excepción
                continue
        
        #print(f"Mejor movimiento seleccionado: {best_move} con valor heurístico: {best_value}")  # Imprimir el mejor movimiento seleccionado
        return best_move