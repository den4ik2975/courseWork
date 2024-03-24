import json


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
        return set(answer[action])

    elif action in ['order', 'revorder']:
        return [set(i) for i in answer[action].split('|')]


def humanizer(act):
    match act:
        case 'maxes':
            return 'Выберите максимальные элементы'
        case 'maxes':
            return 'Выберите максимальные элементы'
        case 'maxes':
            return 'Выберите максимальные элементы'
        case 'maxes':
            return 'Выберите максимальные элементы'
        case 'maxes':
            return 'Выберите максимальные элементы'
        case 'maxes':
            return 'Выберите максимальные элементы'