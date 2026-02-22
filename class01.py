user_input = input("Enter some text to write to the file: ")
with open('example.txt', 'w') as f:
    f.write(user_input + '\n')
    f.write('This is an example file.\n')

example_file = open('example.txt', 'r')

example_file.close()
with open('example.txt', 'r') as file:
    content = file.read()
    with open('example.txt', 'a') as file:
        file.write(user_input + '\n')
    print(content)

with open('example.txt', 'r') as file:
    all_content = file.read()
    print("Using read():")
    print(all_content)

with open('example.txt', 'r') as file:
    print("Using readline():")
    first_line = file.readline()
    print(first_line.strip())
    file.seek(0)
    second_line = file.readline()
    print(second_line.strip())