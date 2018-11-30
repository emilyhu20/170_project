import os
avg = 0
total = 0
<<<<<<< HEAD
inputs = [18]
#inputs = [1, 6, 7, 9, 11] #, 12, 13, 18, 19, 20, 24, 26, 27, 29, 32, 34, 35, 36, 37, 42, 43, 44, 46, 47, 48, 49, 51, 52, 53, 56, 67, 68, 69, 71,73, 74, 76, 77, 81, 83, 84, 87, 88, 89, 90, 94, 95, 104, 108, 110]
#inputs = [1, 3, 6, 7, 9, 11, 12, 13, 18, 20, 21, 24, 26, 27, 29, 30, 32, 34, 36, 37, 38, 40, 41, 43, 43, 45, 46, 47, 48, 49, 51, 52, 53, 54, 56, 59, 62, 63, 65, 67, 68, 69, 70, 71, 73, 74, 76, 77, 78, 81, 84, 83, 87, 88, 89, 90, 91, 95, 97, 100, 101, 102, 104, 105, 107, 108, 109, 110]
for i in inputs:
#for i in range(1000, 1034):
	# if i in [106, 80, 39, 22]:
	#  	continue
	print(i)
	os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " new_small/" + str(i) + ".out")
	os.system("python3 output_scorer.py ../all_inputs/small/" + str(i) + " bitbucket/" + str(i) + ".out")
=======
#inputs = [1000, 1009]
#for i in inputs:
for i in range(221, 332):
	# if i in [139, 178, 162, 153, 142, 188]:
	#  	continue
	print(i)
	os.system("python3 output_scorer.py ../all_inputs/medium/" + str(i) + " medium_final/" + str(i) + ".out")
	os.system("python3 output_scorer.py ../all_inputs/medium/" + str(i) + " temp_medium/" + str(i) + ".out")
>>>>>>> 45701050228d56852a8ef78afe80c573290fbf7e
