import random

class RockPaperScissors:
    
    def __init__(self):
        self.player = []
        self.computer = []
        self.player_score = []
        self.computer_score = []

    def computer_move(self):
        random_number = random.randint(1,3)
        if random_number == 1:
            self.computer.append('Rock')
        elif random_number == 2:
            self.computer.append('Paper')
        elif random_number == 3:
            self.computer.append('Scissors')

    def outcome(self):
        if self.player[-1] == 'Rock' and self.computer[-1] == 'Scissors':
            print('Rock CRUSHES Scissors! Player Victory!')
            print("🌑\n🌑\n🌑\n✂")
            self.player_score.append(1)
        elif self.player[-1] == 'Rock' and self.computer[-1] == 'Paper':
            print('Paper COVERS Rock! Computer Victory!')
            print("📄📄📄\n📄🌑📄\n📄📄📄")
            self.computer_score.append(1)
        elif self.player[-1] == 'Rock' and self.computer[-1] == 'Rock':
            print('Tie')
            print("🌑 🌑")
        elif self.player[-1] == 'Paper' and self.computer[-1] == 'Scissors':
            print('Scissors CUT Paper! Computer Victory!')
            print("✂✂✂📈✂✂✂")
            self.computer_score.append(1)
        elif self.player[-1] == 'Paper' and self.computer[-1] == 'Rock':
            print('Paper COVERS Rock! Player Victory!')
            print("📄📄📄\n📄🌑📄\n📄📄📄")
            self.player_score.append(1)
        elif self.player[-1] == 'Paper' and self.computer[-1] == 'Paper':
            print('Tie')
            print("📄 📄")
        elif self.player[-1] == 'Scissors' and self.computer[-1] == 'Rock':
            print('Rock CRUSHES Paper! Computer Victory!')
            print("🌑\n🌑\n🌑\n✂")
            self.computer_score.append(1)
        elif self.player[-1] == 'Scissors' and self.computer[-1] == 'Paper':
            print('Scissors CUT Paper! Player Victory!')
            print("✂✂✂📈✂✂✂")
            self.player_score.append(1)
        elif self.player[-1] == 'Scissors' and self.computer[-1] == 'Scissors':
            print('Tie')
            print("✂✂")
        elif self.player[-1] == 'Gun':
            print('Gun beats all. Player Wins!')
            print("💥🔫")
            self.player_score.append(100)
                
game = RockPaperScissors()

while True:
    
    action = input('Rock/Paper/Scissors/Score/Quit')
    
    if action.lower() == 'rock':
        game.player.append('Rock')
        game.computer_move()
        game.outcome()
    elif action.lower() == 'paper':
        game.player.append('Paper')
        game.computer_move()
        game.outcome()
    elif action.lower() == 'scissors':
        game.player.append('Scissors')
        game.computer_move()
        game.outcome()
    elif action.lower() == 'gun':
        game.player.append('Gun')
        game.computer_move()
        game.outcome()
    elif action.lower() == 'score':
        print(f'Player: {sum(game.player_score)} Opponent: {sum(game.computer_score)}')
    elif action.lower() == 'quit':
        break
    else:
        print('Invalid input. Try again.')