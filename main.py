from kivy.app import App
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
    )
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height/2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

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

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        global x, y
        self.ball.move()
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))

        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if self.player1.score > 9:
            i.cancel()
            x = Label(text="Player 1 wins", center_x=self.center_x/2, center_y=self.center_y*3/4, font_size=40)
            y = Button(text="play again", on_press=self.play_again)
            self.add_widget(x)
            self.add_widget(y)

        if self.player2.score > 9:
            i.cancel()
            x = Label(text="Player 2 wins", center_x=self.center_x/2, center_y=self.center_y*3/4, font_size=40)
            y = Button(text="play again", on_press=self.play_again)
            self.add_widget(x)
            self.add_widget(y)
            
    def play_again(self, ins, pos=False):
        global i
        self.player2.score = self.player1.score = 0
        self.remove_widget(x)
        self.remove_widget(y)
        self.serve_ball()
        i = Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_move(self, touch):
        anim = Animation(center_y=touch.y, duration=0.5)
        if touch.x < self.width / 3:
            anim.start(self.player1)
            # self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            anim.start(self.player2)
            # self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        global i
        game = PongGame()
        game.serve_ball()
        i = Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()