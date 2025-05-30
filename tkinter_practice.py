import tkinter as tk

def submit_text():
    user_input = input_box.get()
    output_label.config(text="You entered: " + str(user_input))

def submit_text2():
    user_input = input_box2.get()
    output_label2.config(text="You entered: " + str(user_input))

def calc():
    user_input = float(input_box.get())
    user_input2 = float(input_box2.get())
    calc_out.config(text = str(user_input+user_input2))


    
window = tk.Tk()
window.title("Text Input and Output")

input_label = tk.Label(window, text="Enter text:")
input_label.pack()

input_box = tk.Entry()
input_box.pack()

submit_button = tk.Button(window, text="Submit", command=submit_text)
submit_button.pack()

input_label2 = tk.Label(window, text="Enter text:")
input_label2.pack()

input_box2 = tk.Entry()
input_box2.pack()

submit_button2 = tk.Button(window, text="Submit", command=submit_text2)
submit_button2.pack()

calc_button = tk.Button(window, text="Calculation:", command=calc)
calc_button.pack()

output_label = tk.Label(window, text="")
output_label.pack()

output_label2 = tk.Label(window, text="")
output_label2.pack()

calc_out = tk.Label(window, text="")
calc_out.pack()



window.mainloop()


