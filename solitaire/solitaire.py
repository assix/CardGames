import pygame
import random
import sys

# --- SETUP ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 750
CARD_W, CARD_H = 80, 110
STACK_OFFSET_Y = 25
BG_COLOR = (0, 80, 0)     # Darker felt green
CARD_COLOR = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (220, 20, 20)      # Richer Red
YELLOW = (255, 215, 0)   # Gold for selection highlighting

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# --- IMPROVED VECTOR GRAPHICS ENGINE ---

def draw_diamond(surface, x, y, size, color):
    # Slightly elongated vertically for elegance
    half_w = size // 2
    half_h = size * 0.6 
    points = [
        (x, y - half_h), # Top
        (x + half_w, y), # Right
        (x, y + half_h), # Bottom
        (x - half_w, y)  # Left
    ]
    pygame.draw.polygon(surface, color, points)

def draw_heart(surface, x, y, size, color):
    # Uses two circles for lobes and a carefully placed triangle for the body/tip
    radius = size // 3.5
    # Centers for the two top lobes
    c1_x, c1_y = x - radius * 0.9, y - radius * 0.4
    c2_x, c2_y = x + radius * 0.9, y - radius * 0.4
    
    # Draw Lobes
    pygame.draw.circle(surface, color, (int(c1_x), int(c1_y)), int(radius))
    pygame.draw.circle(surface, color, (int(c2_x), int(c2_y)), int(radius))
    
    # Draw Body (Triangle connecting sides to bottom tip)
    tip_y = y + size // 2
    triangle_points = [
        (x - radius * 1.7, c1_y + radius*0.5), # Left flank
        (x + radius * 1.7, c2_y + radius*0.5), # Right flank
        (x, tip_y) # Bottom tip
    ]
    pygame.draw.polygon(surface, color, triangle_points)

def draw_spade(surface, x, y, size, color):
    # Inverted heart logic for the leaf, plus a distinct stem
    radius = size // 3.5
    offset_y = y - size * 0.05 # Shift up slightly for balance

    # Leaf Lobes (at bottom of leaf)
    c1_x, c1_y = x - radius * 0.9, offset_y + radius * 0.4
    c2_x, c2_y = x + radius * 0.9, offset_y + radius * 0.4

    # Draw Leaf Body (Triangle pointing up)
    tip_y = offset_y - size // 2
    triangle_points = [
        (x, tip_y), # Top tip
        (x + radius * 1.7, c2_y - radius*0.5), # Right flank
        (x - radius * 1.7, c1_y - radius*0.5), # Left flank
    ]
    pygame.draw.polygon(surface, color, triangle_points)
    
    # Rounding circles
    pygame.draw.circle(surface, color, (int(c1_x), int(c1_y)), int(radius))
    pygame.draw.circle(surface, color, (int(c2_x), int(c2_y)), int(radius))

    # The Stem (Flared triangle base)
    stem_w = size // 5
    stem_top = offset_y + radius * 0.8
    stem_points = [
        (x, stem_top), 
        (x + stem_w, y + size//2),
        (x - stem_w, y + size//2)
    ]
    pygame.draw.polygon(surface, color, stem_points)

def draw_club(surface, x, y, size, color):
    # Three tightly clustered circles smoothed by a center circle, plus a stem
    radius = size // 3.6
    offset_y = y - size * 0.08

    # Top Circle
    pygame.draw.circle(surface, color, (x, int(offset_y - radius)), int(radius))
    # Bottom Left
    pygame.draw.circle(surface, color, (int(x - radius*0.9), int(offset_y + radius*0.6)), int(radius))
    # Bottom Right
    pygame.draw.circle(surface, color, (int(x + radius*0.9), int(offset_y + radius*0.6)), int(radius))
    # Center Filler (Smooths the gaps between the three)
    pygame.draw.circle(surface, color, (x, int(offset_y)), int(radius*0.8))

    # The Stem
    stem_w = size // 5
    stem_top = offset_y + radius * 0.5
    stem_points = [
        (x, stem_top),
        (x + stem_w, y + size//2),
        (x - stem_w, y + size//2)
    ]
    pygame.draw.polygon(surface, color, stem_points)

def draw_suit_icon(surface, suit, x, y, size, color):
    if suit == 'Hearts': draw_heart(surface, x, y, size, color)
    elif suit == 'Diamonds': draw_diamond(surface, x, y, size, color)
    elif suit == 'Clubs': draw_club(surface, x, y, size, color)
    elif suit == 'Spades': draw_spade(surface, x, y, size, color)

# --- PIXEL FONT (For corner numbers only) ---
# 3x5 grid bitmaps for numbers and letters
PIXEL_FONT = {
    'A': [0b010, 0b101, 0b111, 0b101, 0b101],
    '2': [0b111, 0b001, 0b111, 0b100, 0b111],
    '3': [0b111, 0b001, 0b111, 0b001, 0b111],
    '4': [0b101, 0b101, 0b111, 0b001, 0b001],
    '5': [0b111, 0b100, 0b111, 0b001, 0b111],
    '6': [0b111, 0b100, 0b111, 0b101, 0b111],
    '7': [0b111, 0b001, 0b010, 0b010, 0b010],
    '8': [0b111, 0b101, 0b111, 0b101, 0b111],
    '9': [0b111, 0b101, 0b111, 0b001, 0b111],
    '0': [0b111, 0b101, 0b101, 0b101, 0b111], # For 10
    '1': [0b001, 0b001, 0b001, 0b001, 0b001], # Thin 1
    'J': [0b111, 0b001, 0b001, 0b101, 0b111],
    'Q': [0b010, 0b101, 0b101, 0b101, 0b010],
    'K': [0b101, 0b101, 0b110, 0b101, 0b101],
}

def draw_small_char(surface, char, x, y, color):
    """Draws tiny corner numbers using pixel grid"""
    if char not in PIXEL_FONT: return
    rows = PIXEL_FONT[char]
    scale = 2
    for r_idx, row_val in enumerate(rows):
        for c_idx in range(3):
            # Read bits from left to right (bit 2 down to 0)
            if (row_val >> (2 - c_idx)) & 1:
                pygame.draw.rect(surface, color, (x + c_idx * scale, y + r_idx * scale, scale, scale))

def draw_rank_corner(surface, rank, x, y, color):
    cursor = x
    for char in rank:
        draw_small_char(surface, char, cursor, y, color)
        # Adjust spacing for '1' which is thinner
        spacing = 4 if char == '1' else 8
        cursor += spacing

# --- PIP LAYOUT LOGIC ---
# Coordinates 0.0 to 1.0 relative to inner card area
PIP_POSITIONS = {
    'A': [(0.5, 0.5)],
    '2': [(0.5, 0.2), (0.5, 0.8)],
    '3': [(0.5, 0.2), (0.5, 0.5), (0.5, 0.8)],
    '4': [(0.3, 0.2), (0.7, 0.2), (0.3, 0.8), (0.7, 0.8)],
    '5': [(0.3, 0.2), (0.7, 0.2), (0.5, 0.5), (0.3, 0.8), (0.7, 0.8)],
    '6': [(0.3, 0.2), (0.7, 0.2), (0.3, 0.5), (0.7, 0.5), (0.3, 0.8), (0.7, 0.8)],
    '7': [(0.3, 0.2), (0.7, 0.2), (0.5, 0.35), (0.3, 0.5), (0.7, 0.5), (0.3, 0.8), (0.7, 0.8)],
    '8': [(0.3, 0.2), (0.7, 0.2), (0.3, 0.5), (0.7, 0.5), (0.3, 0.8), (0.7, 0.8), (0.5, 0.35), (0.5, 0.65)],
    '9': [(0.3, 0.2), (0.7, 0.2), (0.3, 0.4), (0.7, 0.4), (0.5, 0.5), (0.3, 0.6), (0.7, 0.6), (0.3, 0.8), (0.7, 0.8)],
    '10': [(0.3, 0.2), (0.7, 0.2), (0.5, 0.3), (0.3, 0.4), (0.7, 0.4), (0.3, 0.6), (0.7, 0.6), (0.5, 0.7), (0.3, 0.8), (0.7, 0.8)],
}

# --- Card Class ---
class Card:
    def __init__(self, rank, suit, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up
        self.color = RED if suit in ['Hearts', 'Diamonds'] else BLACK
        self.value = RANKS.index(rank) + 1 

# --- Game Class ---
class SolitaireGame:
    def __init__(self):
        self.deck = [Card(r, s) for s in SUITS for r in RANKS]
        random.shuffle(self.deck)
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = []
        self.waste = []
        self.foundation_rects = [None] * 4 
        self.stock_rect = None
        self.waste_rect = None
        self.selected_pile = None
        self.selected_index = -1
        self.deal()

    def deal(self):
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.pop()
                card.face_up = (i == j)
                self.tableau[i].append(card)
        self.stock = self.deck

    def is_valid_tableau_move(self, stack, card_index, target_pile):
        moving_cards = stack[card_index:]
        bottom_card = moving_cards[0]
        if not target_pile: return bottom_card.rank == 'K'
        target_card = target_pile[-1]
        if target_card.color == bottom_card.color: return False
        if target_card.value != bottom_card.value + 1: return False
        return True

    def is_valid_foundation_move(self, card, target_pile):
        if card != self.selected_pile[self.selected_index]: return False
        if not target_pile: return card.rank == 'A'
        target_card = target_pile[-1]
        if target_card.suit != card.suit: return False
        if target_card.value == card.value - 1: return True
        return False
    
    def flip_top_card(self, pile):
        if pile and not pile[-1].face_up:
            pile[-1].face_up = True

    def draw_card(self):
        if self.stock:
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
        elif self.waste:
            self.stock = [c for c in reversed(self.waste)]
            for c in self.stock: c.face_up = False
            self.waste = []

    def check_for_win(self):
        return all(len(p) == 13 for p in self.foundation)

# --- Drawing Helpers ---
def draw_card_fancy(screen, card, x, y, is_selected=False):
    rect = pygame.Rect(x, y, CARD_W, CARD_H)
    card_surface = pygame.Surface((CARD_W, CARD_H))
    card_surface.set_colorkey((0, 255, 0)) # Chroma key
    card_surface.fill(BG_COLOR) # Transparent fill

    # Card Body
    body_color = YELLOW if is_selected else CARD_COLOR
    pygame.draw.rect(card_surface, body_color, (0, 0, CARD_W, CARD_H), border_radius=6)
    pygame.draw.rect(card_surface, BLACK, (0, 0, CARD_W, CARD_H), 1, border_radius=6)

    if not card.face_up:
        # Card Back Pattern
        back_color = (60, 60, 180)
        pygame.draw.rect(card_surface, back_color, (4, 4, CARD_W-8, CARD_H-8), border_radius=4)
        # Crosshatch design
        for i in range(0, CARD_W, 10):
             pygame.draw.line(card_surface, (80, 80, 200), (i, 4), (i, CARD_H-4), 1)
        for i in range(0, CARD_H, 10):
             pygame.draw.line(card_surface, (80, 80, 200), (4, i), (CARD_W-4, i), 1)

    else:
        # 1. Corner Rank & Suit
        draw_rank_corner(card_surface, card.rank, 5, 5, card.color)
        draw_suit_icon(card_surface, card.suit, 9, 22, 10, card.color)

        # 2. Main Pip Layout
        if card.rank in ['J', 'Q', 'K']:
            # Face Card - Box frame
            pygame.draw.rect(card_surface, card.color, (20, 30, CARD_W-40, CARD_H-60), 2)
            # Large center suit
            draw_suit_icon(card_surface, card.suit, CARD_W//2, CARD_H//2, 35, card.color)
            # Rank letter in center
            draw_rank_corner(card_surface, card.rank, CARD_W//2 - 4, CARD_H//2 - 5, card.color)
        else:
            # Number Card - Pips
            positions = PIP_POSITIONS.get(card.rank, [])
            pip_size = 13 # Slightly smaller because new shapes are fuller
            for px, py in positions:
                draw_suit_icon(card_surface, card.suit, int(px * CARD_W), int(py * CARD_H) + 5, pip_size, card.color)

    screen.blit(card_surface, rect)
    return rect

def draw_tableau(screen, game, selected_stack=None):
    for i, pile in enumerate(game.tableau):
        x = 20 + i * (CARD_W + 10)
        y = CARD_H + 40
        if not pile:
            pygame.draw.rect(screen, (0, 60, 0), (x, y, CARD_W, CARD_H), 2, border_radius=6)
        for j, card in enumerate(pile):
            is_selected = (selected_stack == game.tableau[i] and j >= game.selected_index)
            rect = draw_card_fancy(screen, card, x, y + j * STACK_OFFSET_Y, is_selected)
            card.rect = rect

def draw_foundation_and_stock(screen, game):
    for i in range(4):
        x = SCREEN_WIDTH - 20 - (4 - i) * (CARD_W + 10)
        y = 20
        rect = pygame.Rect(x, y, CARD_W, CARD_H)
        pygame.draw.rect(screen, (0, 60, 0), rect, 2, border_radius=6)
        game.foundation_rects[i] = rect
        if game.foundation[i]:
            card = game.foundation[i][-1]
            rect = draw_card_fancy(screen, card, x, y)
            card.rect = rect
            
    x_stock = 20
    y_stock = 20
    game.stock_rect = pygame.Rect(x_stock, y_stock, CARD_W, CARD_H)
    if game.stock:
        # Use a dummy card face_up=False to draw the back
        card = Card("A", "Hearts", face_up=False) 
        draw_card_fancy(screen, card, x_stock, y_stock)
    else:
        pygame.draw.rect(screen, (0, 60, 0), game.stock_rect, 2, border_radius=6)

    x_waste = x_stock + CARD_W + 10
    y_waste = 20
    game.waste_rect = pygame.Rect(x_waste, y_waste, CARD_W, CARD_H)
    if game.waste:
        card = game.waste[-1]
        rect = draw_card_fancy(screen, card, x_waste, y_waste, game.waste == game.selected_pile)
        card.rect = rect
    else:
        pygame.draw.rect(screen, (0, 60, 0), game.waste_rect, 2, border_radius=6)

# --- Main Loop ---
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Solitaire Deluxe - Python")
    clock = pygame.time.Clock()
    game = SolitaireGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                if game.selected_pile:
                    for target_index, target_pile in enumerate(game.tableau):
                        target_x = 20 + target_index * (CARD_W + 10)
                        target_y = CARD_H + 40
                        if not target_pile:
                            target_rect = pygame.Rect(target_x, target_y, CARD_W, CARD_H)
                        else:
                            target_rect = pygame.Rect(target_x, target_y + (len(target_pile)-1) * STACK_OFFSET_Y, CARD_W, CARD_H + STACK_OFFSET_Y * 2)

                        if target_rect.collidepoint(pos):
                            if game.is_valid_tableau_move(game.selected_pile, game.selected_index, target_pile):
                                moving_cards = game.selected_pile[game.selected_index:]
                                target_pile.extend(moving_cards)
                                del game.selected_pile[game.selected_index:]
                                game.flip_top_card(game.selected_pile)
                                game.selected_pile = None
                                game.selected_index = -1
                                break
                    
                    if game.selected_pile is not None and game.selected_index == len(game.selected_pile) - 1:
                        for i, target_pile in enumerate(game.foundation):
                            if game.foundation_rects[i].collidepoint(pos):
                                if game.is_valid_foundation_move(game.selected_pile[-1], target_pile):
                                    card = game.selected_pile.pop()
                                    target_pile.append(card)
                                    game.flip_top_card(game.selected_pile)
                                    game.selected_pile = None
                                    game.selected_index = -1
                                    break
                    
                    if game.selected_pile is not None:
                        game.selected_pile = None
                        game.selected_index = -1
                
                else: 
                    if game.stock_rect.collidepoint(pos):
                        game.draw_card()
                        continue
                    
                    for pile in game.tableau:
                        if not pile: continue
                        for i in range(len(pile) - 1, -1, -1):
                            card = pile[i]
                            if card.face_up and card.rect.collidepoint(pos):
                                game.selected_pile = pile
                                game.selected_index = i
                                break
                        if game.selected_pile: break
                    
                    if not game.selected_pile and game.waste and game.waste_rect.collidepoint(pos):
                        game.selected_pile = game.waste
                        game.selected_index = len(game.waste) - 1

        screen.fill(BG_COLOR)
        selected_stack = game.selected_pile
        draw_foundation_and_stock(screen, game)
        draw_tableau(screen, game, selected_stack)
        
        if game.check_for_win():
             # (Placeholder: A pixel-art win message could be added here)
             pass

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
