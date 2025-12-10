# Solitaire Deluxe (Python/Pygame) 🃏

A high-fidelity, single-file implementation of **Klondike Solitaire** built entirely in Python.

Unlike most game projects, this requires **zero external image assets**. All graphics—including card suits, pips, face cards, and text—are drawn procedurally using a custom vector graphics engine and a pixel-font system. This ensures the game is ultra-portable and runs on systems where standard font libraries might fail (e.g., experimental Python versions, macOS, or minimal Linux environments).

## ✨ Features

- **Procedural Vector Graphics:** Hearts, Spades, Diamonds, and Clubs are drawn using geometric primitives (polygons & circles) for crisp visuals at any resolution.
- **Zero Dependencies (besides Pygame):** No images to download, no system fonts required. Just run the script.
- **Cross-Platform Compatible:** Tested on **macOS (Python 3.14)** and **Linux**. Bypasses common `pygame.font` crashes on newer Python builds by using a custom bitmapped font engine.
- **Classic Gameplay:** Standard Klondike rules with "Draw 1" logic.
- **Smart Layouts:** Correct pip patterns for every number card (e.g., the 10 of Spades has 10 properly arranged pips).

## 🕹️ How to Play

The game uses a **Click-to-Select, Click-to-Place** interface:

1. **Select:** Click a card (in the Tableau or Waste pile) to select it. It will highlight in **Gold**.
2. **Move:** Click a valid destination pile (Tableau or Foundation) to move the card(s).
3. **Draw:** Click the **Stock Pile** (top left, face down) to draw a new card.
4. **Win:** Move all cards to the top-right **Foundation Piles**, stacked by suit from Ace to King.

### Rules Recap
- **Tableau (Main Area):** Build **Down** in **Alternating Colors** (e.g., Red 5 on Black 6).
- **Foundation (Top Right):** Build **Up** in **Same Suit** (e.g., Heart 2 on Heart Ace).

## 🎨 Under the Hood

This project implements a custom mini-graphics engine inside the `solitaire.py` file to ensure maximum portability:

* **Vector Engine:** Mathematical functions (`draw_heart`, `draw_spade`, etc.) draw curved suits using `pygame.draw.polygon` and `pygame.draw.circle` rather than loading PNGs.
* **Pixel Font:** A dictionary containing binary grids (bitmaps) is used to render numbers (A, K, Q, J, 1-9) without relying on the system's TrueType font engine, avoiding `pygame.font` errors.

## 📄 License
MIT License - Free to use, modify, and distribute.
