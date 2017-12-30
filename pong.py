from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import math

Window.clearcolor = (.1, .9, .9, .6)

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        
def GetAngleOfLineBetweenTwoPoints(p1, p2):
    xDiff = p2.x - p1.x
    yDiff = p2.y - p1.y
    return math.degrees(math.atan2(yDiff, xDiff))

def PaddleTargetY(point1,point2,distancex):
    angle1 = GetAngleOfLineBetweenTwoPoints(point1,point2)
    return (distancex * math.tan(math.radians(angle1)))


class PongPaddle(Widget):
    score = NumericProperty(0)
  
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            return True


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    startgame = False
    p1, p2 = None, None

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        player1move=20
        player2move=20
        paddlecentersize=100

        if keycode[1] == 'spacebar':
            self.startgame = True    
        if keycode[1] == 'w':
            if (self.top - self.player1.center_y-paddlecentersize) < player1move:
                player1move = self.top - self.player1.center_y-paddlecentersize
            self.player1.center_y += player1move
        elif keycode[1] == 's':
            if (self.player1.center_y-self.y-paddlecentersize) < player1move:
                player1move = self.y-self.player1.center_y-paddlecentersize
            if player1move > 0: self.player1.center_y -= player1move
        elif keycode[1] == 'up':
            if (self.top - self.player2.center_y-paddlecentersize) < player2move:
                player2move = self.top - self.player2.center_y-paddlecentersize
            self.player2.center_y += player2move
        elif keycode[1] == 'down':
            if (self.player2.center_y-self.y-paddlecentersize) < player2move:
                player2move = self.y-self.player2.center_y-paddlecentersize
            if player2move > 0: self.player2.center_y -= player2move
        return True

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        if self.startgame: 
            self.ball.move()
        
        # self play player2
        if self.ball.velocity_x > 0:
            if self.p1 is None: 
                self.p1 = Point(self.ball.x,self.ball.y)
            elif self.p1 is not None and self.p2 is None:   
                self.p2 = Point(self.ball.x,self.ball.y)
                self.player2.center_y = self.p1.y + PaddleTargetY(self.p1,self.p2,self.width)
             

        # bounce of paddles
        if self.player1.bounce_ball(self.ball):
            self.p1, self.p2 = None, None
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            self.p1, self.p2 = None, None

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
            self.startgame = False
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            self.startgame = False

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
    def on_touch_down(self, touch):
        self.startgame = True

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()