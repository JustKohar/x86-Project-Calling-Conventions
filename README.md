# x86-Project-Calling-Conventions

This project simulates x86 calling conventions using a graphical interface built with Pygame. It allows users to visualize stack frames, registers, and pointer boxes, and interact with the simulation through various buttons.

## Features

- **Stack Frames**: Visualize stack frames with key-value pairs.
- **Registers**: Display and update the values of x86 registers (EAX, EBX, ECX, EDX).
- **Pointer Boxes**: Visualize pointer boxes with static arrows.
- **Interactive Buttons**: Perform operations like push, pop, call, return, loop, and multiply.

## How It Works

### Main Components

1. **CPU Class**: Manages the stack, registers, and operations.
2. **Pygame Interface**: Handles the graphical display and user interactions.

### CPU Class

The `CPU` class is responsible for managing the stack and registers. It provides methods to perform various operations:

- `push_stack_frame(frame)`: Pushes a stack frame onto the stack.
- `pop_stack_frame()`: Pops a stack frame from the stack.
- `call_function(function_name, args)`: Simulates a function call and updates the `EAX` register.
- `return_from_function()`: Simulates returning from a function.
- `simulate_loop(iterations)`: Simulates a loop by decrementing the `ECX` register.
- `multiply(a, b)`: Multiplies two numbers and updates the `EAX` register.

### Pygame Interface

The Pygame interface handles the graphical display and user interactions. It includes:

- **Input Box**: Allows users to enter text input.
- **Buttons**: Perform various operations when clicked.
- **Stack Frames**: Displayed with red borders and key-value pairs.
- **Registers**: Displayed at the bottom of the screen.
- **Pointer Boxes**: Displayed with static arrows pointing down.

### Event Handling

The main loop handles events such as button clicks, text input, and dragging pointer boxes. It updates the display accordingly.

### Example Operations

- **Push**: Adds a new stack frame with the input text.
- **Pop**: Removes the top stack frame.
- **Clear**: Clears the stack and resets the registers.
- **Call**: Simulates a function call and updates the `EAX` register.
- **Ret**: Simulates returning from a function.
- **Set EBX**: Sets the `EBX` register to the input value.
- **Loop**: Simulates a loop by decrementing the `ECX` register.
- **Multiply**: Multiplies two numbers and updates the `EAX` register.

## Running the Project

To run the project, ensure you have Pygame installed:

```bash
pip install pygame

then run
python main.py