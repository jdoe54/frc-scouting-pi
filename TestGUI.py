import tkinter as tk
root = tk.Tk()
root.title("Test")

def exitProgram():
	root.quit()



label1= tk.Label(root, text="Scout 1")
label1.pack()


exitButton=tk.Button(root, text='Exit', command=exitProgram, height=1, width=24)
exitButton.pack()

root.mainloop()
