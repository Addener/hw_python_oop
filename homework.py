from typing import List, Dict, Union
from dataclasses import dataclass


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message_info = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message_info


class Training:

    LEN_STEP: float = 0.65  # one step (m)
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        raise NotImplementedError(
            'Переопределите get_spent_colories в всех дочерних классах')

    def show_training_info(self) -> InfoMessage:
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):

    COLORIES_COEF_SPEED: float = 18     # Коэф. для формулы(не менять)
    COLORIES_COEF_WEIGHT: float = 1.79  # Коэф. для формулы(не менять)
    HOUR_IN_MIN: int = 60               # Перевод час. в мин.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_colories_running = ((self.COLORIES_COEF_SPEED
                                  * super().get_mean_speed()
                                  + self.COLORIES_COEF_WEIGHT) * self.weight
                                  / self.M_IN_KM * self.duration
                                  * self.HOUR_IN_MIN)
        return spent_colories_running


class SportsWalking(Training):

    COLORIES_COEF_WEIGHT: float = 0.035  # Коэф. для формулы(не менять)
    COLORIES_COEF_WALK: float = 0.029    # Коэф. для формулы(не менять)
    M_IN_SEC: float = 0.278              # перевод ед. измерения в м/с
    HOUR_IN_MIN: int = 60                # перевод час. в мин.
    HEIGHT_IN_M: int = 100               # перевод роста см. в м.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    # Возврат расчета колорий тренировки: спортивная ходьба.
    def get_spent_calories(self) -> float:
        spent_colories_walking = (
            (self.COLORIES_COEF_WEIGHT * self.weight
             + ((super().get_mean_speed() * self.M_IN_SEC)**2
                / (self.height / self.HEIGHT_IN_M))
                * self.COLORIES_COEF_WALK * self.weight)
            * self.duration * self.HOUR_IN_MIN)
        return spent_colories_walking


class Swimming(Training):

    LEN_STEP: float = 1.38            # One step (m).
    M_IN_KM: int = 1000               # константа для перевода м. в км.
    COLORIES_SPEED_COEF: float = 1.1  # Коэф. для формулы(не менять)
    COLORIES_WEIGHT_COEF: float = 2   # Коэф. для формулы(не менять)
    HOUR_IN_MIN: int = 60             # Перевод час. в мин.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        # Длина бассейна в метрах
        self.length_pool = length_pool
        # Сколько раз тренеруемый переплыл бассейн.
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed_swim = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return mean_speed_swim

    def get_spent_calories(self) -> float:
        spent_colories_swim = (
            (self.get_mean_speed() + self.COLORIES_SPEED_COEF)
            * self.COLORIES_WEIGHT_COEF * self.weight
            * self.duration)
        return spent_colories_swim


def read_package(workout_type: str, data: List[int]) -> Union[Training, None]:
    data_a_training: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        data_for_training = data_a_training[workout_type]
        return data_for_training(*data)
    except KeyError as e:
        print(f"{e} The module doesn't support this type of training")
        return None


def main(training: Union[Training, None]) -> None:
    if training:
        info = training.show_training_info()
        print(info.get_message())
    else:
        pass


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    # Передаем данные с датчиков для получения общей информации.
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
