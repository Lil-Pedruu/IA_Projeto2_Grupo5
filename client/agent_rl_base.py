import client
import ast
import random


def episode(c, res: int):
    if res != -1:
        msg = c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        directions = ["left", "right", "forward"]
        path = []
        end = False
        while not end:
            msg = c.execute("info", "view")
            objects = ast.literal_eval(msg)
            if objects[0] == 'obstacle' or objects[0] == 'bomb':
                c.execute("command", "left")
            else:
                msg = c.execute("info", "position")
                pos = ast.literal_eval(msg)
                if pos == goal:
                    print('GOAL found!')
                    end = True
                else:
                    dir = random.choice(directions)
                    c.execute('command', dir)

                path += pos

        return path


def updateQTable(QTable, c, path):
    msg = c.execute("info", "position")
    pos = ast.literal_eval(msg)
    #reward = QTable[pos[0]][pos[1]]

    return reward


def main():
    c = client.Client('127.0.0.1', 50001)
    res = c.connect()
    random.seed()  # To become true random, a different seed is used! (clock time)
    #msg = c.execute("info", "position")
    #posInicial = ast.literal_eval(msg)

    # Inicializar Q Table.
    QTable = []
    msg = c.execute("info", "maxcoord")
    max_coord = ast.literal_eval(msg)
    for n in range(max_coord[0]):
        QTable += [[0] * max_coord[1]]

    msg = c.execute("info", "goal")
    goal = ast.literal_eval(msg)
    QTable[goal[0]][goal[1]] = 100
    print(QTable)

    numEpisodes = 2
    for n in range(numEpisodes):
        print(n+1, 'º episode')
        path = episode(c, res)

        #updateQTable(QTable, path)


main()
