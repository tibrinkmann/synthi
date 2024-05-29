import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
#from customtkinter import * # type: ignore
import pickle
import os
import subprocess

ANZAHL_PRESETS = 0

# PyAudio für

class App(tk.Tk):

    def __init__(self):

        # main setup
        super().__init__()
        self.title("App")
        self.attributes('-fullscreen', True)

        # widgets
        self.menu = Menu(self)
        self.menu.pack(side="top", fill="x")

        # run
        self.mainloop()

class Preset(ttk.Frame):

    # Constructor
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.input = "default"
        self.input_options = ["Midi" , "XLR" , "AUX"]
        self.waveform = "default"
        self.waveform_options = ["Sine" , "Square" , "Saw"]
        self.envelope = "default"
        self.overtones = "default"
        self.overtone_options = ["set" , "free"]
        self.fx = "none"
        self.preset_index = ANZAHL_PRESETS + 1
        self.widgets = []
        #self.create_widgets()

    def getInput(self):
        return self.input

    def getAnzahlPresets(self):
        return self.preset_index

    def test():
        print("Test")

    def go_back(self,frame):
        frame.destroy()

    # function for saving presets
    def save_preset(self):
        widget_data = {
            "name": self.name,
            "labels": {
                "name_label_text": self.name,
                "input_label_text": "Select input source:",
                "waveform_label_text": "Select Wavefrom:",
                "overtone_label_text": "Select overtone setting:"
            },
            "comboboxes": {
                "input_options": self.input_options,
                "input_default": self.input,
                "waveform_options": self.waveform_options,
                "waveform_default": self.waveform,
                "overtone_options": self.overtone_options,
                "overtone_default": self.overtones
            },
            "button_text": {
                "load_button_text": "Load",
                "save_button_text": "Save",
                "back_button_text": "Back"
            }
        }
        dir = r"/home/synthi/synthi/Presets"
        file_path = os.path.join(dir, self.name + ".pickle")
        try:
            with open(file_path, "wb") as file:
                pickle.dump(widget_data, file)
        except OSError:
            messagebox.showerror("Couldn´t save Preset.")

    # Save-function to save the selected settings
    def save_settings(self,frame, selected_input, selected_waveform, selected_overtone ):
        self.input = selected_input
        self.waveform = selected_waveform
        self.overtones = selected_overtone
        print("Input: " + selected_input + " ||  Waveform: " + selected_waveform + " ||  overtone: " + selected_overtone)
        self.save_preset()
        frame.destroy()

    def load_synth(self):
        syn = ["python3", "/home/synthi/synthi/keyboard_synth.py"]
        subprocess.run(syn)
        return

    # extra function for saving the settings because you cant put parameters in the "command=..."- function thats is bound to the button
    # def get_settings(self, frame):
    #     save_settings(self,frame, input_menu.get(), waveform_menu.get(), overtone_menu.get() )

    # function for loading the saved preset
    def load_preset(self, preset_name):
        # the Frame, in which the widgets for the preset are layed down
        frame = tk.Toplevel(self.master)
        frame.attributes('-fullscreen', True)
        dir = r"/home/synthi/synthi/Presets"
        file_path = os.path.join(dir, preset_name + ".pickle")
        try:
            with open(file_path, "rb") as file:
                widget_data = pickle.load(file)
                # Erstellen und hinzufügen der Labels
                name_label = ttk.Label(frame, text=widget_data["labels"]["name_label_text"], font=("Couruer", 18))
                name_label.pack(side="top", anchor="n", pady=10)

                input_label = ttk.Label(frame, text=widget_data["labels"]["input_label_text"], font=("Couruer", 12))
                input_label.pack(side="top", anchor="n")

                input_menu = ttk.Combobox(frame, values=widget_data["comboboxes"]["input_options"], width=27, height=10)
                input_menu.set(widget_data["comboboxes"]["input_default"])
                input_menu.pack(side="top", anchor="n", pady=5)

                waveform_label = ttk.Label(frame, text=widget_data["labels"]["waveform_label_text"], font=("Couruer", 12))
                waveform_label.pack(side="top", anchor="n")

                waveform_menu = ttk.Combobox(frame, values=widget_data["comboboxes"]["waveform_options"], width=27, height=10)
                waveform_menu.set(widget_data["comboboxes"]["waveform_default"])
                waveform_menu.pack(side="top", anchor="n", pady=5)

                overtone_label = ttk.Label(frame, text=widget_data["labels"]["overtone_label_text"], font=("Couruer", 12))
                overtone_label.pack(side="top", anchor="n")

                overtone_menu = ttk.Combobox(frame, values=widget_data["comboboxes"]["overtone_options"], width=27, height=10)
                overtone_menu.set(widget_data["comboboxes"]["overtone_default"])
                overtone_menu.pack(side="top", anchor="n", pady=5)

                # Erstellen und hinzufügen der Buttons
                load_button = ttk.Button(frame, text=widget_data["button_text"]["load_button_text"], width=30, command=self.load_synth)
                load_button.pack(side="top", anchor="n", pady=5)

                save_button = ttk.Button(frame, text=widget_data["button_text"]["save_button_text"], width=30, command=lambda: self.save_settings(
                                                                                frame,input_menu.get(), waveform_menu.get(), overtone_menu.get() ))
                save_button.pack(side="top", anchor="n", pady=5)

                back_button = ttk.Button(frame, text=widget_data["button_text"]["back_button_text"], command=lambda:self.go_back(frame=frame), width=30)
                back_button.pack(side="top", anchor="n", pady=5)

        except FileNotFoundError:
            messagebox.showerror("Couldn´t load Preset because there is no file with the Presetname.")

    # Main function for the widgets
    def create_widgets(self):

        # the Frame, in which the widgets for the preset are layed down
        frame = tk.Toplevel(self.master)
        frame.attributes('-fullscreen', True)
        frame.title(self.name)
        #+self.widgets.append(frame)

        # Label for the Preset
        label = ttk.Label(frame, text=self.name, font=("Couruer", 18))
        label.pack(side="top", anchor="n", pady=10)
        self.widgets.append(label)

        #label for input selector
        input_label = ttk.Label(frame, text="Select input source:", font=("Couruer", 12))
        input_label.pack(side="top", anchor="n")
        self.widgets.append(input_label)
        # menu for input selection
        input_menu = ttk.Combobox(frame, values=self.input_options, width=27, height=10)
        if self.input == "default":
            input_menu.set("Select Input")
        else:
            input_menu.set(self.input)
        input_menu.pack(side="top", anchor="n", pady=5)
        self.widgets.append(input_menu)

        #label for Waveform selector
        waveform_label = ttk.Label(frame, text="Select Wavefrom:", font=("Couruer", 12))
        waveform_label.pack(side="top", anchor="n")
        self.widgets.append(waveform_label)
        # menu for waveform selection
        waveform_menu = ttk.Combobox(frame, values=self.waveform_options, width=27, height=10)
        if self.waveform == "default":
            waveform_menu.set("Select Wavefrom")
        else:
            waveform_menu.set(self.waveform)
        waveform_menu.pack(side="top", anchor="n", pady=5)
        self.widgets.append(waveform_menu)

        #label for overtone selector
        overtone_label = ttk.Label(frame, text="Select overtone setting:", font=("Couruer", 12))
        overtone_label.pack(side="top", anchor="n")
        self.widgets.append(overtone_label)
        # menu for input selection
        overtone_menu = ttk.Combobox(frame, values=self.overtone_options, width=27, height=10)
        if self.overtones == "default":
            overtone_menu.set("Select overtone setting")
        else:
            overtone_menu.set(self.overtones)
        overtone_menu.pack(side="top", anchor="n", pady=5)
        self.widgets.append(overtone_menu)

        # load button
        load_button = ttk.Button(frame, text="Load", width=30, command=self.load_synth)
        load_button.pack(side="top", anchor="n", pady=5)
        self.widgets.append(load_button)

        # save button
        save_button = ttk.Button(frame, text="Save", width=30, command=lambda:self.save_settings(
                                                                frame,input_menu.get(), waveform_menu.get(), overtone_menu.get()))
        save_button.pack(side="top", anchor="n", pady=5)
        self.widgets.append(save_button)

        # back button
        back_button = ttk.Button(frame, text="Back", command=lambda:self.go_back(frame=frame), width=30)
        back_button.pack(side="top", anchor="n", pady=5)
        self.widgets.append(back_button)



# Menu-class in which the main Menu is setup
# Presets can be created and listed here
class Menu(ttk.Frame):

    #Init function that is needed in every class
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background='grey').pack(expand=True, fill="both")
        self.place(x = 0, y=0, relwidth=1, relheight=1)
        self.create_widgets()
        self.buttons = []
        self.presets = []

    # function for focus shifts
    def focus_up(self,event):
        current_widget = self.focus_get()
        if event.keysym == 'Down':
            #print("Down key was pressed")
            current_widget = self.tk_focusPrev()
        elif event.keysym == 'Up':
            #print("Up key was pressed ")
            current_widget = self.tk_focusNext()
        current_widget.focus_set()

    # functon for enter as mouseclicks
    def enter_to_click(self,event):
        if event.keysym == "Return":
            current_widget = self.focus_get()
            current_widget.invoke()

    # functin for saving the newly created button
    def load_buttons(self,name):
        preset = Preset(name)

        dir = r"/home/synthi/synthi/Buttons"
        file_path = os.path.join(dir, name + ".pickle")
        try:
            with open(file_path, "rb") as file:
                widget_data = pickle.load(file)
                loaded_button = ttk.Button(self, text=widget_data["name"], width=30, command=lambda:preset.load_preset(name))
                loaded_button.pack(side="top", anchor="n", pady=5)
                loaded_button.bind("<Up>", self.focus_up)
                loaded_button.bind("<Down>", self.focus_up)
                loaded_button.bind("<Return>", self.enter_to_click)

        except FileNotFoundError:
            messagebox.showerror("Could not load button!")

    # function for saving button for new preset
    def save_button(self,name):
        widget_data = {
            "name": name,
        }
        dir = r"/home/synthi/synthi/Buttons"
        file_path = os.path.join(dir, name + ".pickle")
        try:
            with open(file_path, "wb") as file:
                pickle.dump(widget_data, file)
        except OSError:
            messagebox.showerror("Couldn´t save Button.")

    # function for the "go back" button - deletes the toplevel frame
    def go_back(self,top):
        top.destroy()


    # Function to create a new button and place it on the menu
    def create_button_with_name(self, entry, top):
        # Get the text from the entry field
        button_name = entry.get()
        # if no name is given -> give standard name
        if len(button_name) == 0:
            button_name = "Preset 1"
        # create new Preset
        new_preset = Preset(button_name)
        self.presets.append(new_preset)
        new_button = ttk.Button(self, text=button_name, width=30, command=new_preset.create_widgets)
        new_button.pack(side="top", anchor="n", pady=5)
        new_button.bind("<Up>", self.focus_up)
        new_button.bind("<Down>", self.focus_up)
        new_button.bind("<Return>",self.enter_to_click)
        self.buttons.append(new_button)
        self.save_button(button_name)

        entry.destroy()  # Destroy the entry field after creating the button
        #create_button.destroy()
        #label.destroy()
        top.destroy()

    # function for creating a new button for a new preset
    def create_new_button(self):

        # create toplevel frame on top of the main menu-frame
        top = tk.Toplevel(self.master)
        top.attributes('-fullscreen', True)
        top.title("New Preset")


        # Label for entry field
        label = ttk.Label(top, text="Preset Name:", width=30)
        label.pack(side="top", anchor="n",pady=5)
        # Entry field for user input
        entry = ttk.Entry(top, width=30)
        entry.pack(side="top", anchor="n")
        entry.focus_set()
        entry.bind("<Up>", self.focus_up)
        entry.bind("<Down>", self.focus_up)
        entry.bind("<Return>",self.enter_to_click)

        # Button to create button with entered name
        create_button = ttk.Button(top, text="Create", command=lambda:self.create_button_with_name(entry=entry,top=top), width=30)
        create_button.pack(side="top", anchor="n", pady=5)
        create_button.bind("<Up>", self.focus_up)
        create_button.bind("<Down>", self.focus_up)
        create_button.bind("<Return>",self.enter_to_click)


        back_button = ttk.Button(top, text="Back", command=lambda:self.go_back(top=top), width=30)
        back_button.pack(side="top", anchor="n", pady=5)
        back_button.bind("<Up>", self.focus_up)
        back_button.bind("<Down>", self.focus_up)
        back_button.bind("<Return>",self.enter_to_click)

    # creates the widgets in the main menu -> the "create new"-Button and the "Exit"-Button
    def create_widgets(self):

        # The Button to create a new Preset
        button1 = ttk.Button(self, text="Create New", command=self.create_new_button, width=30)
        button1.pack(side="top", anchor="n", pady=5)
        button1.focus_set()
        button1.bind("<Up>", self.focus_up)
        button1.bind("<Down>", self.focus_up)
        button1.bind("<Return>",self.enter_to_click)


        # The Exit Button
        exit_button = ttk.Button(self, text="Exit", command=self.quit, width=30)
        exit_button.pack(side="top", anchor="n", pady=5)
        exit_button.bind("<Up>", self.focus_up)
        exit_button.bind("<Down>", self.focus_up)
        exit_button.bind("<Return>",self.enter_to_click)


        files = os.listdir(r"/home/synthi/synthi/Buttons")
        pickle_files = [file for file in files if file.endswith(".pickle")]
        if pickle_files:
            #print("Buttons gefunden")
            for file in pickle_files:
                filename, ending = os.path.splitext(file)
                self.load_buttons(filename)

App()