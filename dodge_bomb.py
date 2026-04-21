import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数: こうかとんRectかばくだんRect
    戻り値: タプル (横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    gm_img = pg.Surface((WIDTH,HEIGHT))
    gm_img.fill((0, 0, 0))
    gm_img.set_alpha(128)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255)) 
    txt_rct = txt.get_rect(center =(WIDTH// 2, HEIGHT// 2))

    kk_img = pg.image.load("fig/8.png")
    kk_rct_1 = kk_img.get_rect()
    kk_rct_1.center = (WIDTH//2 - 250, HEIGHT//2)
    kk_rct_r = kk_img.get_rect()
    kk_rct_r.center = (WIDTH//2 + 250, HEIGHT//2)

    gm_img.blit(txt,txt_rct)
    gm_img.blit(kk_img, kk_rct_1)
    gm_img.blit(kk_img, kk_rct_r)
    screen.blit(gm_img, [0, 0])

    pg.display.update()
    time.sleep(5)
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_img.set_colorkey((0, 0, 0))
    return bb_imgs, bb_accs
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0)) 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = 5, 5

    bb_imgs, bb_accs = init_bb_imgs()
    idx = 0
    bb_img = bb_imgs[idx]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)



    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        original_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = original_center

        bb_rct.move_ip(avx, avy)
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        DELTA = {pg.K_UP:(0, -5),pg.K_DOWN:(0, +5),pg.K_LEFT:(-5, 0),pg.K_RIGHT:(+5, 0)}
        if key_lst[pg.K_UP]:
            sum_mv= DELTA[pg.K_UP]
        if key_lst[pg.K_DOWN]:
            sum_mv= DELTA[pg.K_DOWN]
        if key_lst[pg.K_LEFT]:
            sum_mv= DELTA[pg.K_LEFT]
        if key_lst[pg.K_RIGHT]:
            sum_mv= DELTA[pg.K_RIGHT]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip((vx, vy))
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
