import pygame
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = 'red' if suit in ['♥', '♦'] else 'black'

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)

class Deck:
    def __init__(self, num_decks=4):
        self.cards = []
        suits = ['♠', '♥', '♣', '♦']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for _ in range(num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return self.cards.pop()
        return None

class Hand:
    def __init__(self, is_dealer=False):
        self.cards = []
        self.score = 0
        self.is_dealer = is_dealer

    def add_card(self, card):
        if card:
            self.cards.append(card)
            self.calculate_score()

    def calculate_score(self):
        self.score = 0
        aces = 0
        for card in self.cards:
            self.score += card.get_value()
            if card.rank == 'A':
                aces += 1
        while self.score > 21 and aces > 0:
            self.score -= 10
            aces -= 1

    def draw(self, surface, font, start_x, start_y, reveal):
        global suit_font 
        
        for i, card in enumerate(self.cards):
            rx = start_x + (70 * i)
            ry = start_y + (5 * i)
            
            if self.is_dealer and i == 0 and not reveal:
                pygame.draw.rect(surface, (42,40,40), [rx, ry, 170, 238], 0, 5) 
                pygame.draw.rect(surface, 'white', [rx, ry, 170, 238], 3, 5) 
                
                q_text = font.render('?', True, 'white')
                surface.blit(q_text, (rx + 85 - q_text.get_width()//2, ry + 119 - q_text.get_height()//2))
                
            else:
                pygame.draw.rect(surface, 'white', [rx, ry, 170, 238], 0, 5) 
                pygame.draw.rect(surface, 'black', [rx, ry, 170, 238], 3, 5) 
                
                rank_text = font.render(card.rank, True, card.color)
                suit_text = suit_font.render(card.suit, True, card.color)
                
                surface.blit(rank_text, (rx + 15, ry + 10))
                surface.blit(suit_text, (rx + 15, ry + 50))
                
                rank_inv = pygame.transform.rotate(rank_text, 180)
                suit_inv = pygame.transform.rotate(suit_text, 180)
                surface.blit(suit_inv, (rx + 155 - suit_inv.get_width(), ry + 140))
                surface.blit(rank_inv, (rx + 155 - rank_inv.get_width(), ry + 180))
                
                big_suit = pygame.transform.scale2x(suit_text)
                center_x = rx + 85 - (big_suit.get_width() // 2)
                center_y = ry + 119 - (big_suit.get_height() // 2)
                surface.blit(big_suit, (center_x, center_y))
class PlayerProfile:
    def __init__(self, starting_coins=500):
        self.coins = starting_coins
        self.inventory = []
        self.ranks = ["Jack","Queen","King","Ace","Blackjack"]
        self.current_rank_index = 0
        self.wins = 0
    
    def get_rank(self):
        return self.ranks[self.current_rank_index]
    
    def add_coins(self, amount):
        self.coins += amount
    
    def lose_coins(self,amount):
        self.coins -= amount

    def add_win(self):
        self.wins += 1
        self.check_rank_up()

    def next_rank(self):
        thresholds = [0,3,7,12,21]
        for i in range(len(thresholds)):
            if self.wins < thresholds[i]:
                return thresholds[i]
    
    def check_rank_up(self):
        thresholds = [0,3,7,12,21]

        for i in range(len(thresholds)-1,-1,-1):
            if self.wins >= thresholds[i]:
                if self.current_rank_index != i:
                    self.current_rank_index = i
                    print(f"RANK UP!You are now a {self.get_rank()}!")
                break
class ChaosDisaster:
    def __init__(self):
        self.disasters = ["Acid Rain","The Floor is Lava","10% Service Charge"]
        self.active_disaster = []
        self.lava_threshold = 16
        self.service_charge_count = 0

    def roll_disaster(self):
        new_disaster = random.choice(self.disasters)
        self.active_disaster.append(new_disaster)

        if new_disaster == "The Floor is Lava":
            if self.active_disaster.count("The Floor is Lava") > 1:
                self.lava_threshold += 1
        elif new_disaster == "10% Service Charge":
            self.service_charge_count += 1

    def apply_acid_rain(self, hand):
        if "Acid Rain" in self.active_disaster:
            acid_card = random.choice(hand.cards)
            for i in range(len(hand.cards) - 1, -1, -1):
                if hand.cards[i].get_value() == acid_card:
                    hand.cards.pop(i)
                hand.calculate_score()
    def apply_service_charge(self, score):
        if "10% Service Charge" in self.active_disaster:
            multiplier = 1.1 ** self.service_charge_count
            return int(score * multiplier)
        return score
    
    def check_lava_death(self, score):
        if "The Floor is Lava" in self.active_disaster:
            if 0 < score < self.lava_threshold:
                return True
            return False
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack Chaos')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('blackjack.otf', 44)
smaller_font = pygame.font.Font('blackjack.otf', 36)
suit_font = pygame.font.SysFont('arial', 44)

records = [0, 0, 0]
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
active = False
initial_deal = False
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False

finalized_player_score = 0
finalized_dealer_score = 0

profile = PlayerProfile(starting_coins=1000)
current_bet = 50
disaster = ChaosDisaster()

player_hand = Hand()
dealer_hand = Hand(is_dealer=True)
game_deck = Deck()

def draw_scores(player_score, dealer_score, reveal):
    screen.blit(font.render(f'{player_score}', True, 'white'), (1000, 725))
    pygame.draw.rect(screen,'black',[990,720,54,54], 5, 5)
    if reveal:
        screen.blit(font.render(f'{dealer_score}', True, 'white'), (1000, 85))
        pygame.draw.rect(screen,'black',[985,85,54,54], 5, 5)

def draw_game(act, record, result):
    pygame.draw.rect(screen,'white',[420,0,5,1080])
    buttons = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [960, 540, 300, 100], 0, 5)
        screen.blit(font.render('DEAL HAND',True, 'black'), (960, 540))
        buttons.append(deal)
    else:
        hit = pygame.draw.rect(screen, 'white', [800, 800, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [800, 800, 300, 100], 3, 5)
        screen.blit(font.render('HIT ME', True, 'black'), (820, 820))
        buttons.append(hit)
        
        stand = pygame.draw.rect(screen, 'white', [1100, 800, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [1100, 800, 300, 100], 3, 5)
        screen.blit(font.render('STAND', True, 'black'), (1120, 820))
        buttons.append(stand)
        screen.blit(smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white'), (15, 840))
    if result != 0:
        screen.blit(font.render(results[result], True, 'black'), (1500, 450))
        deal = pygame.draw.rect(screen, 'white', [940, 520, 300, 100], 0, 5)
        screen.blit(font.render('NEW HAND', True, 'black'), (960, 540))
        buttons.append(deal)
    return buttons

def check_endgame(d_score, p_score, res, recs, player_prof, bet_amount):
    if p_score > 21:
        res = 1
    elif d_score > 21:
       res = 2
    elif p_score > d_score:
        res = 2
    elif d_score > p_score:
        res = 3
    else:
        res = 4
    
    if res == 2:
        recs[0] += 1
        player_prof.add_coins(bet_amount)
        player_prof.add_win()
    elif res == 1 or res == 3:
        recs[1] += 1
        player_prof.lose_coins(bet_amount)
    elif res == 4:
        recs[2] += 1

    return res, recs

def draw_chaotic_gui(surface, player_prof, disaster_mgr):
    name_text = smaller_font.render(f"Name: Player", True, 'black')
    surface.blit(name_text, (450,20))

    coin_text = smaller_font.render(f"Coins: {player_prof.coins}", True, 'black')
    surface.blit(coin_text, (450,60))
    
    rank_text = smaller_font.render(f"Rank: {player_prof.get_rank()} ({player_prof.wins}/{player_prof.next_rank()})", True, 'black')
    surface.blit(rank_text, (450,100))

    bet_text = smaller_font.render(f"Bet: {current_bet}", True, 'black')
    surface.blit(bet_text, (450,140))

    for i, disaster_name in  enumerate(disaster_mgr.active_disaster):
        card_x = 25 + (i % 2 * 195)
        card_y = 25 + (i // 2 * 265)

        pygame.draw.rect(surface, 'white', [card_x, card_y, 170,238], 0, 5)
        
        words = disaster_name.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if smaller_font.size(test_line)[0] < 150:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        total_height = len(lines) * smaller_font.get_linesize()
        start_text_y = card_y + (238 // 2) - (total_height // 2)

        for line_index, line in enumerate(lines):
            text_surface = smaller_font.render(line, True, 'black')
            text_x = card_x + (170 // 2) - (text_surface.get_width() // 2)
            text_y = start_text_y + (line_index * smaller_font.get_linesize())
            surface.blit(text_surface, (text_x, text_y))


run = True
casino_green = (53,101,77)
while run:
    timer.tick(fps)
    screen.fill(casino_green)
    
    if initial_deal:
        disaster.roll_disaster()

        for _ in range(2):
            player_hand.add_card(game_deck.deal())
            dealer_hand.add_card(game_deck.deal())

        disaster.apply_acid_rain(player_hand)
        disaster.apply_acid_rain(dealer_hand)

        initial_deal = False
        
    if active:   
        player_hand.draw(screen, font, 900, 460, reveal_dealer)
        dealer_hand.draw(screen, font, 900, 160, reveal_dealer)
        
        if reveal_dealer and dealer_hand.score < 17:
            dealer_hand.add_card(game_deck.deal())
            
        if outcome == 0:
            finalized_player_score = player_hand.score
            finalized_dealer_score = dealer_hand.score
        draw_scores(finalized_player_score, finalized_dealer_score, reveal_dealer)

    buttons = draw_game(active, records, outcome)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = Deck()
                    player_hand = Hand(is_dealer=False)
                    dealer_hand = Hand(is_dealer=True)
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True

            else:
                if buttons[0].collidepoint(event.pos) and player_hand.score < 21 and hand_active:
                    player_hand.add_card(game_deck.deal())
                    
                    disaster.apply_acid_rain(player_hand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False

                    while dealer_hand.score < 17:
                        dealer_hand.add_card(game_deck.deal())
                    
                    finalized_player_score = disaster.apply_service_charge(player_hand.score)
                    finalized_dealer_score = disaster.apply_service_charge(dealer_hand.score)

                    if disaster.check_lava_death(finalized_player_score):
                        finalized_player_score = 999
                    if disaster.check_lava_death(finalized_dealer_score):
                        finalized_dealer_score = 999

                    outcome, records = check_endgame(
                        finalized_dealer_score,
                        finalized_player_score,
                        outcome,
                        records,
                        profile,
                        current_bet
                    )
                elif len(buttons) == 3 and buttons[2].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = Deck()
                    player_hand = Hand(is_dealer=False)
                    dealer_hand = Hand(is_dealer=True)
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True

    if hand_active and player_hand.score >= 21:
        hand_active = False
        reveal_dealer = True

        while dealer_hand.score < 17:
            dealer_hand.add_card(game_deck.deal())
            disaster.apply_acid_rain(dealer_hand)

        finalized_player_score = disaster.apply_service_charge(player_hand.score)
        finalized_dealer_score = disaster.apply_service_charge(dealer_hand.score)

        if disaster.check_lava_death(finalized_player_score):
            finalized_player_score = 999
        if disaster.check_lava_death(finalized_dealer_score):
            finalized_dealer_score = 999

        outcome, records = check_endgame(
            finalized_player_score,
            finalized_player_score,
            outcome,
            records,
            profile,
            current_bet
        )

    draw_chaotic_gui(screen, profile, disaster)

    pygame.display.flip()

pygame.quit()
