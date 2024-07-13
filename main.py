from customtkinter import *
from CTkColorPicker import *
from tkinter import *
from PIL import ImageTk, Image
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox

app = CTk()  # starting loop
app.title("Snakes can Draw")
app.iconbitmap('Icons/logo.ico')
app.geometry("1540x842")
set_appearance_mode("dark")
deactivate_automatic_dpi_awareness()

size = IntVar()
size.set(5)

color = StringVar()
color.set("#e1e1e1")

fontV = StringVar()
fontV.set("Assistant")

preColor = StringVar()
preColor.set("#e1e1e1")

backupColor = StringVar()
backupColor.set("#e1e1e1")

textV = StringVar()
toolsDropV = StringVar()

pre = [0, 0]
now = [0, 0]

undo_list = []
redo_stack = []
current = []
coord_stack = []
alt_stack = []

shape = "paint"

gap_x = 20
gap_y = 20

def undo():
    global undo_list, redo_stack, coord_stack
    if undo_list:
        if shape == "paint":
            last_action = undo_list.pop()
            redo_stack.append(last_action)
            coord_stack.pop()
            for activity in last_action:
                canvas.delete(activity)
        else:
            last_action = undo_list.pop()
            redo_stack.append(last_action)
            coord_stack.pop()
            canvas.delete(last_action)

def redo():
    global undo_list, redo_stack, coord_stack, shape
    if redo_stack:
        last_action = redo_stack.pop()
        undo_list.append(last_action)
        if shape == "paint":
            for c in coord_stack:
                coords = coord_stack.pop()
                alt_stack.append(coords)
                canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())
        elif shape == "rectangle":
            coords = coord_stack.pop()
            canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())
        elif shape == "oval":
            coords = coord_stack.pop()
            alt_stack.append(coords)
            canvas.create_oval(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())
        elif shape == "line":
            coords = coord_stack.pop()
            alt_stack.append(coords)
            canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())
        elif shape == "diamond":
            alt_stack.append(coords)
            coords = coord_stack.pop()
            canvas.create_polygon(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())
        elif shape == "triangle":
            coords = coord_stack.pop()
            alt_stack.append(coords)
            canvas.create_polygon(coords[0], coords[1], coords[2], coords[3], fill=color.get(), width=size.get())

def paint(event):
    global pre, now, current, coord_stack, canvas
    if pre == [0, 0]:
        pre = [event.x, event.y]
        current = []
    else:
        now = [event.x, event.y]
        if "#121212" == color.get():
            activity = canvas.create_polygon(pre[0], pre[1], now[0], now[1], fill=color.get(), outline=color.get(), width=size.get() + 10)  # Increasing eraser size
        else:
            activity = canvas.create_polygon(pre[0], pre[1], now[0], now[1], fill=color.get(), outline=color.get(), width=size.get())
        current.append(activity)
        a, b, c, d = pre[0], pre[1], now[0], now[1]
        other = [a, b, c, d]
        coord_stack.append(other)
        pre = now

def dont_paint(event):
    global undo_list, current, pre
    if current:
        undo_list.append(current)
        redo_stack.clear()
        pre = [0, 0]

def paint_R(event):
    x = event.x
    y = event.y
    canvas.create_arc(x, y, x + size.get(), y + size.get(), fill=color.get(), outline=color.get(), width=size.get())

def Pen():
    if color.get() == "#121212":
        color.set(backupColor.get())
    else:
        color.set(color.get())
    canvas["cursor"] = "tcross"
    shapes("paint")

def Eraser():
    color.set("#121212")
    canvas["cursor"] = DOTBOX
    shapes("paint")

def choose_Color():
    chosen_Color = AskColor(title="Choose Color")
    if chosen_Color:
        color.set(chosen_Color.get())
        backupColor.set(preColor.get())
        preColor.set(color.get())
        selecter.configure(border_color=color.get())
        brush_slider.configure(button_color=color.get(), progress_color=color.get())

def shapes(value):
    global pre, now
    pre = [0, 0]
    now = [0, 0]
    if value == "line":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "line"))
    elif value == "rectangle":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "rectangle"))
    elif value == "oval":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "oval"))
    elif value == "diamond":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "diamond"))
    elif value == "triangle":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "triangle"))
    elif value == "paint":
        canvas.bind("<Button-1>", lambda event: shapes_start(event, "paint"))

def shapes_start(event, shape):
    global pre, now
    pre = [event.x, event.y]
    if shape != "paint":
        canvas.bind("<B1-Motion>", lambda event: shapes_draw(event, shape))
        canvas.bind("<ButtonRelease-1>", shapes_draw_release)
    else:
        canvas.bind("<B1-Motion>", lambda event: paint(event))
        canvas.bind("<ButtonRelease-1>", dont_paint)

def shapes_draw(event, shape):
    global pre, now, current, coord_stack, canvas
    current = []
    now = [event.x, event.y]
    canvas.delete("current_shape")
    activity = 0
    if pre != [0, 0]:
        if shape == "rectangle":
            activity = canvas.create_rectangle(pre[0], pre[1], now[0], now[1], fill="", outline=preColor.get(), tags="current_shape", width=size.get())
            other = [pre[0], pre[1], now[0], now[1]]
        elif shape == "oval":
            activity = canvas.create_oval(pre[0], pre[1], now[0], now[1], fill="", outline=preColor.get(), tags="current_shape", width=size.get())
        elif shape == "line":
            activity = canvas.create_line(pre[0], pre[1], now[0], now[1], fill=preColor.get(), width=size.get(), tags="current_shape")
        elif shape == "diamond":
            activity = canvas.create_polygon((pre[0] + now[0]) / 2, pre[1], now[0], (now[1] + pre[1]) / 2, (pre[0] + now[0]) / 2, now[1], pre[0], (now[1] + pre[1]) / 2, fill="", outline=preColor.get(), tags="current_shape", width=size.get())
        elif shape == "triangle":
            activity = canvas.create_polygon((pre[0] + now[0]) / 2, pre[1], now[0], now[1], pre[0], now[1], fill="", outline=preColor.get(), tags="current_shape", width=size.get())
        current.append(activity)
        a, b, c, d = pre[0], pre[1], now[0], now[1]
        other = [a, b, c, d]
        coord_stack.append(other)

def shapes_draw_release(event):
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.itemconfig("current_shape", tags="")

def textBox():
    canvas.bind("<Button-1>", start_textbox)

def start_textbox(event):
    global textbox_frame, textbox_entry, textbox_x, textbox_y
    textbox_x, textbox_y = event.x, event.y
    textbox_frame = canvas.create_rectangle(textbox_x, textbox_y, textbox_x + 200, textbox_y + 50, outline="red", dash=(2, 2))
    textbox_entry = CTkEntry(app, width=200, font=(fontV.get(), size.get() + 10))
    canvas.create_window(textbox_x + 100, textbox_y + 25, window=textbox_entry)
    textbox_entry.bind("<Return>", finalize_textbox)
    textbox_entry.focus()
def finalize_textbox(event):
    global textbox_frame, textbox_entry, textbox_x, textbox_y
    text = textbox_entry.get()
    canvas.delete(textbox_frame)
    canvas.create_text(textbox_x, textbox_y, text=text, anchor="nw", fill=color.get(), font=(fontV.get(), size.get() + 10))
    textbox_entry.destroy()
    canvas.unbind("<Button-1>")

def update_brush_size(value):
    global size
    size.set(int(value))

def font_changer(value):
    global fontV
    fontV.set(value)

def SaveImg():
    try:
        Loc = filedialog.asksaveasfilename(defaultextension="jpg")
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x + 2, y + 75, x1 - 2, y1 - 2))
        img.save(Loc)
        showImage = messagebox.askyesno("Snakes can Draw", "Do you want to see image?")
        if showImage:
            img.show()
    except Exception as e:
        messagebox.showinfo("Snakes can Draw", "Something went wrong")


frame2 = CTkFrame(app, height=837, width=1535, fg_color="#121212")  # canvas bg
frame2.grid(row=1, column=0)
canvas = CTkCanvas(frame2, height=837, width=1535, bg="#121212", highlightcolor="black")
canvas.grid(row=0, column=0)
tools_frame = CTkFrame(frame2, height=100, width=1760)
tools_frame.grid(row=0, column=0, sticky=N, pady=20)
tools_frame.place()

canvas.bind("<Button-1>", paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", dont_paint)
canvas.bind("<B3-Motion>", paint_R)


pen_img = CTkImage(Image.open("Icons/pen.png").resize((30, 30)))
eraser_img = CTkImage(Image.open("Icons/eraser.png").resize((30, 30)))
color_img = CTkImage(Image.open("Icons/color.png").resize((30, 30)))
save_img = CTkImage(Image.open("Icons/save.png").resize((30, 30)))
text_img = CTkImage(Image.open("Icons/text.png").resize((30, 30)))
undo_img = CTkImage(Image.open("Icons/undo.png").resize((30, 30)))
redo_img = CTkImage(Image.open("Icons/redo.png").resize((30, 30)))
ovrlay = ImageTk.PhotoImage(Image.open("Icons/Snakes Can Draw.png").resize((200, 200)))

canvas.image = ovrlay
canvas.create_image(1370, 700, anchor=NW, image=ovrlay)


brush_slider = CTkSlider(master=tools_frame, from_=1, to=50, number_of_steps=25, button_color="white", progress_color=color.get(), orientation="horizontal", command=update_brush_size, variable=size, button_hover_color="#31303b", corner_radius=1)
brush_slider.grid(row=0, column=7)
pen = CTkButton(text="", master=tools_frame, fg_color="#232329", hover_color="#31303b", command=Pen, image=pen_img, width=50, height=50)
pen.grid(row=0, column=0)
eraserBtn = CTkButton(text="", master=tools_frame, fg_color="#232329", hover_color="#31303b", command=Eraser, image=eraser_img, width=50, height=50)
eraserBtn.grid(row=0, column=1)
selecter = CTkButton(text="", master=tools_frame, fg_color="#232329", command=choose_Color, image=color_img, hover_color="#31303b", width=50, height=50, border_color=preColor.get(), border_width=1)
selecter.grid(row=0, column=3)
saveBtn = CTkButton(text="", master=tools_frame, fg_color="#232329", hover_color="#31303b", command=SaveImg, image=save_img, width=50, height=50)
saveBtn.grid(row=0, column=4)
toolsDrop = CTkOptionMenu(master=tools_frame, variable=toolsDropV, values=["line", "rectangle", "oval", "diamond", "triangle"], command=shapes, fg_color="#232329", button_color="#232329", button_hover_color="#31303b", width=50, height=50)
toolsDrop.grid(row=0, column=2)

txtBtn = CTkButton(text="", master=tools_frame, fg_color="#232329", hover_color="#31303b", command=textBox, image=text_img, width=50, height=50)
txtBtn.grid(row=0, column=5)
fontBtn = CTkOptionMenu(master=tools_frame, fg_color="#232329", command=font_changer, variable=fontV, button_color="#232329", button_hover_color="#31303b", values=["System", "Terminal", "Fixedsys", "Modern", "Roman", "Script", "Courier", "MS Serif", "MS Sans Serif", "Arial"], width=50, height=50)
fontBtn.grid(row=0, column=6)

undoBtn = CTkButton(master=canvas, text="", command=undo, image=undo_img, fg_color="#232329", hover_color="#31303b", width=100, height=50, corner_radius=50)
redoBtn = CTkButton(master=canvas, text="", command=redo, image=redo_img, fg_color="#232329", hover_color="#31303b", width=100, height=50, corner_radius=50)

undoBtn.place(relx=0, rely=1, x=gap_x, y=-gap_y, anchor='sw')
redoBtn.place(relx=0, rely=1, x=gap_x + 100, y=-gap_y, anchor='sw')

app.resizable(False, False)
app.mainloop()  # ending loop