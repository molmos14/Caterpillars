from dagor import JugadorOrugas, TiroInvalido
import random

class JugadorOrugasEquipo13(JugadorOrugas):
    def heuristic(self, tablero):
        """
        Heurística mejorada para evaluar el tablero.
        """
        opponent_moves = len(self.posiciones_siguientes((self.contrario.simbolo, tablero)))
        my_moves = len(self.posiciones_siguientes((self.simbolo, tablero)))
        return (my_moves * 2) - (opponent_moves * 3)

    def es_tiro_valido(self, tablero, movimiento):
        """
        Asegura que el movimiento es válido dentro del tablero.
        """
        posiciones_validas = [pos[1] for pos in self.posiciones_siguientes((self.simbolo, tablero))]
        return movimiento in posiciones_validas

    def tira(self, posicion):
        """
        Determina el mejor movimiento usando Monte Carlo y Heurística.
        """
        print("Ejecutando tira")
        tablero = posicion[1]
        posibles = [(pos[0], pos[1]) for pos in self.posiciones_siguientes((self.simbolo, tablero))]
        if not posibles:
            print("No hay movimientos posibles en tira")
            return None

        best_move = None
        best_value = float('-inf')

        for movimiento in posibles:
            if not self.es_tiro_valido(tablero, movimiento):
                print(f"Movimiento {movimiento} no es válido")
                continue

            tablero_simulado = self.simula_tiro(tablero, movimiento)
            value = self.monte_carlo(tablero_simulado[1], iteraciones=200)
            print(f"Valor Monte Carlo para {movimiento}: {value}")

            if value > best_value:
                best_value = value
                best_move = movimiento

        print(f"Mejor movimiento: {best_move} con valor: {best_value}")
        return best_move if best_move else posibles[0]

    def monte_carlo(self, tablero, iteraciones=200):
        """
        Método de Monte Carlo para evaluar los movimientos posibles.
        """
        print("Ejecutando monte_carlo")
        posibles = [(pos[0], pos[1]) for pos in self.posiciones_siguientes((self.simbolo, tablero))]
        if not posibles:
            print("No hay movimientos posibles en monte_carlo")
            return -1000  # Penalización para movimientos inválidos

        resultados = {movimiento: 0 for movimiento in posibles}

        for movimiento in posibles:
            for _ in range(iteraciones):
                resultado = self.simular_partida(tablero, movimiento)
                resultados[movimiento] += resultado

        mejor_movimiento = max(resultados, key=resultados.get)
        print(f"Resultados de Monte Carlo: {resultados}")
        return resultados[mejor_movimiento] / iteraciones

    def simular_partida(self, tablero, movimiento):
        """
        Simula una partida aleatoria hasta llegar al estado terminal.
        """
        tablero_simulado = self.simula_tiro(tablero, movimiento)[1]
        turno_actual = self.simbolo

        while not self.terminal(tablero_simulado):
            posibles = self.posiciones_siguientes((turno_actual, tablero_simulado))
            if posibles:
                movimiento = random.choice(posibles)
                tablero_simulado = self.simula_tiro(tablero_simulado, movimiento)[1]
            turno_actual = self.contrario.simbolo if turno_actual == self.simbolo else self.simbolo

        return 1 if turno_actual == self.contrario.simbolo else -1

    def simula_tiro(self, tablero, movimiento):
        """
        Aplica un movimiento simulado al tablero sin modificar el original.
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

        if isinstance(movimiento, tuple) and len(movimiento) == 2:
            nuevo_tablero[movimiento[0]][movimiento[1]] = turno_actual

        return (turno_siguiente, tuple(tuple(fila) for fila in nuevo_tablero))
