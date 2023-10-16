from tkinter import *


class AutoCompleteSearchBar:

    def __init__(self, root, listeItems,row=0,col=0,entrySize=50):
        self.frame = Frame(root)
        self.frame.grid(row=row, column=col)

        # creating text box
        self.e = Entry(self.frame,width=entrySize)
        self.e.grid(row=row, column=col)

        # creating list box
        self.lb = Listbox(self.frame,height=int(entrySize/10),width=entrySize)
        self.lb.grid(row=row+1, column=col)

        self.sb = Scrollbar(self.frame, orient=VERTICAL)
        self.sb.grid(row=row+1, column=col,sticky="e")

        self.lb.configure(xscrollcommand=self.sb.set)
        self.sb.config(command=self.lb.xview)

        self.e.bind('<KeyRelease>', lambda event: self.checkkey(event, listeItems, self.lb))
        self.lb.bind("<<ListboxSelect>>", lambda event: self.updateInputOnClick(event, self.e))
        self.frame.bind("<Return>", self.search)

        self.update(listeItems, self.lb)
        print(self.frame.winfo_manager())

    # Function for checking the
    # key pressed and updating
    # the listbox
    def checkkey(self, event, autocompleteList, targetListBox):
        value = event.widget.get()

        # get data from l
        if value == '':
            data = autocompleteList
        else:
            data = []
            for item in autocompleteList:
                if value.lower() in item.lower():
                    data.append(item)

                    # update data in listbox
        self.update(data, targetListBox)

    def setInput(self, input, value):
        if value is not "":
            input.delete(0, END)
            input.insert(0, value)

    def getInput(self):
        return self.e.get()

    def updateInputOnClick(self, event, inputToUpdate):
        target = event.widget
        if target is not None:
            self.setInput(inputToUpdate, target.get(target.curselection()))

    def update(self, data, targetListBox):
        # clear previous data
        targetListBox.delete(0, 'end')

        # put new data
        for item in data:
            targetListBox.insert('end', item)
    def search(self):
        val = self.e.get()
        print("yeah!",val)
    # Driver code


"""
l = ('C', 'C++', 'Java',
     'Python', 'Perl',
     'PHP', 'ASP', 'JS',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP',
     'Python', 'Perl',
     'PHP', 'ASP')

root = Tk()
search = AutoCompleteSearchBar(root,l)
root.mainloop()
"""
