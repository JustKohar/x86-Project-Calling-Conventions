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
        # Store previous EAX value in EDX
        self.registers["EDX"] = self.registers["EAX"]
        self.stack.append(frame)
        # Update EAX with the address of the new frame
        self.registers["EAX"] = frame.return_address

    def pop_stack_frame(self):
        """Pop the top stack frame from the stack."""
        if not self.stack:
            return None
        # Store previous EAX value in EDX
        self.registers["EDX"] = self.registers["EAX"]
        popped_frame = self.stack.pop()
        # Update EAX with the return address of the popped frame
        self.registers["EAX"] = popped_frame.return_address
        return popped_frame
    
    def call_function(self, function_name, parameters):
        """Simulate a function call."""
        # Store previous EAX value in EDX
        self.registers["EDX"] = self.registers["EAX"]
        return_address = f"0x{len(self.stack) + 1:04X}"  # Generate a unique return address
        local_vars = {}
        frame = StackFrame(return_address, parameters, local_vars)
        self.push_stack_frame(frame)
    
        # Simulate function execution and update registers
        if function_name == "add":
            result = parameters[0] + parameters[1] if len(parameters) > 1 else parameters[0]
            self.registers["EAX"] = result  # Store the result in EAX
        elif function_name == "subtract":
            result = parameters[0] - parameters[1] if len(parameters) > 1 else parameters[0]
            self.registers["EAX"] = result  # Store the result in EAX
        elif function_name == "multiply":
            self.multiply(parameters[0], parameters[1])
        elif function_name == "loop":
            self.simulate_loop(parameters[0])

    def multiply(self, a, b):
        """Simulate multiplication using EAX and EDX."""
        # Store previous EAX value in EDX
        self.registers["EDX"] = self.registers["EAX"]
        result = a * b  # Perform multiplication
        self.registers["EAX"] = result & 0xFFFFFFFF  # Lower 32 bits
        self.registers["EDX"] = (result >> 32) & 0xFFFFFFFF  # Upper 32 bits for high bits of multiplication
    
    def simulate_loop(self, iterations):
        """Simulate a loop using ECX as a counter."""
        # Set ECX to the number of iterations (loops played)
        self.registers["ECX"] = iterations
        
        # Store previous EAX value in EDX (before loop execution)
        self.registers["EDX"] = self.registers["EAX"]
        
        # Simulate the loop
        loop_counter = iterations
        while loop_counter > 0:
            print(f"Loop iteration: {loop_counter}")
            loop_counter -= 1
            
        # Keep ECX at the original number of iterations to display how many loops were played
        # This way ECX will always show the number of loops that were requested

    def load_from_memory(self, offset):
        """Simulate loading a value from memory using EBX as a base address."""
        if "EBX" in self.registers:
            address = self.registers["EBX"] + offset
            return self.memory.get(address, 0)  # Simulate memory access
        return 0

    def return_from_function(self):
        """Simulate returning from a function."""
        if self.stack:
            # Store previous EAX value in EDX
            self.registers["EDX"] = self.registers["EAX"]
            self.stack[-1].inactive = True
            # Update EAX with the return address or any other value
            self.registers["EAX"] = self.stack[-1].return_address