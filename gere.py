
import pygame as pg
import json
pg.font.init()


with open('dialog.json') as data_file:
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
name = wrapline("fvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsdfvvdsd", pg.font.SysFont("monospace", 15), 50)
def msg_split(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
