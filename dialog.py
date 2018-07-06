import json

with open('dialog.json') as data_file:
    dialog_msg = json.load(data_file)

def draw_dialog(self):
    image = pg.transform.scale(self.dialog_img, (WIDTH, int(HEIGHT/4)))
    image.set_colorkey(WHITE)
    self.screen.blit(image, (0, HEIGHT-int(HEIGHT/4)))
    label = pg.font.SysFont("monospace", 15).render(dialog_msg[0][], 1, BLACK)
    self.screen.blit(label, (100, 100))
