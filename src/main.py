import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Confirm

console = Console()

def generate_random_number(min_val=1, max_val=100):
    """
    Generates a random integer between min_val and max_val (inclusive).
    """
    return random.randint(min_val, max_val)

def get_valid_int(prompt, min_val=1, max_val=100):
    """
    Repeatedly prompts the user for an integer until a valid one within the range is provided.
    """
    while True:
        val = IntPrompt.ask(prompt)
        if min_val <= val <= max_val:
            return val
        else:
            console.print(f"[bold red]{min_val}에서 {max_val} 사이의 숫자를 입력해주세요.[/bold red]")

def compare_guess(guess, secret_number):
    """
    Compares the user's guess with the secret number.
    Returns 'High', 'Low', or 'Correct'.
    """
    if guess > secret_number:
        return "High"
    elif guess < secret_number:
        return "Low"
    else:
        return "Correct"

def display_instructions():
    """
    Displays the initial game instructions to the user.
    """
    instruction_text = (
        "1에서 100 사이의 숫자 중 하나를 골랐습니다.\n"
        "가능한 한 적은 시도로 숫자를 맞춰보세요!\n"
        "당신이 입력한 숫자가 '너무 높은지' 혹은 '너무 낮은지' 알려드릴게요."
    )
    console.print(Panel(instruction_text, title="[bold magenta]숫자 맞추기 게임에 오신 것을 환영합니다![/bold magenta]", expand=False))

def play_game():
    """
    The main game loop that coordinates the flow of the guessing game.
    """
    display_instructions()
    
    # Allow user to set maximum attempts
    max_attempts = get_valid_int("이번 세션의 최대 시도 횟수를 설정해주세요", 1, 100)
    
    best_score = float('inf')
    while True:
        secret_number = generate_random_number()
        attempts_left = max_attempts
        guessed_correctly = False

        console.print(f"\n[bold cyan]새로운 게임 시작! 1에서 100 사이의 숫자를 생각했습니다.[/bold cyan]")
        if best_score != float('inf'):
            console.print(f"[bold yellow]현재 최고 기록: {best_score}회 시도[/bold yellow]")
        console.print(f"숫자를 맞추기 위해 총 [bold]{max_attempts}번[/bold]의 기회가 있습니다.")

        while not guessed_correctly and attempts_left > 0:
            guess = get_valid_int(f"({attempts_left}번 남음) 숫자를 입력하세요", 1, 100)
            result = compare_guess(guess, secret_number)
            attempts_left -= 1

            if result == "High":
                console.print("[bold red]너무 높아요![/bold red]")
            elif result == "Low":
                console.print("[bold blue]너무 낮아요![/bold blue]")
            else:
                attempts_taken = max_attempts - attempts_left
                console.print(f"[bold green]정답입니다! {attempts_taken}번 만에 맞추셨네요![/bold green]")
                guessed_correctly = True
                if attempts_taken < best_score:
                    best_score = attempts_taken
                    console.print(f"[bold gold1]최고 기록 경신! 현재 최고 기록은 {best_score}회입니다.[/bold gold1]")

        if not guessed_correctly:
            console.print(f"[bold red]게임 오버! 기회를 모두 소진했습니다. 정답은 {secret_number}였습니다.[/bold red]")

        if not Confirm.ask("다시 플레이하시겠습니까?"):
            console.print("[bold magenta]게임을 플레이해주셔서 감사합니다![/bold magenta]")
            break

if __name__ == "__main__":
    play_game()
