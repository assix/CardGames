import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
BG_COLOR = (180, 0, 0)  # Dark Red Table
CARD_WIDTH, CARD_HEIGHT = 70, 100

# UNO Colors
RED = (255, 85, 85)
GREEN = (85, 170, 85)
BLUE = (85, 85, 255)
YELLOW = (255, 170, 0)
BLACK = (50, 50, 50)
WHITE = (255, 255, 255)

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
COLOR_MAP = {'Red': RED, 'Green': GREEN, 'Blue': BLUE, 'Yellow': YELLOW, 'Wild': BLACK}
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Rev', '+2']

# --- Classes ---
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.rect = None
        
    def __str__(self):
        return f"{self.color} {self.value}"

    def get_draw_color(self):
        return COLOR_MAP.get(self.color, BLACK)

class Deck:
    def __init__(self):
        self.cards = []
        # Generate Number Cards & Actions
        for color in COLORS:
            self.cards.append(Card(color, '0'))
            for val in VALUES[1:]:
                self.cards.append(Card(color, val))
                self.cards.append(Card(color, val))
        
        # Generate Wilds
        for _ in range(4):
            self.cards.append(Card('Wild', 'Wild'))
            self.cards.append(Card('Wild', '+4'))
            
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

# --- Game Logic ---
def is_valid_move(card, top_card, current_color):
    if card.color == 'Wild': return True
    if card.color == current_color: return True
    if card.value == top_card.value: return True
    return False

def get_best_color(hand):
    # Counts colors in hand to pick best one for Wild
    colors = [c.color for c in hand if c.color in COLORS]
    if not colors: return 'Red' # Default
    return max(set(colors), key=colors.count)

def draw_text(surface, text, x, y, size=30, color=WHITE, center=False):
    font = pygame.font.SysFont('Arial', size, bold=True)
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
    else:
        surface.blit(img, (x, y))

def draw_card(surface, card, x, y, hidden=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    
    if hidden:
        pygame.draw.rect(surface, BLACK, rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
        draw_text(surface, "UNO", x + CARD_WIDTH//2, y + CARD_HEIGHT//2, 20, RED, True)
    else:
        col = card.get_draw_color()
        pygame.draw.rect(surface, col, rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
        
        # The classic Oval design
        pygame.draw.ellipse(surface, WHITE, (x+5, y+15, CARD_WIDTH-10, CARD_HEIGHT-30))
        
        # Value text
        txt_col = col if col != YELLOW else (200, 140, 0) # Darker yellow for text visibility
        if card.color == 'Wild': txt_col = BLACK
            
        display_val = card.value
        if display_val == 'Skip': display_val = "⊘"
        elif display_val == 'Rev': display_val = "⇄"
        
        draw_text(surface, display_val, x + CARD_WIDTH//2, y + CARD_HEIGHT//2, 25 if len(display_val)<3 else 20, txt_col, True)
        
        # Corner numbers
        draw_text(surface, display_val[0], x + 8, y + 8, 12, WHITE)
        
    card.rect = rect

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UNO - Linux Python")
    clock = pygame.time.Clock()

    deck = Deck()
    player_hand = [deck.draw() for _ in range(7)]
    cpu_hand = [deck.draw() for _ in range(7)]
    
    # Initial Discard (Ensure not Wild for simplicity)
    discard = deck.draw()
    while discard.color == 'Wild':
        deck.cards.insert(0, discard)
        discard = deck.draw()
    
    discard_pile = [discard]
    current_color = discard.color
    
    game_over = False
    message = "Your Turn"
    player_turn = True
    cpu_timer = 0
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # --- Player Interaction ---
            if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Draw Pile
                draw_rect = pygame.Rect(SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 50, CARD_WIDTH, CARD_HEIGHT)
                if draw_rect.collidepoint(pos):
                    new_card = deck.draw()
                    if new_card: player_hand.append(new_card)
                    player_turn = False
                    cpu_timer = current_time + 1000
                    message = "CPU Thinking..."
                
                # Card Play
                else:
                    for card in player_hand:
                        if card.rect and card.rect.collidepoint(pos):
                            if is_valid_move(card, discard_pile[-1], current_color):
                                player_hand.remove(card)
                                discard_pile.append(card)
                                
                                # Effects
                                if card.color == 'Wild':
                                    # Auto-pick best color for player ease
                                    current_color = get_best_color(player_hand)
                                else:
                                    current_color = card.color
                                
                                # Action Cards
                                turn_skip = False
                                if card.value == 'Skip' or card.value == 'Rev': # Rev is Skip in 1v1
                                    turn_skip = True
                                    message = "CPU Skipped!"
                                elif card.value == '+2':
                                    for _ in range(2): cpu_hand.append(deck.draw())
                                    turn_skip = True
                                    message = "CPU Draw 2 & Skipped!"
                                elif card.value == '+4':
                                    for _ in range(4): cpu_hand.append(deck.draw())
                                    turn_skip = True
                                    message = "CPU Draw 4 & Skipped!"

                                if turn_skip:
                                    player_turn = True # It's player turn again
                                else:
                                    player_turn = False
                                    cpu_timer = current_time + 1000
                                    message = "CPU Thinking..."
                                break

        # --- CPU Logic ---
        if not game_over and not player_turn and current_time >= cpu_timer:
            played = False
            
            # Simple AI
            for card in cpu_hand:
                if is_valid_move(card, discard_pile[-1], current_color):
                    cpu_hand.remove(card)
                    discard_pile.append(card)
                    
                    if card.color == 'Wild':
                        current_color = get_best_color(cpu_hand)
                    else:
                        current_color = card.color
                    
                    # Effects
                    turn_skip = False
                    if card.value == 'Skip' or card.value == 'Rev':
                        turn_skip = True
                        message = "You were Skipped!"
                    elif card.value == '+2':
                        for _ in range(2): player_hand.append(deck.draw())
                        turn_skip = True
                        message = "You Draw 2 & Skipped!"
                    elif card.value == '+4':
                        for _ in range(4): player_hand.append(deck.draw())
                        turn_skip = True
                        message = "You Draw 4 & Skipped!"

                    if turn_skip:
                        # CPU goes again effectively (reset timer)
                        cpu_timer = current_time + 1000 
                    else:
                        player_turn = True
                        message = "Your Turn"
                    
                    played = True
                    break
            
            if not played:
                new_card = deck.draw()
                if new_card: cpu_hand.append(new_card)
                player_turn = True
                message = "Your Turn"

        # --- Check Win ---
        if not player_hand:
            game_over = True
            message = "YOU WIN!"
        elif not cpu_hand:
            game_over = True
            message = "CPU WINS!"

        # --- Rendering ---
        screen.fill(BG_COLOR)
        
        # Center Pile
        top_card = discard_pile[-1]
        draw_card(screen, top_card, SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 - 50)
        
        # Current Color Indicator (Circle)
        pygame.draw.circle(screen, COLOR_MAP.get(current_color, BLACK), (SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT//2), 15)
        
        # Draw Pile
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 50, CARD_WIDTH, CARD_HEIGHT), border_radius=8)
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 + 60, SCREEN_HEIGHT//2 - 50, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=8)
        draw_text(screen, "UNO", SCREEN_WIDTH//2 + 75, SCREEN_HEIGHT//2 - 15, 20, RED)

        # Hands
        start_x = (SCREEN_WIDTH - (len(player_hand) * 80)) // 2
        for i, card in enumerate(player_hand):
            # Float card up if hover? Optional polish, keeping simple for now
            draw_card(screen, card, start_x + i * 80, SCREEN_HEIGHT - 130)

        start_x = (SCREEN_WIDTH - (len(cpu_hand) * 80)) // 2
        for i, card in enumerate(cpu_hand):
            draw_card(screen, card, start_x + i * 80, 30, hidden=True)

        # UI Text
        draw_text(screen, message, 20, SCREEN_HEIGHT - 40)
        draw_text(screen, f"Current Color: {current_color}", 20, 20, 20, WHITE)

        # "UNO" Shouts
        if len(player_hand) == 1:
            draw_text(screen, "UNO!", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 80, 40, YELLOW)
        if len(cpu_hand) == 1:
            draw_text(screen, "UNO!", SCREEN_WIDTH - 100, 80, 40, RED)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()