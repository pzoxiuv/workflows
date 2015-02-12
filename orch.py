import sys
import json
import shlex

def prepend_boilerplate(f):
	f.write("import subprocess\n\n")
	f.write("def main():\n")

def append_boilerplate(f):
	f.write("\nif __name__ == \"__main__\":\n")
	f.write("\tmain()")

def add_block(outfile, block, num_tabs):
	# TODO: Add some checks, e.g. that script is a single word
	args = shlex.split(block['arg_string'])
	args.insert(0, block['script'])
	#print(args)
	
	tabs= "\t"	# Starts with at least one tab because they're called from a method, newline for readability
	for x in range(0, num_tabs):
		tabs += "\t"

	subproc_str = "\n" +tabs + "output = subprocess.check_output(["
	for arg in args:
		subproc_str += "\"" + arg + "\", "
	subproc_str = subproc_str[:-2]	# Remove trailing comma and space
	subproc_str += "])\n"
	outfile.write(subproc_str)

	outfile.write(tabs + "print(output)\n")

	outfile.write(tabs + "split_output = output.split(\" \")\n")
	output_num = 0
	for output in block['outputs']:
		outfile.write(tabs + output + " = split_output[" + str(output_num) + "]\n")
		output_num += 1

def add_cond(outfile, cond, num_tabs):
	cond_str = "\n\t"	# Starts with at least one tab because they're called from a method, newline for readability
	for x in range(0, num_tabs):
		cond_str += "\t"
	cond_str += cond + "\n"

	outfile.write(cond_str)

def parse_control(outfile, control_file_data, blocks):
	for line in control_file_data:
		# XXX: Need to account for tabs on right side?  That'll mess this up
		num_tabs = line.count('\t')
		line = line.strip()
		if line[0] == 'b':
			add_block(outfile, blocks[int(line[1:])-1], num_tabs)
		else:
			add_cond(outfile, line, num_tabs)

def main(wf_file, control_file, output_filename):
	outfile = open(output_filename, 'w')
	prepend_boilerplate(outfile)

	with open(wf_file) as workflow_data:
		workflow = json.loads(workflow_data.read())

	#for block in workflow['blocks']:
	#	add_block(outfile, block)
	#	print('id: ' + str(block['id']))
	#	print('script: ' + block['script'])
	#	print('arg_string: ' + block['arg_string'])

	with open(control_file) as control_file_data:
		parse_control(outfile, control_file_data, workflow['blocks'])

	append_boilerplate(outfile)
	outfile.close()

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], 'outfile.py')
