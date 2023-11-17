import re

def remove_newlines_within_quotes(line):
    fields = re.split('(".*?")', line)
    for i, field in enumerate(fields):
        if field.startswith('"') and field.endswith('"'):
            fields[i] = field.replace('\n', ' ')
    return ''.join(fields)

input_file_path = 'rimi_cleaned.csv'
output_file_path = 'rimi_cleaned_nice.csv'

with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    in_quotes = False
    buffer_line = ''
    for line in infile:
        buffer_line += line
        in_quotes = buffer_line.count('"') % 2 != 0
        if not in_quotes:
            fixed_line = remove_newlines_within_quotes(buffer_line)
            outfile.write(fixed_line)
            buffer_line = ''
