import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (34, 139, 34)
CARD_WIDTH, CARD_HEIGHT = 80, 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

SUITS = ['♥', '♦', '♣', '♠']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# --- Classes ---
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.color = RED if suit in ['♥', '♦'] else BLACK
        self.rect = None

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

# --- Game Logic ---
def is_valid_move(card, top_card, active_suit):
    if card.rank == '8': return True
    if card.suit == active_suit: return True
    if card.rank == top_card.rank: return True
    return False

def draw_text(surface, text, x, y, size=30, color=BLACK):
    font = pygame.font.SysFont('Arial', size, bold=True)
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def draw_card(surface, card, x, y, hidden=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(surface, WHITE if not hidden else RED, rect, border_radius=5)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=5)
    
    if not hidden:
        draw_text(surface, card.rank, x + 5, y + 5, 20, card.color)
        draw_text(surface, card.suit, x + 5, y + 25, 30, card.color)
        draw_text(surface, card.suit, x + 25, y + 40, 50, card.color)
    else:
        # Card back design
        pygame.draw.line(surface, WHITE, (x+10, y+10), (x+70, y+110), 2)
        pygame.draw.line(surface, WHITE, (x+70, y+10), (x+10, y+110), 2)
    
    card.rect = rect
    return rect

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crazy 8s - Linux (Smooth)")
    clock = pygame.time.Clock()

    # Game State
    deck = Deck()
    player_hand = [deck.draw() for _ in range(5)]
    cpu_hand = [deck.draw() for _ in range(5)]
    discard_pile = [deck.draw()]
    
    active_suit = discard_pile[-1].suit
    game_over = False
    message = "Your Turn"
    
    player_turn = True
    cpu_timer = 0  # Timestamp for when CPU should act

    while True:
        # 1. Update Logic
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # Player Input
            if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                card_played = False
                # Check Hand
                for card in player_hand:
                    if card.rect and card.rect.collidepoint(pos):
                        if is_valid_move(card, discard_pile[-1], active_suit):
                            discard_pile.append(card)
                            player_hand.remove(card)
                            active_suit = card.suit
                            card_played = True
                            player_turn = False
                            cpu_timer = current_time + 1000 # Schedule CPU move in 1s
                            message = "CPU Thinking..."
                            break
                
                # Check Draw
                draw_rect = pygame.Rect(SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 60, CARD_WIDTH, CARD_HEIGHT)
                if not card_played and draw_rect.collidepoint(pos):
                    new_card = deck.draw()
                    if new_card: player_hand.append(new_card)
                    # Pass turn on draw
                    player_turn = False
                    cpu_timer = current_time + 1000
                    message = "CPU Thinking..."

        # CPU Logic (Non-blocking)
        if not game_over and not player_turn:
            if current_time >= cpu_timer:
                played = False
                for card in cpu_hand:
                    if is_valid_move(card, discard_pile[-1], active_suit):
                        discard_pile.append(card)
                        cpu_hand.remove(card)
                        active_suit = card.suit
                        if card.rank == '8':
                            suits = [c.suit for c in cpu_hand]
                            if suits: active_suit = max(set(suits), key=suits.count)
                        played = True
                        break
                
                if not played:
                    new_card = deck.draw()
                    if new_card: cpu_hand.append(new_card)
                
                player_turn = True
                message = "Your Turn"

        # Win Check
        if not player_hand:
            message = "YOU WIN!"
            game_over = True
        elif not cpu_hand:
            message = "CPU WINS!"
            game_over = True

        # 2. Draw Everything
        screen.fill(BG_COLOR)
        
        # Center Area
        top_card = discard_pile[-1]
        draw_card(screen, top_card, SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 - 60)
        draw_text(screen, f"Active Suit: {active_suit}", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 70, 20, WHITE)

        # Draw Pile
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 60, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 60, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)
        draw_text(screen, "DRAW", SCREEN_WIDTH//2 + 75, SCREEN_HEIGHT//2 - 10, 20, WHITE)

        # Hands
        start_x = (SCREEN_WIDTH - (len(player_hand) * 90)) // 2
        for i, card in enumerate(player_hand):
            draw_card(screen, card, start_x + i * 90, SCREEN_HEIGHT - 150)

        start_x = (SCREEN_WIDTH - (len(cpu_hand) * 90)) // 2
        for i, card in enumerate(cpu_hand):
            draw_card(screen, card, start_x + i * 90, 30, hidden=True)

        draw_text(screen, message, 20, SCREEN_HEIGHT - 40, 30, WHITE)

        pygame.display.flip()
        clock.tick(60) # Smooth 60 FPS

if __name__ == "__main__":
    main()