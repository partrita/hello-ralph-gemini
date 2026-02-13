import unittest
from unittest.mock import patch
from main import generate_random_number, get_user_input, compare_guess, get_valid_int

class TestMain(unittest.TestCase):
    def test_generate_random_number_range(self):
        """난수가 지정된 범위 내에 있는지 확인합니다."""
        for _ in range(1000):
            num = generate_random_number(1, 100)
            self.assertTrue(1 <= num <= 100)

    def test_generate_random_number_types(self):
        """반환값이 정수인지 확인합니다."""
        num = generate_random_number()
        self.assertIsInstance(num, int)

    def test_get_user_input(self):
        """사용자 입력을 올바르게 받는지 확인합니다."""
        with patch('builtins.input', return_value='42'):
            result = get_user_input()
            self.assertEqual(result, '42')

    def test_get_valid_int(self):
        """get_valid_int가 유효한 입력, 잘못된 형식 및 범위를 벗어난 입력을 처리하는지 확인합니다."""
        with patch('main.get_user_input', side_effect=['abc', '150', '50']):
            with patch('builtins.print') as mock_print:
                result = get_valid_int("Prompt: ", 1, 100)
                self.assertEqual(result, 50)
                mock_print.assert_any_call("Invalid input. Please enter a valid integer.")
                mock_print.assert_any_call("Please enter a number between 1 and 100.")

    def test_compare_guess_high(self):
        """추측이 높을 때 'High'를 반환하는지 확인합니다."""
        self.assertEqual(compare_guess(75, 50), "High")

    def test_compare_guess_low(self):
        """추측이 낮을 때 'Low'를 반환하는지 확인합니다."""
        self.assertEqual(compare_guess(25, 50), "Low")

    def test_compare_guess_correct(self):
        """추측이 정확할 때 'Correct'를 반환하는지 확인합니다."""
        self.assertEqual(compare_guess(50, 50), "Correct")

    @patch('main.generate_random_number', return_value=50)
    @patch('main.get_user_input', side_effect=['10', '25', '75', '50', 'n'])
    @patch('builtins.print')
    def test_play_game_loop(self, mock_print, mock_input, mock_gen_rand):
        """메인 게임 루프가 정답을 맞출 때까지 올바르게 작동하는지 확인합니다."""
        from main import play_game
        # Inputs: '10' (max_attempts), '25', '75', '50' (guesses), 'n' (play again)
        play_game()
        
        # Check if feedback was printed
        mock_print.assert_any_call("Too low!")
        mock_print.assert_any_call("Too high!")
        self.assertTrue(any("You won!" in str(call) for call in mock_print.call_args_list))
        mock_print.assert_any_call("Thanks for playing!")

    @patch('main.generate_random_number', side_effect=[50, 30])
    @patch('main.get_user_input', side_effect=['10', '50', 'y', '30', 'n'])
    @patch('builtins.print')
    def test_play_again_logic(self, mock_print, mock_input, mock_gen_rand):
        """다시 하기 기능이 올바르게 작동하는지 확인합니다."""
        from main import play_game
        # Inputs: '10' (max_attempts), '50' (guess), 'y' (again), '30' (guess), 'n' (again)
        play_game()
        
        self.assertEqual(mock_gen_rand.call_count, 2)
        self.assertTrue(any("You won!" in str(call) for call in mock_print.call_args_list))
        mock_print.assert_any_call("Thanks for playing!")

    @patch('main.generate_random_number', side_effect=[50, 30])
    @patch('main.get_user_input', side_effect=['10', '50', 'y', '30', 'n'])
    @patch('builtins.print')
    def test_high_score_tracking(self, mock_print, mock_input, mock_gen_rand):
        """최고 점수가 세션 동안 올바르게 추적되는지 확인합니다."""
        from main import play_game
        # Inputs: '10' (max_attempts), '50' (guess), 'y' (again), '30' (guess), 'n' (again)
        play_game()
        
        # 첫 번째 게임 승리 (1번의 시도)
        mock_print.assert_any_call("New high score! Your best score is now 1 attempts.")
        # 두 번째 게임 시작 시 최고 점수 표시 확인
        mock_print.assert_any_call("Current best score: 1 attempts")

    @patch('main.generate_random_number', return_value=50)
    @patch('main.get_user_input', side_effect=['2', '10', '20', 'n'])
    @patch('builtins.print')
    def test_game_over_out_of_attempts(self, mock_print, mock_input, mock_gen_rand):
        """시도 횟수를 모두 소진했을 때 게임 오버가 되는지 확인합니다."""
        from main import play_game
        # Inputs: '2' (max_attempts), '10', '20' (guesses), 'n' (play again)
        play_game()
        
        mock_print.assert_any_call("Game over! You've run out of attempts. The number was 50.")
        mock_print.assert_any_call("Thanks for playing!")

if __name__ == "__main__":
    unittest.main()
