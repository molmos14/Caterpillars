from dagor import JuegoOrugas, JugadorOrugasAleatorio
from equipo13 import JugadorOrugasEquipo13

if __name__ == '__main__':
    juego = JuegoOrugas(
        JugadorOrugasEquipo13('Equipo 13'),
        JugadorOrugasAleatorio('RandomBoy'),
        5, 8)
    juego.inicia(veces=100, delta_max=2)