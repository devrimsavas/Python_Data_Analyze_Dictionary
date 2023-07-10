from dictionary_people import person_dict #import data from another file as dictionary
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np


b_captions=["Get Names"," Add new Person"," Show Records",
"Search in Records"," Add New Interest",
"Gender&Age Analyzing"," Meta Analyzing","...",
"Search a Person","Search Activity"," Exit"]




#Embedded graphic class
class EmbeddedGraph:
    def __init__(self, root, figure, xpos, ypos):
        self.canvas = FigureCanvasTkAgg(figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=xpos, y=ypos)


#let create button class so we do not need to do it again and again.

class Fbutton:
    def  __init__(self,root,b_caption,xsize,ysize,xpos,ypos,**kwargs):
        self.button=Button(root,text=b_caption,width=xsize,height=ysize,font=("Tahoma",12),borderwidth=3,**kwargs)
        self.button.place(x=xpos,y=ypos)

class Fframe: #flat, groove, raised, ridge, solid, or sunken
    def  __init__(self,root,f_caption,xsize,ysize,xpos,ypos,**kwargs):
        #self.frame=LabelFrame(root,text=f_caption,width=xsize,height=ysize,borderwidth=1,bg="beige",relief="solid",labelanchor="n")
        self.frame=LabelFrame(root,text=f_caption,width=xsize,height=ysize,borderwidth=4,relief="sunken",labelanchor="n",**kwargs)
        self.frame.place(x=xpos,y=ypos)
        #labelanchor be e, en, es, n, ne, nw, s, se, sw, w, wn, or ws

#END CLASSES 
#Functions
#exit program
def exit_program():
    exit_box=messagebox.askyesno("Quit program","Are you sure (y/n)")
    if exit_box:
        root.destroy()
        exit()
    else:
        pass

def get_names(dictionary):
    clear_statistic()
    names=dictionary.keys()
    for no,name in enumerate(names):
        #print(f'{no+1}-{name}')
        statistic_textbox.insert(END,f'{no+1}-{name}\n')

def clear_statistic():
    statistic_textbox.delete("1.0",END)

#add person to dictionary
def open_new_person_window():
    hobbies=[]
    global person_dict
    open_new_person=messagebox.askyesno("NEW ENTRY","Do you want to add new person? (y/n)")
    if not open_new_person:
        pass
    else:
        

        def add_person(dictionary):
            new_name=name_entry.get()
            if new_name in dictionary:
                messagebox.showwarning("DOUBLE ENTRY","the given name already exists")
                return
            hobbies=hobbies_textbox.get("1.0",END).splitlines() # take each column as seperate hobby
            dictionary[new_name]={"hobbies":hobbies}
            messagebox.showinfo("Success","Person added succesfully")
            get_names(dictionary)

            #clear entry
            name_entry.delete(0,END)
            hobbies_textbox.delete("1.0",END)
            
        
        new_person_window=Toplevel(statistic_textbox)
        new_person_window.title("ADD NEW PERSON")
        new_person_window.geometry("550x450")
        new_person_window.resizable(False,False)
        new_person_frame=LabelFrame=Fframe(new_person_window,"NEW PERSON ENTRY",480,330,30,20)

        name_label=Label(new_person_frame.frame,text="NAME   :",font=("Tahoma",16)).place(x=5,y=5)
        name_entry=Entry(new_person_frame.frame,width=20,font=("Tahoma",16))
        name_entry.place(x=95,y=5)
        person_interests=Label(new_person_frame.frame,text="ENTER INTERESTS BELOW").place(x=5,y=30)
        hobbies_textbox=Text(new_person_frame.frame,width=40,height=10,wrap="word",font=("Tahoma",16))
        hobbies_textbox.place(x=5,y=50)

        submit_button=Fbutton(new_person_window,"SUBMIT",12,1,30,360,command=lambda:add_person(person_dict))
        exit_button=Fbutton(new_person_window,"EXIT",15,1,170,360,command=new_person_window.destroy)
        new_person_window.mainloop()



def show_dict(dictionary):
    statistic_textbox.delete("1.0", END)
    for no, keys in enumerate(dictionary):
        values = dictionary[keys]
        values_str = ', '.join(map(str, values))  
        values_str = values_str.replace('[', '').replace(']', '').replace('"', '')  
        statistic_textbox.insert(END, f'{no+1}- {keys}, {values_str}\n')



def search_person(dictionary):
    person_to_search=search_person_entry.get()
    if not person_to_search:
        return
    found=False
    statistic_textbox.delete("1.0",END)
    for person,hobbies in dictionary.items():
        if person_to_search.lower() in person.lower():
            found=True
            statistic_textbox.insert(END,f"{person} - {hobbies}")

    if not found:
        messagebox.showinfo("PERSON","PERSON NOT FOUND")

    search_person_entry.delete(0,END)

def search_activity(dictionary):
    index=0
    activity_to_search=search_activity_entry.get().strip()
    if not activity_to_search:
        return
    found=False
    for person,hobbies in dictionary.items():
        if any(activity_to_search.lower() in hobby.lower() for hobby in hobbies[1:]):
            found=True
            index+=1
            statistic_textbox.insert(END,f'{index}-{person}-{hobbies} {activity_to_search.upper()}\n')

    if not found:
        messagebox.showinfo("ACTIVITY","ACTIVITY NOT FOUND")
    search_activity_entry.delete(0,END)


def add_record_to_existed_person():
    hobbies=[]
    global person_dict
    show_dict(person_dict)
    
    def add_new_hobby(dictionary):
        person=name_entry.get()
        if person not in dictionary.keys():
            messagebox.showwarning("non existed person","This person not in the dictionary.Open a new entry")
            return
        hobbies=hobbies_textbox.get("1.0",END).splitlines() # take each column as seperate hobby

        for new_hobby in hobbies:
            if new_hobby not in dictionary[person]:
                dictionary[person].append(hobbies)
        
        show_dict(dictionary)

            #clear entry
        name_entry.delete(0,END)
        hobbies_textbox.delete("1.0",END)

    new_person_window=Toplevel(statistic_textbox)
    new_person_window.title("ADD NEW HOBBY TO EXISTED PERSON")
    new_person_window.geometry("550x450")
    new_person_window.resizable(False,False)
    new_person_frame=LabelFrame=Fframe(new_person_window,"NEW HOBBY ENTRY",480,330,30,20)

    name_label=Label(new_person_frame.frame,text="NAME   :",font=("Tahoma",16)).place(x=5,y=5)
    name_entry=Entry(new_person_frame.frame,width=20,font=("Tahoma",16))
    name_entry.place(x=95,y=5)

    person_new_interests=Label(new_person_frame.frame,text="ENTER NEW INTERESTS BELOW").place(x=5,y=30)
    hobbies_textbox=Text(new_person_frame.frame,width=30,height=8,wrap="word",font=("Tahoma",16))
    hobbies_textbox.place(x=5,y=50)

    submit_button=Fbutton(new_person_window,"SUBMIT",12,1,25,360,command=lambda:add_new_hobby(person_dict))
    exit_button=Fbutton(new_person_window,"EXIT",12,1,150,360,command=new_person_window.destroy)

    new_person_window.mainloop()

def gender_analysis(dictionary):
    statistic_textbox.delete("1.0",END)
    population_number=len(dictionary)
    statistic_textbox.insert("1.0",f'population number: {population_number}\n')
    total_num_males=0
    total_num_females=0
    total_num_unknown=0
    male_word="male"
    female_word="female"
    unknown_word="unknown"
    ages=[]

    for values in dictionary.values():
        if len(values) >= 2:  # Check if the list has at least two elements
            gender = values[0]
            age = values[1]
            
            if gender.lower() == male_word:
                total_num_males += 1
            elif gender.lower() == female_word:
                total_num_females += 1
            elif gender.lower() == unknown_word:
                total_num_unknown += 1

            if age.isdigit():
                ages.append(int(age))
    
    statistic_textbox.insert(END,f'Group members ages: {ages}\n')
    print(ages)
    total_age=sum(ages)
    min_age=min(ages)
    max_age=max(ages)
    average_age=round(total_age/population_number,3)
    median=np.median(ages)
    standard_deviation=np.std(ages)

    stat_text=f"""males: {total_num_males}
females: {total_num_females}
unknown: {total_num_unknown}
minimum age       : {min_age}
maximum age       : {max_age}
average age       : {average_age}
median            : {median}
standard deviation: {standard_deviation}
"""
    statistic_textbox.insert(END,stat_text)
    clear_graphic_frame()

    labels=['Males','Females',"Unknown"]
    sizes=[total_num_males,total_num_females,total_num_unknown]
    fig, axs = plt.subplots(1, 2, figsize=(9.1, 3.7),facecolor="#e2d3dc") #graphic size 
    axs[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    axs[0].axis('equal')
    axs[0].set_title('Gender Distribution')

    # plot histogram on second subplot
    axs[1].hist(ages,bins=5)
    axs[1].set_xlabel('AGE')
    axs[1].set_ylabel('FREQUENCY')
    axs[1].set_title('Age Distribution')

# adjust spacing between subplots and show the plot
    plt.subplots_adjust(wspace=0.4)
    EmbeddedGraph(graphics_holder.frame,fig,5,5)
    #plt.show()
    
def search_item(dictionary):
    search_text=search_text_entry.get()
    search_text_freq=0
    found=False

    for name, values in dictionary.items():
        if any(search_text.lower()  in value.lower()for value in values[1:]):
            
            search_text_freq+=1
            statistic_textbox.insert(END,f'{name} has: {search_text}\n')
            found=True
    statistic_textbox.insert(END,f'\ntotally {search_text_freq} person has {search_text}')
    if not found:
        messagebox.showwarning("RECORD","KEY WORD NOT FOUND")

    search_text_entry.delete(0,END)



def meta_analyzing(dictionary):
    statistic_textbox.delete("1.0",END)
    freq_list=[]
    word_freq={}
    for values in dictionary.values():
        
        #for value in values[2:]: why it made error? 
            #word_freq[value]=word_freq.get(value,0)+1
        if isinstance(values, list):  # Ensure that 'values' is a list before slicing
            for value in values[2:]:
                word_freq[value]=word_freq.get(value,0)+1

    sorted_word_freq=sorted(word_freq.items(),key=lambda x: x[1],reverse=True)
            

    for word,freq in word_freq.items():
        statistic_textbox.insert(END,f'{word}: {freq}\n')

    
    graphic=messagebox.askyesno("GRAPHIC","do you want to see it on a Pie Chart?")

    if graphic:
        clear_graphic_frame()
        fig1,ax1=plt.subplots(facecolor="#e2d3dc")
        #fig, axs = plt.subplots(1, 2, figsize=(8, 3.7),facecolor="white")
        
        plt.pie(word_freq.values(),labels=word_freq.keys())
        plt.subplots_adjust(wspace=0.4)
        EmbeddedGraph(piechart_holder.frame,fig1,2,2)
   
        


def about_program():
    about_window = Toplevel(root)
    about_text = """
This program was written to demonstrate the flexibility and power of the python dictionary.
The program shows records,
adds new contacts, adds new interests to existing contacts. The program displays the gender
and age distribution by creating graphics from the records.As sample data, program uses an external
dictionary. But it is possible to create your own dictionary. 
Devrim Savas Yilmaz
"""


    
    about_window.title("About This Program")
    about_window.geometry("420x260")
    info_text = Text(about_window, width=40, height=10, wrap=WORD, borderwidth=3, spacing3=2, font=("Arial",12 ))
    info_text.place(x=10, y=10)
    info_text.insert(END, about_text)
    info_text.config(state="disabled", bg="beige")
    close_this = Button(about_window, text="CLOSE THIS WINDOW", command=about_window.destroy)
    close_this.place(x=150, y=230)

def donothing():
    #add anything to menu.
    #here for further development for menu
    pass
    

def clear_graphic_frame():
    #no need now since i use 2 different holders
    """
    for widget in graphics_holder.frame.winfo_children():
        widget.destroy()"""
    pass

#prepare Tkinter preface

root=Tk()
root.geometry("1840x960")
root.title("Data & Person Analyze")
root.config(bg="#002240")
root.iconbitmap("icon.ico")
root.resizable(False,False)

#COMPENENTS HOLDERS 
#holder for menu 
menu_holder=Fframe(root,"MENU",210,300,5,10,bg="beige") #w,h,xp,yp

#holder for DATA ENTRY
menu_holder1=Fframe(root,"DATA ENTRY",665,300,1150,10,bg="#8393ca")


#holder for text &statistics 
statistic_holder=Fframe(root,"STATISTIC",920,470,220,10,bg="gray") #w,h,xp,yp

#create scrollvar
scrollbar=Scrollbar(statistic_holder.frame)
scrollbar.place(x=890,y=5,height=440)



#textbox for statistics
statistic_textbox=Text(statistic_holder.frame,width=98,height=23,wrap="word",font=("Tahoma",12),fg="#ffbb00",bg="#002e61")
statistic_textbox.place(x=5,y=5)

scrollbar.config(command=statistic_textbox.yview)


#holder for graphics
graphics_holder=Fframe(root," FREQUENCY GRAPHICS",920,440,220,490,bg="#e2d3dc") #w,h,xp,yp
piechart_holder=Fframe(root,"PIE CHART GRAPHIC",660,600,1150,330,bg="#e2d3dc")




#button sets
bx_size=18
#########MENU BUTTONS
get_names_button=Fbutton(menu_holder.frame,"Get Names",bx_size,1,5,5,command=lambda:get_names(person_dict))

add_new_person_button=Fbutton(menu_holder.frame,"Add Person",bx_size,1,5,45,command=lambda:open_new_person_window())

show_records_button=Fbutton(menu_holder.frame,"Show Records",bx_size,1,5,85,command=lambda:show_dict(person_dict))

add_new_interest_button=Fbutton(menu_holder.frame,"Add New Interest",bx_size,1,5,125,command=lambda:add_record_to_existed_person())

gender_age_button=Fbutton(menu_holder.frame,"Gender&Age Analysis",bx_size,1,5,165,command=lambda:gender_analysis(person_dict))

meta_analyzing_button=Fbutton(menu_holder.frame,b_captions[6],bx_size,1,5,205,command=lambda:meta_analyzing(person_dict))

######DATA ENTRY BUTTONS
search_person_button=Fbutton(menu_holder1.frame,"Search Person",bx_size,1,5,5,command=lambda:search_person(person_dict))

search_in_records_button=Fbutton(menu_holder1.frame,"Search in Records",bx_size,1,5,45,command=lambda:search_item(person_dict))

search_interest_button=Fbutton(menu_holder1.frame,"Search Interest",bx_size,1,5,85,command=lambda:search_activity(person_dict))

clear_statistic_button=Fbutton(menu_holder1.frame,"Clear Statistic",bx_size,1,5,165,command=clear_statistic)

#SEARCH FOR PERSON ENTRY
search_person_entry=Entry(menu_holder1.frame,width=15,font=("Arial",16),borderwidth=2)
search_person_entry.place(x=190,y=5)
#sEARCH FOR ACTIVITY ENTRY
search_activity_entry=Entry(menu_holder1.frame,width=15,font=("Arial",16),borderwidth=2)
search_activity_entry.place(x=190,y=45)

search_text_entry=Entry(menu_holder1.frame,width=15,font=("Arial",16),borderwidth=2)
search_text_entry.place(x=190,y=85)



menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=about_program)
menubar.add_cascade(label="Help", menu=helpmenu)



root.config(menu=menubar)

#END BUTTON SET
root.mainloop()

