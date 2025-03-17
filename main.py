import pygame
from stack_logic import StackFrame, CPU

# Initialize pygame
pygame.init()

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
pygame.display.set_caption("Stack Frame Tinker Tool")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Fonts
large_font = pygame.font.Font(None, 36)  # For buttons and other UI elements
small_font = pygame.font.Font(None, 18)  # For stack frame text

# Initialize CPU
cpu = CPU()

# Input box
input_box = pygame.Rect(50, 50, 200, 40)
input_text = ""
active = False

# Buttons
buttons = {
    "Push": pygame.Rect(50, 100, 100, 40),
    "Pop": pygame.Rect(160, 100, 100, 40),
    "Clear": pygame.Rect(270, 100, 100, 40),
    "Call": pygame.Rect(50, 150, 100, 40),
    "Ret": pygame.Rect(160, 150, 100, 40),
    "Set EBX": pygame.Rect(50, 200, 100, 40),
    "Loop": pygame.Rect(160, 200, 100, 40),
    "Multiply": pygame.Rect(270, 200, 100, 40),
}

# PointerBox class
class PointerBox:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.dragging = False

    def draw(self, screen, font):
        """Draw the box and its text."""
        pygame.draw.rect(screen, BLUE, self.rect)  # Draw the box
        text_surface = font.render(self.text, True, WHITE)  # Draw the text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def check_drag(self, event):
        """Check if the box is being dragged."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.move_ip(event.rel)  # Move the box with the mouse

# Initialize pointer boxes
esp_box = PointerBox(50, 400, 100, 40, "ESP")
eip_box = PointerBox(200, 400, 100, 40, "EIP")
ebp_box = PointerBox(350, 400, 100, 40, "EBP")
pointer_boxes = [esp_box, eip_box, ebp_box]

# Draw static arrows next to the boxes
def draw_static_arrow(screen, box, direction="right"):
    """Draw a static arrow next to a box."""
    if direction == "right":
        start = (box.rect.right + 10, box.rect.centery)
        end = (start[0] + 50, start[1])
    elif direction == "left":
        start = (box.rect.left - 10, box.rect.centery)
        end = (start[0] - 50, start[1])
    elif direction == "up":
        start = (box.rect.centerx, box.rect.top - 10)
        end = (start[0], start[1] - 50)
    elif direction == "down":
        start = (box.rect.centerx, box.rect.bottom + 10)
        end = (start[0], start[1] + 50)

    # Draw the arrow line
    pygame.draw.line(screen, BLACK, start, end, 2)

    # Draw the arrowhead (optional)
    dx, dy = end[0] - start[0], end[1] - start[1]
    angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))
    arrow_length = 10
    arrow_points = [
        end,
        (end[0] + arrow_length, end[1] + arrow_length // 2),
        (end[0] + arrow_length, end[1] - arrow_length // 2),
    ]
    pygame.draw.polygon(screen, BLACK, arrow_points)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle dragging for pointer boxes
        for box in pointer_boxes:
            box.check_drag(event)

        # Handle other events (e.g., button clicks, text input)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle input box activity
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False

            # Handle button clicks
            for button_name, button_rect in buttons.items():
                if button_rect.collidepoint(event.pos):
                    if button_name == "Push":
                        if input_text:
                            frame = StackFrame(input_text, [], {})
                            cpu.push_stack_frame(frame)
                            input_text = ""
                    elif button_name == "Pop":
                        cpu.pop_stack_frame()
                    elif button_name == "Clear":
                        cpu.stack.clear()
                        cpu.registers = {"EAX": 0, "EBX": 0, "ECX": 0, "EDX": 0}  # Reset registers
                    elif button_name == "Call":
                        if input_text:
                            try:
                                # Handle hexadecimal input (e.g., "0x1034")
                                if input_text.startswith("0x"):
                                    args = [int(input_text, 16)]  # Convert hex to integer
                                else:
                                    args = list(map(int, input_text.split()))  # Convert decimal to integer
                                cpu.call_function("add", args)
                                input_text = ""
                            except ValueError:
                                print("Invalid input. Please enter a valid number or hexadecimal value.")
                    elif button_name == "Ret":
                        cpu.return_from_function()
                    elif button_name == "Set EBX":
                        if input_text:
                            cpu.registers["EBX"] = int(input_text, 16)  # Set EBX to the input value
                            input_text = ""
                    elif button_name == "Loop":
                        if input_text:
                            iterations = int(input_text)
                            cpu.simulate_loop(iterations)
                            input_text = ""
                    elif button_name == "Multiply":
                        if input_text:
                            args = list(map(int, input_text.split()))  # Convert input to integers
                            cpu.multiply(args[0], args[1])
                            input_text = ""

        # Handle text input
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if input_text:
                        frame = StackFrame(input_text, [], {})
                        cpu.push_stack_frame(frame)
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Clear the screen
    screen.fill(WHITE)

    # Draw input box
    pygame.draw.rect(screen, BLUE if active else GRAY, input_box, 2)
    text_surface = large_font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Draw buttons
    for button_name, button_rect in buttons.items():
        pygame.draw.rect(screen, GREEN, button_rect)
        text_surface = large_font.render(button_name, True, BLACK)
        screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))

    # Draw stack frames
    stack_x, stack_y = 400, 500  # Starting position for the first frame
    frame_height = 60  # Reduced height for smaller text
    vertical_spacing = 80  # Reduced spacing for smaller text

    for frame in cpu.stack:
        text_y = stack_y + 5  # Adjust vertical position for smaller text
        for key, value in frame.__dict__.items():
            if key != "inactive":
                text_surface = small_font.render(f"{key}: {value}", True, BLACK)  # Use small_font
                screen.blit(text_surface, (stack_x + 5, text_y))  # Adjust horizontal position
                text_y += 15  # Adjust line spacing for smaller text
        stack_y -= vertical_spacing  # Move up for the next frame

    # Draw registers
    register_x, register_y = 50, 300
    for reg, value in cpu.registers.items():
        text_surface = large_font.render(f"{reg}: {value}", True, BLACK)
        screen.blit(text_surface, (register_x, register_y))
        register_y += 40

    # Draw pointer boxes
    for box in pointer_boxes:
        box.draw(screen, large_font)

    # Draw static arrows next to the boxes
    draw_static_arrow(screen, esp_box, direction="right")
    draw_static_arrow(screen, eip_box, direction="right")
    draw_static_arrow(screen, ebp_box, direction="right")

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()