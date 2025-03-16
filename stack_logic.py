class StackFrame:
    def __init__(self, return_address, parameters, local_vars):
        self.return_address = return_address
        self.parameters = parameters
        self.local_vars = local_vars
        self.inactive = False  # Add this line

    def __repr__(self):
        return f"StackFrame(return_address={self.return_address}, parameters={self.parameters}, locals={self.local_vars}, inactive={self.inactive})"

class CPU:
    def __init__(self):
        self.stack = []  # Represents the call stack
        self.registers = {"EAX": 0, "EBX": 0, "ECX": 0, "EDX": 0}  # Simulate CPU registers
        self.memory = {}  # Simulate memory

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
        elif function_name == "multiply":
            self.multiply(parameters[0], parameters[1])

    def multiply(self, a, b):
        """Simulate multiplication using EAX and EDX."""
        result = a * b
        self.registers["EAX"] = result & 0xFFFFFFFF  # Lower 32 bits
        self.registers["EDX"] = (result >> 32) & 0xFFFFFFFF  # Upper 32 bits

    def return_from_function(self):
        """Simulate returning from a function."""
        if self.stack:
            self.stack[-1].inactive = True
            # Update EAX with the return address or any other value
            self.registers["EAX"] = self.stack[-1].return_address

    def load_from_memory(self, offset):
        """Simulate loading a value from memory using EBX as a base address."""
        if "EBX" in self.registers:
            address = self.registers["EBX"] + offset
            return self.memory.get(address, 0)  # Simulate memory access
        return 0

    def simulate_loop(self, iterations):
        """Simulate a loop using ECX as a counter."""
        self.registers["ECX"] = iterations
        while self.registers["ECX"] > 0:
            print(f"Loop iteration: {self.registers['ECX']}")
            self.registers["ECX"] -= 1