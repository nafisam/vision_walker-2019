import obstacle_detection

answer_file = open('answers.txt', 'r')
# First line of answers.txt is the number of tests.
test_count = int(answer_file.readline())
print(test_count)
answers = []

# Data from answers.txt is stored as an array of tuples.
# (boolean Answer, distance in mm)
for answer in xrange(0, test_count):
    hasObstacle, distance = answer_file.readline().split(' ')
    answers.append((hasObstacle, distance))

for test in xrange(0, test_count):
                result_string = ""
                result = obstacle_detection.detect_file("test" + str(test + 1) + '.txt', 2, 2500)
                print(result)

                # Detection returns -1 for no obstacle.
                if result != -1 and result <= 2500:
                    if answers[test][0] == 'True':
                        result_string = "Correct True"
                    elif answers[test][0] == 'False':
                        result_string = "Incorrect True"
                else:
                    if answers[test][0] == 'True':
                        result_string = "Incorrect False"
                    elif answers[test][0] == 'False':
                        result_string = "Correct False"

                print('{}.txt Expected: {} Measured: {} Result: {}\n'.format(
                    str(test + 1), answers[test][1], result, result_string))
