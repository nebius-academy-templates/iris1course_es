import re
import pytest
import types
import inspect
from conftest import Capturing

try:
    import homework
except ModuleNotFoundError:
    assert False, 'No se encontró el archivo `homework.py` con el ejercicio.'
except NameError as exc:
    name = re.findall("name '(\w+)' is not defined", str(exc))[0]
    assert False, f'No se encontró la clase {name} en el archivo de los ejercicios.'
except ImportError:
    assert False, 'No se encontró el archivo `homework.py` con el ejercicio.'


def test_read_package():
    assert hasattr(homework, 'read_package'), (
        'Define una función para procesar '
        'paquetes entrantes: `read_package`'
    )
    assert callable(homework.read_package), (
        '`read_package` debe ser una función.'
    )
    assert isinstance(homework.read_package, types.FunctionType), (
        '`read_package` debe ser una función.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (('SWM', [720, 1, 80, 25, 40]), 'Swimming'),
    (('RUN', [15000, 1, 75]), 'Running'),
    (('WLK', [9000, 1, 75, 180]), 'SportsWalking'),
])
def test_read_package_return(input_data, expected):
    result = homework.read_package(*input_data)
    assert result.__class__.__name__ == expected, (
        'La función `read_package` debe devolver la clase '
        'del deporte en función del código de entrenamiento.'
    )


def test_InfoMessage():
    assert inspect.isclass(homework.InfoMessage), (
        '`InfoMessage` debe ser una clase.'
    )
    info_message = homework.InfoMessage
    info_message_signature = inspect.signature(info_message)
    info_message_signature_list = list(info_message_signature.parameters)
    for p in ['training_type', 'duration', 'distance', 'speed', 'calories']:
        assert p in info_message_signature_list, (
            'El método `__init__` de la clase `InfoMessage` debe tener '
            f'un parámetro {p}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    (['Swimming', 1, 75, 1, 80],
        'Tipo de entrenamiento: Natación; '
        'Duración: 1.000 h; '
        'Distancia: 75.000 km; '
        'Vel. promedio: 1.000 km/h; '
        'Calorías quemadas: 80.000.'
     ),
    (['Running', 4, 20, 4, 20],
        'Tipo de entrenamiento: Correr; '
        'Duración: 4.000 h; '
        'Distancia: 20.000 km; '
        'Vel. promedio: 4.000 km/h; '
        'Calorías quemadas: 20.000.'
     ),
    (['SportsWalking', 12, 6, 12, 6],
        'Tipo de entrenamiento: Marcha rápida; '
        'Duración: 12.000 h; '
        'Distancia: 6.000 km; '
        'Vel. promedio: 12.000 km/h; '
        'Calorías quemadas: 6.000.'
     ),
])
def test_InfoMessage_get_message(input_data, expected):
    info_message = homework.InfoMessage(*input_data)
    assert hasattr(info_message, 'get_message'), (
        'Crea un método `get_message` en la clase `InfoMessage`.'
    )
    assert callable(info_message.get_message), (
        '`get_message` en la clase `InfoMessage` debe ser un método.'
    )
    result = info_message.get_message()
    assert isinstance(result, str), (
        'El método `get_message` en la clase `InfoMessage`'
        'debe devolver un valor de tipo `str`'
    )
    assert result == expected, (
        'El método `get_message` de la clase `InfoMessage` debe devolver un string.\n'
        'Ejemplo: \n'
        'Tipo de entrenamiento: Natación; '
        'Duración: 1.000 h; '
        'Distancia: 75.000 km; '
        'Vel. promedio: 1.000 km/h; '
        'Calorías quemadas: 80.000.'
    )


def test_Training():
    assert inspect.isclass(homework.Training), (
        '`Training` debe ser una clase.'
    )
    for attr, value in {'LEN_STEP': 0.65, 'M_IN_KM': 1000, 'MIN_IN_H': 60}.items():
        assert hasattr(homework.Training, attr), (
            f'La clase `Training` (entrenamiento) debe tener un atributo `{attr}`'
        )
        assert getattr(homework.Training, attr) == value, (
            'La clase `Training` debe tener '
            f'un atributo `{attr}` establecido en `{value}`'
        )
    training = homework.Training
    training_signature = inspect.signature(training)
    training_signature_list = list(training_signature.parameters)
    for param in ['action', 'duration', 'weight']:
        assert param in training_signature_list, (
            'El método `__init__` de la clase `Training` debe tener '
            f' el parámetro {param}.'
        )
    assert 'LEN_STEP' in list(training.__dict__), (
        'Establece el atributo `LEN_STEP` en la clase `Training`'
    )
    assert training.LEN_STEP == 0.65, (
        'La longitud del paso en la clase `Training` debe ser igual a 0,65'
    )
    assert 'M_IN_KM' in list(training.__dict__), (
        'Establece el atributo `M_IN_KM` en la clase `Training`'
    )
    assert training.M_IN_KM == 1000, (
        'En la clase `Training`, especifica cuántos '
        'metros hay en un kilómetro: 1000'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.273),
    ([1206, 12, 6], 0.7838999999999999),
])
def test_Training_get_distance(input_data, expected):
    training = homework.Training(*input_data)
    assert hasattr(training, 'get_distance'), (
        'Define un método `get_distance` en la clase `Training`.'
    )
    result = training.get_distance()
    assert type(result) == float, (
        'El método `get_distance` de la clase `Training`'
        'debe devolver un valor `float`'
    )
    assert result == expected, (
        'Comprueba la fórmula para calcular distancias en la clase `Training`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.06825),
    ([1206, 12, 6], 0.065325),
])
def test_Training_get_mean_speed(input_data, expected):
    training = homework.Training(*input_data)
    assert hasattr(training, 'get_mean_speed'), (
        'Define un método `get_mean_speed` en la clase `Training`.'
    )
    result = training.get_mean_speed()
    assert type(result) == float, (
        'El método `get_mean_speed` de la clase `Training`'
        'debe devolver un valor `float`'
    )
    assert result == expected, (
        'Comprueba la fórmula para calcular la velocidad promedio de movimiento '
        'en la clase `Training`'
    )


@pytest.mark.parametrize('input_data', [
    ([9000, 1, 75]),
    ([420, 4, 20]),
    ([1206, 12, 6]),
])
def test_Training_get_spent_calories(input_data):
    training = homework.Training(*input_data)
    assert hasattr(training, 'get_spent_calories'), (
        'Define un método `get_spent_calories` en la clase `Training`.'
    )
    assert callable(training.get_spent_calories), (
        '`get_spent_calories` debe ser una función.'
    )
    assert training.get_spent_calories() is None, (
        'El método `get_spent_calories` de la clase `Training` no debe '
        'calcular la cantidad de calorías quemadas porque cada '
        'tipo de entrenamiento tiene su propia fórmula para calcular las calorías.'
    )


def test_Training_show_training_info(monkeypatch):
    training = homework.Training(*[720, 1, 80])
    assert hasattr(training, 'show_training_info'), (
        'Define un método `show_training_info` en la clase `Training`.'
    )

    def mock_get_spent_calories():
        return 100
    monkeypatch.setattr(
        training,
        'get_spent_calories',
        mock_get_spent_calories
    )
    result = training.show_training_info()
    assert result.__class__.__name__ == 'InfoMessage', (
        'El método `show_training_info` de la clase `Training` '
        'debe devolver una instancia de la clase `InfoMessage`.'
    )


def test_Swimming():
    assert hasattr(homework, 'Swimming'), 'Crea una clase `Swimming`'
    assert inspect.isclass(homework.Swimming), (
        '`Swimming` debe ser una clase.'
    )
    assert issubclass(homework.Swimming, homework.Training), (
        'La clase `Swimming` se debe heredar de la clase `Training`.'
    )
    for attr, value in {
            'LEN_STEP': 1.38,
            'CALORIES_MEAN_SPEED_SHIFT': 1.1,
            'CALORIES_WEIGHT_MULTIPLIER': 2,
    }.items():
        assert hasattr(homework.Swimming, attr), (
            f'La clase `Swimming` debe tener un atributo `{attr}`'
        )
        assert getattr(homework.Swimming, attr) == value, (
            'La clase `Swimming` debe tener '
            f'un atributo `{attr}` establecido en `{value}`'
        )
    swimming = homework.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            'El método `__init__` de la clase `Swimming`'
            f' debe tener el parámetro {param}.'
        )
    assert 'LEN_STEP' in list(swimming.__dict__), (
        'Establece el atributo `LEN_STEP` en la clase `Swimming`'
    )
    assert swimming.LEN_STEP == 1.38, (
        'La longitud de la brazada en la clase `Swimming` debe ser igual a 1,38'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Anula el método `get_mean_speed` en la clase `Swimming`. '
        'Comprueba la fórmula para calcular la velocidad media en la clase `Swimming`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], 182.72000000000003),
    ([1206, 12, 6, 12, 6], 159.264),
])
def test_Swimming_get_spent_calories(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_spent_calories()
    assert type(result) == float, (
        'Anula el método `get_spent_calories` en la clase `Swimming`.'
    )
    assert result == expected, (
        'Comprueba la fórmula para calcular las calorías quemadas en la clase `Swimming`'
    )


def test_SportsWalking():
    assert hasattr(homework, 'SportsWalking'), 'Crea una clase `PowerWalking`'
    assert inspect.isclass(homework.SportsWalking), (
        '`PowerWalking` debe ser una clase.'
    )
    assert issubclass(homework.SportsWalking, homework.Training), (
        'La clase `PowerWalking` debe heredarse de la clase `Training`.'
    )
    for attr, value in {
            'CALORIES_WEIGHT_MULTIPLIER': 0.035,
            'CALORIES_SPEED_HEIGHT_MULTIPLIER': 0.029,
            'KMH_IN_MSEC': 0.278,
            'CM_IN_M': 100
    }.items():
        assert hasattr(homework.SportsWalking, attr), (
            f'La clase `PowerWalking` debe tener un atributo `{attr}`'
        )
        assert getattr(homework.SportsWalking, attr) == value, (
            'The `PowerWalking` debe ser '
            f'un atributo `{attr}` establecido en `{value}`'
        )
    sports_walking = homework.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            'El método `__init__` de la clase `PowerWalking`'
            f'debe tener el parámetro {param}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 349.2517475250001),
    ([420, 4, 20, 42], 168.11931219846002),
    ([1206, 12, 6, 12], 151.54430943785593),
])
def test_SportsWalking_get_spent_calories(input_data, expected):
    sports_walking = homework.SportsWalking(*input_data)
    result = sports_walking.get_spent_calories()
    assert type(result) == float, (
        'Anula el método `get_spent_calories` en la clase `PowerWalking`.'
    )
    assert result == expected, (
        'Comprueba la fórmula para calcular las calorías '
        'quemadas en la clase `PowerWalking`'
    )


def test_Running():
    assert hasattr(homework, 'Running'), 'Crea una clase `Running`'
    assert inspect.isclass(homework.Running), '`Running` debe ser una clase.'
    assert issubclass(homework.Running, homework.Training), (
        'La clase `Running` debe heredarse de la clase `Training`.'
    )
    for attr, value in {'CALORIES_MEAN_SPEED_MULTIPLIER': 18, 'CALORIES_MEAN_SPEED_SHIFT': 1.79}.items():
        assert hasattr(homework.Running, attr), (
            f'La clase `Running` debe tener un atributo `{attr}`'
        )
        assert getattr(homework.Running, attr) == value, (
            'La clase `Running` debe tener '
            f'un atributo `{attr}` establecido en `{value}`'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 481.90500000000003),
    ([420, 4, 20], 14.488800000000001),
    ([1206, 12, 6], 12.812472),
])
def test_Running_get_spent_calories(input_data, expected):
    running = homework.Running(*input_data)
    assert hasattr(running, 'get_spent_calories'), (
        'Define un método `get_spent_calories` en la clase `Running`.'
    )
    result = running.get_spent_calories()
    assert type(result) == float, (
        'Anula el método `get_spent_calories` en la clase `Running`.'
    )
    assert result == expected, (
        'Comprueba la fórmula para calcular las calorías quemadas en la clase `Running`'
    )


def test_main():
    assert hasattr(homework, 'main'), (
        'Define la función principal del programa y llámala `main`.'
    )
    assert callable(homework.main), '`main` debe ser una función.'
    assert isinstance(homework.main, types.FunctionType), (
        '`main` debe ser una función.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Tipo de entrenamiento: Natación; '
        'Duración: 1.000 h; '
        'Distancia: 0.994 km; '
        'Vel. promedio: 1.000 km/h; '
        'Calorías quemadas: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Tipo de entrenamiento: Correr; '
        'Duración: 12.000 h; '
        'Distancia: 0.784 km; '
        'Vel. promedio: 0.065 km/h; '
        'Calorías quemadas: 12.812.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Tipo de entrenamiento: Marcha rápida; '
        'Duración: 1.000 h; '
        'Distancia: 5.850 km; '
        'Vel. promedio: 5.850 km/h; '
        'Calorías quemadas: 349.252.'
    ]),
    (['WLK', [9000, 1.5, 75, 180]], [
        'Tipo de entrenamiento: Marcha rápida; '
        'Duración: 1.500 h; '
        'Distancia: 5.850 km; '
        'Vel. promedio: 3.900 km/h; '
        'Calorías quemadas: 364.084.'
    ]),
    (['WLK', [3000.33, 2.512, 75.8, 180.1]], [
        'Tipo de entrenamiento: Marcha rápida; '
        'Duración: 2.512 h; '
        'Distancia: 1.950 km; '
        'Vel. promedio: 0.776 km/h; '
        'Calorías quemadas: 408.429.'
    ]),
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        training = homework.read_package(*input_data)
        homework.main(training)
    assert get_message_output == expected, (
        'El método `main` debe mostrar el resultado en la consola.\n'
    )
