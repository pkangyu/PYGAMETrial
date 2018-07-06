
from __future__ import with_statement
from __future__ import absolute_import
import pygame as pg
import json
from io import open
pg.font.init()

def draw_dialog(self):
        self.dialog_now2 = pg.time.get_ticks()
        hit = self.collide_dialog[0].name
        image = pg.transform.scale(self.game.dialog_img, (WIDTH, MSG_HEIGHT))
        image.set_colorkey(WHITE)
        #blit dialog box
        self.game.screen.blit(image, (0, MSG_HEIGHT*3))
        Name = pg.font.SysFont(u"monospace", 15).render(dialog_msg[hit][u"Name"] + u":",  1, BLACK)
        #blit name
        self.game.screen.blit(Name, (MSG_WRAP_WIDTH, MSG_WRAP_HEIGHT))
        msg = wrapline(dialog_msg[hit][u"msg"], pg.font.SysFont(u"monospace", 15), WIDTH)
        msg_splitted = [msg[x:x+4] for x in xrange(0, len(msg), 4)]
        if len(msg_splitted) > 1:
            self.more_dialog = True
        if self.more_dialog:
                if pg.key.get_pressed()[pg.K_SPACE] and self.dialog_now2 - self.dialog_time2 > 500 :
                    self.dialog_no += 1
                    self.dialog_time2 = self.dialog_now2
        try:
            self.display_msg = msg_splitted[self.dialog_no]
        except IndexError:
            self.display_msg = msg_splitted[0]
            self.dialog_no = 0
            self.more_dialog = False
            self.dialog_activation = False
        LINE_HEIGHT = 15
        for i in self.display_msg:
            Msg = pg.font.SysFont(u"monospace", 15).render(i,1, BLACK)
            self.game.screen.blit(Msg, (MSG_WRAP_WIDTH, MSG_WRAP_HEIGHT + LINE_HEIGHT))
            LINE_HEIGHT += 15


with open(u'dialog.json') as data_file:
    dialog_msg = json.load(data_file)

def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]

    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text=text[nl:]
    return wrapped
def truncline(text, font, maxwidth):
        real=len(text)
        stext=text
        l=font.size(text)[0]
        cut=0
        a=0
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)
            done=0
        return real, done, stext
