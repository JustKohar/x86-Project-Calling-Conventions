import pygame
import unittest
from main import StackFrame, CPU  # Import your main application logic

class TestUI(unittest.TestCase):
    def setUp(self):
        """Set up Pygame and the CPU instance for testing."""
        pygame.init()
        self.cpu = CPU()

    def test_push_button(self):
        # Simulate clicking the "Push" button
        self.cpu.push_stack_frame(StackFrame("0x1000", ["arg1", "arg2"], {}))
        self.assertEqual(len(self.cpu.stack), 1)

    def test_pop_button(self):
        # Simulate clicking the "Pop" button
        self.cpu.push_stack_frame(StackFrame("0x1000", ["arg1", "arg2"], {}))
        self.cpu.pop_stack_frame()
        self.assertEqual(len(self.cpu.stack), 0)

    def tearDown(self):
        """Clean up Pygame after each test."""
        pygame.quit()

if __name__ == "__main__":
    unittest.main()