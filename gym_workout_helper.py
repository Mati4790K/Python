from tkinter import *
import datetime

class Application(Frame):
    def __init__(self, master, variable):
        """ Initialize Frame. """
        super(Application, self).__init__(master)  
        self.grid()
        self.OptionList = open("list.txt", "r")
        self.sets = 0
        self.arms = 0
        self.legs = 0
        self.back = 0
        self.abs = 0
        self.chest = 0
        self.user = 0
        self.create_widgets(variable, self.OptionList)
        self.OptionList.close()
        self.total_1_volume = 0.0
        self.total_2_volume = 0.0
        self.total_3_volume = 0.0
        self.total_4_volume = 0.0
        self.total_5_volume = 0.0
        self.total_6_volume = 0.0

    def create_widgets(self,variable,OptionList):
        """ Create widgets to get workout information and to display it. """
        # create instruction label
        Label(self,
              text = "Select your exercise"
              ).grid(row = 0, column = 0, columnspan = 2, sticky = W)


        variable.set("Arms")
        self.popupMenu = OptionMenu(self, variable, *OptionList)
        self.popupMenu.grid(row = 1, column = 0, sticky = W)


        # create a label and text entry for a verb
        Label(self,
              text = "Add new exercise"
              ).grid(row = 0, column = 2, sticky = W)
        
        self.new_exercise = Entry(self)
        self.new_exercise.grid(row = 1, column = 2, sticky = W)

        # create add exercise button
        Button(self,
               text = "Add exercise",
               command = lambda: self.add_exercise(self.popupMenu,variable)
               ).grid(row = 1, column = 3)

        
     
        # create a label for reps and weight
        Label(self,
              text = "Reps:"
              ).grid(row = 5, column = 0, sticky = E)

        self.reps = Entry(self)
        self.reps.grid(row = 5, column = 1, sticky = W)

        Label(self,
              text = "Your set data:"
              ).grid(row = 4, column = 0, sticky = E)

        Label(self,
              text = "Weight in kg:"
              ).grid(row = 5, column = 2, sticky = E)

        self.weight = Entry(self)
        self.weight.grid(row = 5, column = 3, sticky = W)

        # create an add set button        
        Button(self,
               text = "Add your set",
               command = lambda: self.add_set(variable)
               ).grid(row = 6, column = 0, sticky = W)

        self.story_txt = Text(self, width = 75, height = 25, wrap = WORD)
        self.story_txt.grid(row = 7, column = 0, columnspan = 4)

        # create a recommend button        
        Button(self,
               text = "Recommend training",
               command = lambda: self.recommend(self.reps, self.weight, variable)
               ).grid(row = 6, column = 3, sticky = E)


    def recommend(self, reps, weight, popupMenu):
        exercise = popupMenu.get()
        r_reps = float(reps.get())
        r_weight = float(weight.get())
        suggested_weight = r_weight
        suggested_reps = r_reps


        #perform initial calculations
        if r_reps >= 6 and r_reps < 9:
            suggested_reps = r_reps + 1
        elif r_reps >= 3 and r_reps < 6:
            suggested_reps = r_reps - 1
        elif r_reps > 0 and r_reps < 3:
            suggested_reps = r_reps
            suggested_weight = r_weight - 2.5
        elif r_reps > 9 and r_weight < 50:
            suggested_weight = r_weight + 2.5
            suggested_reps = r_reps - 3
        elif suggested_reps > 6 and suggested_weight > 60:
            suggested_reps -= 1
        else:
            suggested_weight = r_weight + 5
            suggested_reps = r_reps - 1


        #calculate recommended volume
        r_volume = suggested_reps * suggested_weight


        #run this loop until recommended volume is higher than the current volume 
        while r_volume < self.total_1_volume or r_volume < self.total_2_volume or r_volume < self.total_3_volume or r_volume < self.total_4_volume or r_volume < self.total_5_volume or r_volume < self.total_6_volume:
            suggested_reps += 1
            r_volume = suggested_reps * suggested_weight
            if suggested_reps > 9 and suggested_weight < 60:
                suggested_weight += 2.5
                suggested_reps -= 3
            elif suggested_reps > 6 and suggested_weight >= 60:
                suggested_weight += 5
            elif suggested_reps < 4 and suggested_weight >= 60:
                suggested_weight -= 2.5
                
            r_volume = suggested_reps * suggested_weight


        suggestion = str(exercise) + "\nSuggested reps: " + str(suggested_reps) + "\nSuggested weight: " + str(suggested_weight) + "kg"

        self.story_txt.delete(0.0, END)
        self.story_txt.insert(0.0, suggestion)
        
    def add_set(self, popupMenu):
        """ Fill text box with workout history based on user input. """
        # get values from the GUI
        exercise = popupMenu.get()
        setNumber = 0

        reps = self.reps.get()
        weight = self.weight.get()

        #add set amount and calculates the volume for each exercise
        if exercise == "Arms" or exercise == "Arms\n":
            self.arms += 1
            setNumber = self.arms
            self.total_1_volume = float(reps) * float(weight)
        elif exercise == "Legs" or exercise == "Legs\n":
            self.legs += 1
            setNumber = self.legs
            self.total_2_volume = float(reps) * float(weight)
        elif exercise == "Back" or exercise == "Back\n":
            self.back += 1
            setNumber = self.back
            self.total_3_volume = float(reps) * float(weight)
        elif exercise == "Chest" or exercise == "Chest\n":
            self.chest += 1
            setNumber = self.chest
            self.total_4_volume = float(reps) * float(weight)
        elif exercise == "Abs" or exercise == "Abs\n":
            self.abs += 1
            setNumber = self.abs
            self.total_5_volume = float(reps) * float(weight)
        else:
            self.user += 1
            setNumber = self.user
            self.total_6_volume = float(reps) * float(weight)
                    
               
        # create the workout
        workout = "  " + exercise     
        workout += "  Set " + str(setNumber) + " : " + reps + " reps;" + " Weight: " + weight + "kg\n"

        text_file = open("workout_database.txt", "a+")
        self.write_file(workout)
        text_file.close()
        text_file = open("workout_database.txt", "r")
        whole_text = text_file.read()
        

        # display the workout
        self.story_txt.delete(0.0, END)
        self.story_txt.insert(0.0, whole_text)
        text_file.close()

    def add_exercise(self, popupMenu, variable):
        
        text_file = open("list.txt", "a+")
        text_file.write("\n" + self.new_exercise.get())

        text_file.seek(0)
        text_file.close()

        self.update_list(variable)

    def write_file(self, workout):
        
        text_file = open("workout_database.txt", "a+")
        text_file.write(workout)

        text_file.seek(0)
        text_file.close()

    def update_list(self, variable):
        # Clear the menu.
        new_choices = open("list.txt", "r")
        menu = self.popupMenu['menu']
        menu.delete(0, 'end')
        for choice in new_choices:
            # Add menu items.
            menu.add_command(label=choice, command=lambda choice=choice: variable.set(choice))
        new_choices.close()
        self.new_exercise.delete(0, 'end')
    
# main
root = Tk()
root.title("Gym Workout Helper")
tkvar = StringVar(root)

x = datetime.datetime.now()

day = x.strftime("\n%A\n")
date = str(x.day) + "/" + str(x.month) + "/" + str(x.year)
time = x.strftime(" %X\n\n")
text_file = open("workout_database.txt", "a+")
text_file.write(day + date + time)
text_file.close()

app = Application(root,tkvar)
root.mainloop()
