import openai

# Function to set up OpenAI API key
def setup_openai_api():
    api_key = input("Enter your OpenAI API key: ").strip()
    openai.api_key = api_key

# Function to generate hints using OpenAI API
def generate_hints(movie_title):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Using a supported model
            prompt=f"Provide 5 hints about the movie: {movie_title}.",
            max_tokens=100,
            temperature=0.7
        )
        hints = response['choices'][0]['text'].strip().split("\n")
        return [hint.strip() for hint in hints if hint.strip()]
    except openai.OpenAIError as e:  # Catch all OpenAI errors directly
        print(f"Error generating hints: {e}")
        return ["Hint generation failed. Try again later."]
    except Exception as e:
        # Catch other general exceptions
        print(f"Unexpected error: {e}")
        return ["Error occurred. Please try again later."]

# Main game logic
class MovieGuessGame:
    def __init__(self, movie_title, main_star):
        self.movie_title = movie_title
        self.main_star = main_star
        self.hints = []
        self.current_hint_index = 0
        self.points = 0

    def start_game(self):
        print("Welcome to the Movie Guessing Game!")
        print("You will get hints to guess the movie. Let’s start!")

        # Generate hints for the movie
        self.hints = generate_hints(self.movie_title)
        self.current_hint_index = 0
        self.points = 0

        if self.hints:
            print(f"Hint 1: {self.hints[self.current_hint_index]}")

        # Game loop
        while True:
            user_input = input("\nYour guess (or type 'exit' to quit): ").strip()

            if user_input.lower() == "exit":
                print(f"Game Over! Your total points: {self.points}")
                break

            self.submit_guess(user_input)
            if self.current_hint_index < len(self.hints) - 1:
                self.next_hint()

            print(f"Current Points: {self.points}")
            print("\n")

    def submit_guess(self, guess):
        guess = guess.strip()

        if not guess:
            print("Please enter your guess.")
            return

        if guess.lower() == self.movie_title.lower():
            self.points += 5
            print("You guessed the movie correctly! +5 points")
        elif guess.lower() == self.main_star.lower():
            self.points += 4
            print("You guessed the main star correctly! +4 points")
        elif any(guess.lower() in hint.lower() for hint in self.hints):
            self.points += 2
            print("Your guess matches part of the hint! +2 points")
        else:
            self.points -= 2
            print("Incorrect guess! -2 points")

    def next_hint(self):
        if self.current_hint_index < len(self.hints) - 1:
            self.current_hint_index += 1
            print(f"\nHint {self.current_hint_index + 1}: {self.hints[self.current_hint_index]}")

# Main program execution
if __name__ == "__main__":
    # Set up OpenAI API key
    setup_openai_api()

    # Game details (you can change these as needed)
    movie_title = "Inception"
    main_star = "Leonardo DiCaprio"

    # Initialize and start the game
    game = MovieGuessGame(movie_title, main_star)
    game.start_game()
