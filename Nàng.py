import pygame, sys, random, math, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_DIR, "assets", "PlaywriteIE-VariableFont_wght.ttf")

WIDTH, HEIGHT = 1200, 700

LYRICS = [
    (1.0,"Và nàng ơi những nỗi đau trên đời"),
    (2.5,"Nàng đừng giữ nó ở trên người.."),
    (4.0,"Cứ tin lời anh là tia nắng mai"),
    (6.0,"Bình minh sẽ đưa nó đi xa vời"),
    (8.0,"Và từng buồn đau và từng vết cắt"),
    (9.75,"Và từng tiếc nuối sẽ luôn theo nàng"),
    (11.5,"Nhưng em ơi nó sẽ theo cơn mưa"),
    (13.5,"Biến tâm hồn em thành một rừng hoa sắc màu"),
]

BG_TOP=(255,210,235); BG_BOT=(252,228,243)
CREAM=(255,249,244); PINK_DARK=(107,37,64)
PINK_MID=(224,80,122); PINK_LIGHT=(245,194,213)
ENV_BODY_TOP=(249,197,213); ENV_BODY_BOT=(240,128,158)
ENV_FLAP=(232,81,122); WAX_RED=(192,40,74)
WAX_DARK=(140,24,48); TEXT_HINT=(194,69,106)
DIVIDER=(245,194,213)

class Petal:
    def __init__(self,w,h):
        self.w=w; self.h=h
        self.reset()
        self.y=random.uniform(-h,h)

    def reset(self):
        self.x=random.uniform(0,self.w)
        self.y=self.h+20
        self.size=random.uniform(6,15)
        self.speed=random.uniform(0.7,1.8)
        self.drift=random.uniform(-0.6,0.6)
        self.angle=random.uniform(0,math.tau)
        self.spin=random.uniform(-0.04,0.04)
        self.alpha=random.randint(110,210)
        self.color=(random.randint(220,255),random.randint(140,200),random.randint(180,220))

    def update(self):
        self.y-=self.speed
        self.x+=self.drift
        self.angle+=self.spin
        if self.y<-20: self.reset()

    def draw(self,s):
        tmp=pygame.Surface((int(self.size*2+4),)*2,pygame.SRCALPHA)
        cx=cy=self.size+2
        pts=[(
            cx+self.size*0.52*math.cos(a)*math.cos(self.angle)-self.size*math.sin(a)*math.sin(self.angle),
            cy+self.size*0.52*math.cos(a)*math.sin(self.angle)+self.size*math.sin(a)*math.cos(self.angle)
        ) for a in [i*math.tau/16 for i in range(16)]]
        pygame.draw.polygon(tmp,(*self.color,self.alpha),pts)
        s.blit(tmp,(int(self.x-self.size-2),int(self.y-self.size-2)))

def draw_bg(s):
    for y in range(HEIGHT):
        t=y/HEIGHT
        color=tuple(int(BG_TOP[i]+(BG_BOT[i]-BG_TOP[i])*t) for i in range(3))
        pygame.draw.line(s,color,(0,y),(WIDTH,y))

def draw_env(s,cx,cy,w=350,h=250,open=False):
    x,y=cx-w//2,cy-h//2
    pygame.draw.rect(s,ENV_BODY_BOT,(x,y,w,h),border_radius=12)
    pygame.draw.rect(s,ENV_BODY_TOP,(x,y,w,h//2),border_radius=12)

    pts=[(x,y),(x+w,y),(cx,cy+h//3-10 if not open else y-h//3+10)]
    pygame.draw.polygon(s,ENV_FLAP,pts)
    pygame.draw.polygon(s,PINK_MID,pts,2)

    pygame.draw.rect(s,PINK_MID,(x,y,w,h),2,border_radius=12)

    pygame.draw.circle(s,WAX_DARK,(cx,cy+14),20)
    pygame.draw.circle(s,WAX_RED,(cx,cy+14),18)

    return pygame.Rect(x,y,w,h)

def draw_star(s,x,y,size,color):
    pts=[(
        x+(size if i%2==0 else size//2)*math.sin(i*math.pi/5),
        y-(size if i%2==0 else size//2)*math.cos(i*math.pi/5)
    ) for i in range(10)]
    pygame.draw.polygon(s,color,pts)

def draw_letter(s,a,text,ta,f):
    lw,lh=600,380
    lx,ly=(WIDTH-lw)//2,(HEIGHT-lh)//2

    paper=pygame.Surface((lw,lh),pygame.SRCALPHA)
    paper.fill((*CREAM,a))
    pygame.draw.rect(paper,(*PINK_LIGHT,a),paper.get_rect(),2,14)
    s.blit(paper,(lx,ly))

    if a<80: return None

    center_x=WIDTH//2
    y=ly+25

    draw_star(s,center_x-40,y,6,PINK_MID)
    draw_star(s,center_x+40,y,6,PINK_MID)

    s2=6
    pygame.draw.circle(s,PINK_MID,(center_x-s2//2,y),s2//2)
    pygame.draw.circle(s,PINK_MID,(center_x+s2//2,y),s2//2)
    pygame.draw.polygon(s,PINK_MID,[(center_x-s2,y),(center_x+s2,y),(center_x,y+s2)])

    pygame.draw.circle(s,WAX_DARK,(center_x,ly+70),30)
    pygame.draw.circle(s,WAX_RED,(center_x,ly+70),28)

    ht=f["heart"].render("Duck",True,(255,255,255))
    s.blit(ht,ht.get_rect(center=(center_x,ly+70)))

    if text:
        t=f["lyric"].render(text,True,PINK_DARK)
        t.set_alpha(ta)
        shadow=f["lyric"].render(text,True,(220,190,200))
        shadow.set_alpha(ta//3)
        r=t.get_rect(center=(center_x,ly+lh//2))
        s.blit(shadow,(r.x+2,r.y+2))
        s.blit(t,r)

    sig=f["sig"].render("-Nàng-",True,(192,128,144))
    s.blit(sig,sig.get_rect(center=(center_x,ly+lh-40)))

    btn=pygame.Rect(center_x-60,ly+lh+30,120,24)
    pygame.draw.rect(s,PINK_LIGHT,btn,12)
    pygame.draw.rect(s,PINK_MID,btn,1,12)

    txt=f["small"].render("X Đóng lại",True,TEXT_HINT)
    s.blit(txt,txt.get_rect(center=btn.center))

    return btn

def get_lyric(t):
    for time,line in reversed(LYRICS):
        if t>=time: return line
    return ""

def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()

    def font(size):
        try: return pygame.font.Font(font_path,size)
        except: return pygame.font.SysFont("arial",size)

    fonts={
        "lyric":font(30),
        "sig":font(18),
        "small":font(16),
        "heart":font(20),
        "hint":font(18),
    }

    petals=[Petal(WIDTH,HEIGHT) for _ in range(30)]
    bg=pygame.Surface((WIDTH,HEIGHT)); draw_bg(bg)

    state="closed"
    start=0
    la=ta=0
    text=""
    btn=None
    hint_a=0; hint_t=0

    while True:
        dt=clock.tick(60)

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if state=="closed":
                    state="opening"; start=pygame.time.get_ticks()
                elif state=="open" and btn and btn.collidepoint(e.pos):
                    state="closed"; la=ta=0

        for p in petals: p.update()

        hint_t+=dt
        if hint_t>1200: hint_a=min(255,hint_a+4)

        if state=="opening":
            la=min(255,la+6)
            if la>=255: state="open"

        if state in ("opening","open"):
            t=(pygame.time.get_ticks()-start)/1000
            text=get_lyric(t)
            ta=min(255,ta+5)

        screen.blit(bg,(0,0))
        for p in petals: p.draw(screen)

        if state=="closed":
            draw_env(screen,WIDTH//2,HEIGHT//2)
            hint=fonts["hint"].render("✦ Nhấp vào phong bì để mở ✦",True,TEXT_HINT)
            hint.set_alpha(hint_a)
            screen.blit(hint,hint.get_rect(center=(WIDTH//2,HEIGHT//2+150)))
        else:
            draw_env(screen,WIDTH-90,HEIGHT-75,150,107,True)
            btn=draw_letter(screen,la,text,ta,fonts)

        pygame.display.flip()

if __name__=="__main__":
    main()