#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src import Run
from tkinter import *
import tkinter as tk
import tkinter.font as font
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from src.init import *
matplotlib.use('TkAgg')


#--- window ---
root = tk.Tk()
root.geometry('1300x900')
root.title("Low Energy Adaptive Clustering Hierarchy")
root.configure(bg='orange') 
#------------

#-- Frames ---
left_frame = tk.Frame(root)
left_frame.place(relx=0.03, rely=0.05, relwidth=0.25, relheight=0.9) #26

right_frame = tk.Frame(root, bg='#C0C0C0', bd=1.5)
right_frame.place(relx=0.3, rely=0.05, relwidth=0.65, relheight=0.9)
#---------------

#--- figures ---
figure = plt.Figure(figsize=(5,6), dpi=70)
ax = figure.add_subplot(221)
ay = figure.add_subplot(223)
az = figure.add_subplot(222)
line = FigureCanvasTkAgg(figure, right_frame)
line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)
#----------------------    

def capture(Sensors: list[Sensor], model, round_number):
    n = model.n
    ay.set_xlim(left=0, right=model.x)
    ay.set_ylim(bottom=0, top=model.y)
    n_flag = True
    c_flag = True
    d_flag = True
    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                if n_flag:
                    ay.scatter([sensor.xd], [sensor.yd], c='g', edgecolors='k', label='Nodes')
                    n_flag = False
                else:
                    ay.scatter([sensor.xd], [sensor.yd], c='g', edgecolors='k')
            elif sensor.type == 'C':
                if c_flag:
                    ay.scatter([sensor.xd], [sensor.yd], c='r', edgecolors='k', label='Cluster Head')
                    c_flag = False
                else:
                    ay.scatter([sensor.xd], [sensor.yd], c='r', edgecolors='k')
        else:
            if d_flag:
                ay.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k', label='Dead')
                d_flag = False
            else:
                ay.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k')

    ay.scatter([Sensors[n].xd], [Sensors[n].yd], s=80, c='b', edgecolors='k', label="Sink")
    ay.legend(loc='upper right',  bbox_to_anchor=(1.6, 0.6),prop={'size': 15})
    ay.set_xlabel('Longueur [m]'),ay.set_ylabel('Largeur [m]')
    ay.set_title('Vue sur le réseau au round No: %d' %round_number, y=-0.25)
    ay.spines['bottom'].set_color('black')
    ay.spines['top'].set_color('black')
    ay.spines['left'].set_color('black')
    ay.spines['right'].set_color('black')
    ay.spines['bottom'].set_lw(2)
    ay.spines['top'].set_lw(2)
    ay.spines['right'].set_lw(2)
    ay.spines['left'].set_lw(2)
    ay.set_facecolor('white')
    ay.xaxis.label.set_color('black')
    ay.yaxis.label.set_color('black')


def newSimulation(state:int):
    global App, n, my_model, alive_sensors,sum_energy_left_all_nodes
    n=int(entry1.get())
    p=float(entry2.get())
    En_max=float(entry3.get())
    roundReseau=int(entry4.get())
    App=Run.Simulation(n,p,En_max,roundReseau,state)
    n,my_model,alive_sensors,sum_energy_left_all_nodes,noeuds,model,tour=App.start()
    ax.clear()
    ax.set_xlim(left=0, right=my_model.rmax)
    ax.set_ylim(bottom=0, top=n)
    ax.plot(alive_sensors, color="skyblue"), ax.grid(True)
    ax.set_xlabel('Rounds'),ax.set_ylabel('Nombre de nœuds actifs')
    ax.set_title('Durée de vie des nœuds capteurs')
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_lw(2)
    ax.spines['left'].set_lw(2)
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')          
    ay.clear()

    capture(noeuds,model,tour)

    az.clear()
    az.set_xlim(left=0, right=my_model.rmax)
    az.set_ylim(bottom=0, top=n*my_model.Eo)
    az.plot(sum_energy_left_all_nodes, color="chocolate"), ay.grid(True)
    az.set_xlabel('Rounds'),az.set_ylabel('Energie [J]')
    az.set_title('Energie résiduelle totale dans le réseau')
    az.set_facecolor('white')
    az.spines['bottom'].set_color('black')
    az.spines['left'].set_color('black')
    az.spines['bottom'].set_lw(2)
    az.spines['left'].set_lw(2)
    az.xaxis.label.set_color('black')
    az.yaxis.label.set_color('black')

    line.draw()


def clean():
    ax.clear()
    ay.clear()
    az.clear()
    line.draw()

#--- image ---
image=PhotoImage(file="src/images/formule.png")
#--------------


def f1():
    newSimulation(2)


RH = 0.095

f = font.Font(family='Times New Roman', size=15)

lb2 = Label(left_frame, text = 'Formule:')
lb2.place(rely= 1*(0.1 + RH*0.54))
lb2['font'] = f
Button2 = tk.Button(left_frame,image=image, bg="white", borderwidth=2,command = f1)
Button2.place(rely=1.20*(0.1 + RH*0.54) ,relheight=RH, relwidth=1)

Button4 = tk.Button(left_frame,text="Effacer", borderwidth=2,command = clean, bg="red")
Button4.place(rely= 3*(0.1 + RH*0.54) ,relheight=0.5*RH, relwidth=1)
Button4['font'] = f

info = Label(left_frame, text = '<Cliquez sur la formule ci-dessus>')
info.place(rely= 3.5*(0.1 + RH*0.54))
info['font'] = f
info2 = Label(left_frame, text = 'Vous pouvez changer les valeurs\n des champs ci-dessous')
info2.place(rely= 3.7*(0.1 + RH*0.54))
info2['font'] = f

label1 = Label(left_frame, text = 'Nombre de noeuds')
label1.place(rely= 4.2*(0.1 + RH*0.54))
label1['font'] = f
entry1 = Entry(left_frame)
entry1.place(rely= 4.4*(0.1 + RH*0.54))
entry1.insert(0,100)

label2 = Label(left_frame, text = "Pourcentage de cluster Head: 'P'")
label2.place(rely= 4.8*(0.1 + RH*0.54))
label2['font'] = f
entry2 = Entry(left_frame)
entry2.place(rely= 5*(0.1 + RH*0.54))
entry2.insert(0,0.1)

label3 = Label(left_frame, text = "En_max d'un noeud (joule)")
label3.place(rely= 5.4*(0.1 + RH*0.54))
label3['font'] = f
entry3 = Entry(left_frame)
entry3.place(rely= 5.6*(0.1 + RH*0.54))
entry3.insert(0,5)

label4 = Label(left_frame, text = "Voir le reseau au round No")
label4.place(rely= 6*(0.1 + RH*0.54))
label4['font'] = f
entry4 = Entry(left_frame)
entry4.place(rely= 6.2*(0.1 + RH*0.54))
entry4.insert(0,20)

def main():
    newSimulation(1)
    root.mainloop()

if __name__ == '__main__':
    main()
