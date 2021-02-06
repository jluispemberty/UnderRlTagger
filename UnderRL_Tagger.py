# -*- coding: utf-8 -*-

import os
import codecs
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from nltk import word_tokenize

#This class creates a small window for the about info.
class AboutWindow(ttk.Frame):
    def __init__(self, About_Window):
        self.About_Window = About_Window
        self.About_Window.resizable(width=False,height=False)
        self.About_Window.iconbitmap(os.getcwd() + "\\UnderRL.ico")
        self.About_Window.columnconfigure(0, weight=1)
        self.About_Window.rowconfigure(0, weight=1)
         
        self.aboutInfo = tk.Text(About_Window, width=35, height=16)
        self.aboutInfo.grid(row=0, column=0, padx=5, pady=5)
        self.aboutInfo.insert(tk.INSERT, "UnderRL Tagger 1.0\n\nDeveloped by José Luis Pemberty\nSupported by María Isabel Marín &\nJorge Mauricio Molina\n\nCorpus Ex Machina research group\n\nUniversity of Antioquia, Colombia\n\njluispemberty@gmail.com\n\nFebruary 2020")
        self.aboutInfo.config(state="disabled")
        
#This class creates the window and packs the frames inside      
class Application(ttk.Frame):
    
    def __init__(self, main_window):
        global savedSesions
        
        super().__init__(main_window)
        main_window.title("UnderRL Tagger")
        main_window.resizable(width=False,height=False)
        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(0, weight=1)
        
        #Here are all the controls in the top toolbar
        self.topMenu = tk.Menu(self)
        
        self.fileMenu = tk.Menu(self.topMenu)
        self.fileMenu.add_command(label='New...', command=self.new)
        self.topMenu.add_cascade(label='File', menu=self.fileMenu, underline=0)
        
        self.helpMenu = tk.Menu(self.topMenu)
        self.helpMenu.add_command(label='About', command= lambda: self.new_window(AboutWindow))
        self.topMenu.add_cascade(label='Help', menu=self.helpMenu, underline=0)
        
        main_window.config(menu=self.topMenu)
        
        
        self.notebook = ttk.Notebook(self)
        
        #Here are all the controls in the Home Tab
        self.Home_Frame = ttk.Label(self.notebook)
        self.separInv = ttk.Separator(self.Home_Frame, orient=tk.HORIZONTAL).grid(row=0, column=0, padx=105, pady=15)
        
        self.separH0 = ttk.Separator(self.Home_Frame, orient=tk.HORIZONTAL).grid(row=1, column=1, sticky="wes", pady=15, padx=10, columnspan=2)
        self.recoverSesion = ttk.Label(self.Home_Frame, text="OPEN A PREVIUS SESION").grid(row=1, column=1, columnspan=2)
        self.InstructionsH1 = ttk.Label(self.Home_Frame, text="To open a previus work on UnderRL Tagger select it from the list below").grid(row=2, column=1)
        self.PreviusList = ttk.Combobox(self.Home_Frame, values= savedSesions, state="readonly")
        self.PreviusList.grid(row=3, column=1, pady=5, sticky="ew")
        self.PreviusList.current(0)
        self.recoverButton = ttk.Button(self.Home_Frame, text= "Open", command=self.load).grid(row= 3, column= 2)
        
        self.separH1 = ttk.Separator(self.Home_Frame, orient=tk.HORIZONTAL).grid(row=5, column=1, sticky="wes", pady=25, padx=10, columnspan=2)
        
        self.labelCorpusSearch = ttk.Label(self.Home_Frame, text="START NEW PROJECT").grid(row=5, column=1, columnspan=2)
        
        self.InstructionsH1 = ttk.Label(self.Home_Frame, text="CORPUS DIRECTORY: Paste the corpus directory on the bar below or search it using the button\n                                       Then introduce a name on the text box to identify this new project").grid(row=6, column=1)
        self.CorpusDirectory = ttk.Entry(self.Home_Frame)
        self.CorpusDirectory.grid(row=7, column=1, sticky="we")
        self.ProjectName = ttk.Entry(self.Home_Frame)
        self.ProjectName.grid(row= 8, column= 1, sticky= "we")
        self.ProjectName.insert(0, "Project name")
       
        self.SearchButton= ttk.Button(self.Home_Frame, text="...", command=self.browseDir).grid(row=7, column=2)
        
        self.separH2 = ttk.Separator(self.Home_Frame, orient=tk.HORIZONTAL).grid(row=9, column=1, sticky="we", pady=15, padx=10, columnspan=2)
        
        self.InstructionsH2 = ttk.Label(self.Home_Frame, text="If you already have a dictionary file, insert the direction below, otherwise leave this box empty").grid(row=10, column=1)
        self.labelDictionaryFile = ttk.Label(self.Home_Frame, text="DICTIONARY FILE").grid(row=9, column=1, columnspan=2)
        
        self.DictionaryFile = ttk.Entry(self.Home_Frame)
        self.DictionaryFile.grid(row=11, column=1, sticky="we")
        self.SearchDictButton= ttk.Button(self.Home_Frame, text="...", command=self.browseDic).grid(row=11, column=2, padx=5)
        
        self.StartButton = ttk.Button(self.Home_Frame, text="Start Tagging", command=self.Start).grid(row=12, column= 1, pady=5, columnspan=2)
        self.notebook.add(self.Home_Frame, text="Home", padding=10)
        
        
        #Here are all the controls in the Tagging Tab
        self.Tag_Frame = ttk.Label(self.notebook)
        
        self.separ0 = ttk.Separator(self.Tag_Frame, orient=tk.HORIZONTAL).grid(row=0, column=0, columnspan=3, sticky="we", pady=15, padx=10)
        self.separ1 = ttk.Separator(self.Tag_Frame, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=12, sticky="ns", pady=20, padx=15)
        
        self.labelCorpus = ttk.Label(self.Tag_Frame, text="CORPUS")
        self.labelCorpus.grid(row=0, column=0, columnspan=3)
        
        self.labelTextSelect = ttk.Label(self.Tag_Frame, text="Current Text:\nCurrent Token:")
        self.labelTextSelect.grid(row=0, column=4)
        
        self.statusVar = tk.StringVar()
        self.statusVar.set("")
        self.labelStatus = ttk.Label(self.Tag_Frame, textvariable=self.statusVar)
        self.labelStatus.grid(row=0, column=5, columnspan=2, sticky="w")
        
        
        self.separ2 = ttk.Separator(self.Tag_Frame, orient=tk.HORIZONTAL).grid(row=1, column=4, columnspan=4, sticky="we", pady=15, padx=10)
        
        self.Instructions1 = ttk.Label(self.Tag_Frame, text="Select a text from the list below")
        self.Instructions1.grid(row=1, column=0)
        
        self.LabelToken = ttk.Label(self.Tag_Frame, text="TOKEN")
        self.LabelToken.grid(row=1, column=4, columnspan=4, pady= 15)
        
        self.Instuction2 = ttk.Label(self.Tag_Frame, text="If you want to tag more than one token, select the number using the buttons on the right")
        self.Instuction2.grid(row=2, column=4, columnspan=4)
        
        scrollbar = ttk.Scrollbar(self.Tag_Frame, orient=tk.VERTICAL)
        self.TextsList = tk.Listbox(self.Tag_Frame, yscrollcommand=scrollbar.set)
        self.TextsList.grid(row=2, column=0, rowspan=10, sticky="ewns", pady=10)
        scrollbar.config(command=self.TextsList.yview)
        scrollbar.grid(row=2, column=1, rowspan=10, sticky="ns", pady=10)  
        
        
        self.SelectButton = ttk.Button(self.Tag_Frame, text='Select \n  text', command=self.selectText).grid(row=2, column=2, rowspan=10)
        
        self.context1Var = tk.StringVar()
        self.context1Var.set("")
        self.Context1 = ttk.Label(self.Tag_Frame, textvariable=self.context1Var).grid(row=3, column=4, columnspan=4, sticky="sw")
        
        self.context2Var = tk.StringVar()
        self.context2Var.set("")
        self.Context2 = ttk.Label(self.Tag_Frame, textvariable=self.context2Var).grid(row=5, column=4, columnspan=4, sticky="nw")
        
        self.tokenVar = tk.StringVar()
        self.tokenVar.set("")
        self.CurrentToken = ttk.Entry(self.Tag_Frame, textvariable=self.tokenVar)
        self.CurrentToken.grid(row=4, column=4, columnspan=4, sticky="we")
        self.CurrentToken.config(font=("Arial",14))
        self.CurrentToken.config(state="readonly")
        
        self.PlusButton = ttk.Button(self.Tag_Frame, text='+', width=1, command=self.plusNumber).grid(row=3, column=8, padx=5)
        self.MinusButton = ttk.Button(self.Tag_Frame, text='-', width=1, command=self.minusNumber).grid(row=5, column=8)
        
        self.multiTokenVar = tk.StringVar()
        self.multiTokenVar.set("1")
        self.MultiTokenLabel = ttk.Label(self.Tag_Frame, text="1", textvariable=self.multiTokenVar).grid(row=4, column=8)
        
        self.separ3 = ttk.Separator(self.Tag_Frame, orient=tk.HORIZONTAL).grid(row=6, column=4, columnspan=4, sticky="we", pady=15, padx=10)
        self.LabelTag = ttk.Label(self.Tag_Frame, text="TAG")
        self.LabelTag.grid(row=6, column=4, columnspan=4, pady= 15)
        
        self.Instruction3 = ttk.Label(self.Tag_Frame, text="Use the boxes below to select the morphosyntactic elements of the token")
        self.Instruction3.grid(row=7, column=4, columnspan=4)
        
        self.Combo1 = ttk.Combobox(self.Tag_Frame, values=["Category", "Adjective A","Conjunction C","Determiner D", "Noun N", "Pronoun P", "Adverb R", "Adposition S", "Verb V", "Number Z", "Date W", "Interjection I", "Punctuation"], state="readonly")
        self.Combo1.grid(row=8, column=4, pady=5)
        self.Combo1.current(0)
        
        
        self.Combo2 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo2.grid(row=8, column=5)
        
        self.Combo3 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo3.grid(row=8, column=6)
        
        self.Combo4 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo4.grid(row=8, column=7)
        
        self.Combo5 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo5.grid(row=9, column=5)
        
        self.Combo6 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo6.grid(row=9, column=6)
        
        self.Combo7 = ttk.Combobox(self.Tag_Frame, state="disabled")
        self.Combo7.grid(row=9, column=7)
        
        self.ShowTagButton = ttk.Button(self.Tag_Frame, text='Show Tag', command=self.showTag).grid(row=9, column=4)
        
        self.Instruction4 = ttk.Label(self.Tag_Frame, text="Click on \"Show tag\" button to see the EAGLES tag\nYou can edit the tag if EAGLES is not exactly what you need or just jump boxes selection and write one\nClick on \"Simple tag\" button if you want to assign this tag to this token only for this time\nClick on \"Fix on Dict.\" button if you want to save this tag for this token and use it automatically every time it appears on this corpus")
        self.Instruction4.grid(row=10, column=4, columnspan=4)
        
        
        self.Tag = ttk.Entry(self.Tag_Frame)
        self.Tag.grid(row=11, column=4)
        
        
       
        self.SimpleTagButton = ttk.Button(self.Tag_Frame, text='Simple\n  Tag', command = self.simpleTag).grid(row=11, column=6)
        self.FixOnDictButton = ttk.Button(self.Tag_Frame, text='Fix on\n  Dict.', command = self.fixDictTag).grid(row=11, column=7, pady=10)
        
        self.notebook.add(self.Tag_Frame, text="Tagging", padding=10, state= "disabled")
        
        
        #Here we put the notebook on the Main Window
        self.notebook.pack()
        
        
        self.pack()
        #This are the options that configure when you select a category on the combobox
        def categorySelect(eventObject):
            global adjectiveOptions
            global conjunctionOptions
            global determinerOptions
            global nounOptions
            global pronounOptions
            global adverbOptions
            global adpositionOptions
            global conjunctionOptions
            global numberOptions
            global punctuationOptions 
            
            
            if self.Combo1.get() == "Category":
                
                self.Combo2["values"] = [""]
                self.Combo2.config(state="disabled")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
            if self.Combo1.get() == "Date W":
                
                self.Combo2["values"] = [""]
                self.Combo2.config(state="disabled")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
            if self.Combo1.get() == "Interjection I":
                
                self.Combo2["values"] = [""]
                self.Combo2.config(state="disabled")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
            
            if self.Combo1.get() == "Adjective A":
                
                x = 0                                
                self.Combo2["values"] = adjectiveOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                x = x + 1
                self.Combo3["values"] = adjectiveOptions[x]
                self.Combo3.config(state="readonly")
                self.Combo3.current(0)
                x = x + 1
                self.Combo4["values"] = adjectiveOptions[x]
                self.Combo4.config(state="readonly")
                self.Combo4.current(0)
                x = x + 1
                self.Combo5["values"] = adjectiveOptions[x]
                self.Combo5.config(state="readonly")
                self.Combo5.current(0)
                x = x + 1
                self.Combo6["values"] = adjectiveOptions[x]
                self.Combo6.config(state="readonly")
                self.Combo6.current(0)
                x = x + 1
                self.Combo7["values"] = adjectiveOptions[x]
                self.Combo7.config(state="readonly")
                self.Combo7.current(0)
            
            if self.Combo1.get() == "Conjunction C":
                
                x = 0                                
                self.Combo2["values"] = conjunctionOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
                
            if self.Combo1.get() == "Determiner D":
                
                x = 0                                
                self.Combo2["values"] = determinerOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                x = x + 1
                self.Combo3["values"] = determinerOptions[x]
                self.Combo3.config(state="readonly")
                self.Combo3.current(0)
                x = x + 1
                self.Combo4["values"] = determinerOptions[x]
                self.Combo4.config(state="readonly")
                self.Combo4.current(0)
                x = x + 1
                self.Combo5["values"] = determinerOptions[x]
                self.Combo5.config(state="readonly")
                self.Combo5.current(0)
                x = x + 1
                self.Combo6["values"] = determinerOptions[x]
                self.Combo6.config(state="readonly")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
            
            if self.Combo1.get() == "Noun N":
                
                x = 0                                
                self.Combo2["values"] = nounOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                x = x + 1
                self.Combo3["values"] = nounOptions[x]
                self.Combo3.config(state="readonly")
                self.Combo3.current(0)
                x = x + 1
                self.Combo4["values"] = nounOptions[x]
                self.Combo4.config(state="readonly")
                self.Combo4.current(0)
                x = x + 1
                self.Combo5["values"] = nounOptions[x]
                self.Combo5.config(state="readonly")
                self.Combo5.current(0)
                x = x + 1
                self.Combo6["values"] = nounOptions[x]
                self.Combo6.config(state="readonly")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
                
            if self.Combo1.get() == "Pronoun P":
                
                x = 0                                
                self.Combo2["values"] = pronounOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                x = x + 1
                self.Combo3["values"] = pronounOptions[x]
                self.Combo3.config(state="readonly")
                self.Combo3.current(0)
                x = x + 1
                self.Combo4["values"] = pronounOptions[x]
                self.Combo4.config(state="readonly")
                self.Combo4.current(0)
                x = x + 1
                self.Combo5["values"] = pronounOptions[x]
                self.Combo5.config(state="readonly")
                self.Combo5.current(0)
                x = x + 1
                self.Combo6["values"] = pronounOptions[x]
                self.Combo6.config(state="readonly")
                self.Combo6.current(0)
                x = x + 1
                self.Combo7["values"] = pronounOptions[x]
                self.Combo7.config(state="readonly")
                self.Combo7.current(0)
             
            if self.Combo1.get() == "Adverb R":
                
                x = 0                                
                self.Combo2["values"] = adverbOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
            if self.Combo1.get() == "Adposition S":
                
                x = 0                                
                self.Combo2["values"] = adpositionOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
            if self.Combo1.get() == "Verb V":
                
                x = 0                                
                self.Combo2["values"] = verbOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                x = x + 1
                self.Combo3["values"] = verbOptions[x]
                self.Combo3.config(state="readonly")
                self.Combo3.current(0)
                x = x + 1
                self.Combo4["values"] = verbOptions[x]
                self.Combo4.config(state="readonly")
                self.Combo4.current(0)
                x = x + 1
                self.Combo5["values"] = verbOptions[x]
                self.Combo5.config(state="readonly")
                self.Combo5.current(0)
                x = x + 1
                self.Combo6["values"] = verbOptions[x]
                self.Combo6.config(state="readonly")
                self.Combo6.current(0)
                x = x + 1
                self.Combo7["values"] = verbOptions[x]
                self.Combo7.config(state="readonly")
                self.Combo7.current(0)
              
            if self.Combo1.get() == "Number Z":
                
                x = 0                                
                self.Combo2["values"] = numberOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
                
            if self.Combo1.get() == "Punctuation":
                
                x = 0                                
                self.Combo2["values"] = punctuationOptions[x]
                self.Combo2.config(state="readonly")
                self.Combo2.current(0)
                self.Combo3["values"] = [""]
                self.Combo3.config(state="disabled")
                self.Combo3.current(0)
                self.Combo4["values"] = [""]
                self.Combo4.config(state="disabled")
                self.Combo4.current(0)
                self.Combo5["values"] = [""]
                self.Combo5.config(state="disabled")
                self.Combo5.current(0)
                self.Combo6["values"] = [""]
                self.Combo6.config(state="disabled")
                self.Combo6.current(0)
                self.Combo7["values"] = [""]
                self.Combo7.config(state="disabled")
                self.Combo7.current(0)
            
                
        self.Combo1.bind("<<ComboboxSelected>>", categorySelect)
        
    def new_window(self, _class):
        try:
            if self.newWindow.state() == "normal":
                self.newWindow.focus()
        except:
            self.newWindow = tk.Toplevel(self)
            _class(self.newWindow)
    
        """
        self.newWindow = tk.Toplevel(self)
        _class(self.newWindow)
    """
    def new(self):
        global savedSesions
        
        x = tk.messagebox.askokcancel(message="Are you sure you want to start a new project?", title="Start new project")
        
        if x == True:
            
            #Clean the token box and his info
            self.tokenVar.set("")
            self.statusVar.set(selectedText + "\n" + "none")
            self.multiTokenVar.set("1")
            self.Tag.delete(0, tk.END)
            self.context1Var.set("")
            self.context2Var.set("")
            
            #Clean Home tab info
            self.CorpusDirectory.delete(0, tk.END)
            self.ProjectName.delete(0, tk.END)
            self.DictionaryFile.delete(0, tk.END)
            self.PreviusList.delete(0,tk.END)
            self.PreviusList.current(0)
            
            #Refresh saved sesions info
            savedSesions = ["Saved Sesions"]
            for doc in os.listdir(savedSesionsDir):
                doc1 = doc.split(".")        
                savedSesions.append(doc1[0])
            
            self.PreviusList.config(values= savedSesions)
            self.PreviusList.current(0)
            
            #Change selection in notebook
            self.notebook.tab(self.Home_Frame, state="normal")
            self.notebook.select(self.Home_Frame)
            self.notebook.tab(self.Tag_Frame, state="disabled")
        
    def Start(self):
        
        global corpusDir
        global dictDir
        global textNames
        global exitDir
        global projectName
        global saveDir
        
        canContinue = True
        
        if self.CorpusDirectory.get():
            
            if os.path.exists(self.CorpusDirectory.get()):
                corpusDir = self.CorpusDirectory.get()
                
                exitDir = os.path.join(corpusDir, "Tagged")
                if os.path.exists(exitDir):
                    print(tk.messagebox.showwarning(message="The directory you entered allready has a \"Tagged\" folder; please move it, eare it or use a new directory.\nIf you want to load a previous project use the load button above.", title="Corpus directory already has a Tagged folder"))
                    canContinue = False
            
            else:
                print(tk.messagebox.showwarning(message="The directory you entered for the corpus is invalid", title="Invalid Directory"))
                canContinue = False
                
        
        else:
            print(tk.messagebox.showwarning(message="You have to introduce the directory where the corpus is located", title="There's no corpus directory"))
            canContinue = False
        
        if self.ProjectName.get():
            projectName = self.ProjectName.get()
            
            if projectName in savedSesions:
                print(tk.messagebox.showwarning(message="The name you introduced for the project is aready in use for another one", title="The projects name already exists"))
                canContinue = False
            
        else:
            print(tk.messagebox.showwarning(message="You have to introduce a name for the new project", title="There's no project name"))
            canContinue = False
        
        if self.DictionaryFile.get():
            
            if os.path.exists(self.DictionaryFile.get()):
                dictDir = self.DictionaryFile.get()
            
            else:
                print(tk.messagebox.showwarning(message="The archive you selected for the dictionary is invalid", title="Invalid Directory"))
                canContinue = False
        else:
            #Create dictionary file
            dictDir = os.path.join(os.getcwd(), "dict", self.ProjectName.get() + "_dict.txt")
            if os.path.exists(dictDir):
                doNothing = True
            else:
                if canContinue == True:
                    dictionary = codecs.open(dictDir, "w", "utf-8") 
                    dictionary.close()
            
        if canContinue == True:
        
            for doc in os.listdir(corpusDir):
                if doc[-4:] == ".txt":
                    textsNames.append(doc)
                
            for textName in textsNames:
                self.TextsList.insert(tk.END, textName)
            
                
            
            os.mkdir(exitDir)
            
            saveDir = os.path.join(savedSesionsDir, projectName + ".txt")
            save = open(saveDir , "w")
            
            save.write(corpusDir)
            
            save.write("\n" + dictDir)
            
            save.close()
            
            
            
            #Change selection in notebook
            self.notebook.tab(self.Tag_Frame, state="normal")
            self.notebook.select(self.Tag_Frame)
            self.notebook.tab(self.Home_Frame, state="disabled")
        
        
     
    def selectText(self):
        
        global corpusDir
        global tokens
        global token
        global numberSelectedTokens
        global xmlDir
        global selectedText
        global lastWord
        
        
        numberSelectedTokens = 0
        self.multiTokenVar.set(str(numberSelectedTokens + 1))
        
        posSelectedText = self.TextsList.curselection()
        selectedText = self.TextsList.get(posSelectedText[0])
        
        selectedTextDir = os.path.join(corpusDir, selectedText)
        
        #Refresh save archive
                    
        save = open(saveDir , "w")
        
        save.write(corpusDir)
        
        save.write("\n" + dictDir)
        
        save.write("\n" + selectedText)
        
        save.close()
        
        #Creates the exit xml directory
        xmlDir = os.path.join(exitDir, selectedText[0:len(selectedText)-4] + '.xml')
        
        
        #If exit file for this text allready exists, search for the last tagged token or the end of xml for stablish the current point.
        ended = False
        started = False
        if os.path.exists(xmlDir):
            xml = codecs.open(xmlDir, "r", "utf-8")
            xmlLines = xml.readlines()
            
            
            patron1 = "</text>"
            patron2 = "<token form="
            x = len(xmlLines)
            
            
            
            while x >= 1:
                #If it finds an ended text, show an advice asking for select another text
                if xmlLines[x - 1].find(patron1) >= 0:
                    ended = True
                    print(tk.messagebox.showwarning(message="This text is already tagged, select another one", title="Text already tagged"))
                    
                    #Clean the token box and his info
                    self.tokenVar.set("")
                    self.statusVar.set(selectedText + "\n" + "none")
                    self.multiTokenVar.set("1")
                    self.Tag.delete(0, tk.END)
                    self.context1Var.set("")
                    self.context2Var.set("")
                    break
                
                #If it finds an started but not ended text, set the token info one after the last finded.
                if xmlLines[x - 1].find(patron2) >= 0:
                    started = True
                    dividedLine = xmlLines[x - 1].split('"')
                    break
                    
                x = x - 1
            
            
        #If exit file doesn't exist, it creates it.    
        else:
            xml = open(xmlDir, "w")
            xml.write('<?xml version="1.0" encoding="UTF-8" standalone= "yes"?>\n\n')
            xml.write('<text name="' + selectedText +'">\n')
            xml.close()
        
        #If it wasn't a finished text...
        if ended == False:
            readText = codecs.open(selectedTextDir, "r", "utf-8")
            
            #Tokenyze
            text = readText.read()
            allTokens = word_tokenize(text)
            
            tokens = []
            
            x=0
            while x < len(allTokens):
                t = [allTokens[x], x]
                tokens.append(t)
                x = x+1
            
            #If text was started but not finished
            if started == True:
                
                #Takes data from line extrated from xml
                token[2] = int(dividedLine[5].split('.')[2])
                token[1] = int(dividedLine[5].split('.')[1]) + token[2]
                token[0] = tokens[token[1]][0]
            
            #If was not started, just fix token info from the first token
            else:
                token[0] = tokens[0][0]
                token[1] = 0
                token[2] = 0
                
            self.statusVar.set(selectedText + "\n" + str(token[1]))                   
            self.tokenVar.set(token[0])
                
            
            
            self.context1Var.set("")
        
            #Refresh context after token
            self.context2Var.set("")
            
            y=1
            p2= False
            lastWord = False
            
            if token[1] + 1 == len(tokens):
                y = 11
                lastWord = True
                
            while y < 10:
                
                
                if tokens[token[1] + y][0] in punctuation1:
                    self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                    
                elif tokens[token[1] + y][0] in punctuation2:
                    self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                    p2 = True
                    
                else:
                    if p2 == True:
                        self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                        p2 = False
                    
                    else:
                        self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                
                if tokens[token[1] + y][1] + 1 >= len(tokens):
                    y = 11
                
                else:
                    y = y + 1
             
            #Refresh context before token
            if token[1] >= 10:
                y=1
                p2= False
                self.context1Var.set("")
                
                while y <= 10:
                    
                    
                    if tokens[token[1] - y][0] in punctuation1:
                        self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                        
                    elif tokens[token[1] - y][0] in punctuation2:
                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                        p2 = True
                        
                    else:
                        if p2 == True:
                            self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                            p2 = False
                        
                        else:
                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                            
                    y = y + 1
            
            else:
                y=1
                p2= False
                self.context1Var.set("")
                
                while y <= token[1]:
                    
                    
                    if tokens[token[1] - y][0] in punctuation1:
                        self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                        
                    elif tokens[token[1] - y][0] in punctuation2:
                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                        p2 = True
                        
                    else:
                        if p2 == True:
                            self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                            p2 = False
                        
                        else:
                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                            
                    y = y + 1
            
            #Starts an automatic search with the token obtained or created
            wordOnDict = False
                    
            dictionaryRead = codecs.open(dictDir, "r", "utf-8")
            entries = dictionaryRead.readlines()
            entry = ""
            isMultiToken = False
            isEnd = False
            
            #In first place we look if there's a multitoken word with token and next token on dict. Just if word is not the last one. 
            if lastWord == False:
                patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                for e in entries:
                    
                    x = e.count(patron)
                    if x >= 1:
                        entry = e
                        multitoken = entry[6:-14]
                        entryTokens = word_tokenize(multitoken)
                        multitoken2 = []
                        multitoken3 = []
                        
                        count = 0
                        for t in entryTokens:
                            multitoken2.append(entryTokens[count])
                            multitoken3.append(tokens[token[1] + count][0])
                            count = count + 1
                        
                        if multitoken3 == multitoken2:
                            isMultiToken = True
                            wordOnDict = True
                            break
            
            #If is not a multitoken, search for the single token
            if isMultiToken == False:
                patron = "entry_ " + token[0].lower() + " *****"
                for e in entries:
                    x = e.count(patron)
                    if x >= 1:
                        entry = e
                        wordOnDict = True
                        break
            
            #If word exists...
            while wordOnDict == True:
                
                
                
                #Obtain the tag
                entryParts = entry.split(" ***** ")
                
                #If its multitoken, change the token info before writing
                if isMultiToken == True:
                    token[0] = multitoken
                    token[2] = len(multitoken3) - 1                            
                    numberSelectedTokens = token[2]
                    
                #Open the exit xml and write the current token info.
                xml = codecs.open(xmlDir, "a", "utf-8")
                xml.write('\n<token form="' + token[0] + '" tag="' + entryParts[1][0:len(entryParts[1]) - 1] + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                xml.close()
                
                
                #Change the info of the current token and show it, only if is not the last one
                if tokens[token[1] + numberSelectedTokens][1] + 1 < len(tokens):
                    token[0] = tokens[token[1] + numberSelectedTokens + 1][0]
                    token[1] = tokens[token[1] + numberSelectedTokens + 1][1]
                    token[2] = 0
                    
                    self.tokenVar.set(token[0])
                    self.statusVar.set(selectedText + "\n" + str(token[1]))
                    self.multiTokenVar.set("1")
                    
                
                    #Refresh context after token
                    self.context2Var.set("")
                     
                    y=1
                    p2= False
                    lastWord = False
                    
                    if token[1] + 1 == len(tokens):
                        y = 11
                        lastWord = True
                        
                    while y < 10:
                        
                        
                        if tokens[token[1] + y][0] in punctuation1:
                            self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                            
                        elif tokens[token[1] + y][0] in punctuation2:
                            self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                            p2 = True
                            
                        else:
                            if p2 == True:
                                self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                                p2 = False
                            
                            else:
                                self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                        
                        if tokens[token[1] + y][1] + 1 >= len(tokens):
                            y = 11
                        
                        else:
                            y = y + 1
                        
                    #Refresh context before token
                    
                    
                    if token[1] >= 10:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= 10:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                    
                    else:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= token[1]:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                            
                    
                    
                    #Search again on dictionary first the multitoken then the single one, if find the token, starts the while again, if not, the program cotinues on manual mode.
                    
                    wordOnDict = False
                    #Only if token is not the last one, search multitokens
                    
                    if isEnd == False:
                        if token[1] + 3 <= len(tokens):
                            patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                            for e in entries:
                                
                                if e.find(patron) >= 0:
                                    entry = e
                                    multitoken = entry[6:-14]
                                    entryTokens = word_tokenize(multitoken)
                                    multitoken2 = []
                                    multitoken3 = []
                                    
                                    #Only continues if current piece of text extension can have the found expression
                                    tokensLeft = len(tokens) - token[1]
                                    if tokensLeft >= len(entryTokens):
                                        count = 0
                                        for t in entryTokens:
                                            multitoken2.append(entryTokens[count])
                                            multitoken3.append(tokens[token[1] + count][0])
                                            count = count + 1
                                        
                                        if multitoken3 == multitoken2:
                                            isMultiToken = True
                                            wordOnDict = True
                                            #if is just one before the last, search, but no continues searching the next time the while comes here
                                            if token[1] + 2 > len(tokens):
                                                isEnd = True    
                                            break
                        
                    
                        if isMultiToken == False:
                            patron = "entry_ " + token[0].lower() + " *****"
                            
                            for e in entries:
                                
                                if patron in e:
                                    entry = e
                                    wordOnDict = True                        
                                    if token[1] + 1 > len(tokens):
                                        isEnd = True
                                    break
                    
                
                #If in automatic search, token is the last one
                else:
                    #Open the exit xml and write the last line of the file
                    xml = codecs.open(xmlDir, "a", "utf-8")
                    xml.write('\n</text>')
                    xml.close()
                    
                    #Clean the token box and his info
                    self.tokenVar.set("")
                    self.statusVar.set(selectedText + "\n" + "none")
                    self.multiTokenVar.set("1")
                    self.Tag.delete(0, tk.END)
                    self.context1Var.set("")
                    self.context2Var.set("") 
                    
                    #Show an advice aking for select another text.
                    print(tk.messagebox.showwarning(message="This text is completely tagged, select another one", title="Tagging completed"))
                    break
    
    def load(self):
        
        global corpusDir
        global dictDir
        global textNames
        global exitDir
        global projectName
        global saveDir
        
        #open saved archive and take info from it
        if self.PreviusList.get() != "Saved Sesions":
            saveDir = os.path.join(savedSesionsDir , self.PreviusList.get() + ".txt")
            saved = open(saveDir, "r")
            savedLines = saved.readlines()
            saved.close()
            
            
            corpusDir = savedLines[0][:-1]
            dictDir = savedLines[1][:-1]
            
            textNames = []
            for doc in os.listdir(corpusDir):
                if doc[-4:] == ".txt":
                    textNames.append(doc)
            
            self.TextsList.delete(0,tk.END)
            for textName in textNames:
                self.TextsList.insert(tk.END, textName)
                
            #Change selection in notebook
            self.notebook.tab(self.Tag_Frame, state="normal")
            self.notebook.select(self.Tag_Frame)
            self.notebook.tab(self.Home_Frame, state="disabled")

        
    def plusNumber(self):
        global token
        global tokens
        global numberSelectedTokens
        

        #If there's anything on token box...
        if self.CurrentToken.get():
            
            #Only continues if a next token does really exists
            if token[2] + 1 < len(tokens):
                numberSelectedTokens = numberSelectedTokens + 1
                self.multiTokenVar.set(str(numberSelectedTokens + 1))
                
                p2 = False
                
                if  tokens[token[1] + numberSelectedTokens][0] in punctuation1:
                    token[0] = token[0] + tokens[token[1] + numberSelectedTokens][0]
                    token[2] = token[2] + 1
                
                elif tokens[token[1] + numberSelectedTokens][0] in punctuation2:
                    token[0] = token[0] + " " + tokens[token[1] + numberSelectedTokens][0]
                    token[2] = token[2] + 1
                    p2 = True
                
                else:
                    if p2 == True:
                        token[0] = token[0] + tokens[token[1] + numberSelectedTokens][0]
                        token[2] = token[2] + 1
                        p2 = False
                        
                    else:
                        token[0] = token[0] + " " + tokens[token[1] + numberSelectedTokens][0]
                        token[2] = token[2] + 1
                
                self.tokenVar.set(token[0])
                
                #Refresh context after token
                self.context2Var.set("")
                 
                y=1
                p2= False
                
                if token[2] + 1 == len(tokens):
                    y = 11
                
                while y < 10:
                    
                    
                    if tokens[token[2] + y][0] in punctuation1:
                        self.context2Var.set(self.context2Var.get() + tokens[token[2]+y][0])
                        
                    elif tokens[token[2] + y][0] in punctuation2:
                        self.context2Var.set(self.context2Var.get() + " " + tokens[token[2]+y][0])
                        p2 = True
                        
                    else:
                        if p2 == True:
                            self.context2Var.set(self.context2Var.get() + tokens[token[2] + y][0])
                            p2 = False
                        
                        else:
                            self.context2Var.set(self.context2Var.get() + " " + tokens[token[2] + y][0])
                    
                    if tokens[token[2] + y][1] + 1 >= len(tokens):
                        y = 11
                    
                    else:
                        y = y + 1
        
    def minusNumber(self):
        global token
        global tokens
        global numberSelectedTokens
        
        #If there's anything on token box...
        if self.CurrentToken.get():
            if numberSelectedTokens >= 1:
                numberSelectedTokens = numberSelectedTokens - 1
                
                
                self.multiTokenVar.set(str(numberSelectedTokens + 1))
                
                
                token[2] = token[2] - 1
                token[0] = tokens[token[1]][0]
                
                x=1
                p2 = False
                while x <= numberSelectedTokens:
                    if tokens[token[1] + x][0] in punctuation1:
                        token[0] = token[0] + tokens[token[1]+x][0]
                        
                    elif tokens[token[1] + x][0] in punctuation2:
                        token[0] = token[0] + " " + tokens[token[1]+x][0]
                        p2 = True
                        
                    else:
                        if p2 == True:
                            token[0] = token[0] + tokens[token[1] + x][0]
                            p2 = False
                        
                        else:
                            token[0] = token[0] + " " + tokens[token[1] + x][0]
                            
                    x = x + 1
                
                self.tokenVar.set(token[0])
                
                #Refresh context after token
                self.context2Var.set("")
                 
                y=1
                p2= False
                
                if token[2] + 1 == len(tokens):
                    y = 11
                
                while y < 10:
                    
                    
                    if tokens[token[2] + y][0] in punctuation1:
                        self.context2Var.set(self.context2Var.get() + tokens[token[2]+y][0])
                        
                    elif tokens[token[2] + y][0] in punctuation2:
                        self.context2Var.set(self.context2Var.get() + " " + tokens[token[2]+y][0])
                        p2 = True
                        
                    else:
                        if p2 == True:
                            self.context2Var.set(self.context2Var.get() + tokens[token[2] + y][0])
                            p2 = False
                        
                        else:
                            self.context2Var.set(self.context2Var.get() + " " + tokens[token[2] + y][0])
                    
                    if tokens[token[2] + y][1] + 1 >= len(tokens):
                        y = 11
                    
                    else:
                        y = y + 1
    
    
    def showTag(self):
        
        letter1 = ""
        letter2 = ""
        letter3 = ""
        letter4 = ""
        letter5 = ""
        letter6 = ""
        letter7 = ""
        
        if self.Combo1.current() == 0:
            doNothing = True
            
        else:
            comboText = self.Combo1.get()
            letter1 = comboText[len(comboText) - 1]
        
            if self.Combo2.current() == 0:
                letter2 = "-"
            
            else:
                comboText = self.Combo2.get()
                letter2 = comboText[len(comboText) - 1]
                
            if self.Combo3.current() == 0:
                letter3 = "-"
            
            else:
                comboText = self.Combo3.get()
                letter3 = comboText[len(comboText) - 1]
                
            if self.Combo4.current() == 0:
                letter4 = "-"
            
            else:
                comboText = self.Combo4.get()
                letter4 = comboText[len(comboText) - 1]
                
            if self.Combo5.current() == 0:
                letter5 = "-"
            
            else:
                comboText = self.Combo5.get()
                letter5 = comboText[len(comboText) - 1]
                
            if self.Combo6.current() == 0:
                letter6 = "-"
            
            else:
                comboText = self.Combo6.get()
                letter6 = comboText[len(comboText) - 1]
                
            if self.Combo7.current() == 0:
                letter7 = "-"
            
            else:
                comboText = self.Combo7.get()
                letter7 = comboText[len(comboText) - 1]
            
            #If punctuation, select the tag in this way
            if self.Combo1.current() == 12:
                comboText = self.Combo2.get()
                aux_tag = comboText.split(" ")
                tag0 = aux_tag[-1]
            
            else:
                tag0 = letter1 + letter2 + letter3 + letter4 + letter5 + letter6 + letter7
            
            self.Tag.delete(0, tk.END)
            self.Tag.insert(0, tag0)
    
    
    def simpleTag(self):
        global xmlDir
        global token
        global selectedText
        global saveDir
        global dictDir
        global numberSelectedTokens
        global lastWord
        
        #If there's anything on token box...
        if self.CurrentToken.get():
            
            #If there's something on the tag textbox...
            if self.Tag.get():
                
                #If token is not the last token on document.
                if token[1] < len(tokens) - 1:
                
                    #Open the exit xml and write the current token info.
                    xml = codecs.open(xmlDir, "a", "utf-8")
                    xml.write('\n<token form="' + token[0] + '" tag="' + self.Tag.get() + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                    xml.close()
                    
                    #Change the info of the current token and show it
                    token[0] = tokens[token[1] + numberSelectedTokens + 1][0]
                    token[1] = tokens[token[1] + numberSelectedTokens + 1][1]
                    token[2] = 0
                    
                    
                    self.tokenVar.set(token[0])
                    self.statusVar.set(selectedText + "\n" + str(token[1]))
                    self.multiTokenVar.set("1")
                    numberSelectedTokens = 0
                    
                    #Refresh select boxes and clean tag box
                    self.Combo1.current(0)
                    self.Combo2["values"] = [""]
                    self.Combo2.config(state="disabled")
                    self.Combo2.current(0)
                    self.Combo3["values"] = [""]
                    self.Combo3.config(state="disabled")
                    self.Combo3.current(0)
                    self.Combo4["values"] = [""]
                    self.Combo4.config(state="disabled")
                    self.Combo4.current(0)
                    self.Combo5["values"] = [""]
                    self.Combo5.config(state="disabled")
                    self.Combo5.current(0)
                    self.Combo6["values"] = [""]
                    self.Combo6.config(state="disabled")
                    self.Combo6.current(0)
                    self.Combo7["values"] = [""]
                    self.Combo7.config(state="disabled")
                    self.Combo7.current(0)
                    
                    self.Tag.delete(0, tk.END)
                    
                    #Refresh context after token
                    self.context2Var.set("")
                    
                    y=1
                    p2= False
                    lastWord = False
                    
                    if token[1] + 1 == len(tokens):
                        y = 11
                        lastWord = True
                        
                    while y < 10:
                        
                        
                        if tokens[token[1] + y][0] in punctuation1:
                            self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                            
                        elif tokens[token[1] + y][0] in punctuation2:
                            self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                            p2 = True
                            
                        else:
                            if p2 == True:
                                self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                                p2 = False
                            
                            else:
                                self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                        
                        if tokens[token[1] + y][1] + 1 >= len(tokens):
                            y = 11
                        
                        else:
                            y = y + 1
                        
                    #Refresh context before token
                    
                    
                    if token[1] >= 10:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= 10:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                    
                    else:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= token[1]:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                            
                    
                    
                    #After tagging the token manually, program search for the new token on dictionary... if exists, repeat all the previous process for tagging automatically and continues doing it for all the text.
                    
                    
                    wordOnDict = False
                    
                    dictionaryRead = codecs.open(dictDir, "r", "utf-8")
                    entries = dictionaryRead.readlines()
                    entry = ""
                    isMultiToken = False
                    isEnd = False
                    
                    #In first place we look if there's a multitoken word with token and next token on dict. Just if word is not the last one. 
                    if lastWord == False:
                        patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                        for e in entries:
                            
                            x = e.count(patron)
                            if x >= 1:
                                entry = e
                                multitoken = entry[6:-14]
                                entryTokens = word_tokenize(multitoken)
                                multitoken2 = []
                                multitoken3 = []
                                
                                count = 0
                                for t in entryTokens:
                                    multitoken2.append(entryTokens[count])
                                    multitoken3.append(tokens[token[1] + count][0])
                                    count = count + 1
                                
                                if multitoken3 == multitoken2:
                                    isMultiToken = True
                                    wordOnDict = True
                                    break
                    
                    #If is not a multitoken, search for the single token
                    if isMultiToken == False:
                        patron = "entry_ " + token[0].lower() + " *****"
                        
                        for e in entries:
                            if patron in e:
                                entry = e
                                wordOnDict = True
                                break
                    
                    #If word exists...
                    while wordOnDict == True:
                        
                        
                        
                        #Obtain the tag
                        entryParts = entry.split(" ***** ")
                        
                        #If its multitoken, change the token info before writing
                        if isMultiToken == True:
                            token[0] = multitoken
                            token[2] = len(multitoken3) - 1                            
                            numberSelectedTokens = token[2]
                            
                        #Open the exit xml and write the current token info.
                        xml = codecs.open(xmlDir, "a", "utf-8")
                        xml.write('\n<token form="' + token[0] + '" tag="' + entryParts[1][0:len(entryParts[1]) - 1] + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                        xml.close()
                        
                        
                        #Change the info of the current token and show it, only if is not the last one
                        if tokens[token[1] + numberSelectedTokens][1] + 1 < len(tokens):
                            token[0] = tokens[token[1] + numberSelectedTokens + 1][0]
                            token[1] = tokens[token[1] + numberSelectedTokens + 1][1]
                            token[2] = 0
                            
                            self.tokenVar.set(token[0])
                            self.statusVar.set(selectedText + "\n" + str(token[1]))
                            self.multiTokenVar.set("1")
                        
                        
                            #Refresh context after token
                            self.context2Var.set("")
                            
                            y=1
                            p2= False
                            lastWord = False
                            
                            if token[1] + 1 == len(tokens):
                                y = 11
                                lastWord = True
                                
                            while y < 10:
                                
                                
                                if tokens[token[1] + y][0] in punctuation1:
                                    self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                                    
                                elif tokens[token[1] + y][0] in punctuation2:
                                    self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                                    p2 = True
                                    
                                else:
                                    if p2 == True:
                                        self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                                        p2 = False
                                    
                                    else:
                                        self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                                
                                if tokens[token[1] + y][1] + 1 >= len(tokens):
                                    y = 11
                                
                                else:
                                    y = y + 1
                                
                            #Refresh context before token
                            
                            
                            if token[1] >= 10:
                                y=1
                                p2= False
                                self.context1Var.set("")
                                
                                while y <= 10:
                                    
                                    
                                    if tokens[token[1] - y][0] in punctuation1:
                                        self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                        
                                    elif tokens[token[1] - y][0] in punctuation2:
                                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                        p2 = True
                                        
                                    else:
                                        if p2 == True:
                                            self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                                            p2 = False
                                        
                                        else:
                                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                            
                                    y = y + 1
                            
                            else:
                                y=1
                                p2= False
                                self.context1Var.set("")
                                
                                while y <= token[1]:
                                    
                                    
                                    if tokens[token[1] - y][0] in punctuation1:
                                        self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                                        
                                    elif tokens[token[1] - y][0] in punctuation2:
                                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                        p2 = True
                                        
                                    else:
                                        if p2 == True:
                                            self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                            p2 = False
                                        
                                        else:
                                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                            
                                    y = y + 1
                                    
                            
                            
                            #Search again on dictionary first the multitoken then the single one, if find the token, starts the while again, if not, the program cotinues on manual mode.
                            
                            wordOnDict = False
                            #Only if token is not the last one, search multitokens
                            
                            if isEnd == False:
                                if token[1] + 3 <= len(tokens):
                                    patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                                    for e in entries:
                                        
                                        if e.find(patron) >= 0:
                                            entry = e
                                            multitoken = entry[6:-14]
                                            entryTokens = word_tokenize(multitoken)
                                            multitoken2 = []
                                            multitoken3 = []
                                            
                                            #Only continues if current piece of text extension can have the found expression
                                            tokensLeft = len(tokens) - token[1]
                                            if tokensLeft >= len(entryTokens):
                                                count = 0
                                                for t in entryTokens:
                                                    multitoken2.append(entryTokens[count])
                                                    multitoken3.append(tokens[token[1] + count][0])
                                                    count = count + 1
                                                
                                                if multitoken3 == multitoken2:
                                                    isMultiToken = True
                                                    wordOnDict = True
                                                    #if is just one before the last, search, but no continues searching the next time the while comes here
                                                    if token[1] + 2 > len(tokens):
                                                        isEnd = True    
                                                    break
                                
                            
                                if isMultiToken == False:
                                    patron = "entry_ " + token[0].lower() + " *****"
                                    
                                    for e in entries:
                                        
                                        if patron in e:
                                            entry = e
                                            wordOnDict = True                        
                                            if token[1] + 1 > len(tokens):
                                                isEnd = True
                                            break
                            
                        
                        #If in automatic search, token is the last one
                        else:
                            #Open the exit xml and write the last line of the file
                            xml = codecs.open(xmlDir, "a", "utf-8")
                            xml.write('\n</text>')
                            xml.close()
                            
                            #Clean the token box and his info
                            self.tokenVar.set("")
                            self.statusVar.set(selectedText + "\n" + "none")
                            self.multiTokenVar.set("1")
                            self.Tag.delete(0, tk.END)
                            self.context1Var.set("")
                            self.context2Var.set("") 
                            
                            #Show an advice aking for select another text.
                            print(tk.messagebox.showwarning(message="This text is completely tagged, select another one", title="Tagging completed"))
                            break
                
                #If token is the last token on document.
                else:
                    #Open the exit xml and write the current token info. Then, close the last line of the file.
                    xml = codecs.open(xmlDir, "a", "utf-8")
                    xml.write('\n<token form="' + token[0] + '" tag="' + self.Tag.get() + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                    xml.write('\n</text>')
                    xml.close()
                    
                    #Clean the token box and his info
                    self.tokenVar.set("")
                    self.statusVar.set(selectedText + "\n" + "none")
                    self.multiTokenVar.set("1")
                    
                    #Refresh select boxes and clean tag box
                    self.Combo1.current(0)
                    self.Combo2["values"] = [""]
                    self.Combo2.config(state="disabled")
                    self.Combo2.current(0)
                    self.Combo3["values"] = [""]
                    self.Combo3.config(state="disabled")
                    self.Combo3.current(0)
                    self.Combo4["values"] = [""]
                    self.Combo4.config(state="disabled")
                    self.Combo4.current(0)
                    self.Combo5["values"] = [""]
                    self.Combo5.config(state="disabled")
                    self.Combo5.current(0)
                    self.Combo6["values"] = [""]
                    self.Combo6.config(state="disabled")
                    self.Combo6.current(0)
                    self.Combo7["values"] = [""]
                    self.Combo7.config(state="disabled")
                    self.Combo7.current(0)
                    
                    self.Tag.delete(0, tk.END)
                    
                    #Show and advice aking for select another text.
                    print(tk.messagebox.showwarning(message="This text is completely tagged, select another one", title="Tagging completed"))
                    
                
            #If Tag textbox is empty... show an advice.
            else:
                print(tk.messagebox.showwarning(message="You have no introduced any tag", title="Empty Tag"))
        
        #If there's nothing on tag box, show and advice asking for selecting a text.
        else:
            print(tk.messagebox.showwarning(message="Select a text in order to start tagging", title="No text selected"))
        
        
    def fixDictTag(self):
        global xmlDir
        global token
        global selectedText
        global dictDir
        global numberSelectedTokens
        global lastWord
        
        #If there's anything on token box...
        if self.CurrentToken.get():
        
            #If there's something on the tag textbox...
            if self.Tag.get():
                
                #If token is not the last token on document...
                if token[1] < len(tokens) - 1:
                
                    #Open xml and write the token with his tag
                    xml = codecs.open(xmlDir, "a", "utf-8")
                    xml.write('\n<token form="' + token[0] + '" tag="' + self.Tag.get() + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                    xml.close()
                    
                    #Open dict and write the new token with his tag, then organize it
                    dictionaryRead = codecs.open(dictDir, "r", "utf-8")
                    entries = dictionaryRead.readlines()
                    newEntry = ("entry_ " + token[0].lower() + " ***** " + self.Tag.get() + '\n')
                    entries.append(newEntry)
                    entries.sort()
                    dictionaryRead.close()
                    
                    #Write new organized dictionary in file
                    dictionaryWrite = codecs.open(dictDir, "w", "utf-8")
                    dictionaryWrite.writelines(entries)
                    dictionaryWrite.close()
                    
                    #Change the info of the current token and show it
                    token[0] = tokens[token[1] + numberSelectedTokens + 1][0]
                    token[1] = tokens[token[1] + numberSelectedTokens + 1][1]
                    token[2] = 0
                    
                    self.tokenVar.set(token[0])
                    self.statusVar.set(selectedText + "\n" + str(token[1]))
                    self.multiTokenVar.set("1")
                    numberSelectedTokens = 0
                    
                    #Refresh select boxes and clean tag box
                    self.Combo1.current(0)
                    self.Combo2["values"] = [""]
                    self.Combo2.config(state="disabled")
                    self.Combo2.current(0)
                    self.Combo3["values"] = [""]
                    self.Combo3.config(state="disabled")
                    self.Combo3.current(0)
                    self.Combo4["values"] = [""]
                    self.Combo4.config(state="disabled")
                    self.Combo4.current(0)
                    self.Combo5["values"] = [""]
                    self.Combo5.config(state="disabled")
                    self.Combo5.current(0)
                    self.Combo6["values"] = [""]
                    self.Combo6.config(state="disabled")
                    self.Combo6.current(0)
                    self.Combo7["values"] = [""]
                    self.Combo7.config(state="disabled")
                    self.Combo7.current(0)
                    
                    self.Tag.delete(0, tk.END)
                    
                    #Refresh context after token
                    self.context2Var.set("")
                    
                    y=1
                    p2= False
                    lastWord = False
                    
                    if token[1] + 1 == len(tokens):
                        y = 11
                        lastWord = True
                        
                    while y < 10:
                        
                        
                        if tokens[token[1] + y][0] in punctuation1:
                            self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                            
                        elif tokens[token[1] + y][0] in punctuation2:
                            self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                            p2 = True
                            
                        else:
                            if p2 == True:
                                self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                                p2 = False
                            
                            else:
                                self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                        
                        if tokens[token[1] + y][1] + 1 >= len(tokens):
                            y = 11
                        
                        else:
                            y = y + 1
                        
                    #Refresh context before token
                    
                    
                    if token[1] >= 10:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= 10:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                    
                    else:
                        y=1
                        p2= False
                        self.context1Var.set("")
                        
                        while y <= token[1]:
                            
                            
                            if tokens[token[1] - y][0] in punctuation1:
                                self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                                
                            elif tokens[token[1] - y][0] in punctuation2:
                                self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                p2 = True
                                
                            else:
                                if p2 == True:
                                    self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                    p2 = False
                                
                                else:
                                    self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                    
                            y = y + 1
                        
                    #After tagging the token manually, program search for the new token on dictionary... if exists, repeat all the previous process for tagging automatically and continues doing it for all the text.
                    
                    
                    wordOnDict = False
                    
                    dictionaryRead = codecs.open(dictDir, "r", "utf-8")
                    entries = dictionaryRead.readlines()
                    entry = ""
                    isMultiToken = False
                    isEnd = False
                    
                    #In first place we look if there's a multitoken word with token and next token on dict; just if its not the last word.
                    if lastWord == False:
                        patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                        for e in entries:
                            
                            x = e.count(patron)
                            if x >= 1:
                                entry = e
                                multitoken = entry[6:-14]
                                entryTokens = word_tokenize(multitoken)
                                multitoken2 = []
                                multitoken3 = []
                                
                                count = 0
                                for t in entryTokens:
                                    multitoken2.append(entryTokens[count])
                                    multitoken3.append(tokens[token[1] + count][0])
                                    count = count + 1
                                
                                if multitoken3 == multitoken2:
                                    isMultiToken = True
                                    wordOnDict = True
                                    break
                    
                    #If is not a multitoken, search for the single token
                    if isMultiToken == False:
                        patron = "entry_ " + token[0].lower() + " *****"
                        
                        for e in entries:
                            if patron in e:
                                entry = e
                                wordOnDict = True
                                break
                    
                    #If word exists...
                    while wordOnDict == True:
                        
                        
                        
                        #Obtain the tag
                        entryParts = entry.split(" ***** ")
                        
                        #If its multitoken, change the token info before writing
                        if isMultiToken == True:
                            token[0] = multitoken
                            token[2] = len(multitoken3) - 1                            
                            numberSelectedTokens = token[2]
                            
                        #Open the exit xml and write the current token info.
                        xml = codecs.open(xmlDir, "a", "utf-8")
                        xml.write('\n<token form="' + token[0] + '" tag="' + entryParts[1][0:len(entryParts[1]) - 1] + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                        xml.close()
                        
                        
                        #Change the info of the current token and show it, only if is not the last one
                        if tokens[token[1] + numberSelectedTokens][1] + 1 < len(tokens):
                            token[0] = tokens[token[1] + numberSelectedTokens + 1][0]
                            token[1] = tokens[token[1] + numberSelectedTokens + 1][1]
                            token[2] = 0
                            
                            self.tokenVar.set(token[0])
                            self.statusVar.set(selectedText + "\n" + str(token[1]))
                            self.multiTokenVar.set("1")
                        
                        
                            #Refresh context after token
                            self.context2Var.set("")
                            
                            y=1
                            p2= False
                            lastWord = False
                            
                            if token[1] + 1 == len(tokens):
                                y = 11
                                lastWord = True
                                
                            while y < 10:
                                
                                
                                if tokens[token[1] + y][0] in punctuation1:
                                    self.context2Var.set(self.context2Var.get() + tokens[token[1]+y][0])
                                    
                                elif tokens[token[1] + y][0] in punctuation2:
                                    self.context2Var.set(self.context2Var.get() + " " + tokens[token[1]+y][0])
                                    p2 = True
                                    
                                else:
                                    if p2 == True:
                                        self.context2Var.set(self.context2Var.get() + tokens[token[1] + y][0])
                                        p2 = False
                                    
                                    else:
                                        self.context2Var.set(self.context2Var.get() + " " + tokens[token[1] + y][0])
                                
                                if tokens[token[1] + y][1] + 1 >= len(tokens):
                                    y = 11
                                
                                else:
                                    y = y + 1
                                
                            #Refresh context before token
                            
                            
                            if token[1] >= 10:
                                y=1
                                p2= False
                                self.context1Var.set("")
                                
                                while y <= 10:
                                    
                                    
                                    if tokens[token[1] - y][0] in punctuation1:
                                        self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                        
                                    elif tokens[token[1] - y][0] in punctuation2:
                                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                        p2 = True
                                        
                                    else:
                                        if p2 == True:
                                            self.context1Var.set(tokens[token[1] - y][0]  + self.context1Var.get())
                                            p2 = False
                                        
                                        else:
                                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                            
                                    y = y + 1
                            
                            else:
                                y=1
                                p2= False
                                self.context1Var.set("")
                                
                                while y <= token[1]:
                                    
                                    
                                    if tokens[token[1] - y][0] in punctuation1:
                                        self.context1Var.set(tokens[token[1]-y][0] + self.context1Var.get())
                                        
                                    elif tokens[token[1] - y][0] in punctuation2:
                                        self.context1Var.set(tokens[token[1]-y][0] + " " + self.context1Var.get())
                                        p2 = True
                                        
                                    else:
                                        if p2 == True:
                                            self.context1Var.set(tokens[token[1] - y][0] + self.context1Var.get())
                                            p2 = False
                                        
                                        else:
                                            self.context1Var.set(tokens[token[1] - y][0] + " " + self.context1Var.get())
                                            
                                    y = y + 1
                                    
                            
                            
                            #Search again on dictionary first the multitoken then the single one, if find the token, starts the while again, if not, the program cotinues on manual mode.
                            
                            wordOnDict = False
                            #Only if token is not the last one, search multitokens
                            
                            if isEnd == False:
                                if token[1] + 3 <= len(tokens):
                                    patron = "entry_ " + token[0].lower() + " " + tokens[token [1] + 1][0].lower()
                                    for e in entries:
                                        
                                        if e.find(patron) >= 0:
                                            entry = e
                                            multitoken = entry[6:-14]
                                            entryTokens = word_tokenize(multitoken)
                                            multitoken2 = []
                                            multitoken3 = []
                                            
                                            #Only continues if current piece of text extension can have the found expression
                                            tokensLeft = len(tokens) - token[1]
                                            if tokensLeft >= len(entryTokens):
                                                count = 0
                                                for t in entryTokens:
                                                    multitoken2.append(entryTokens[count])
                                                    multitoken3.append(tokens[token[1] + count][0])
                                                    count = count + 1
                                                
                                                if multitoken3 == multitoken2:
                                                    isMultiToken = True
                                                    wordOnDict = True
                                                    #if is just one before the last, search, but no continues searching the next time the while comes here
                                                    if token[1] + 2 > len(tokens):
                                                        isEnd = True    
                                                    break
                                
                            
                                if isMultiToken == False:
                                    patron = "entry_ " + token[0].lower() + " *****"
                                    
                                    for e in entries:
                                        
                                        if patron in e:
                                            entry = e
                                            wordOnDict = True                        
                                            if token[1] + 1 > len(tokens):
                                                isEnd = True
                                            break
                            
                        
                        #If in automatic search, token is the last one
                        else:
                            #Open the exit xml and write the last line of the file
                            xml = codecs.open(xmlDir, "a", "utf-8")
                            xml.write('\n</text>')
                            xml.close()
                            
                            #Clean the token box and his info
                            self.tokenVar.set("")
                            self.statusVar.set(selectedText + "\n" + "none")
                            self.multiTokenVar.set("1")
                            self.Tag.delete(0, tk.END)
                            self.context1Var.set("")
                            self.context2Var.set("") 
                            
                            #Show an advice aking for select another text.
                            print(tk.messagebox.showwarning(message="This text is completely tagged, select another one", title="Tagging completed"))
                            break
                
                #If token is the last token on document.
                else:
                    
                    #Open the exit xml and write the current token info. Then, close the last line of the file.
                    xml = codecs.open(xmlDir, "a", "utf-8")
                    xml.write('\n<token form="' + token[0] + '" tag="' + self.Tag.get() + '" id="t.' + str(token[1]) + "." + str(token[2] + 1) + '"/>')
                    xml.write('\n</text>')
                    xml.close()
                    
                    #Open dict and write the new token with his tag, then organize it
                    dictionaryRead = codecs.open(dictDir, "r", "utf-8")
                    entries = dictionaryRead.readlines()
                    newEntry = ("entry_ " + token[0].lower() + " ***** " + self.Tag.get() + '\n')
                    entries.append(newEntry)
                    entries.sort()
                    dictionaryRead.close()
                    
                    #Write new organized dictionary in file
                    dictionaryWrite = codecs.open(dictDir, "w", "utf-8")
                    dictionaryWrite.writelines(entries)
                    dictionaryWrite.close()
                    
                    #Clean the token box and his info
                    self.tokenVar.set("")
                    self.statusVar.set(selectedText + "\n" + "none")
                    self.multiTokenVar.set("1")
                    
                    #Refresh select boxes and clean tag box
                    self.Combo1.current(0)
                    self.Combo2["values"] = [""]
                    self.Combo2.config(state="disabled")
                    self.Combo2.current(0)
                    self.Combo3["values"] = [""]
                    self.Combo3.config(state="disabled")
                    self.Combo3.current(0)
                    self.Combo4["values"] = [""]
                    self.Combo4.config(state="disabled")
                    self.Combo4.current(0)
                    self.Combo5["values"] = [""]
                    self.Combo5.config(state="disabled")
                    self.Combo5.current(0)
                    self.Combo6["values"] = [""]
                    self.Combo6.config(state="disabled")
                    self.Combo6.current(0)
                    self.Combo7["values"] = [""]
                    self.Combo7.config(state="disabled")
                    self.Combo7.current(0)
                    
                    self.Tag.delete(0, tk.END)
                    
                    #Show and advice aking for select another text.
                    print(tk.messagebox.showwarning(message="This text is completely tagged, select another one", title="Tagging completed"))
                
            #If Tag textbox is empty... show an advice.
            else:
                print(tk.messagebox.showwarning(message="You have no introduced any tag", title="Empty Tag"))
        
        #If there's no nothing on token textbox
        else:
            print(tk.messagebox.showwarning(message="Select a text in order to start tagging", title="No text selected"))
            
                
    def browseDir(self):
        corpusDir0 = filedialog.askdirectory()
        if corpusDir0:
            self.CorpusDirectory.insert(0, corpusDir0)
            
        
    def browseDic(self):
        dictionaryiDir0 = filedialog.askopenfilename()
        if  dictionaryiDir0:
            self.DictionaryFile.insert(0, dictionaryiDir0)
            

#Here are all the variables we will need
      
corpusDir = ""
dictDir = ""
exitDir = ""
projectName = ""
saveDir = ""
xmlDir= ""

textsNames =  [] 
selectedTextDir = ""
selectedText = ""
tokens = []
token = ["", 0, 0] 
numberSelectedTokens = 1

punctuation1 = (".", ",", ":", ";", "!", "?", '”', "%", ")", "]", "}")
punctuation2 = ("¿", "¡", '“', "(", "[", "{", "$")

adjectiveOptions = [("Type", "Ordinal O",  "Qualificative Q", "Possessive P"), ("Degree", "Superlative S", "Evaluative V"), ("Genere", "Feminine F", "Masculine M", "Common C"), ("Number", "Singular S", "Plural P", "Invariable N"), ("Possessor person", "1", "2", "3"), ("Possessor number", "Singular S", "Plural P", "Invariable N")]
conjunctionOptions = [("Type", "Coordinating C", "Subordinating S")]
determinerOptions = [("Type", "Article A", "Demonstrative D", "Indefinite I", "Possessive P", "Interrogative T", "Exclamative E"), ("Person", "1", "2", "3"), ("Genere", "Feminine F", "Masculine M", "Common C"), ("Number", "Singular S", "Plural P", "Invariable N"),("Possessor number", "Singular S", "Plural P", "Invariable N")]
nounOptions = [("Type", "Common C", "Proper P"), ("Genere", "Feminine F", "Masculine M", "Common C"), ("Number", "Singular S", "Plural P", "Invariable N"), ("Neclass", "Person S", "Location G", "Organization O", "Other V"), ("Degree", "Evaluative V")]
pronounOptions = [("Type", "Demonstrative D", "Exclamative E", "Indefinite I", "Personal P", "Relative R", "Interrogative T"), ("Person", "1", "2", "3"), ("Genere", "Feminine F", "Masculine M", "Common C"), ("Number", "Singular S", "Plural P", "Invariable N"), ("Case", "Nominative N", "Accusative A", "Dative D", "Oblique O"), ("Polite", "Yes P")]
adverbOptions = [("Type", "Negative N", "General G")]
adpositionOptions = [("Type", "Preposition P", "Postposition S", "Circumposition C", "Particle Z")]
verbOptions = [("Type", "Main M", "Auxiliary A" "Semiauxiliary S"), ("Mood", "Indicative I", "Subjunctive S", "Imperative M", "Participle P", "Gerund G", "Infinitive N"), ("Tense", "Present P", "Imperfect I", "Future F", "Past S", "Conditional C"), ("Person", "1", "2", "3"), ("Number", "Singular S", "Plural P", "Invariable N"), ("Genere", "Feminine F", "Masculine M", "Common C")]
numberOptions =[("Type", "Partitive d", "Currency m", "Percentage p", "Unit u" )]
punctuationOptions = [("Type", "Period Fp", "Comma Fc", "Colon FD", "Semicolon Fx", "Questionmark close Fit", "Questionmark open Fia", "Exclamationmark close Fat", "Exclamationmark open Faa", "Parenthesis close Fpt", "Parenthesis open Fpa", "Quotation Fe", "Quotation close Frc", "Quotation open Fra", "Curlybracket close Flt", "Curlybracket open Fla", "Suspension points Fs", "Hyphen Fg", "Other Fz", "Percentage Ft", "Slash Fh", "Squarebracket close Fct", "Squarebracket open Fca")]

savedSesionsDir = os.path.join(os.getcwd(), "saved")
savedSesions= ["Saved Sesions"]

lastWord = False

for doc in os.listdir(savedSesionsDir):
    doc1 = doc.split(".")        
    savedSesions.append(doc1[0])
print("UnderRL Tagger will start soon, please don't close this window")
main_window = tk.Tk()
main_window.iconbitmap(os.getcwd() + "\\UnderRL.ico")
app = Application(main_window)


app.mainloop()






