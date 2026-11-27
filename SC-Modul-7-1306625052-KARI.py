import pygame, math, sys, random, os
from collections import deque

pygame.init()
# --- CONFIG ---
WIDTH, HEIGHT = 1050, 600
FPS = 60

# Table margins (where ball bounces)
TABLE_LEFT = 50
TABLE_TOP = 60
TABLE_WIDTH = 950
TABLE_HEIGHT = 470
TABLE_RIGHT = TABLE_LEFT + TABLE_WIDTH
TABLE_BOTTOM = TABLE_TOP + TABLE_HEIGHT

# Colors
GREEN = (0, 150, 80)
WHITE = (250, 250, 250)
WHITEDULL = (243, 243, 242)
BLACK = (10, 10, 10)
GRAY = (200, 200, 200)
RED = (200, 20, 20)
BLUE = (45, 127, 184)
GOLD = (248, 179, 35)
BROWN = (90, 60, 40)
YELLOW = (255, 215, 0)

# Pockets (6)
POCKETS = [
    (TABLE_LEFT, TABLE_TOP),
    ((TABLE_LEFT + TABLE_RIGHT) // 2, TABLE_TOP),
    (TABLE_RIGHT, TABLE_TOP),
    (TABLE_LEFT, TABLE_BOTTOM),
    ((TABLE_LEFT + TABLE_RIGHT) // 2, TABLE_BOTTOM),
    (TABLE_RIGHT, TABLE_BOTTOM)
]
POCKET_RADIUS = 30

# Ball config
BALL_RADIUS = 14
BALL_MASS = 1.0
FRICTION = 0.994  # per frame multiplier
MIN_VEL = 0.02

# Power config
MAX_POWER = 28.0  # multiplier for velocity from drag
POWER_BAR_POS = (15, 60, 16, 200)  # x,y,w,h

# UI
FONT = pygame.font.Font(None, 28)
FONT_BIG = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIMULASI BILYARD - Full")

clock = pygame.time.Clock()

# Load sounds if available
hit_sound = None
pocket_sound = None
try:
    hit_sound = pygame.mixer.Sound("hit.wav")
    pocket_sound = pygame.mixer.Sound("pocket.wav")
except:
    # sounds optional
    pass

# ------------------ Vector helpers ------------------
def length(vx, vy):
    return math.hypot(vx, vy)

def normalize(vx, vy):
    L = length(vx, vy)
    if L == 0:
        return 0.0, 0.0
    return vx / L, vy / L

def dot(ax, ay, bx, by):
    return ax*bx + ay*by

# ------------------ Ball class ------------------
class Ball:
    def __init__(self, x, y, color, name=""):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.color = color
        self.radius = BALL_RADIUS
        self.mass = BALL_MASS
        self.alive = True
        self.name = name  # e.g. "cue", "1", ...

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def update(self):
        if not self.alive:
            return
        self.x += self.vx
        self.y += self.vy
        # friction
        self.vx *= FRICTION
        self.vy *= FRICTION
        if abs(self.vx) < MIN_VEL:
            self.vx = 0.0
        if abs(self.vy) < MIN_VEL:
            self.vy = 0.0

        # wall bounce (consider inner table edges with radius offset)
        left = TABLE_LEFT + self.radius
        right = TABLE_RIGHT - self.radius
        top = TABLE_TOP + self.radius
        bottom = TABLE_BOTTOM - self.radius

        bounced = False
        # x axis
        if self.x < left:
            self.x = left
            self.vx = -self.vx
            bounced = True
        elif self.x > right:
            self.x = right
            self.vx = -self.vx
            bounced = True
        # y axis
        if self.y < top:
            self.y = top
            self.vy = -self.vy
            bounced = True
        elif self.y > bottom:
            self.y = bottom
            self.vy = -self.vy
            bounced = True

        if bounced and hit_sound:
            try:
                hit_sound.play()
            except:
                pass

    def draw(self, surf):
        if not self.alive:
            return
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        # small border
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), self.radius, 1)

# ------------------ Physics collision ------------------
def resolve_ball_collision(b1: Ball, b2: Ball):
    # only if both alive
    if not (b1.alive and b2.alive):
        return
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        # jitter a bit if exactly same position
        dist = 0.001
        dx = 0.001
    if dist < b1.radius + b2.radius:
        # move them apart
        overlap = 0.5 * (b1.radius + b2.radius - dist + 0.001)
        nx, ny = dx / dist, dy / dist
        b1.x -= nx * overlap
        b1.y -= ny * overlap
        b2.x += nx * overlap
        b2.y += ny * overlap

        # relative velocity
        rvx = b2.vx - b1.vx
        rvy = b2.vy - b1.vy
        vel_along_normal = rvx * nx + rvy * ny
        if vel_along_normal > 0:
            return  # moving apart

        # coefficient of restitution (elastic-ish)
        e = 0.95
        j = -(1 + e) * vel_along_normal
        j /= (1 / b1.mass + 1 / b2.mass)

        # apply impulse
        impulse_x = j * nx
        impulse_y = j * ny
        b1.vx -= impulse_x / b1.mass
        b1.vy -= impulse_y / b1.mass
        b2.vx += impulse_x / b2.mass
        b2.vy += impulse_y / b2.mass

        if hit_sound:
            try:
                hit_sound.play()
            except:
                pass

# ------------------ Game Init ------------------
def create_standard_rack(origin_x, origin_y):
    # create triangular rack of 15 colored balls (simplified coloring)
    balls = []
    colors = [RED, BLUE, GOLD, (128,0,128), (0,200,120), (255,140,0)]
    # we will arrange 5 rows: 1,2,3,4,5 -> total 15
    idx = 1
    for row in range(5):
        for col in range(row+1):
            # hexagonal packing
            offset_x = row * (BALL_RADIUS * 2 + 1)
            start_x = origin_x + offset_x
            start_y = origin_y - row * (BALL_RADIUS + 0.5)
            x = start_x
            y = start_y + col * (2 * BALL_RADIUS + 1)
            color = colors[(idx-1) % len(colors)]
            balls.append(Ball(x, y, color, name=str(idx)))
            idx += 1
    return balls

# create balls: cue on left, rack on right
cue_ball = Ball(TABLE_LEFT + 150, TABLE_TOP + TABLE_HEIGHT // 2, WHITE, name="cue")
rack_origin_x = TABLE_LEFT + 600
rack_origin_y = TABLE_TOP + TABLE_HEIGHT // 2
rack_balls = create_standard_rack(rack_origin_x, rack_origin_y)

balls = [cue_ball] + rack_balls  # master list

# Player state
players = ["Player 1", "Player 2"]
scores = [0, 0]
turn = 0  # index of current player
message = "Klik dan tarik bola putih untuk menembak."

# Input state
dragging = False
drag_start = (0, 0)
power = 0.0

# Utility
def any_ball_moving():
    for b in balls:
        if b.alive and (abs(b.vx) > 0 or abs(b.vy) > 0):
            return True
    return False

def balls_in_play():
    return sum(1 for b in balls if b.alive and b.name != "cue")

# ------------------ Main loop ------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # if left button & clicked near cue and cue is alive and all balls are stationary
            if event.button == 1 and cue_ball.alive and not any_ball_moving():
                dx = mx - cue_ball.x
                dy = my - cue_ball.y
                if math.hypot(dx, dy) <= cue_ball.radius + 4:
                    dragging = True
                    drag_start = (mx, my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                dragging = False
                mx, my = pygame.mouse.get_pos()
                # compute power & direction (drag vector from cue to mouse)
                dx = mx - cue_ball.x
                dy = my - cue_ball.y
                # shot vector is opposite direction of drag (pull back)
                shot_vx = -(dx) / 10.0
                shot_vy = -(dy) / 10.0
                # clamp magnitude
                mag = math.hypot(shot_vx, shot_vy)
                if mag > MAX_POWER:
                    scale = MAX_POWER / mag
                    shot_vx *= scale
                    shot_vy *= scale
                cue_ball.vx += shot_vx
                cue_ball.vy += shot_vy
                # small message
                message = f"{players[turn]} menembak (power {round(mag,1)})"

    # Update physics
    # update positions
    for b in balls:
        b.update()

    # resolve collisions pairwise (O(n^2) - OK for ~16 balls)
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            resolve_ball_collision(balls[i], balls[j])

    # pocket detection
    # For any ball that enters pocket radius -> mark not alive and update score/turn rules
    pocketed_queue = deque()
    for b in balls:
        if not b.alive:
            continue
        for px, py in POCKETS:
            if math.hypot(b.x - px, b.y - py) <= POCKET_RADIUS:
                b.alive = False
                # add to queue for scoring handling
                pocketed_queue.append(b)
                if pocket_sound:
                    try:
                        pocket_sound.play()
                    except:
                        pass
                break

    # handle pocketed balls (order matters a little)
    any_color_pocketed = False
    cue_pocketed = False
    while pocketed_queue:
        pb = pocketed_queue.popleft()
        if pb.name == "cue":
            cue_pocketed = True
        else:
            any_color_pocketed = True
            # award points
            scores[turn] += 10

    # if cue pocketed -> penalty & respawn cue to a fixed safe spot, change turn
    if cue_pocketed:
        scores[turn] -= 5
        message = f"{players[turn]} foul! Bola putih masuk (-5)."
        # respawn cue to default location and zero velocity
        cue_ball.x = TABLE_LEFT + 150
        cue_ball.y = TABLE_TOP + TABLE_HEIGHT // 2
        cue_ball.vx = cue_ball.vy = 0.0
        cue_ball.alive = True
        # change turn
        turn = 1 - turn

    # if no color pocketed -> and if cue moved and all balls stopped -> change turn
    # detect if all balls stopped
    if not any_ball_moving():
        # if there were pocketed color balls -> same player continues (like normal pool)
        if any_color_pocketed:
            message = f"{players[turn]} mendapatkan poin dan tetap menembak."
        else:
            # if there was a shot (we can detect from cue velocity zero and not dragging)
            # switch turn if previously a shot happened and no colors pocketed
            # For simplicity: if last message said "menembak" and now all stop without color pocketed -> turn changes
            if "menembak" in message:
                turn = 1 - turn
                message = f"Giliran: {players[turn]}"

    # Drawing
    screen.fill(BROWN)  # outer wood
    # table surface
    pygame.draw.rect(screen, GREEN, (TABLE_LEFT - 10, TABLE_TOP - 10, TABLE_WIDTH + 20, TABLE_HEIGHT + 20))
    # table inner border (white)
    pygame.draw.rect(screen, WHITEDULL, (TABLE_LEFT, TABLE_TOP, TABLE_WIDTH, TABLE_HEIGHT), 6)

    # pockets
    for px, py in POCKETS:
        pygame.draw.circle(screen, BLACK, (int(px), int(py)), POCKET_RADIUS)

    # draw balls
    for b in balls:
        b.draw(screen)

    # draw cue stick (when cue alive and player not moving balls)
    if cue_ball.alive and not any_ball_moving():
        # compute aim direction: mouse -> cue
        mx, my = pygame.mouse.get_pos()
        dx = mx - cue_ball.x
        dy = my - cue_ball.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            nx, ny = 1, 0
        else:
            nx, ny = dx / dist, dy / dist
        # draw a guideline (prediction simple: straight line reflecting walls once)
        # basic prediction: draw a line from cue in opposite direction of pull
        if dragging:
            # draw line from cue to mouse
            pygame.draw.line(screen, WHITE, (int(cue_ball.x), int(cue_ball.y)), (mx, my), 2)
        else:
            # show faint aim line following mouse (visual only)
            aim_len = 220
            ax = cue_ball.x + nx * aim_len
            ay = cue_ball.y + ny * aim_len
            pygame.draw.line(screen, (200,200,200), (int(cue_ball.x), int(cue_ball.y)), (int(ax), int(ay)), 1)

        # draw cue stick rotated: stick extends opposite direction of aim (simulate pulling)
        # stick length
        stick_len = 140
        # stick angle points opposite direction from mouse (you push cue forward to ball)
        stick_end_x = cue_ball.x - nx * (cue_ball.radius + stick_len)
        stick_end_y = cue_ball.y - ny * (cue_ball.radius + stick_len)
        # draw stick (simple thick line)
        pygame.draw.line(screen, (160,110,60), (int(stick_end_x), int(stick_end_y)), (int(cue_ball.x), int(cue_ball.y)), 8)
        # small highlight
        pygame.draw.line(screen, (220,180,120), (int(stick_end_x), int(stick_end_y)), (int(cue_ball.x), int(cue_ball.y)), 2)

    # power bar (visual fill based on drag distance)
    pygame.draw.rect(screen, (80,80,80), POWER_BAR_POS, 2)
    # compute current power fill if dragging
    if dragging:
        mx, my = pygame.mouse.get_pos()
        dx = mx - cue_ball.x
        dy = my - cue_ball.y
        p = math.hypot(dx, dy) / 10.0
        if p > MAX_POWER:
            p = MAX_POWER
        # map p to bar height
        bar_x, bar_y, bar_w, bar_h = POWER_BAR_POS
        fill_h = int((p / MAX_POWER) * (bar_h - 6))
        pygame.draw.rect(screen, YELLOW, (bar_x+3, bar_y + bar_h - 3 - fill_h, bar_w-6, fill_h))

    # UI text: scores and turn
    score_text = FONT.render(f"{players[0]}: {scores[0]}     {players[1]}: {scores[1]}", True, WHITE)
    turn_text = FONT.render(f"Giliran: {players[turn]}", True, WHITE)
    balls_left = FONT.render(f"Bola warna tersisa: {balls_in_play()}", True, WHITE)
    screen.blit(score_text, (20, HEIGHT - 35))
    screen.blit(turn_text, (20, HEIGHT - 60))
    screen.blit(balls_left, (WIDTH - 240, HEIGHT - 35))

    # message center
    msg_surf = FONT_BIG.render(message, True, WHITE)
    screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 10))

    # victory check
    if balls_in_play() == 0:
        win_msg = FONT_BIG.render(f"{players[turn]} menang! Semua bola masuk.", True, YELLOW)
        screen.blit(win_msg, (WIDTH//2 - win_msg.get_width()//2, HEIGHT//2 - 20))

    pygame.display.flip()

pygame.quit()
sys.exit()