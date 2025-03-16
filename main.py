import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stack Frame Tinker Tool")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Font
font = pygame.font.Font(None, 36)

# StackFrame class
class StackFrame:
    def __init__(self, return_address, parameters, local_vars):
        self.return_address = return_address
        self.parameters = parameters
        self.local_vars = local_vars
        self.inactive = False  # Track if the frame is inactive

    def __repr__(self):
        return f"StackFrame(return_address={self.return_address}, parameters={self.parameters}, locals={self.local_vars}, inactive={self.inactive})"


# CPU class
class CPU:
    def __init__(self):
        self.stack = []  # Represents the call stack
        self.registers = {"EAX": 0, "EBX": 0, "ECX": 0, "EDX": 0}  # Simulate CPU registers

    def push_stack_frame(self, frame):
        """Push a new stack frame onto the stack."""
        self.stack.append(frame)
        # Update EAX with the address of the new frame
        self.registers["EAX"] = frame.return_address

    def pop_stack_frame(self):
        """Pop the top stack frame from the stack."""
        if not self.stack:
            return None
        popped_frame = self.stack.pop()
        # Update EAX with the address of the popped frame
        self.registers["EAX"] = popped_frame.return_address
        return popped_frame

    def call_function(self, function_name, parameters):
        """Simulate a function call."""
        return_address = f"next_instruction_after_{function_name}"
        local_vars = {}
        frame = StackFrame(return_address, parameters, local_vars)
        self.push_stack_frame(frame)

        # Simulate function execution and update registers
        if function_name == "add":
            result = parameters[0] + parameters[1]
            self.registers["EAX"] = result  # Store the result in EAX
        elif function_name == "subtract":
            result = parameters[0] - parameters[1]
            self.registers["EAX"] = result  # Store the result in EAX

    def return_from_function(self):
        """Simulate returning from a function."""
        if self.stack:
            self.stack[-1].inactive = True
            # Update EAX with the return address or any other value
            self.registers["EAX"] = self.stack[-1].return_address


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
}

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks
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
                            # Simulate a function call with arguments
                            args = list(map(int, input_text.split()))  # Convert input to integers
                            cpu.call_function("add", args)
                            input_text = ""
                    elif button_name == "Ret":
                        cpu.return_from_function()

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
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Draw buttons
    for button_name, button_rect in buttons.items():
        pygame.draw.rect(screen, GREEN, button_rect)
        text_surface = font.render(button_name, True, BLACK)
        screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))

    # Draw stack frames
    stack_x, stack_y = 400, 500
    for frame in cpu.stack:
        color = BLUE if not frame.inactive else GRAY
        pygame.draw.rect(screen, color, (stack_x, stack_y, 300, 80))
        text_y = stack_y + 10
        for key, value in frame.__dict__.items():
            if key != "inactive":
                text_surface = font.render(f"{key}: {value}", True, BLACK)
                screen.blit(text_surface, (stack_x + 10, text_y))
                text_y += 20
        stack_y -= 60  # Move up for the next frame

    # Draw registers
    register_x, register_y = 50, 300
    for reg, value in cpu.registers.items():
        text_surface = font.render(f"{reg}: {value}", True, BLACK)
        screen.blit(text_surface, (register_x, register_y))
        register_y += 40

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()