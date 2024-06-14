import analyze

input_arg = '--i'
input_path = r"C:\Users\Nazrul\Documents\bfg_hackathon\birdnet\train_data\Ardea purpurea_Purple Heron\PurpleHeron_2.mp3"
output_arg = '--o'
output_path = r"C:\Users\Nazrul\Documents\bfg_hackathon\koel-backend\koel_backend\PurpleHeron_21.csv"
output_file_arg = '--rtype'
output_file_type = 'csv' 

# Call analyze.main with corrected paths
analyze.main([input_arg, input_path, output_arg, output_path, output_file_arg, output_file_type])


# import os
# import sys

# print(os.path.dirname(os.path.abspath(sys.argv[0])))