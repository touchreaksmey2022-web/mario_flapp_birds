"""Generate all Super Mario-themed game assets using PIL."""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "/home/claude/mario_flappy/assets"
os.makedirs(OUT, exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def save(img, name):
    img.save(f"{OUT}/{name}")
    print(f"  saved {name}")

# ══════════════════════════════════════════════════════════════════════════════
# MARIO CHARACTER  (34×40 px sprite-sheet style)
# ══════════════════════════════════════════════════════════════════════════════
def make_mario(w=34, h=40):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # hat (red)
    d.rectangle([10,2,24,8],  fill=(200,30,30))
    d.rectangle([7,8,27,10],  fill=(200,30,30))
    # face (skin)
    d.rectangle([8,10,26,20], fill=(255,198,148))
    # eyes
    d.rectangle([12,12,15,14],fill=(0,0,0))
    d.rectangle([20,12,23,14],fill=(0,0,0))
    # moustache
    d.rectangle([10,16,16,18],fill=(100,50,0))
    d.rectangle([19,16,25,18],fill=(100,50,0))
    d.rectangle([13,18,22,20],fill=(100,50,0))
    # overalls (blue)
    d.rectangle([8,20,26,32], fill=(30,80,200))
    # buttons
    d.rectangle([12,22,14,24],fill=(255,220,0))
    d.rectangle([21,22,23,24],fill=(255,220,0))
    # shirt (red)
    d.rectangle([6,22,9,30],  fill=(200,30,30))
    d.rectangle([26,22,29,30],fill=(200,30,30))
    # shoes
    d.rectangle([6,32,16,38], fill=(100,50,0))
    d.rectangle([18,32,28,38],fill=(100,50,0))
    return img

save(make_mario(), "mario.png")

# ══════════════════════════════════════════════════════════════════════════════
# PIPE (green, top/bottom variants)
# ══════════════════════════════════════════════════════════════════════════════
def make_pipe(top=True, pw=64, ph=512):
    img = Image.new("RGBA", (pw, ph), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # body
    d.rectangle([4,0,pw-4,ph], fill=(0,160,0))
    # stripe
    for y in range(0, ph, 32):
        d.rectangle([4,y,pw-4,y+16], fill=(0,180,0))
    # border
    d.rectangle([4,0,pw-4,ph], outline=(0,80,0), width=2)
    # rim
    rim_h = 30
    rim_color = (0,200,0)
    rim_y = 0 if top else ph - rim_h
    d.rectangle([0, rim_y, pw, rim_y+rim_h], fill=rim_color, outline=(0,100,0), width=2)
    return img

save(make_pipe(top=True),  "top_pipe.png")
save(make_pipe(top=False), "bottom_pipe.png")

# ══════════════════════════════════════════════════════════════════════════════
# BACKGROUNDS – 3 Levels
# ══════════════════════════════════════════════════════════════════════════════
def draw_clouds(d, level):
    """Draw simple white clouds."""
    clouds = [(50,60),(150,40),(260,70),(80,130),(200,110)]
    for cx,cy in clouds:
        for dx,dy in [(0,0),(-15,8),(15,8),(-8,15),(8,15),(0,18)]:
            r = 18 if (dx,dy)==(0,0) else 12
            d.ellipse([cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r], fill=(255,255,255,200))

def make_bg_easy(W=360, H=640):
    """World 1: sunny grass plains."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # Sky gradient (blue top → lighter blue bottom)
    for y in range(H):
        t = y/H
        r = int(100+t*55); g = int(160+t*50); b = int(240-t*20)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    draw_clouds(d, 1)
    # Sun
    d.ellipse([290,30,340,80], fill=(255,240,0), outline=(255,200,0), width=3)
    # Ground
    d.rectangle([0,H-60,W,H], fill=(100,70,30))
    d.rectangle([0,H-80,W,H-60], fill=(60,160,60))
    # Brick blocks row
    bw=40; bh=20
    for bx in range(0,W,bw):
        d.rectangle([bx,H-130,bx+bw-2,H-111], fill=(180,100,40), outline=(120,60,20))
    # Hills
    for hx,hy,hr in [(60,H-80,50),(200,H-80,40),(300,H-80,60)]:
        d.ellipse([hx-hr,hy-hr//2,hx+hr,hy], fill=(50,140,50))
    # Mushrooms
    for mx in [100,250]:
        d.ellipse([mx-12,H-105,mx+12,H-85], fill=(220,40,40))
        d.rectangle([mx-4,H-88,mx+4,H-70], fill=(210,180,140))
    return img

def make_bg_medium(W=360, H=640):
    """World 2: underground cave."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # Dark cave bg
    for y in range(H):
        t = y/H
        r = int(20+t*15); g = int(15+t*10); b = int(40+t*20)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    # Rock ceiling
    for x in range(0, W, 20):
        h2 = 30 + (hash(x)%20)
        d.polygon([(x,0),(x+20,0),(x+10,h2)], fill=(80,70,60))
    # Rock floor
    for x in range(0, W, 20):
        h2 = 30 + (hash(x*3)%20)
        d.polygon([(x,H),(x+20,H),(x+10,H-h2)], fill=(80,70,60))
    # Glowing crystals
    for cx,cy,col in [(40,200,(100,200,255)),(280,300,(200,100,255)),(150,450,(100,255,200))]:
        for size in [30,20,12]:
            alpha = 80 if size==30 else (140 if size==20 else 200)
            overlay = Image.new("RGBA",(W,H),(0,0,0,0))
            od = ImageDraw.Draw(overlay)
            od.ellipse([cx-size,cy-size,cx+size,cy+size], fill=(*col,alpha))
            img = Image.alpha_composite(img, overlay)
            d = ImageDraw.Draw(img)
        d.polygon([(cx,cy-25),(cx-10,cy),(cx,cy+15),(cx+10,cy)], fill=col)
    # Coins
    for coinx in [80,160,240,320]:
        d.ellipse([coinx-8,H//2-8,coinx+8,H//2+8], fill=(255,220,0), outline=(200,160,0))
        d.text((coinx-4, H//2-7),"$", fill=(180,130,0))
    return img

def make_bg_hard(W=360, H=640):
    """World 3: volcano / lava castle."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # Dark red/orange sky
    for y in range(H):
        t = y/H
        r = int(60+t*80); g = int(10+t*20); b = 0
        d.line([(0,y),(W,y)], fill=(r,g,b))
    # Castle walls
    d.rectangle([20,100,100,H-60], fill=(80,70,70), outline=(50,40,40))
    d.rectangle([260,100,340,H-60],fill=(80,70,70), outline=(50,40,40))
    # Battlements
    for bx in range(20,100,20):
        d.rectangle([bx,80,bx+15,100], fill=(80,70,70))
    for bx in range(260,340,20):
        d.rectangle([bx,80,bx+15,100], fill=(80,70,70))
    # Castle windows (glowing)
    for wx,wy in [(40,160),(70,160),(275,160),(305,160),(40,240),(70,240)]:
        d.rectangle([wx,wy,wx+20,wy+25], fill=(255,180,0))
    # Volcano
    d.polygon([(130,H-60),(180,200),(230,H-60)], fill=(100,80,80), outline=(70,50,50))
    # Lava glow
    for lx,ly,lr in [(180,H-80,40),(100,H-70,25),(270,H-75,30)]:
        for size in [lr,lr//2]:
            overlay = Image.new("RGBA",(W,H),(0,0,0,0))
            od = ImageDraw.Draw(overlay)
            alpha = 80 if size==lr else 160
            od.ellipse([lx-size,ly-size//2,lx+size,ly+size//2], fill=(255,100,0,alpha))
            img = Image.alpha_composite(img, overlay)
            d = ImageDraw.Draw(img)
    # Lava river
    d.rectangle([0,H-60,W,H], fill=(220,60,0))
    for lx in range(0,W,20):
        wave_y = H-60 + int(5*math.sin(lx/15))
        d.ellipse([lx,wave_y,lx+20,wave_y+12], fill=(255,120,0))
    # Bats
    for bx,by in [(60,300),(290,250),(180,350)]:
        d.polygon([(bx,by),(bx-20,by-10),(bx-5,by)], fill=(30,0,30))
        d.polygon([(bx,by),(bx+20,by-10),(bx+5,by)], fill=(30,0,30))
    return img

save(make_bg_easy(),   "bg_easy.png")
save(make_bg_medium(), "bg_medium.png")
save(make_bg_hard(),   "bg_hard.png")

print("\nAll assets generated!")
