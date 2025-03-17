import unittest
from stack_logic import CPU

class TestRegisters(unittest.TestCase):
    def setUp(self):
        """Set up a CPU instance for testing."""
        self.cpu = CPU()

    def test_ebx_memory_addressing(self):
        """Test EBX for memory addressing."""
        self.cpu.registers["EBX"] = 0x1000  # Set base address
        self.cpu.memory = {0x1000: 42, 0x1004: 100}  # Simulate memory
        value = self.cpu.load_from_memory(0)  # Load from address 0x1000
        self.assertEqual(value, 42)

    def test_ecx_loop_counter(self):
        """Test ECX as a loop counter."""
        self.cpu.simulate_loop(5)
        self.assertEqual(self.cpu.registers["ECX"], 0)  # ECX should be 0 after the loop

    def test_edx_multiplication(self):
        """Test EDX for extended multiplication."""
        self.cpu.multiply(0x1000, 0x1000)  # Multiply two large numbers
        self.assertEqual(self.cpu.registers["EAX"], 0x1000000 & 0xFFFFFFFF)  # Lower 32 bits
        self.assertEqual(self.cpu.registers["EDX"], (0x1000000 >> 32) & 0xFFFFFFFF)  # Upper 32 bits

if __name__ == "__main__":
    unittest.main()