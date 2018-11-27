import os
avg = 0
total = 0
for i in range(1, 111):
	if i == 22 or i == 36:
		continue
	os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " small/" + str(i) + ".out")