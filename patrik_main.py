import os 
name = os.path.basename(__file__)

info = name.split("_")

print("Aha! Your name is " + info[0])
def choose(times):
	c = int(input("Choose 1 or 2: "))
	if c == 1:
		print((name + "\n")*10)
		return
	elif c == 2:
		if times > 1:
			print("IT TOOK YOU " + str(times) + " ATTEMPTS TO CLOSE THIS???")
		print("Cya D:")
		return
	else:
		print("Try again ;-;")
		choose(times + 1)

choose(1)

input()