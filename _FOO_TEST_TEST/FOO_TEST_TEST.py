#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# FFXIII-2
# clock solver

from copy import deepcopy


def is_win(clock_data: dict) -> bool:
    return all(x == 0 for x in clock_data['items'])


def get_arrows_value(clock_data: dict) -> (int, int):
    items = clock_data['items']
    arrow_1 = clock_data['left_arrow_index']
    arrow_2 = clock_data['right_arrow_index']

    return items[arrow_1], items[arrow_2]


def is_fail(clock_data: dict) -> bool:
    a, b = get_arrows_value(clock_data)
    return a == 0 and b == 0


def click_clock_item(clock_data: dict, selected_index: int):
    items = clock_data['items']
    move_value = items[selected_index]

    clock_data['selected_indexes'].append(selected_index)
    clock_data['selected_values'].append(move_value)

    # После клика кнопка теперь не активна
    items[selected_index] = 0

    # Остаток по модулю поможет получить индекс после вращения стрелки по часовой или против
    left_arrow_index = (selected_index - move_value) % len(items)
    right_arrow_index = (selected_index + move_value) % len(items)

    clock_data['left_arrow_index'] = left_arrow_index
    clock_data['right_arrow_index'] = right_arrow_index

    # После клика, часы изменились, поэтому нужно сохранить это в истории
    clock_data['history'].append(deepcopy(clock_data['items']))


def solve_step(clock_data: dict, index: int, result_win: dict):
    # Если текущий индекс указывает на уже активированную кнопку
    if clock_data['items'][index] == 0:
        return

    # Т.к. этот объект используется в рекурсии, нужно делать его копии
    # чтобы изменения в одной функции рекурсии не повлияло на другую
    clock_data = deepcopy(clock_data)

    click_clock_item(clock_data, index)

    if is_win(clock_data):
        # Для удаления дубликатов выбранные индексы преобразуем в ключ для словаря
        key = ','.join(map(str, clock_data['selected_indexes']))

        result_win[key] = clock_data
        return

    if is_fail(clock_data):
        return

    arrow_1 = clock_data['left_arrow_index']
    solve_step(clock_data, arrow_1, result_win)

    arrow_2 = clock_data['right_arrow_index']
    solve_step(clock_data, arrow_2, result_win)


def solver(clock_items: list) -> list:
    clock_data = {
        'items': deepcopy(clock_items),
        'history': [deepcopy(clock_items)],
        'left_arrow_index': 0,
        'right_arrow_index': 0,
        'selected_indexes': [],
        'selected_values': [],
    }

    result_win = dict()

    items = clock_data['items']
    for index in range(len(items)):
        solve_step(clock_data, index, result_win)

    return list(result_win.values())


if __name__ == '__main__':
    #       2
    #    4     4
    #   1        1
    # 2           3
    #   5      4
    #       3
    clock_items = [2, 4, 1, 3, 4, 3, 5, 2, 1, 4]

    result_win = solver(clock_items)

    print('Winning results:', len(result_win))
    for i, clock_data in enumerate(result_win, 1):
        print(f'{i}.')

        # Совмещение элемента истории, выбранного индекса и значения
        total_result = zip(clock_data['history'], clock_data['selected_indexes'], clock_data['selected_values'])
        for item, index, value in total_result:
            print(f'{item} -> #{index} ({value})')

        print()
