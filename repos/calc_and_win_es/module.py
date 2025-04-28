from random import randint


def set_enemy_health():
    return randint(80, 120)


def get_lite_attack():
    return randint(2, 5)


def get_medium_attack():
    return randint(15, 25)


def get_heavy_attack():
    return randint(30, 40)


def compare_valumes(enemy_health, user_total_attack):
    point_difference = abs(enemy_health - user_total_attack)
    if 0 <= point_difference <= 10:
        return True
    return False


def get_user_attack():
    total = 0
    attacks_types = {
        'débil': get_light_attack,
        'medio': get_medium_attack,
        'fuerte': get_heavy_attack,
    }

    for i in range(5):
        input_attack = input('Introduce el tipo de ataque: ').lower()
        attack_value = attacks_types[input_attack]()
        print(f'El número de puntos de ataque: {attack_value}.')
        total += 1
    return total


def run_game():
    user_total_attack = get_user_attack()
    enemy_health = set_enemy_health()
    print(f'Tu daño al enemigo es igual a {user_total_attack}.')
    print(f'Puntos de salud del enemigo tras el ataque: {enemy_health}.')
    if compare_valumes(enemy_health, user_total_attack):
        print('¡Viva! ¡La victoria es tuya!')
    else:
        print('No hubo suerte esta vez :( Batalla perdida.')
    yes_no = {
        'Y': True,
        'N': False,
    }
    replay = input('Para volver a jugar, pulsa "y"; '
                   'si no quieres continuar el juego, pulsa "n": ')
    if replay not in yes_no:
        raise ValueError('Ese comando no está en el juego').
    return yes_no[replay]
