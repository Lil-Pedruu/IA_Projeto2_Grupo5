import client
import ast
import random


# Função que executa um episódio.
def episode(c, res: int):
    if res != -1:
        msg = c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        commands = ["left", "right", "forward"]
        path = []
        end = False
        while not end:
            msg = c.execute("info", "view")
            objects = ast.literal_eval(msg)
            msg = c.execute("info", "position")
            pos = ast.literal_eval(msg)
            command = random.choice(commands)
            if objects[0] == 'obstacle' or objects[0] == 'bomb':
                c.execute("command", "left")
            else:
                if pos == goal:
                    print('GOAL found!')
                    end = True
                else:
                    if command == 'forward':
                        direction = c.execute("info", "direction")
                        pos = list(pos)
                        pos.append(direction)
                        pos = tuple(pos)
                        path.append(pos)
                    c.execute('command', command)

        print('Path:\n', path)
        return path


# Função para atualizar tabela Q learning.
# Recebe como argumentos a respetiva tabela e o percurso feito pelo agente.
def updateQTable(QTable, path, c):
    msg = c.execute("info", "goal")
    goal = ast.literal_eval(msg)
    lastX, lastY, lastDirection = goal[0], goal[1], 'north'
    for i in range(len(path)-1, -1, -1):
        newPos = path[i]
        x, y, direction = newPos[0], newPos[1], newPos[2]

        q = 0.9*QTable[lastX][lastY][lastDirection]
        if q > QTable[x][y][direction]:
            QTable[x][y][direction] = q
            lastX, lastY, lastDirection = x, y, direction

    print('QTable:')
    for column in QTable:
        print(column)

    return QTable


# Main.
def main():
    c = client.Client('127.0.0.1', 50001)
    res = c.connect()
    random.seed()  # To become true random, a different seed is used! (clock time)

    # Inicializar Q Table.
    QTable = []
    msg = c.execute("info", "maxcoord")
    max_coord = ast.literal_eval(msg)
    for n in range(max_coord[0]):
        QTable += [[0] * max_coord[1]]

    for column in range(len(QTable)):
        for row in range(len(QTable[column])):
            QTable[column][row] = {'north': 0, 'south': 0, 'east': 0, 'west': 0}

    msg = c.execute("info", "goal")
    goal = ast.literal_eval(msg)
    for direction in ['north', 'south', 'east', 'west']:
        QTable[goal[0]][goal[1]][direction] = 100  # Reward do Goal igual a 100.
    print(QTable)

    # Executar episódios.
    numEpisodes = 1
    for n in range(numEpisodes):
        print(n + 1, 'º episode')
        path = episode(c, res)  # Realizar um episódio.
        QTable = updateQTable(QTable, path, c)  # Atualizar matriz Q-learning.
        c.execute("command", "home")  # Voltar ao ponto de partida após um episódio.

    # Depois de concluídos todos os episódios, efetuar trajeto óptimo.
    # optimalPath(QTable, c, res)


main()