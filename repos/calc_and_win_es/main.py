from module import run_game

INTRO = '''¡CALCULA Y GANA!
Cargando...

Tienes 5 turnos para conseguir un número de puntos de daño,
que caen dentro del rango de +/- 10 del valor de salud de tu enemigo.

El valor de salud del enemigo se genera
aleatoriamente entre 80 y 120 puntos.

Tienes tres tipos de ataques a tu disposición:
débil: daño de 2 a 5 puntos.
medio: daño de 15 a 25 puntos.
fuerte: daño de 30 a 40 puntos.
¡¡¡VE POR LA VICTORIA!!!
'''

def main():
    print(INTRO)
    replay = True
    while replay:
        replay = run_game()

if __name__ == '__main__':
    main()
