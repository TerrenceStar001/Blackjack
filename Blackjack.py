import pygame
import random
from pygame_emojis import load_emoji
import time

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
    
    def check_rank_up(self):
        thresholds = [0,3,7,12,21]
        for i in range(len(thresholds) -1, -1, -1):
            if self.wins >= thresholds[i]:
                if self.current_rank_index != i:
                    self.current_rank_index = i
                break
    def next_rank(self):
        thresholds = [0,3,7,12,21]
        for i in range(len(thresholds)):
            if self.wins < thresholds[i]:
                return thresholds[i]
    
    def setup_action_hand(self):
        self.inventory = [card for card in self.inventory if card.name not in["Hit", "Stand"]]
        
        self.inventory.insert(0, ChaosCard("Stand"))
        self.inventory.insert(0, ChaosCard("Hit"))

        chaos_list = ["Nuclear Bomb", "UNO Reverse","Redraw","Robots"]

        if len(self.inventory) < 8:
            new_card = ChaosCard(random.choice(chaos_list))
            self.inventory.append(new_card)
class ChaosDisaster:
    def __init__(self):
        self.disasters = ["Acid Rain","The Floor is Lava","5% Service Charge"]
        self.active_disaster = ['None','None','None','None','None','None','None','None']
        self.lava_threshold = 16
        self.service_charge_count = 0
        self.disaster_idx = 0

    def roll_disaster(self):
        new_disaster = random.choice(self.disasters)
        self.active_disaster[self.disaster_idx % 8] = new_disaster #circular active disaster list!let's go

        if new_disaster == "The Floor is Lava":
            if self.active_disaster.count("The Floor is Lava") > 1:
                self.lava_threshold += 1
        elif new_disaster == "5% Service Charge":
            self.service_charge_count += 1

        self.disaster_idx += 1

    def apply_acid_rain(self, hand):
        if "Acid Rain" in self.active_disaster:
            acid_card = random.choice(hand.cards)
            for i in range(len(hand.cards) - 1, -1, -1):
                if hand.cards[i].get_value() == acid_card:
                    hand.cards.pop(i)
                hand.calculate_score()
    def apply_service_charge(self, score):
        if "5% Service Charge" in self.active_disaster:
            multiplier = 1.05 ** self.service_charge_count
            return int(score * multiplier)
        return score
    
    def check_lava_death(self, score):
        if "The Floor is Lava" in self.active_disaster:
            if 0 < score < self.lava_threshold:
                return True
            return False
class ChaosCard:
    def __init__(self, name):
        self.name = name
        if self.name == "Hit":
            self.color = (120, 0, 0)
        elif self.name == "Nuclear Bomb":
            self.color = (0, 180, 0)
        elif self.name == "UNO Reverse":
            self.color = (0, 120, 0)
        elif self.name == "Redraw":
            self.color = (0, 0, 150)
        elif self.name == "Robots":
            self.color = (80,80, 90)
        else:
            self.color = (212, 175, 55)

class VisualEngine:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.acid_drop = []
        self.active_anims = []
        self.big_font = pygame.font.Font('blackjack2.ttf', 150)
        self.icon_font = pygame.font.Font('blackjack2.ttf', 800)
        self.service_timer = 0.7 * 60

    def trigger_anim(self, anim_type):
        self.active_anims.append({'type': anim_type, 'frame': 0})

    def update_and_draw(self,surface, active_disaster):
        lava_count = active_disaster.count("The Floor is Lava")
        if lava_count > 0:
            overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            
            alpha = min(40 + (lava_count * 30), 200) 
            overlay.fill((255, 69, 0, alpha)) 
            
            surface.blit(overlay, (0, 0))
        service_count = active_disaster.count("5% Service Charge")
        if service_count > 0:
            icon = self.get_emoji_icon("💰" * service_count,(self.icon_font))

            if self.service_timer > 0:
                self.service_timer -= 1 
                surface.blit(icon, (self.w // 2 - icon.get_width() // 2, self.h // 2 - icon.get_height() // 2))

        
        acid_count = active_disaster.count("Acid Rain")
        if acid_count > 0:
            for _ in range(acid_count * 2):
                self.acid_drop.append([random.randint(0, self.w), -20, random.randint(10, 25)])
            for drop in self.acid_drop[:]:
                pygame.draw.line(surface, (50, 255, 50), (drop[0], drop[1]), (drop[0], drop[1] +20), 4)
                drop[1] += drop[2]
                if drop[1] > self.h:
                    self.acid_drop.remove(drop)

        for anim in self.active_anims[:]:
            anim['frame'] +=  1
            f = anim['frame']
            
            if anim['type'] == 'bomb':
                if f < 40:
                    pygame.draw.rect(surface, (139,0,0), [self.w // 2 - 20, f * 30, 40, 80], 0, 10)
                elif f < 90:
                    radius = (f - 40) * 40
                    pygame.draw.circle(surface, (255,50,50), (self.w // 2, self.h // 2),radius)
                else:
                    self.active_anims.remove(anim)
            elif anim['type'] == 'uno':
                if f < 40:
                    color = 'green' if f % 10 < 5 else"yellow"
                    icon = self.get_emoji_icon("🔁",(self.icon_font))
                    surface.blit(icon, (self.w // 2 - icon.get_width() // 2, self.h // 2 - icon.get_height() // 2))
                else:
                    self.active_anims.remove(anim)

            elif anim['type'] == 'robot':
                if f < 60:
                    icon = self.get_emoji_icon("🤖",(self.icon_font))
                    surface.blit(icon, (self.w // 2 - icon.get_width() // 2, self.h // 2 - icon.get_height() // 2))
                else:
                    self.active_anims.remove(anim)
            elif anim['type'] in ['win', 'lose','tie']:
                overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                alpha = min(f * 5, 200)
                
                if anim['type'] == 'win':
                    overlay.fill((212, 175, 55, alpha))
                elif anim['type'] == 'lose':
                    overlay.fill((150,0,0,alpha))
                else:
                    overlay.fill((50,50,50,alpha))
                surface.blit(overlay,(0,0))
            elif anim['type'] == 'redraw':
                if f < 40:
                    color = (0,100,255) if f % 10 < 5 else (100, 200, 255)
                    icon = self.get_emoji_icon("🔄",(self.icon_font))
                    surface.blit(icon, (self.w // 2 - icon.get_width() // 2, self.h // 2 - icon.get_height() // 2))
                else:
                    self.active_anims.remove(anim)
    def get_emoji_icon(self,emoji_char,reference_font):
        size = reference_font.get_height()
        return load_emoji(emoji_char, (size,size))

pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack Chaos')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('blackjack2.ttf', 44)
smaller_font = pygame.font.Font('blackjack2.ttf', 36)
bigger_font = pygame.font.Font('blackjack2.ttf',52)
suit_font = pygame.font.SysFont('arial', 44)

pygame.mixer.music.load("blackjack_music.mp3")
pygame.mixer.music.set_volume(0.65)
pygame.mixer.music.play(-1)

sfx_card = pygame.mixer.Sound('240776__f4ngy__card-flip.wav')
sfx_bust = pygame.mixer.Sound('201809__fartheststar__poker_chips5.wav')
sfx_lose = pygame.mixer.Sound('157218__adamweeden__video-game-die-or-lose-life.flac')
sfx_win = pygame.mixer.Sound('527650__fupicat__winsquare.wav')

sfx_bomb = pygame.mixer.Sound('826627__artninja__custom_powerful_thunderous_speed_boost_09152025.wav')
sfx_uno = pygame.mixer.Sound('647583__espinho123__vinyl-scratch.wav')
sfx_robot = pygame.mixer.Sound('610306__brickdeveloper171__beep-pattern.wav')
sfx_redraw = pygame.mixer.Sound('715784__dustywind__magic-whoosh.wav')

sfx_charge = pygame.mixer.Sound('351304__deleted_user_96253__cha-ching.wav')
sfx_lava = pygame.mixer.Sound('98857__timbre__simulated-underground-lava-stream.wav')
sfx_acid = pygame.mixer.Sound('202094__spookymodem__acid-bubbling.wav')

records = [0, 0, 0]
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
active = False
initial_deal = False
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
deal_queue = []
deal_timer = 0

finalized_player_score = 0
finalized_dealer_score = 0

game_state = "MENU"  

play_btn_rect = pygame.Rect(450, 350, 300, 60)
exit_btn_rect = pygame.Rect(450, 500, 300, 60)

ingame_exit_rect = pygame.Rect(1800, 700, 70, 30) 

visualengine = VisualEngine(WIDTH,HEIGHT)

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
        screen.blit(smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'black'), (450, 180))
    if result != 0:
        screen.blit(bigger_font.render(results[result], True, 'black'), (1500, 450))
        deal = pygame.draw.rect(screen, casino_green, [1490, 480, 350, 60], 0, 5)
        screen.blit(font.render('NEW HAND', True, 'black'), (1500, 490))
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
        card_y = 5 + (i // 2 * 265)
        
        pygame.draw.rect(surface, 'red', [card_x - 3, card_y - 3, 176, 244], 0, 5)
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
def draw_chaos_inventory(surface, player_prof):
    pygame.draw.rect(surface, (30, 50, 40), [430,800,1500,275])
    
    card_hitboxes = []

    for i, chaos_card in enumerate(player_prof.inventory):
        card_x = 450 + (i * 190)
        card_y = 805

        rect = pygame.draw.rect(surface, chaos_card.color, [card_x,card_y, 170, 238], 0, 8)
        pygame.draw.rect(surface,'white',[card_x, card_y, 170, 238], 3, 8)
        
        card_hitboxes.append((rect, chaos_card))

        words = chaos_card.name.split(' ')
        for line_index, word in enumerate(words):
            text_surface = smaller_font.render(word, True, 'white')
            text_x = card_x + (170 // 2)- (text_surface.get_width() // 2)
            text_y = card_y + 70 + (line_index * 35)
            surface.blit(text_surface, (text_x, text_y))
    return card_hitboxes


run = True
casino_green = (53,101,77)
while run:
    timer.tick(fps)
    screen.fill(casino_green)
    
    if game_state == "MENU":
        title_shadow = font.render("♣ BLACKJACKED POKER ♦", True, (10, 40, 20))
        title_text = font.render("♣ BLACKJACKED POKER ♦", True, (255, 215, 0)) 
        screen.blit(title_shadow, (454, 154))
        screen.blit(title_text, (450, 150))
        
        sub_text = font.render("Chaos Edition", True, (200, 205, 200))
        screen.blit(sub_text, (450, 220))

        mouse_pos = pygame.mouse.get_pos()
        play_color = (40, 180, 99) if play_btn_rect.collidepoint(mouse_pos) else (34, 139, 34)
        pygame.draw.rect(screen, play_color, play_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), play_btn_rect, 2, border_radius=10) 
        
        play_label = font.render("PLAY GAME", True, (255, 255, 255))
        screen.blit(play_label, (play_btn_rect.x + 65, play_btn_rect.y + 12))

        exit_color = (231, 76, 60) if exit_btn_rect.collidepoint(mouse_pos) else (178, 34, 34)
        pygame.draw.rect(screen, exit_color, exit_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), exit_btn_rect, 2, border_radius=10)
        
        exit_label = font.render("EXIT TO DESKTOP", True, (255, 255, 255))
        screen.blit(exit_label, (exit_btn_rect.x + 25, exit_btn_rect.y + 12))

    elif game_state == "GAME":
        if initial_deal:
            disaster.roll_disaster()
            profile.setup_action_hand()
            deal_queue.extend(['player', 'dealer', 'player', 'dealer'])
            deal_timer = 30
            initial_deal = False

        if len(deal_queue) > 0:
            if deal_timer > 0:
                deal_timer -= 1
            else:
                next_target = deal_queue.pop(0)

                if next_target == 'player':
                    player_hand.add_card(game_deck.deal())
                    sfx_card.play()
                    disaster.apply_acid_rain(player_hand)
                    if hand_active and player_hand.score >= 21:
                        hand_active = False
                        reveal_dealer = True
                        if dealer_hand.score < 17:
                            deal_queue.append('dealer')
                elif next_target == 'dealer':
                    dealer_hand.add_card(game_deck.deal())
                    disaster.apply_acid_rain(dealer_hand)
                    sfx_card.play()

                deal_timer = 30

        if active:   
            player_hand.draw(screen, font, 900, 460, reveal_dealer)
            dealer_hand.draw(screen, font, 900, 160, reveal_dealer)

            if reveal_dealer and dealer_hand.score < 17:
                dealer_hand.add_card(game_deck.deal()) 
            if outcome == 0:
                finalized_player_score = player_hand.score
                finalized_dealer_score = dealer_hand.score
                if not hand_active and reveal_dealer and len(deal_queue) == 0 and dealer_hand.score >= 17:
                    finalized_player_score = disaster.apply_service_charge(player_hand.score)
                    finalized_dealer_score = disaster.apply_service_charge(dealer_hand.score)

                    if disaster.check_lava_death(finalized_player_score):
                        finalized_player_score = 999
                    if disaster.check_lava_death(finalized_dealer_score):
                        finalized_dealer_score = 999

                    outcome, records = check_endgame(
                        finalized_dealer_score, finalized_player_score, outcome, records, profile, current_bet
                    )
            draw_scores(finalized_player_score, finalized_dealer_score, reveal_dealer)

        buttons = draw_game(active, records, outcome)

        pygame.draw.rect(screen, (100, 20, 20), ingame_exit_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), ingame_exit_rect, 1, border_radius=5)
        screen.blit(smaller_font.render("QUIT", True, (255, 255, 255)), (ingame_exit_rect.x + 10, ingame_exit_rect.y))

        draw_chaotic_gui(screen, profile, disaster)
        inventory_buttons = draw_chaos_inventory(screen, profile)
        visualengine.update_and_draw(screen, disaster.active_disaster)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            
            if game_state == "MENU":
                if play_btn_rect.collidepoint(mouse_pos):
                    initial_deal = True
                    active = True
                    outcome = 0
                    player_hand.cards.clear()
                    dealer_hand.cards.clear()
                    deal_queue.clear()
                    game_state = "GAME" 
                
                elif exit_btn_rect.collidepoint(mouse_pos):
                    run = False 
                    
            elif game_state == "GAME":
                if ingame_exit_rect.collidepoint(mouse_pos):
                    game_state = "MENU"
                elif not active:
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
                else:
                    for rect, clicked_card in inventory_buttons:
                        if rect.collidepoint(event.pos):
                            if clicked_card.name == "Hit" and player_hand.score < 22 and hand_active:
                                deal_queue.append('player')
                            elif clicked_card.name == "Stand" and not reveal_dealer and hand_active:
                                reveal_dealer = True
                                hand_active = False

                                finalized_player_score =  disaster.apply_service_charge(player_hand.score)
                                finalized_dealer_score = disaster.apply_service_charge(dealer_hand.score)

                                if disaster.check_lava_death(finalized_player_score):
                                    finalized_player_score = 999
                                if disaster.check_lava_death(finalized_dealer_score):
                                    finalized_dealer_score = 999

                                outcome, records = check_endgame(
                                    finalized_dealer_score, finalized_player_score, outcome, records, profile, current_bet
                                )
                            elif clicked_card.name == "Nuclear Bomb" and hand_active:
                                profile.inventory.remove(clicked_card)
                                visualengine.trigger_anim('bomb')
                                active = True
                                initial_deal = True
                                game_deck = Deck()
                                player_hand = Hand(is_dealer=False)
                                dealer_hand = Hand(is_dealer=True)
                                outcome = 0
                                hand_active = True
                                reveal_dealer = False
                                add_score = True
                            elif clicked_card.name == "UNO Reverse" and hand_active:
                                profile.inventory.remove(clicked_card)
                                visualengine.trigger_anim('uno')

                                temp_cards = player_hand.cards
                                player_hand.cards = dealer_hand.cards
                                dealer_hand.cards = temp_cards

                                player_hand.calculate_score()
                                dealer_hand.calculate_score()

                                if player_hand.score >= 21:
                                    disaster.apply_acid_rain(player_hand)
                            elif clicked_card.name == "Robots" and hand_active:
                                profile.inventory.remove(clicked_card)
                                visualengine.trigger_anim('robot')

                                dealer_upcard = dealer_hand.cards[1].get_value() if len(dealer_hand.cards) > 1 else 10
                                action_type = "Hit" if player_hand.score < 12 or (player_hand.score < 17 and dealer_upcard >= 7) else "Stand"

                                if action_type == "Hit":
                                    player_hand.add_card(game_deck.deal())
                                    disaster.apply_acid_rain(player_hand)
                                else:
                                    reveal_dealer = True
                                    hand_active = False

                                    finalized_player_score = disaster.apply_service_charge(player_hand.score)
                                    finalized_dealer_score = disaster.apply_service_charge(dealer_hand.score)
                                    if disaster.check_lava_death(finalized_dealer_score):
                                        finalized_player_score = 999
                                    if disaster.check_lava_death(finalized_dealer_score):
                                        finalized_dealer_score = 999

                                    outcome, record = check_endgame(
                                        finalized_dealer_score, finalized_player_score, outcome, records, profile, current_bet
                                    )
                            elif clicked_card.name == "Redraw" and hand_active:
                                profile.inventory.remove(clicked_card)
                                visualengine.trigger_anim('redraw')

                                player_hand.cards.clear()
                                deal_queue.extend(['player', 'player'])

                                disaster.apply_acid_rain(player_hand)

    pygame.display.flip()

pygame.quit()
