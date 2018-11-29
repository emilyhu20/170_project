import os
avg = 0
total = 0
#inputs = [1000, 1009]
#for i in inputs:
for i in range(111, 221):
	# if i in [139, 178, 162, 153, 142, 188]:
	#  	continue
	print(i)
	os.system("python3 output_scorer.py ../all_inputs/medium/" + str(i) + " ../outputs/medium2/" + str(i) + ".out")
	#os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " old_small/" + str(i) + ".out")