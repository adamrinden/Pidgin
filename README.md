# Pidgin

## Description
Pidgin is a Domain-Specific Language that streamlines player to NPC dialogue creation in Role-playing games.

## Files
- `pidgin.py`: Is the Python interpreter.
- `pidgin.tx`: Is the textX grammar rules.
- `dialogue.pdg`: Is an example program.

## Prerequisites
To run this program you'll need to setup a Python 3 virtual enviroment and install [textX](https://textx.github.io/textX/index.html).

## Running
In `pidgin.py` change `your_dialogue_file_here.pdg` to your own dialogue file.  
`pidgin_model = pidgin_mm.model_from_file("your_dialogue_file_here.pdg")
`
```
$ python3 pidgin.py
```

## Implementation
For this language I utilized textX to assist in creating the syntax and semantics of the language.

## Keywords
- `npc` Declare npc.
- `name` Define npc name.
- `entry` Initial dialogue block.
- `dialogue` Defines a dialogue block with a unique ID.
- `say` What the npc says to the player.
- `choice` A block that defines a choice on dialogue to the player
- `continue` Defines what dialogue block is next.
- `if, else` Handles standard conditionals for choice blocks.
- `update` Used to update game variables, like player gold. 
## Example Program
```
npc {
	name "Dominic"
	entry intro

	dialogue intro {
		say "Welcome to class, player.name!"
		continue initialChoices
	}

	dialogue initialChoices {
		say "Tell me player.name, what is an int?"
		choice "A variable type that represents a whole number." {
			continue pass_int
		}
		choice "It is shorthand for interrupt."{
			continue fail_int
		}
	}

	dialogue pass_int {
		say "Correct, A for the day!"
	}

	dialogue fail_int {
		say "Wrong, try again!"
		continue initialChoices
	}
}
```
## Example Output
```
$ python3 pidgin.py           
Please enter your name: Adam
Dominic:
Welcome to class, Adam!
Dominic:
Tell me Adam, what is an int?
1. A variable type that represents a whole number.
2. It is shorthand for interrupt.
Choose an option: 2
Dominic:
Wrong, try again!
Dominic:
Tell me Adam, what is an int?
1. A variable type that represents a whole number.
2. It is shorthand for interrupt.
Choose an option: 1
Dominic:
Correct, A for the day!
```
## Contact Information
- **Name:** Adam Rinden
- **Email:** arinden4688@sdsu.edu
