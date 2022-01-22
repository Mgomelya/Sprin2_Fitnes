# from turtle import distance


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,  # Тип тренеровки
        duration: float,  # Время тренеровки в часах
        distance: float,  # Дистанция в км
        speed: float,  # Скорость
        calories: float,  # Потраченные калории
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Константа - Средняя длина шага
    M_IN_KM = 1000  # Константа - количество метров в 1 км
    TRAINING_TYPE = ""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,  # вес спортсмена
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEF_RUN_1 = 18  # Коэффициент расчета калорий для бега
    COEF_RUN_2 = 20  # Коэффициент расчета калорий для бега
    TRAINING_TYPE = "RUN"

    def get_spent_calories(self) -> float:
        return (
            (self.COEF_RUN_1 * self.get_mean_speed() - self.COEF_RUN_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * 60
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_WLK_1 = 0.035  # Коэффициент для расчета калорий для ходьбы
    COEF_WLK_2 = 2  # Коэффициент для расчета калорий для ходьбы
    COEF_WLK_3 = 0.029  # Коэффициент для расчета калорий для ходьбы
    TRAINING_TYPE = "WLK"

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.COEF_WLK_1 * self.weight
                + (self.get_mean_speed() ** self.COEF_WLK_2 // self.height)
                * self.COEF_WLK_3
                * self.weight
            )
            * self.duration
            * 60
        )


class Swimming(Training):
    """Тренировка: плавание."""

    COEF_SWM_1 = 1.1  # Коэффициент для расчета калорий плавание
    COEF_SWM_2 = 2  # Коэффициент для расчета калорий плавание
    LEN_STEP = 1.38  # Коэффициент для расчета калорий плавание
    TRAINING_TYPE = "SWM"

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_SWM_1)
                * self.COEF_SWM_2 * self.weight)

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
