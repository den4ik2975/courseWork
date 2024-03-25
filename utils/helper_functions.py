import copy


def hasse_parser(diag: dict) -> dict[str, list[list, list]]:
    graph = {}

    for node, connections in diag.items():
        for down in connections["downs"]:
            if graph.get(node, False) is False:
                graph[node] = []
            graph[node].append(down)

        for up in connections["ups"]:
            if graph.get(node, False) is False:
                graph[node] = []
            graph[node].append(up)

    return graph


def answers_parser(answer, action):

    if action in ['maxes', 'mins', 'largest', 'smallest']:
        return [set(answer[action])]

    elif action in ['section', 'revsection']:
        return [set(i) for i in answer[action].split('|')]


def humanizer(act, start, end):
    label_dict = {
        'maxes': 'Выберите максимальные элементы',
        'mins': 'Выберите минимальные элементы',
        'largest': 'Выберите наибольший элемент',
        'smallest': 'Выберите наименьший элемент',
        'section': f'Выберите отрезок [{start}; {end}]',
        'revsection': f'Выберите отрезок [{start}; {end}]',
        'order': f'Составьте линейный порядок',
        'pair': f'Выберите все пары'
    }

    return label_dict[act]


def linear_checker(variant, answer):

    if len(answer) != 9:
        return False

    for letter in answer:
        if len(variant[letter]['ups']) == 0:
            for down in variant[letter]['downs']:
                try:
                    variant[down]['ups'].remove(letter)
                except ValueError:
                    pass
        else:
            return False

    return True


def step_in(variant: dict, last_steps: list, current: str, ans: set, checked: set):
    checked.add(current)
    for last in last_steps:
        ans.add((current, last))

    for down in variant[current]['downs']:
        last_steps.append(current)
        step_in(variant, last_steps[:], down, ans, checked)

    return ans


def pair_checker(variant):
    checked = set()
    alls = 'ABCDEFGHI'
    ans = set()

    for node in alls:
        if node not in checked and not variant[node]['ups']:
            ans = step_in(variant, [], node, ans, checked)

    return ans


