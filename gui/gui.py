from Tkinter import *
import ttk
import json

# Dict: {'script', 'arg_string', 'outputs', box_bounds}

# Click, no box under mouse, create box.
# Click, box under mouse:
#	If drag, then move the box
#	If click then click another box, connect the boxes

cur_box = -1
num_boxes = -1
boxes = []
script_tb = None
arg_tb = None
outputs_tb = None

def assemble():
	global script, arg_string, outputs, cur_box, boxes

	if cur_box < 0:
		print("No boxes")
	else:
		# Update current box's values before building json
		boxes[cur_box]['script'] = script_tb.get()
		boxes[cur_box]['arg_string'] = arg_tb.get()
		boxes[cur_box]['outputs'] = outputs_tb.get()

		# Build workflow json output
		blocks = []
		for box in boxes:
			block = {'id': box['box_id'], 'script': box['script'], 'arg_string': box['arg_string'], 'outputs': box['outputs'].split()}
			blocks.append(block)
		wf_dict = {'blocks': blocks}
		print(json.dumps(wf_dict))

def canvas_clicked(click):
	global cur_box, num_boxes, boxes, script_tb, arg_tb, outputs_tb
	# For now, just assume it was a click for new box

	# We're either focusing to a different box, or placing a new box.  Either way,
	# current cur_box is no longer going to be cur_box.
	# Eventually, this might change (e.g. if there's a 'place' mode vs 'connect' mode
	if cur_box >= 0:
		boxes[cur_box]['script'] = script_tb.get()
		boxes[cur_box]['arg_string'] = arg_tb.get()
		boxes[cur_box]['outputs'] = outputs_tb.get()
		click.widget.itemconfig(boxes[cur_box]['box_id'], outline="white")

	under_mouse = click.widget.find_overlapping(click.x, click.y, click.x, click.y)
	if len(under_mouse) > 0:
		# TODO: For now, just focus on the first one. Should focus on top one.
		cur_box = under_mouse[0]-1	# Subtract one b/c tkinter starts index at 1, our boxes list starts at 0
		script_tb.delete(0, END)
		arg_tb.delete(0, END)
		outputs_tb.delete(0, END)
		script_tb.insert(0, boxes[cur_box]['script'])
		arg_tb.insert(0, boxes[cur_box]['arg_string'])
		outputs_tb.insert(0, boxes[cur_box]['outputs'])
		click.widget.itemconfig(boxes[cur_box]['box_id'], outline="black")
	else:
		new_box_id = click.widget.create_rectangle(click.x, click.y, click.x+50, click.y+50, fill="red", outline="black")
		num_boxes += 1
		cur_box = num_boxes
		boxes.append({'script': '', 'arg_string': '', 'outputs': '', 'box_id': new_box_id})
		script_tb.config(state=NORMAL)
		arg_tb.config(state=NORMAL)
		outputs_tb.config(state=NORMAL)
		script_tb.delete(0, END)
		arg_tb.delete(0, END)
		outputs_tb.delete(0, END)

def main():
	global script_tb, arg_tb, outputs_tb

	root = Tk()
	root.title("Testing")
	root.grid_columnconfigure(0, weight=1)
	root.grid_rowconfigure(0, weight=1)

	root_frame = ttk.Panedwindow(root, orient=VERTICAL)
	root_frame.grid(column=0, row=0, sticky=(N, W, E, S))

	wf_canvas = Canvas(root_frame, background="white")
	wf_canvas.pack(side="top", fill=BOTH, expand=1)
	wf_canvas.bind("<Button-1>", canvas_clicked)
	
	def_frame = ttk.Labelframe(root_frame, padding="3 3 3 3", text="Definitions")
	def_frame.pack(side="bottom", fill="x")

	root_frame.add(wf_canvas)
	root_frame.add(def_frame)

	ttk.Label(def_frame, text="Script (provide full path)").grid(column=0, row=0, sticky=(W, E, S))
	script_tb = ttk.Entry(def_frame, width=50)
	script_tb.grid(column=1, row=0, sticky=(W, E))

	ttk.Label(def_frame, text="Argument string (prepend variables with a dollar sign)").grid(column=0, row=1, sticky=(W, E, S))
	arg_tb = ttk.Entry(def_frame, width=50)
	arg_tb.grid(column=1, row=1, sticky=(W, E))

	ttk.Label(def_frame, text="Output names (separate names with a space)").grid(column=0, row=2, sticky=(W, E, S))
	outputs_tb = ttk.Entry(def_frame, width=50)
	outputs_tb.grid(column=1, row=2, sticky=(W, E))

	Button(def_frame, text="Compile", command=assemble).grid(column=0, row=3, sticky=(W, E, S))

	# Disable until a box is selected
	script_tb.config(state=DISABLED)
	arg_tb.config(state=DISABLED)
	outputs_tb.config(state=DISABLED)

	for child in def_frame.winfo_children(): child.grid_configure(padx=5, pady=5)

	root.mainloop()

if __name__ == "__main__":
	main()
