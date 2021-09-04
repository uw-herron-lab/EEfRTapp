import random
import tkinter as tk
import time
from tkinter import ttk
from tkinter import font as tkFont
import PracticeIntro
import StartEndPage
import TimedIntro


def reward_generator(master):
    global current_reward
    current_reward = random.uniform(1.24, 4.30).__round__(2)
    master.record_data(current_reward)
    return current_reward

def probability_generator(master):
    global probability_to_win
    probability_to_win = random.choice(master.get_probability())
    master.record_data(probability_to_win)
    return probability_to_win

global task_level

global complete_status

global winning_status

global start_time

global start_collect

global trial_number

class TrialCue(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        subFrame = tk.Frame(master=self)
        subFrame.pack()

        global trial_number
        trial_number += 1

        master.new_data()
        master.record_data(trial_number)

        lbl = tk.Label(subFrame,
                       text= " + ",
                       font=tkFont.Font(size=50, weight = "bold"))
        lbl.grid(row=0, column=0)

        self.after(500, lambda: master.switch_frame(TrialChoose))

class TrialChoose(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        subFrame = tk.Frame(master=self)
        subFrame.pack()

        lbl = tk.Label(subFrame,
                       text="Choose Your Task",
                       font=tkFont.Font(size=25))
        lbl.grid(row=0, column=1)
        lbl2 = tk.Label(subFrame,
                        text=f"probability of win: {probability_generator(master)}%", font=tkFont.Font(size=15))

        lbl2.grid(row=1, column=1)

        s = ttk.Style()
        s.configure('my.TButton', font=(15))
        btn_to_EasyTask = ttk.Button(subFrame,
                                     text= "Easy Task \n $1.00 ", style = 'my.TButton',
                                     command=lambda: self.swtich_to_EasyTask(master))
        btn_to_EasyTask.grid(row=2, column=0)

        btn_to_HardTask = ttk.Button(subFrame,
                                     text=f"Hard Task \n ${reward_generator(master)} ", style='my.TButton',
                                     command=lambda: self.swtich_to_HardTask(master))
        btn_to_HardTask.grid(row=2, column=2)

        master.set_frame_switch_status(False)
        self.after(4500, lambda: self.switch_to_Task(master))

    def switch_to_Task(self, master):
        if master.get_frame_swtich_status() is False:
            global task_level
            task_level = random.randint(0, 1)
            master.record_data(task_level)
            self.after(0, lambda: master.switch_frame(Task))

    def swtich_to_EasyTask(self, master):
        global task_level
        task_level = 0
        master.set_frame_switch_status(True)
        master.record_data(task_level)
        self.after(0, lambda: master.switch_frame(Task))

    def swtich_to_HardTask(self, master):
        global task_level
        task_level = 1
        master.set_frame_switch_status(True)
        master.record_data(task_level)
        self.after(0, lambda: master.switch_frame(Task))


class Task(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        maximum_level = 30
        maximum_time = 6500

        global task_level
        global current_reward

        if task_level == 0:
            current_reward = 1
            maximum_level = 30
            maximum_time = 6500
        elif task_level == 1:
            maximum_level = 100
            maximum_time = 20500


        global indicator
        indicator = tk.IntVar(value = 0)

        subFrame = tk.Frame(master=self)
        subFrame.pack()

        progress = ttk.Progressbar(subFrame,
                                   orient = tk.VERTICAL, length = 500, maximum = maximum_level + 1,
                                   mode = 'determinate',
                                   variable = indicator)
        progress.grid(row = 0, column = 0)


        def progress_increase(event):
            if indicator.get() == maximum_level:
                global complete_status
                complete_status = True
                self.after(0, lambda: master.switch_frame(CompleteStatusPage))
                master.unbind("<space>", increase_progress)
            else:
                progress.step(1)

        global increase_progress
        increase_progress = master.bind("<space>", progress_increase)

        master.set_frame_switch_status(False)
        self.after(maximum_time, lambda: self.switch_to_FailPage(master))


    def switch_to_FailPage(self, master):
        if master.get_frame_swtich_status() is False:
            global complete_status
            complete_status = False
            self.after(0, lambda: master.switch_frame(CompleteStatusPage))
            master.unbind("<space>", increase_progress)

class CompleteStatusPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        subFrame = tk.Frame(master=self)
        subFrame.pack()

        master.record_data(complete_status)

        lbl = tk.Label(subFrame,
                       text = f"You {self.status_to_string()} the task!", font = tkFont.Font(size=25))
        lbl.grid(row = 0, column = 0)

        if complete_status is True:
            if random.randint(0, 100) <= probability_to_win:
                global  winning_status
                winning_status = True
            else:
                winning_status = False
        elif complete_status is False:
            winning_status = False

        self.after(1500, lambda: master.switch_frame(WinningStatusPage))


    def status_to_string(self):
        global complete_status
        if complete_status is True:
            status_in_string = "completed"
        else:
            status_in_string = "failed"
        return status_in_string

class WinningStatusPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        subFrame = tk.Frame(master=self)
        subFrame.pack()

        master.record_data(winning_status)
        master.data_merge()

        global status_in_string
        status_in_string = tk.StringVar()

        lbl = tk.Label(subFrame,
                       text= f"{self.status_to_string()}", font=tkFont.Font(size=25))
        lbl.grid(row=0, column=0)

        if PracticeIntro.number_of_practice < master.get_maximum_practice():
            self.after(1500, lambda: master.switch_frame(PracticeIntro.PracticeTrial))
        elif PracticeIntro.number_of_practice == master.get_maximum_practice():
            PracticeIntro.number_of_practice += 1
            self.after(1500, lambda: master.switch_frame(TimedIntro.TimedTrialIntro))
        elif master.get_current_time() - start_time > master.get_maximum_time():
            self.after(1500, lambda: master.switch_frame(StartEndPage.EndPage))
        else:
            self.after(1500, lambda: master.switch_frame(TrialCue))

    def status_to_string(self):
        global status_in_string
        if winning_status is True:
            status_in_string = f"You won ${current_reward}!"
        else:
            status_in_string = "You did not win this trial"
        return status_in_string









