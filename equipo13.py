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
        best_value = float('-inf')
        
        for movimiento in posibles:
            try:
                if not self.es_tiro_valido(tablero, movimiento):
                    continue
                # Simulate the move
                tablero_simulado = self.simula_tiro(tablero, movimiento)
                # Evaluate the move using the minimax algorithm
                value = self.minimax(tablero_simulado[1], 4, False)  # Depth is set to 3 for example
                if value > best_value:
                    best_value = value
                    best_move = movimiento
            except TiroInvalido:
                continue
        
        return best_move
    
    def terminal(self, tablero):
        """
        Checks if the game has reached a terminal state.
        """
        # Check if there are no valid moves for either player
        if not self.posiciones_siguientes((self.simbolo, tablero)) and not self.posiciones_siguientes((self.contrario.simbolo, tablero)):
            return True
        return False

    def minimax(self, tablero, depth, maximizing_player):
        """
        Minimax algorithm to determine the best move based on the current game board.
        A player that is maximizing will try to maximize the heuristic value, 
        while a player that is minimizing will try to minimize the heuristic value.
        """
        if depth == 0 or self.terminal(tablero):
            return self.heuristic(tablero)
        
        if maximizing_player:
            max_eval = float('-inf')
            for movimiento in self.posiciones_siguientes((self.simbolo, tablero)):
                if not self.es_tiro_valido(tablero, movimiento):
                    continue
                tablero_simulado = self.simula_tiro(tablero, movimiento)
                eval = self.minimax(tablero_simulado[1], depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for movimiento in self.posiciones_siguientes((self.contrario.simbolo, tablero)):
                if not self.es_tiro_valido(tablero, movimiento):
                    continue
                tablero_simulado = self.simula_tiro(tablero, movimiento)
                eval = self.minimax(tablero_simulado[1], depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval