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

def game_over(screen: pg.Surface) -> None: #演習1
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
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:#演習2
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_img.set_colorkey((0, 0, 0))
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int],pg.Surface]: #演習3
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img_f = pg.transform.flip(kk_img, True, False)
    kk_dict = {
        (0, 0): kk_img_f, # キー押下がない場合
        (+5, 0): kk_img_f, # 右
        (+5, -5): pg.transform.rotozoom(kk_img_f, 45, 1.0), # 右上
        (0, -5): pg.transform.rotozoom(kk_img_f, 90, 1.0),  # 上
        (+5, +5): pg.transform.rotozoom(kk_img_f, -45, 1.0),# 右下
        (0, +5): pg.transform.rotozoom(kk_img_f, -90, 1.0), # 下
        (-5, 0): kk_img, # 左
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 左上
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),   # 左下
    }
    return kk_dict
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) # 爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10) # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0)) # 爆弾の黒い部分を透過させる
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9) # 爆弾Rectを取得する
    kk_rct = kk_img.get_rect() # 爆弾の初期横座標を設定する
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)# 爆弾の初期横座標を設定する
    bb_rct.centery = random.randint(0, HEIGHT)# 爆弾の初期縦座標を設定する
    vx, vy = 5, 5 # 爆弾の速度

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
        if kk_rct.colliderect(bb_rct):# こうかとんと爆弾の衝突判定
            game_over(screen)
            return  # ゲームオーバーの意味でmain関数から出る
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
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip((vx, vy)) # 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横方向の判定
            vx *= -1
        if not tate: # 縦方向の判定
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾を表示させる
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
