#-*- coding:utf-8 -*-

import curses
from random import randrange, choice # generate and place new tile
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq'] #存储有效输入
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit'] #记录用户行为
actions_dict = dict(zip(letter_codes, actions * 2)) #生成一个字典

#用户输入处理
def get_user_action(keyboard):    
    char = "N"
    while char not in actions_dict:    
        char = keyboard.getch()
    return actions_dict[char]

#矩阵转置
def transpose(field):
    #从右向左看，先循环便利zip(*field)中的每个元素，对每个元素进行如下操作：
    #先将其值赋给变量row，然后进行list(row)操作，最后将返回的数据追加到要返回的list中
    return [list(row) for row in zip(*field)] 

#矩阵逆转
def invert(field):
    return [row[::-1] for row in field] #[::-1]将列表或字符倒过来

#创建棋盘，初始化棋盘的参数
class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win #过关分数
        self.score = 0 #当前分数
        self.highscore = 0 #最高分
        self.reset() #棋盘重置

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        #field代表一个(x,y)坐标对应的一个方格,将所有方格的数值设置为0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self, direction):
        #一行向左合并
        def move_row_left(row):
            def tighten(row): #把零散的非零单元挤都一块
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row): #对邻近元素进行合并
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            #先挤到一块再合并再挤到一块
            return tighten(merge(tighten(row)))

        #通过矩阵进行转置与逆转，可以从左移得到其余三个方向的移动操作
        moves = {}
        moves['Left']  = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down']  = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        #any():只要有任何元素不为0,'',False,就返回True
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    #随机生成一个2或者4
    def spawn(self):
        #randrange():生成一个随机数，可以指定起始范围和递增基数
        new_element = 4 if randrange(100) > 89 else 2
        #生成一个随机的坐标
        #choice():返回一个列表，元组或字符串的随机项
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    #判断能否移动
    def move_is_possible(self, direction):
        def row_is_left_movable(row): 
            def change(i): 
                if row[i] == 0 and row[i + 1] != 0: # 可以移动
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # 可以合并
                    return True
                return False
            #不能移动，不能合并，返回的都是false
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left']  = lambda field:                              \
                any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

#stdscr代表一个屏幕的对象，属于curses库
def main(stdscr):
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同的状态
        return responses[action]

    def game():
        #画出当前棋盘状态
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'


    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    curses.use_default_colors()
    game_field = GameField(win=32)


    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()


curses.wrapper(main)













