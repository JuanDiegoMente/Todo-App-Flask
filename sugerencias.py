import random

def create_sugerencia_username(default: str) -> str :
	string_ = "qwertyuiopasdfghjklzxcvbnm<>1234567890[]:_;:-.,+"

	newName = default
	if len(default) >= 14:
		return newName + str(random.randint(10, 99))

	elif len(default) >= 1:
		for i in range(5):
			newName+=string_[random.randint(0, len(string_)-1)]
			print(newName)

		return newName

