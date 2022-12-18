'''
Grupo 16
João Assis - fc56325
Marina Novaes - fc55942
Ricardo Mateus - fc56366
'''
from copy import *
from random import *
from jogos import *
from jogar import *
from utils import *
import string
import random
import copy

from collections import namedtuple

stateBreakthru = namedtuple('EstadoBreakthru', 'to_move')

class EstadoBreakthru(stateBreakthru):
    
    def __init__(self, to_move=1, n=8):
        self.board = [['.' for i in range(n)] for i in range(n)]
        #self.terminou = self.verificar_terminou()
        for i in range(2):
            for j in range(8):
                self.board[i][j] = 'B'

        for i in range(6, 8):
            for j in range(8):
                self.board[i][j] = 'W'

    def verificar_terminou(self):
        # 1 = White,  2 = Black
        if self.to_move == 2:
            for row in range(len(self.board)):
                if (self.board[0][row] == 'W'):
                    return 1
        elif self.to_move == 1:
            for row in range(len(self.board)):
                if (self.board[7][row] == 'B'):
                    return 2
        return 0
    
    def pos_convert(self, i, j):
        alfabeto = "abcdefgh"
        return alfabeto[j] + str(8 - i)

    def move_convert(self, move):
        numbers = []
        alfabeto = "abcdefgh"
        numbers.append(int(alfabeto.rfind(move[0]))) 
        numbers.append(int(move[1]) - 1)
        return numbers

    def moves(self, to_move):
        list_moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board)):

                if to_move == 1 and self.board[col][row] == 'W': # para as brancas

                    if col > 0 and self.board[col-1][row] == '.': # cima
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col-1,row)))

                    if col > 0 and row < 7 and (self.board[col-1][row+1] == '.' or self.board[col-1][row+1] == 'B'): # diagonal direita cima
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col-1,row+1)))

                    if col > 0 and row > 0 and (self.board[col-1][row-1] == '.' or self.board[col-1][row-1] == 'B'): # diagonal esquerda cima
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col-1,row-1)))
                        
                if to_move == 2 and self.board[col][row] == 'B': # para as pretas

                    if col < 7 and self.board[col+1][row] == '.': # baixo
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col+1,row)))

                    if col < 7 and row < 7 and (self.board[col+1][row+1] == '.' or self.board[col+1][row+1] == 'W'): # diagonal direita baixo
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col+1,row+1)))

                    if col < 7 and row > 0 and (self.board[col+1][row-1] == '.' or self.board[col+1][row-1] == 'W'): # diagonal esquerda baixo
                        list_moves.append("{pos1}-{pos2}".format(pos1=self.pos_convert(col,row), pos2=self.pos_convert(col+1,row-1)))
    
        return sorted(list_moves)

## CLASS JOGO ##
class JogoBT_16(Game):
    """Play Breakthrough on an 8 x 8 board, with Max (first player) playing 'W' (1).
    """
    def __init__(self):
        self.initial = EstadoBreakthru(to_move=1)
        self.board = [['.' for i in range(8)] for i in range(8)]
        for i in range(2):
            for j in range(8):
                self.board[i][j] = 'B'

        for i in range(6, 8):
            for j in range(8):
                self.board[i][j] = 'W'

    def actions(self, state):
        "Legal moves for B and W"
        #Apenas queremos ver as ações possíveis para o jogador atual (to_move)
        return state.moves(state.to_move)

    def result(self, state, move):
        if state.to_move == 1:
            novo_estado = state._replace(to_move=2)
            novo_estado.board = copy.deepcopy(state.board)
            index_start = state.move_convert(move[0:2])
            new_index = state.move_convert(move[3:5])
            novo_estado.board[7 - index_start[1]][index_start[0]] = '.'
            novo_estado.board[7 - new_index[1]][new_index[0]] = 'W'
            return novo_estado
        else:
            novo_estado = state._replace(to_move=1)
            novo_estado.board = copy.deepcopy(state.board)
            index_start = state.move_convert(move[0:2])
            new_index = state.move_convert(move[3:5])
            novo_estado.board[7 - index_start[1]][index_start[0]] = '.'
            novo_estado.board[7 - new_index[1]][new_index[0]] = 'B'
            return novo_estado

    def utility(self, state, player):
        "If player wins in this state, return 1; if otherplayer wins return -1; else return 0."
        if player == state.verificar_terminou():
            return 1
        elif player != state.verificar_terminou() and state.verificar_terminou() > 0:
            return -1
        else:
            return 0

    def terminal_test(self, state):
        "A state is terminal if the whites reached line 8 or some black reached line 1."
        return state.verificar_terminou() >= 1

    def display(self, state):
        symbols = "abcdefgh"
        print("-"*17)
        for i in range(len(state.board)):
            print("{num}|".format(num=8-i) + ' '.join(state.board[i]))
        print("-+" + "-"*15)
        print(" |" + ' '.join(i for i in symbols))

        if state.verificar_terminou() >= 1:
            return
        elif state.to_move == 1:
            print("--NEXT PLAYER: W")
        elif state.to_move == 2:
            print("--NEXT PLAYER: B")

    def executa(self, estado, listaJogadas):
        "executa varias jogadas sobre um estado dado"
        "devolve o estado final "
        s = estado
        for j in listaJogadas:
            s = self.result(s, j)
        return s

## Jogadores ##
 
depth_for_all = 3

def count_pieces_line(state, jogador, line):
    count = 0
    if jogador == 1:
        for i in range(len(state.board)):
            if state.board[line - 1][i] == 'W':
                count += 1
    elif jogador == 2:
        for i in range(len(state.board)):
            if state.board[line - 1][i] == 'B':
                count += 1     
    return count

def func_simples1(game, state):
    moves = game.actions(state)
    return moves[0] #faz sempre o 1º move

def func_simples2(game, state):
    moves = game.actions(state)
    return moves[len(moves) - 1] #fazsempre o último move

def func_aval_player2(estado, jogador): #uma heurística defensiva
    count = 0
    if jogador == 1:
        for col in range(len(estado.board)):
            for line in range(len(estado.board)):
                if estado.board[col][line] == 'W':
                    count += col

    elif jogador == 2:
        for col in range(len(estado.board)):
            for line in range(len(estado.board)):
                if estado.board[col][line] == 'B':
                    count += col
                    
    return count

def func_aval_16(estado, jogador): #uma heurística ofensiva
    count = 0
    if jogador == 1:
        for col in range(len(estado.board)):
            for line in range(len(estado.board)):
                if estado.board[col][line] == 'W':
                    count += len(estado.board) - col

    elif jogador == 2:
        for col in range(len(estado.board)):
            for line in range(len(estado.board)):
                if estado.board[col][line] == 'B':
                    count += len(estado.board) - col

    return count

def func_aval_belarmino(state, jogador):
    count = 0
    if jogador == 1:
        for i in range(1, 9):
            count += (i ** i) * count_pieces_line(state, jogador, i)
    else:
        for i in range(8, 0, -1):
            count += ((9-i) ** (9-i)) * count_pieces_line(state, jogador, i)
    return count