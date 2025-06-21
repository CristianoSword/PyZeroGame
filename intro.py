import pgzrun
from pgzero.actor import Actor
from pgzero.rect import Rect

WIDTH = 800
HEIGHT = 450
FLOOR_Y = 380
GRAVITY = 0.7

# Estados do jogo
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'
STATE_LEVEL_COMPLETE = 'level_complete'

# Começa no menu
game_state = STATE_MENU

# Controle som
sound_on = True

# Herói do jogo
class Player:
    def __init__(self):
        self.actor = Actor('hero_idle1')
        self.actor.pos = (100, FLOOR_Y)
        self.vy = 0
        self.on_ground = False
        self.speed = 4

    def update(self):
        # Movimenta esquerda/direita
        if keyboard.left:
            self.actor.x -= self.speed
            self.actor.image = 'hero_walk1'
            self.actor.angle = 0
        elif keyboard.right:
            self.actor.x += self.speed
            self.actor.image = 'hero_walk1'
            self.actor.angle = 0
        else:
            self.actor.image = 'hero_idle1'

        # Aplica gravidade
        self.vy += GRAVITY
        self.actor.y += self.vy

        # Checa colisão com plataformas
        self.on_ground = False
        for plat in platforms:
            if self.actor.colliderect(plat) and self.vy >= 0:
                self.actor.bottom = plat.top
                self.vy = 0
                self.on_ground = True

        # Impede cair no chão (fundo da tela)
        if self.actor.bottom > FLOOR_Y + 70:
            self.actor.bottom = FLOOR_Y + 70
            self.vy = 0
            self.on_ground = True

        # Pulo
        if keyboard.space and self.on_ground:
            self.vy = -14
            # if sound_on:
            #     sounds.jump.play()

    def draw(self):
        self.actor.draw()

# Inimigo simples que patrulha entre 2 pontos
class Enemy:
    def __init__(self, x_min, x_max, y):
        self.actor = Actor('enemy_idle1')
        self.actor.pos = (x_min, y)
        self.x_min = x_min
        self.x_max = x_max
        self.speed = 2
        self.direction = 1  # 1 = direita, -1 = esquerda

    def update(self):
        self.actor.x += self.speed * self.direction
        if self.actor.x > self.x_max:
            self.direction = -1
            self.actor.image = 'enemy_idle1'
            self.actor.angle = 180  # vira para esquerda
        elif self.actor.x < self.x_min:
            self.direction = 1
            self.actor.image = 'enemy_idle1'
            self.actor.angle = 0  # vira para direita

    def draw(self):
        self.actor.draw()

# Botão simples para menu
class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.pos = pos
        self.callback = callback
        self.rect = Rect((pos[0] - 100, pos[1] - 25), (200, 50))

    def draw(self):
        screen.draw.filled_rect(self.rect, (50, 50, 50))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            color='white',
            fontsize=40
        )


    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# Plataformas na tela (x, y, largura, altura)
platforms = [
    Rect((0, FLOOR_Y + 50), (WIDTH, 20)),          # chão
    Rect((100, 340), (100, 15)),
    Rect((230, 310), (90, 15)),
    Rect((360, 280), (80, 15)),
    Rect((480, 250), (70, 15)),
    Rect((600, 220), (60, 15)),
    Rect((700, 190), (50, 15)),
    Rect((620, 150), (60, 15)),
    Rect((520, 120), (50, 15)),
    Rect((420, 90), (40, 15)),
    Rect((320, 60), (30, 15)),  # Pequena plataforma final
]

# Moeda que fica no lugar difícil (topo da última plataforma)
coin = Actor('coin')
coin.pos = (335, 40)

# Cria o jogador e inimigos
player = Player()
enemies = [
    Enemy(250, 320, FLOOR_Y + 35),
    Enemy(420, 540, FLOOR_Y - 100),
]

# Mensagem para mostrar quando passar de fase
level_complete_msg = "Level Complete!"

# Funções dos botões do menu
def start_game():
    global game_state
    game_state = STATE_PLAYING
    reset_game()

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        music.play('background_music.wav')
    else:
        music.stop()

def quit_game():
    exit()

# Cria botões do menu
buttons = [
    Button("Iniciar Game", (WIDTH // 2, 150), start_game),
    Button("Som on/off", (WIDTH // 2, 250), toggle_sound),
    Button("Sair", (WIDTH // 2, 350), quit_game),
]

def reset_game():
    global player, enemies, level_complete_msg
    player.actor.pos = (100, FLOOR_Y)
    player.vy = 0
    player.on_ground = False
    level_complete_msg = ""
    if sound_on:
        music.play('background_music.wav')

def update():
    global game_state, level_complete_msg

    if game_state == STATE_PLAYING:
        player.update()
        for enemy in enemies:
            enemy.update()

        # Verifica colisão com inimigos (morre)
        for enemy in enemies:
            if player.actor.colliderect(enemy.actor):
                game_state = STATE_GAME_OVER
                # if sound_on:
                    # sounds.death.play()

        # Verifica se pegou a moeda (passa de fase)
        if player.actor.colliderect(coin):
            level_complete_msg = "Level Complete!"
            game_state = STATE_LEVEL_COMPLETE
            # if sound_on:
            #     sounds.levelup.play()

def draw():
    screen.clear()

    if game_state == STATE_MENU:
        screen.fill((30, 30, 30))
        screen.draw.text("Cogumelo Game", center=(WIDTH // 2, 80), fontsize=60, color="white")
        for button in buttons:
            button.draw()

    elif game_state == STATE_PLAYING:
        screen.fill((135, 206, 235))  # céu azul

        # Desenha plataformas
        for plat in platforms:
            screen.draw.filled_rect(plat, (100, 200, 100))

        # Desenha moeda
        coin.draw()

        # Desenha inimigos e jogador
        for enemy in enemies:
            enemy.draw()
        player.draw()

    elif game_state == STATE_GAME_OVER:
        screen.fill((100, 0, 0))
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=70, color="white")
        screen.draw.text("Clique na tela para jogar de novo!", center=(WIDTH // 2, HEIGHT // 2 + 40), fontsize=40, color="white")

    elif game_state == STATE_LEVEL_COMPLETE:
        screen.fill((0, 100, 0))
        screen.draw.text(level_complete_msg, center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        screen.draw.text("Clique na tela para continuar", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")

def on_mouse_down(pos):
    global game_state
    if game_state == STATE_MENU:
        for button in buttons:
            button.check_click(pos)
    elif game_state == STATE_GAME_OVER:
        reset_game()
        game_state = STATE_MENU
    elif game_state == STATE_LEVEL_COMPLETE:
        reset_game()
        game_state = STATE_MENU

# Inicia música ('background_music.wav' na pasta music)
    if sound_on:
        music.play('background_music.wav')
