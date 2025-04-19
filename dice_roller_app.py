import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

# Removed invalid lines as they are not valid Python syntax
# c:\Users\USER\Downloads\bin\dice_roller-0.1-debug.apk

class DiceRollerApp(App):
    def build(self):
        self.player1_score = 0
        self.player2_score = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.game_paused = False

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        with self.layout.canvas.before:
            Color(0.1, 0.2, 0.5, 1)  # Dark blue background
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        self.title_label = Label(
            text="[b]Dice Rolling Game[/b]",  # Uppercase and bold
            font_size=30,
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1),
            markup=True  # Enable markup for bold text
        )
        self.layout.add_widget(self.title_label)

        # Player Names Section
        self.player1_name_input = TextInput(
            hint_text="Enter Player 1 Name",
            multiline=False,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.player1_name_input)

        self.player2_name_input = TextInput(
            hint_text="Enter Player 2 Name",
            multiline=False,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.player2_name_input)

        # Player 1 Section
        self.player1_label = Label(
            text="Player 1: Waiting to roll...",
            font_size=18,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.player1_label)

        self.player1_button = Button(
            text="Roll for Player 1",
            size_hint=(1, 0.1),
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        self.player1_button.bind(on_press=self.roll_player1)
        self.layout.add_widget(self.player1_button)

        # Player 2 Section
        self.player2_label = Label(
            text="Player 2: Waiting to roll...",
            font_size=18,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.player2_label)

        self.player2_button = Button(
            text="Roll for Player 2",
            size_hint=(1, 0.1),
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        self.player2_button.bind(on_press=self.roll_player2)
        self.layout.add_widget(self.player2_button)

        # Scoreboard Section
        self.scoreboard_label = Label(
            text="Scoreboard: Player 1 Wins: 0 | Player 2 Wins: 0",
            font_size=16,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.scoreboard_label)

        # Control Buttons Section
        self.control_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.start_button = Button(text="Start", background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        self.start_button.bind(on_press=self.start_game)
        self.control_layout.add_widget(self.start_button)

        self.reset_button = Button(text="Reset Game", background_color=(1, 0.5, 0, 1), color=(1, 1, 1, 1))
        self.reset_button.bind(on_press=self.reset_game)
        self.control_layout.add_widget(self.reset_button)

        self.quit_button = Button(text="Quit", background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
        self.quit_button.bind(on_press=self.confirm_quit)
        self.control_layout.add_widget(self.quit_button)

        self.layout.add_widget(self.control_layout)

        # Winner Section
        self.winner_label = Label(
            text="",
            font_size=20,
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.winner_label)

        # Developer Credit Section
        self.credit_label = Label(
            text="Game developed by Joy",
            font_size=14,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.credit_label)

        return self.layout

    def roll_player1(self, instance):
        if not self.game_paused:
            player1_name = self.player1_name_input.text or "Player 1"
            self.player1_score = random.randint(1, 6)
            self.player1_label.text = f"{player1_name} rolled: {self.player1_score}"
            self.check_winner()

    def roll_player2(self, instance):
        if not self.game_paused:
            player2_name = self.player2_name_input.text or "Player 2"
            self.player2_score = random.randint(1, 6)
            self.player2_label.text = f"{player2_name} rolled: {self.player2_score}"
            self.check_winner()

    def check_winner(self):
        if self.player1_score > 0 and self.player2_score > 0:
            if self.player1_score > self.player2_score:
                self.player1_wins += 1
                self.winner_label.text = "Player 1 Wins! 🎉"
            elif self.player1_score < self.player2_score:
                self.player2_wins += 1
                self.winner_label.text = "Player 2 Wins! 🎉"
            else:
                self.winner_label.text = "It's a Tie! 🤝"

            # Update the scoreboard
            self.scoreboard_label.text = f"Scoreboard: Player 1 Wins: {self.player1_wins} | Player 2 Wins: {self.player2_wins}"

    def start_game(self, instance):
        self.game_paused = False
        self.winner_label.text = ""
        self.player1_label.text = "Player 1: Waiting to roll..."
        self.player2_label.text = "Player 2: Waiting to roll..."

    def reset_game(self, instance):
        self.player1_score = 0
        self.player2_score = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.start_game(instance)
        self.scoreboard_label.text = "Scoreboard: Player 1 Wins: 0 | Player 2 Wins: 0"

    def confirm_quit(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text="Do you really want to quit?", font_size=18)
        popup_layout.add_widget(popup_label)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(text="Yes", background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
        yes_button.bind(on_press=self.quit_game)
        button_layout.add_widget(yes_button)

        no_button = Button(text="No", background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        no_button.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(no_button)

        popup_layout.add_widget(button_layout)

        popup = Popup(title="Quit Confirmation", content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

    def quit_game(self, instance):
        App.get_running_app().stop()

    def _update_rect(self, instance, value):
        """Update the size and position of the background rectangle."""
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos


# Run the app
if __name__ == "__main__":
    DiceRollerApp().run()