import os
avg = 0
total = 0
#inputs = [1000, 1009]
#for i in inputs:
for i in range(221, 332):
	# if i in [139, 178, 162, 153, 142, 188]:
	#  	continue
	print(i)
	os.system("python3 output_scorer.py ../all_inputs/medium/" + str(i) + " medium_final/" + str(i) + ".out")
	os.system("python3 output_scorer.py ../all_inputs/medium/" + str(i) + " temp_medium/" + str(i) + ".out")