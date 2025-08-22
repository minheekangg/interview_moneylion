import unittest
from unittest.mock import patch
import io
from bounding_box import main  

class TestBoundingBox(unittest.TestCase):

    def run_main_with_input(self, input_text):
        """
        This method simulates standard input by patching sys.stdin with a StringIO object.
        It allows us to test the main function without needing to modify it to accept parameters.
        """
        with patch('sys.stdin', new=io.StringIO(input_text)):
            res = main()
        
        return res
    

    def test_single_group(self):
        """Tests a single, simple bounding box."""
        input_data = (
            "--***--\n"
            "-*****-\n"
            "--***--\n"
            "--***--\n"
        )
        
        expected_output = "(1,2)(4,6)"
        
        output = self.run_main_with_input(input_data)
        
        self.assertEqual(output, expected_output)

    def test_multiple_non_overlapping_groups(self):
        """Tests multiple non-overlapping boxes and finds the largest by area."""
        input_data = (
            "**--\n"
            "**--\n"
            "----\n"
            "---*\n"
            "---*\n"
        )
        # Box 1: (1,1)(2,2), Area = 4
        # Box 2: (5,4)(6,4), Area = 2
        # expected_output = "(1,1)(2,2)"
        expected_output = "(1,1)(2,33)"
        
        output = self.run_main_with_input(input_data)
        
        self.assertEqual(output, expected_output)

    
    def test_overlapping_groups(self):
        """
        Tests a scenario where the largest group's bounding box overlaps
        with another, so a smaller, non-overlapping box is the correct answer.
        This mirrors the original prompt's example.
        """
        input_data = (
            "**-------***\n"
            "-*--**--***-\n"
            "-----***--**\n"
            "-------***--\n"
        )
        # Box 1: (1,1)(2,2), Area = 4
        # Box 2: (1,8)(3,12), Area = 12, but overlaps with Box 3
        # Box 3: (2,5)(4,10), Area = 18, but overlaps with Box 2
        expected_output = "(1,1)(2,2)"
    
        output = self.run_main_with_input(input_data)
        self.assertEqual(output, expected_output)

        

if __name__ == '__main__':
    unittest.main()