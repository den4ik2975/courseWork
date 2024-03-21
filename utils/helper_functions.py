import json


def hasseParser(diag: dict) -> dict[str, list[list, list]]:
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