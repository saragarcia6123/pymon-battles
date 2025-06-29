from game import Game
from resources import TITLE_FONT


def title():
    title = TITLE_FONT.render("PyMon Battles!", True, (255, 255, 0))
    title_rect = title.get_rect()
    title_rect.centerx = int(Game().WIDTH / 2)
    title_rect.centery = int(Game().HEIGHT * 0.25)
    return title, title_rect
