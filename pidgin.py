from textx import metamodel_from_file
pidgin_mm = metamodel_from_file('pidgin.tx')
pidgin_model = pidgin_mm.model_from_file("dialogue.pdg")

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

				# Handles converstation to specific dialogue tree
				playerInput = int(input("Type number: "))
				playerChoice = dialogueBlock.dialogueEnding.choiceBlocks[playerInput - 1]

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

player = Player()
player.name = input("Please enter your name: ")
player.gold = int(input("Please enter in your amount of gold: "))
pidgin = NPC(pidgin_model)
pidgin.conversion(player)