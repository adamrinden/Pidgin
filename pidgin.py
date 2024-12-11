from textx import metamodel_from_file

# Load metamodel and model
pidgin_mm = metamodel_from_file('pidgin.tx')
pidgin_model = pidgin_mm.model_from_file("dialogue.pdg")

# Player class holds the player name and gold amount
class Player:
	name = "Name"
	gold = 0

class NPC:
	def __init__(self, model):
		self.name = model.name.npcName
		self.entry = model.entry.entry
		self.dialogue_dict = {}

		for block in model.dialogueBlocks:
			self.dialogue_dict[block.id] = block

	def preProcc(self, dialogue, player):
		return dialogue.replace("player.name", player.name).replace("player.gold", str(player.gold))

	def dialogueProcc(self, dialogue):
		for command in dialogue:
				if command.__class__.__name__ == "Say":
					print(self.preProcc(command.sentence, player))
				elif command.__class__.__name__ == "Update":
					player.gold += command.value
					print(f"Current gold: {player.gold}")
				else:
					print(command.action)

	def conversion(self, player):
		state = self.entry

		# Manages dialogue state and loops through available dialogue options
		while state is not None:
			print(f"{self.name}:")
			dialogueBlock = self.dialogue_dict[state]
			self.dialogueProcc(dialogueBlock.dialogueCommands)

			# Handles end of dialogue blocks 
			if dialogueBlock.dialogueEnding.__class__.__name__ == "Choices": 
				for i, choice in enumerate(dialogueBlock.dialogueEnding.choiceBlocks):
					print(f"{i + 1}. {self.preProcc(choice.text, player)}")

				# Validate player input
				playerChoice = None
				while playerChoice is None:
					try:
						playerInput = int(input("Choose an option: "))
						if 1 <= playerInput <= len(dialogueBlock.dialogueEnding.choiceBlocks):
							playerChoice = dialogueBlock.dialogueEnding.choiceBlocks[playerInput - 1]
						else:
							print("Invalid choice. Please select a valid option.")
					except ValueError:
						print("Invalid input. Please enter a number.")

				self.dialogueProcc(playerChoice.dialogueCommands)

				# Handles player gold success or fail conditions
				if playerChoice.cont is not None:
					if playerChoice.cont.__class__.__name__ == "ConditionalContinue":
						if playerChoice.cont.conditional.operator == ">=" and player.gold >= playerChoice.cont.conditional.value:
							state = playerChoice.cont.success.id
						elif playerChoice.cont.conditional.operator == "<=" and player.gold <= playerChoice.cont.conditional.value:
							state = playerChoice.cont.success.id
						elif playerChoice.cont.conditional.operator == ">" and player.gold > playerChoice.cont.conditional.value:
							state = playerChoice.cont.success.id
						elif playerChoice.cont.conditional.operator == "<" and player.gold < playerChoice.cont.conditional.value:
							state = playerChoice.cont.success.id
						elif playerChoice.cont.conditional.operator == "==" and player.gold == playerChoice.cont.conditional.value:
							state = playerChoice.cont.success.id
						else:
							state = playerChoice.cont.fail.id
					else:
						state = playerChoice.cont.id
				else:
					state = None

			elif dialogueBlock.dialogueEnding.__class__.__name__ == "Continue":
				state = dialogueBlock.dialogueEnding.id
			else:
				state = None

# Create player object
player = Player()

# Validate name input
player.name = input("Please enter your name: ").strip()
while not (player.name.isalpha() and len(player.name) > 1):  # Ensures name is alphabetic and at least 2 characters
    print("Invalid name. Please enter a valid name with only letters.")
    player.name = input("Please enter your name: ").strip()

# Validate gold input
try:
    player.gold = int(input("Please enter your amount of gold: "))
    while player.gold < 0:  # Ensures gold is non-negative
        print("Gold cannot be negative. Please enter a valid number.")
        player.gold = int(input("Please enter your amount of gold: "))
except ValueError:
    print("Invalid input. Gold must be a whole number.")
    player.gold = int(input("Please enter your amount of gold: "))

# Start the program
pidgin = NPC(pidgin_model)
pidgin.conversion(player)