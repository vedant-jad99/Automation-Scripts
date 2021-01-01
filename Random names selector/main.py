#!/usr/bin/env python3

import os
import tkinter as tk
from random import randint
from bs4 import BeautifulSoup as bs
import webbrowser

UNSELECT = "unselected.txt"
SELECT = "select.txt"

HTML = '''<!DOCTYPE html>
<html lang="en">

<head>
    <title>
        Activity Report
    </title>
    <link rel="stylesheet" href="tabledesign.css">
    <meta charset="UTF-8">
</head>

<body>
    <div id="title">
        <img src="images/score.jpeg" id="image">
    </div>
    <table id="activityReport">
        <thead>
            <tr>
                <th id="name">Name</th>
                <th id="score">Score</th>
            </tr>
        </thead>
        <tbody id="tableBody">
        </tbody>
    </table>

    <script type="module" src="scripts/activity.js"></script>
</body>

</html>'''

class random_selector:
    def __init__(self, re_list):
        file_list = os.listdir()
        if UNSELECT not in file_list and SELECT not in file_list:
            with open(UNSELECT, 'w+') as f:
                for i in re_list[:-1]:
                    f.write(i + "\n")
                f.write(re_list[-1])
                f.close()
            with open(SELECT, 'w') as f:
                f.close()

        self.score_dict = {}
    
    def random_name(self):
        names = []
        with open(UNSELECT, 'r') as f:
            for name in f:
                names.append(name)
        
        if names == []:
            return None, None
        i = randint(0, len(names) - 1)
        select = names.pop(i)
        with open(SELECT, 'a') as f:
            f.write(select)
            f.close()
        with open(UNSELECT, 'w') as f:
            for i in names[:-1]:
                f.write(i)
            try:
                f.write(names[-1])
            except IndexError:
                pass
            f.close()
        return select, names

    def increase_one_point(self, label):
        name = label.cget("text")
        if name in self.score_dict:
            self.score_dict[name] += 1
        else:
            self.score_dict[name] = 1

    def add_5_points(self, label):
        name = label.cget("text")
        if name in self.score_dict:
            self.score_dict[name] += 4
        else:
            self.score_dict[name] = 4 


class UI:
    def __init__(self, root, re_list):
        selector = random_selector(re_list)
        self.frame = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        self.frame3 = tk.Frame(root, width=50)
        
        self.text = tk.Label(self.frame, text="", relief=tk.GROOVE, borderwidth=5, height=13, width=10)
        self.shuffle = tk.Button(self.frame, text="SHUFFLE", width=6, relief=tk.RAISED, borderwidth=5, command=lambda: self.__on_shuffle__(selector))
        self.reset = tk.Button(self.frame, text="AGAIN", width=6, relief=tk.RAISED, borderwidth=5, command=lambda: self.__on_reset__(selector, re_list, True))
        self.scoreboard = tk.Button(self.frame, text="SCORE", width=6, relief=tk.RAISED, borderwidth=5, command=lambda: self.showHTML(selector))
        self.zero_score = tk.Button(self.frame, text="RESET", width=6, relief=tk.RAISED, borderwidth=5, command=lambda: self.__on_reset__(selector, re_list))
        self.name = tk.Label(self.frame2, text="", width=55, height=20, relief=tk.GROOVE, borderwidth=5)
        
        self.list = [tk.Label(self.frame3, text=i, width=10, relief=tk.GROOVE, borderwidth=5, bg="white") for i in re_list]
        self.__set_name_on_label__(re_list)

        self.shuffle.grid(row=1, column=0, padx=2, pady=5)
        self.reset.grid(row=2, column=0, padx=2, pady=5)
        self.scoreboard.grid(row=3, column=0, padx=2, pady=5)
        self.zero_score.grid(row=4, column=0, padx=2, pady=5)
        self.text.grid(row=0, column=0, padx=2)
        self.name.grid(row=0, column=0)
        
        for count, i in enumerate(self.list):
            if count > len(self.list)/2:
                i.grid(row=1, column=int(abs(len(self.list)/2 - count)), padx=2, pady=2)
            else:
                i.grid(row=0, column=count)
        
        for i in self.list:
            i.bind('<Double-1>', lambda event, a=i: selector.add_5_points(a))
            i.bind('<Button-1>', lambda event, a=i: selector.increase_one_point(a))

        self.frame3.grid(row=1, column=1)
        self.frame2.grid(row=0, column=1)
        self.frame.grid(row=0, column=0)
    
    def __on_shuffle__(self, selector):
        name, names = selector.random_name()
        if name == None:
            self.name.config(text="No more names in the list")
            return
        self.text.config(height=16)
        self.name.config(text=name, font=44)
        self.__set_name_on_label__(names=names)
    
    def __on_reset__(self, selector, re_list, again=False):
        with open(UNSELECT, 'w+') as f:
            for i in re_list[:-1]:
                f.write(i + "\n")
            f.write(re_list[-1])
            f.close()
        with open(SELECT, 'w') as f:
             f.close()
        self.name.config(text="")
        self.__set_name_on_label__(re_list=re_list)
        if not again:
            selector.score_dict = {}


    def __set_name_on_label__(self, re_list=None, names=None):
        if names == None:
            string = ""
            for i in re_list[:-1]:
                string += i + "\n"
            string += re_list[-1]
            self.text.config(text=string)
        else:
            string = ""
            for i in names[:-1]:
                string += i
            try:
                string += names[-1]
            except IndexError:
                pass
            self.text.config(text=string)

    def showHTML(self, selector):
        html = bs(HTML, 'html.parser')
        body = html.find('tbody')
        for key, val in selector.score_dict.items():
            row = html.new_tag('tr')
            child1 = html.new_tag('td')
            child2 = html.new_tag('td')
            child1.string = key
            child2.string = str(val)
            row.append(child1)
            row.append(child2)
            body.append(row)
        
        with open('score.html', 'w') as f:
            f.write(str(html))
            f.close()
        webbrowser.open('score.html')
        


if __name__ == '__main__':
    reset_list = ['Abhishek', 'Aditi', 'Chandana', 'Mahesh', 'Rahul', 'Rutvik', 'Sarang', 'Shantanu', 'Sreehari', 'Tejaravind', 'Yashdeep']
    root = tk.Tk()
    UI(root, reset_list)
    root.mainloop()