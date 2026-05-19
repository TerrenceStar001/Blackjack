# ♣️ Blackjack Chaos ♦️

> **"In the game of chaos and casinos, the only winning strategy is never to play."**

Welcome to **Blackjack Chaos**—a fully Object-Oriented, Pygame-powered descent into gambling madness. Originally conceived as an NSS ICT Programming Project to demonstrate the mathematics of card counting, this project evolved into a brutal simulation of variance, unfair advantages, and pure chaos.

You think you have the perfect Blackjack strategy? Let's see how well your math holds up when the floor turns into lava.

---

## 🚀 Overview & Origin Story

What started as a procedural script inspired by a YouTube tutorial was completely torn down and rebuilt from scratch in Neovim. The codebase was transformed into a robust **Object-Oriented Programming (OOP) factory**, featuring custom classes for Cards, Decks, Hands, Player Profiles, and an entirely custom `VisualEngine` and `ChaosDisaster` state machine.

This isn't just a casino game; it's a value education simulator. By implementing a mathematically perfect "Robot" bot that continually loses to the game's unpredictable disasters, this project proves a critical point: real-life casinos don't operate in a static mathematical vacuum. The house *always* wins because they control the environment.

---

## ✨ Features

### 🏛️ Core Blackjack Mechanics

* **Authentic Ruleset:** Standard Hit, Stand, and Dealer logic (Dealer hits until 17).
* **Dynamic Ace Handling:** Aces dynamically shift between 1 and 11 based on bust risk.
* **Betting & Economy:** Full currency system (`PlayerProfile.coins`) with escalating bets.
* **Rank Progression:** Win-based ranking system (Jack ➔ Queen ➔ King ➔ Ace ➔ Blackjack).

### 🌪️ The Chaos Engine

Standard Blackjack is boring. We added unpredictable disasters and overpowered abilities.

| Mechanic | Description | Impact |
| --- | --- | --- |
| **Acid Rain** | A disaster that melts your hand by randomly deleting your highest-value cards. | Ruins your carefully built 20. |
| **The Floor is Lava** | A shifting minimum-score threshold. If your final score is below it, you instantly die. | Forces you to hit when you shouldn't. |
| **5% Service Charge** | A compounding multiplier applied to final scores right at the endgame check. | Skews the math, turning a safe 19 into a bust. |

### 🃏 Chaos Inventory System

Players are dealt random "Chaos Cards" to fight back against the house:

* 🟢 **Nuclear Bomb:** Clears the board and forces a complete restart of the hand.
* 🟢 **UNO Reverse:** Swaps your hand with the dealer's hand.
* 🔵 **Redraw:** Burns your current hand and draws two completely new cards.
* 🔘 **Robots:** Automates standard perfect Blackjack strategy (and proves why it fails against true chaos).

---

## 🛠️ Project Architecture (OOP Design)

The codebase is structured around several dedicated Python classes to ensure modularity and scalability:

* `Card` & `Deck`: Handles card generation, values, colors, and shuffling.
* `Hand`: Manages scoring logic, dynamic Aces, and specialized rendering (flipping hidden dealer cards).
* `PlayerProfile`: Tracks inventory, wins, currency, and rank progression.
* `ChaosDisaster`: The cruel state machine managing environmental modifiers.
* `ChaosCard`: Data structures for the inventory action system.
* `VisualEngine`: Manages transparent overlays, screen shakes, falling acid rain animations, and emoji rendering.

---

## 💻 Installation & Setup

To run this simulation locally, you will need Python installed on your machine along with a few dependencies.

### 1. Prerequisites

Ensure you have Python 3.8+ installed. You will also need the `pygame` and `pygame_emojis` libraries.

```bash
pip install pygame pygame-emojis

```

### 2. Assets Required

The code relies on external assets. Ensure the following files are in the root directory alongside your `main.py` script:

* **Fonts:** `blackjack2.ttf` (Main UI Font), `arial` (System font for suits)
* **Music:** `blackjack_music.mp3`
* **SFX:** * `240776__f4ngy__card-flip.wav`
* `201809__fartheststar__poker_chips5.wav`
* `157218__adamweeden__video-game-die-or-lose-life.flac`
* *(Plus the other custom sound effects referenced in the code)*



### 3. Run the Game

```bash
python blackjack.py

```

---

## 🎮 How to Play

1. **The Menu:** Click `PLAY GAME` to enter the casino.
2. **The Interface:** Your stats (Coins, Rank, Bet, Active Disasters) are on the top left. Your inventory of Chaos Cards is at the bottom.
3. **Taking Action:** Click `HIT ME` to draw, `STAND` to lock in your score, or click any of your colored **Chaos Cards** in your inventory to trigger special abilities.
4. **Surviving:** Keep an eye on the red Disaster cards on the left side of the screen. If *The Floor is Lava* is active, playing conservatively will get you killed.

---

## 🧠 Developer Reflection & Value Education

As the "God" of this codebase, I had the power to peek at arrays, manipulate dealer logic, and code a guaranteed win. The temptation to create a "cheat mode" was strong, highlighting a massive gray area in software integrity.

When I coded the **Robot** card to execute perfect, mathematical Blackjack strategy, I expected it to print virtual money. Instead, it lost 5-to-1. The Robot assumed the game was fair, but the `ChaosDisaster` engine proved otherwise.

**The Lesson:** This game is a micro-simulation of real-world casinos. Casinos introduce multiple decks, shifting house rules, and psychological pressure—their version of "Chaos Disasters." You can memorize all the card-counting strategies in the world, but you cannot out-math unpredictable variables designed to siphon your wealth.

**Do not gamble.** You cannot beat a system where the house controls the rules of reality.

---

*Developed with caffeine, Neovim, and a hard-learned lesson in probability.*
