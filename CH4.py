import tkinter
import random
import time

tk = tkinter.Tk()
# 呼叫 Tk() 函數建立一個視窗實體
tk.title("Game")
# 窗口取一个名字叫game
tk.resizable(0,0)
# 通知窗口管理器调整布局大小,0,0表示不能被拉升
tk.wm_attributes("-topmost",True)
# 窗口置于其它窗口前面
# 原本是1, 類似true
canvas = tkinter.Canvas(tk,width = 700,height = 700,bd = 0,highlightthickness=0)
#让画布更加美观，之外无边框 / highlightthickness: 讓球碰到底部的線不見,強制為0
canvas.configure(background='black')
canvas.pack()
# #让画布按照前一行给出的宽度与高度调整自身大小
tk.update()
# #游戏动画初始

class Ball:
    def __init__(self, canvas, paddle,score, color):
        # #初始化函数，包括画布与颜色
        self.canvas = canvas
        # 把參數canvas 指派給物件變數 canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(50,50,75,75,fill=color)
        # 記錄球的位置(x,y),呼叫create_oval Function,建立橢圓形物件,其中五個參數：左上角x,y座標,右上角x,y座標,最後是填充的顏色(color parameter放進去）, id 也就是球的位置保存起來
        self.canvas.move(self.id,290,100)
        # 把橢圓形物件移動到畫布中心
        starts = [-3,-2,-1,1,2,3]
        # 增starts 列表變數
        random.shuffle(starts)
        # starts 列表年的元素順序隨機變動
        self.x = starts[0]
        # 列表內的第一個元素指派給x物件變數
        self.y = -3
        # -3
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        # 獲取畫布當前的高度, 並回傳給canvas_height
        self.hit_button = False
        #  增加輸贏機制：當小球碰到畫布底部,玩家就輸了

# 判斷彈力球是否擊中球拍
    def hit_paddle(self,pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
        # 判斷小球的右下角x2 大於等於球拍左邊框x1 ,小球左上角x1 小於等於球拍右邊框x2
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                # 判斷小球底部是否在球拍的頂部與底部之間
                self.x += self.paddle.x
                # 球的速度加上球拍速度 ball = ball + paddle
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        # 增加x,y
        pos = self.canvas.coords(self.id)
        # 新增pos , coords 這個功能可取得id物件的座標,變成list: pos[x1,y1,x2,y2]
        if pos[1] <= 0:
            # 判斷y1座標是否小於等於0,
            self.y = 1
        if pos[3] >= self.canvas_height:
            # 判斷y2座標是否大於畫布高度,有沒有碰到底部
            self.hit_button = True
        if self.hit_paddle(pos) == True:
            self.y = -3
            # 擊中球拍後往上走
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

# 球拍
# 按下左鍵瞬間->球拍往左移->變數 x = x-2
# 按下右鍵瞬間->球拍往右移->變數 x = x+2
# 增加：按下滑鼠左鍵,開始遊戲
class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,200,20,fill=color)
        self.canvas.move(self.id,250,500)
        self.x = 0
        # 和Ball的class一樣,設定x變數記住位置
        self.started = False
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        self.canvas.bind_all('<Button-1>',self.start_game)


    def draw(self):
        self.canvas.move(self.id,self.x,0)
        # 增加x,y變數
        pos = self.canvas.coords(self.id)
        # 新增pos變數取得id物件的座標
        if pos[0] <= 0:
            self.x = 0
            # 球拍不像小球依樣需要自動回彈,所以設置水平x為0,讓他停止動作
        if pos[2] >= self.canvas_width:
            self.x = 0
            # 如果右下角x ,右邊已經達到右邊框,同樣設置為0,停止動作

    def turn_left(self,evt):
        # 建立向左移的function,方便呼叫使用 （evt:event簡寫
        self.x = -2
    def turn_right(self,evt):
        # 建立向右移的function,方便呼叫使用
        self.x = 2
    def start_game(self,evt):
        self.started = True

class Score:
    def __init__(self,canvas,color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(600,70,text=self.score,fill=color,font=("Purisa",50))

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id,text=self.score)
        # itemconfig是一個轉換的功能

score = Score(canvas,'green')
paddle = Paddle(canvas,'blue')
ball = Ball(canvas,paddle,score,'red')
# 建立一個紅色彈力球物件
game_over_text = canvas.create_text(350,300,text='GAME OVER',state='hidden',fill='white')
# 定義一個game over變數 , text 是具名參數

while True:
    if ball.hit_button == False and paddle.started == True:
     # 根據hit_bottom決定是否結束遊戲 / paddle.stared 決定遊戲是否開始
        ball.draw()
        paddle.draw()
    if ball.hit_button == True:
        time.sleep(1)
        # 暫停一秒再顯示game over
        canvas.itemconfig(game_over_text,state='normal')
    tk.update_idletasks()
    # 不段的運行下去,tkinter 會任不斷重新畫製畫布
    tk.update()
    # 讓更新畫製畫布速度加快
    time.sleep(0.01)
    # sleep 是暫停執行的秒數,參數可以是浮點數,以指示更精確的暫停時間