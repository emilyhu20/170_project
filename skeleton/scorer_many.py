import os
avg = 0
total = 0
for i in range(1, 22):
	print(i)
	os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " small/" + str(i) + ".out")
	os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " small2/" + str(i) + ".out")