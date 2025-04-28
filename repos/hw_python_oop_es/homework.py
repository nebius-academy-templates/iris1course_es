class InfoMessage:
    """Mensaje sobre el entrenamiento."""
    pass


class Training:
    """Clase de entrenamiento de base."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        pass

    def get_distance(self) -> float:
        """Obtiene la distancia en km."""
        pass

    def get_mean_speed(self) -> float:
        """Obtiene la velocidad media."""
        pass

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Devuelve mensaje sobre el entrenamiento completado."""
        pass


class Running(Training):
    """Entrenamiento: correr."""
    pass


class SportsWalking(Training):
    """Entrenamiento: marcha rápida."""
    pass


class Swimming(Training):
    """Entrenamiento: natación."""
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Lee los datos de los sensores."""
    pass


def main(training: Training) -> None:
    """Función principal."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

