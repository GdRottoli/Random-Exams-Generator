import errno
from tkinter import *
from tkinter import ttk

from tkinter import filedialog, simpledialog, messagebox
import yaml
import os
import generator

class Application():

    def __init__(self, master):

        self.master = master
        self._topFrame = Frame(self.master, borderwidth=1)
        self._topFrame.pack(fill=BOTH, expand=True)
        self._bottomFrame = Frame(self.master)
        self._bottomFrame.pack(side=BOTTOM, expand=True)

        self._buttonGenerate = Button(self._bottomFrame, text="Generate", command=self.__generation_event)
        self._buttonGenerate.pack(side=RIGHT)

        # Read info...the main strategy for now is read from config, save in config and execute from config, in order to
        # avoid problems...

        with open("config.yaml") as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

            student_number_frame = Frame(self._topFrame)
            student_number_frame.pack(fill=X)
            lb_student_number = Label(student_number_frame, text="Tests:", width=6)
            lb_student_number.pack(side=LEFT, padx=5, pady=5)
            self._entryStudentNumber = Entry(student_number_frame)
            self._entryStudentNumber.pack(fill=X, padx=5, expand=True)
            self._entryStudentNumber.insert(END, self.config["student_number"])

            subject_frame = Frame(self._topFrame)
            subject_frame.pack(fill=X)
            lb_subject = Label(subject_frame, text="Subject:", width=6)
            lb_subject.pack(side=LEFT, padx=5, pady=5)
            self._entrySubject = Entry(subject_frame)
            self._entrySubject.pack(fill=X, padx=5, expand=True)
            self._entrySubject.insert(END, self.config["subject"])

            topic_frame = Frame(self._topFrame)
            topic_frame.pack(fill=X)
            lb_topic = Label(topic_frame, text="Topic:", width=6)
            lb_topic.pack(side=LEFT, padx=5, pady=5)
            self._entryTopic = Entry(topic_frame)
            self._entryTopic.pack(fill=X, padx=5, expand=True)
            self._entryTopic.insert(END, self.config["topic"])

            date_Frame = Frame(self._topFrame)
            date_Frame.pack(fill=X)
            lb_date = Label(date_Frame, text="Date:", width=6)
            lb_date.pack(side=LEFT, padx=5, pady=5)
            self._entryDate = Entry(date_Frame)
            self._entryDate.pack(fill=X, padx=5, expand=True)
            self._entryDate.insert(END, self.config["date"])

            bases_title_frame = Frame(self._topFrame)
            bases_title_frame.pack(fill=X)
            self._lbBases = Label(bases_title_frame, text="Problems Bases:", width=15)
            self._lbBases.pack(side=LEFT, padx=5, pady=5)

            bases_content_frame = Frame(self._topFrame)
            bases_content_frame.pack(fill=X)
            self._listBases = Listbox(bases_content_frame)
            self._listBases.pack(fill=X, padx=5, pady=5)
            self.__updateList()

        list_buttons_frame = Frame(self._topFrame)
        list_buttons_frame.pack(fill=X)
        bt_add_base = Button(list_buttons_frame, text="Add", command=self.__add_new_base)
        bt_remove_base = Button(list_buttons_frame, text="Remove", command=self.__remove_base)
        bt_remove_base.pack(side=RIGHT, padx=5, pady=5)
        bt_add_base.pack(side=RIGHT)

        root.mainloop()

    def __updateList(self):
        self._listBases.delete(0, END)
        bases = self.config["question_bases"]
        questions_per_file = self.config["questions_per_file"]
        for i in range(len(bases)):
            self._listBases.insert(END, "%s (%s)" % (bases[i], questions_per_file[i]))

    def __generation_event(self):
        if len(self.config["question_bases"]) == 0:
            messagebox.showerror("Error", "You must select at least one question base")
        else:
            try:
                self.config["student_number"] = int(self._entryStudentNumber.get())
                self.config["date"] = self._entryDate.get()
                self.config["subject"] = self._entrySubject.get()
                self.config["topic"] = self._entryTopic.get()
                self.__save_config()
                generator.file_generation()
            except ValueError:
                messagebox.showerror("Error", "Tests must be a number")


    def __add_new_base(self):
        my_filetypes = [('all files', '.*'), ('text files', '.tex')]
        path = filedialog.askopenfilename(parent=self.master,
                                            initialdir=os.getcwd(),
                                            title="Please select a file:",
                                            filetypes=my_filetypes)
        answer = simpledialog.askstring("Input", "Number of problems from this base?",
                                                parent=self.master)
        self.config["question_bases"].append(path)
        self.config["questions_per_file"].append(int(answer))
        self.__updateList()

    def __remove_base(self):
        try:
            selection = self._listBases.curselection()[0]
            del self.config["question_bases"][selection]
            del self.config["questions_per_file"][selection]
            self.__updateList()
        except IndexError:
            pass

    def __save_config(self):
        with open("config.yaml", 'w') as config_file:
            yaml.dump(self.config, config_file)


if __name__ == '__main__':
    root = Tk()
    root.title("Random Test Generator")
    root.geometry("600x400")
    app = Application(root)
    root.mainloop()