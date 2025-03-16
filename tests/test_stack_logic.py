import unittest
from stack_logic import CPU, StackFrame

class TestStackLogic(unittest.TestCase):
    def setUp(self):
        """Set up a CPU instance for testing."""
        self.cpu = CPU()

    def test_push_stack_frame(self):
        frame = StackFrame("0x1000", ["arg1", "arg2"], {})
        self.cpu.push_stack_frame(frame)
        self.assertEqual(len(self.cpu.stack), 1)
        self.assertEqual(self.cpu.stack[0].return_address, "0x1000")

    def test_pop_stack_frame(self):
        frame = StackFrame("0x1000", ["arg1", "arg2"], {})
        self.cpu.push_stack_frame(frame)
        popped_frame = self.cpu.pop_stack_frame()
        self.assertEqual(popped_frame.return_address, "0x1000")
        self.assertEqual(len(self.cpu.stack), 0)

    def test_call_function(self):
        self.cpu.call_function("add", [5, 3])
        self.assertEqual(len(self.cpu.stack), 1)
        self.assertEqual(self.cpu.stack[0].return_address, "next_instruction_after_add")

    def test_return_from_function(self):
        self.cpu.call_function("add", [5, 3])
        self.cpu.return_from_function()
        self.assertTrue(self.cpu.stack[-1].inactive)  # Update this line

if __name__ == "__main__":
    unittest.main()