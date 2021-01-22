import client
import ast
import random


# Função que executa um episódio.
def episode(c, res: int):
    if res != -1:
        msg = c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        directions = ["left", "right", "forward"]
        msg = c.execute("info", "position")
        pos = ast.literal_eval(msg)
        path = []
        path.append(pos)
        end = False
        while not end:
            msg = c.execute("info", "view")
            objects = ast.literal_eval(msg)
            if objects[0] == 'obstacle' or objects[0] == 'bomb':
                c.execute("command", "left")
            else:
                if pos == goal:
                    print('GOAL found!')
                    end = True
                else:
                    direction = random.choice(directions)
                    c.execute('command', direction)
                    msg = c.execute("info", "position")
                    pos = ast.literal_eval(msg)
                    if direction == 'forward':
                        path.append(pos)

        print('Path:\n', path)
        return path


# Função para atualizar tabela Q learning.
# Recebe como argumentos a respetiva tabela e o percurso feito pelo agente.
def updateQTable(QTable, path):
    prevPos = path[len(path)-1]  # Posição do goal.
    prevX, prevY = prevPos[0], prevPos[1]
    for i in range(len(path)-2, -1, -1):
        newPos = path[i]
        x, y = newPos[0], newPos[1]
        if QTable[x][y] < 0.9*QTable[prevX][prevY]:
            QTable[x][y] = 0.9*QTable[prevX][prevY]
            prevX, prevY = x, y

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

    msg = c.execute("info", "goal")
    goal = ast.literal_eval(msg)
    QTable[goal[0]][goal[1]] = 100  # Reward do Goal igual a 100.
    print(QTable)

    # Executar episódios.
    numEpisodes = 100
    for n in range(numEpisodes):
        print(n + 1, 'º episode')
        path = episode(c, res)  # Realizar um episódio.
        QTable = updateQTable(QTable, path)  # Atualizar matriz Q-learning.
        c.execute("command", "home")  # Voltar ao ponto de partida após um episódio.

    # Depois de concluídos todos os episódios, efetuar trajeto óptimo.
    # optimalPath(QTable, c, res)


main()