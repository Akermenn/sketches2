
from __future__ import annotations
from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Tuple


class ValidationError(Exception):
    pass


@dataclass(frozen=True)
class PipeKey:
    diameter_mm: int
    wall_thickness_mm: int


@dataclass
class OrderItem:
    diameter_mm: int
    wall_thickness_mm: int
    length_m: float
    weight_per_pipe_t: float
    quantity: int


@dataclass
class TransportLoad:
    transport_name: str
    transport_category: str
    pipe_key: PipeKey
    unit_index: int
    pipes_loaded: int


@dataclass
class CalculationResult:
    total_units: int
    loads: List[TransportLoad]
    warnings: List[str]


TRANSPORTS = {
    "wagon": {
        "name": "Полувагон 12.118 м",
        "payload_t": 69.0,
        "inner_length_m": 12.118,
        "inner_width_m": 2.878,
        "inner_height_m": 2.060,
    },
    "truck": {
        "name": "Еврофура 13.6 м",
        "payload_t": 40.0,
        "inner_length_m": 13.6,
        "inner_width_m": 2.45,
        "inner_height_m": 2.40,
    },
}

# Консервативная вместимость по таблицам задания:
# для диапазонов используется нижняя граница, чтобы результат гарантированно оставался допустимым.
CAPACITY_TABLE: Dict[str, Dict[PipeKey, int]] = {
    "wagon": {
        PipeKey(273, 6): 103,
        PipeKey(273, 8): 103,
        PipeKey(325, 6): 70,
        PipeKey(325, 7): 70,
        PipeKey(325, 10): 44,
        PipeKey(377, 9): 52,
        PipeKey(426, 7): 40,
        PipeKey(426, 8): 40,
        PipeKey(426, 10): 40,
        PipeKey(530, 8): 29,
        PipeKey(630, 8): 21,
        PipeKey(630, 9): 21,
        PipeKey(720, 8): 13,
        PipeKey(820, 8): 11,
        PipeKey(820, 9): 11,
        PipeKey(920, 8): 16,
        PipeKey(1020, 10): 6,
        PipeKey(1020, 12): 6,
        PipeKey(1020, 14): 5,
    },
    "truck": {
        PipeKey(426, 7): 19,
        PipeKey(426, 8): 19,
        PipeKey(426, 10): 19,
        PipeKey(530, 8): 16,
        PipeKey(630, 8): 11,
        PipeKey(630, 9): 11,
        PipeKey(720, 8): 8,
        PipeKey(820, 8): 8,
        PipeKey(820, 9): 8,
        PipeKey(920, 8): 5,
        PipeKey(1020, 10): 4,
        PipeKey(1020, 12): 4,
        PipeKey(1420, 14): 2,
    },
}


def validate_item(item: OrderItem) -> None:
    if item.quantity <= 0:
        raise ValidationError("Количество труб должно быть положительным.")
    if item.length_m <= 0:
        raise ValidationError("Длина трубы должна быть положительной.")
    if item.weight_per_pipe_t <= 0:
        raise ValidationError("Масса одной трубы должна быть положительной.")
    if item.diameter_mm <= 0 or item.wall_thickness_mm <= 0:
        raise ValidationError("Диаметр и толщина стенки должны быть положительными.")


def get_capacity(item: OrderItem, transport_category: str) -> int:
    transport = TRANSPORTS[transport_category]
    if item.length_m > transport["inner_length_m"]:
        raise ValidationError(
            f"Труба длиной {item.length_m} м не помещается в {transport['name']} "
            f"по длине полезного объема."
        )

    pipe_key = PipeKey(item.diameter_mm, item.wall_thickness_mm)
    if pipe_key not in CAPACITY_TABLE[transport_category]:
        raise ValidationError(
            f"Для сортамента {item.diameter_mm}x{item.wall_thickness_mm} "
            f"нет справочной вместимости для транспорта '{transport['name']}'."
        )

    table_capacity = CAPACITY_TABLE[transport_category][pipe_key]
    weight_capacity = int(transport["payload_t"] // item.weight_per_pipe_t)
    effective_capacity = min(table_capacity, weight_capacity)

    if effective_capacity <= 0:
        raise ValidationError(
            "По ограничениям грузоподъемности нельзя разместить даже одну трубу."
        )

    return effective_capacity


def optimize_transport(
    items: List[OrderItem],
    priority_transport: str,
    allow_fallback: bool = True,
) -> CalculationResult:
    if priority_transport not in TRANSPORTS:
        raise ValidationError("Приоритет транспорта должен быть 'wagon' или 'truck'.")

    fallback = "truck" if priority_transport == "wagon" else "wagon"
    loads: List[TransportLoad] = []
    warnings: List[str] = []

    for item in items:
        validate_item(item)

        selected_transport = priority_transport
        try:
            capacity = get_capacity(item, selected_transport)
        except ValidationError as primary_error:
            if not allow_fallback:
                raise
            try:
                capacity = get_capacity(item, fallback)
                selected_transport = fallback
                warnings.append(
                    f"Для сортамента {item.diameter_mm}x{item.wall_thickness_mm} "
                    f"использован резервный тип транспорта '{TRANSPORTS[fallback]['name']}', "
                    f"так как приоритетный вариант недоступен."
                )
            except ValidationError:
                raise primary_error

        unit_count = ceil(item.quantity / capacity)
        remaining = item.quantity
        for unit_index in range(1, unit_count + 1):
            loaded = min(capacity, remaining)
            loads.append(
                TransportLoad(
                    transport_name=TRANSPORTS[selected_transport]["name"],
                    transport_category=selected_transport,
                    pipe_key=PipeKey(item.diameter_mm, item.wall_thickness_mm),
                    unit_index=unit_index,
                    pipes_loaded=loaded,
                )
            )
            remaining -= loaded

    return CalculationResult(total_units=len(loads), loads=loads, warnings=warnings)


if __name__ == "__main__":
    demo_items = [
        OrderItem(426, 8, 11.0, 0.95, 70),
        OrderItem(1020, 12, 11.0, 4.0, 9),
    ]
    result = optimize_transport(demo_items, priority_transport="truck", allow_fallback=True)
    print("Всего единиц транспорта:", result.total_units)
    for load in result.loads:
        print(
            f"{load.transport_name} | {load.pipe_key.diameter_mm}x{load.pipe_key.wall_thickness_mm} | "
            f"ед. #{load.unit_index} | труб: {load.pipes_loaded}"
        )
    if result.warnings:
        print("Предупреждения:")
        for warning in result.warnings:
            print("-", warning)
