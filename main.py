import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 640, 480
CARD_SIZE = (100, 100)
BACKGROUND_COLOR = (30, 30, 30)
CARD_BACK_COLOR = (100, 100, 255)  # Blue for the back of the cards
FPS = 30

# Path to images
IMAGE_PATH = "./images"

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Matching Game")
font = pygame.font.SysFont("Arial", 40)

# Load images
def load_images():
    images = []
    for i in range(1, 9):
        img = pygame.image.load(os.path.join(IMAGE_PATH, f"{i}.png"))
        img = pygame.transform.scale(img, CARD_SIZE)
        images.append(img)
    return images

def draw_text(text, font, color, surface, x, y):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_card(card, surface):
    if card["revealed"]:
        surface.blit(card["image"], card["rect"].topleft)
    else:
        pygame.draw.rect(surface, CARD_BACK_COLOR, card["rect"])  # Draw solid blue card
        draw_text("?", font, (255, 255, 255), surface, card["rect"].centerx - 15, card["rect"].centery - 20)

class Game:
    def __init__(self, images):
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.start_time = time.time()

        self.generate_cards(images)

    def generate_cards(self, images):
        image_list = images * 2
        random.shuffle(image_list)

        for i in range(4):
            for j in range(4):
                img = image_list.pop()
                rect = pygame.Rect(j * (CARD_SIZE[0] + 20) + 50, i * (CARD_SIZE[1] + 20) + 50, *CARD_SIZE)
                self.cards.append({"rect": rect, "image": img, "revealed": False})

    def flip_card(self, card):
        card["revealed"] = True
        self.selected_cards.append(card)

    def check_match(self):
        if len(self.selected_cards) == 2:
            card1, card2 = self.selected_cards
            if card1["image"] == card2["image"]:
                self.matched_pairs += 1
            else:
                pygame.time.wait(500)
                card1["revealed"] = False
                card2["revealed"] = False
            self.selected_cards = []

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)

        # Draw cards
        for card in self.cards:
            draw_card(card, surface)

        # Display the timer
        elapsed_time = round(time.time() - self.start_time, 2)
        draw_text(f"Time: {elapsed_time}s", font, (255, 255, 255), surface, 20, 20)

        # Check if pairs are matched
        if self.matched_pairs == 8:
            draw_text("You Win!", font, (0, 255, 0), surface, WIDTH // 2 - 100, HEIGHT // 2 - 20)

# Main Loop
def main():
    clock = pygame.time.Clock()

    # Load images for the cards
    images = load_images()

    game = Game(images)
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a card was clicked
                mouse_pos = pygame.mouse.get_pos()
                for card in game.cards:
                    if card["rect"].collidepoint(mouse_pos) and not card["revealed"]:
                        game.flip_card(card)
                        game.check_match()

        # Draw the game
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
