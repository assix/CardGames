# UNO - Python/Pygame implementation

A faithful recreation of the classic **UNO** card game, built with Python and Pygame. 
This version features a smart AI opponent, complete support for action cards (Skip, Reverse, Draw 2/4), and automatic "UNO!" declarations.

## 🎮 Features
- **Full Ruleset:** Includes Skips, Reverses, Draw +2, Wilds, and Wild Draw +4.
- **Procedural Graphics:** Cards are drawn using code (ellipses and rectangles), so no image assets are needed.
- **Smart AI:** The CPU automatically picks the best color when playing a Wild card and tries to hinder your progress.
- **Auto-UNO:** The game automatically detects when you (or the CPU) are down to one card and displays the "UNO!" alert.

## 🕹️ How to Play

### Objective
Be the first player to get rid of all your cards.

### The Rules
1. **Match the Card:** Play a card that matches the **Color** or **Value** of the top card on the discard pile.
2. **Action Cards:**
   - **Skip (⊘):** The next player loses their turn.
   - **Reverse (⇄):** In 1v1, acts exactly like a Skip (you get another turn).
   - **Draw +2:** Next player draws 2 cards and loses their turn.
   - **Wild:** Change the active color to any of the 4 colors.
   - **Wild Draw +4:** Change the color, next player draws 4 cards and loses their turn.
3. **Drawing:** If you have no playable cards, click the **Draw Deck** to pick one up.

### Controls
- **Left Click:** Select a card to play or click the deck to draw.

## 🚀 Running the Game
From the root of the repository, run:

```bash
python3 uno/uno.py

