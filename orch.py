import sys
import json
import shlex

def prepend_boilerplate(f):
	f.write("import subprocess\n\n")
	f.write("def main():\n")

def append_boilerplate(f):
	f.write("if __name__ == \"__main__\":\n")
	f.write("\tmain()")

def add_block(f, block):
	# TODO: Add some checks, e.g. that script is a single word
	args = shlex.split(block['arg_string'])
	args.insert(0, block['script'])
	print(args)
	
	subproc_str = "\tsubprocess.call(["
	for arg in args:
		subproc_str += "\"" + arg + "\", "
	subproc_str = subproc_str[:-2]	# Remove trailing comma and space
	subproc_str += "])\n\n"
	f.write(subproc_str)
	outfile.close()

def main(wf_file, output_filename):
	outfile = open(output_filename, 'w')
	prepend_boilerplate(outfile)

	with open(wf_file) as workflow_data:
		workflow = json.loads(workflow_data.read())

	for block in workflow['blocks']:
		add_block(outfile, block)
		print('id: ' + str(block['id']))
		print('script: ' + block['script'])
		print('arg_string: ' + block['arg_string'])

	append_boilerplate(outfile)
	outfile.close()

if __name__ == "__main__":
	main(sys.argv[1], 'outfile.py')
