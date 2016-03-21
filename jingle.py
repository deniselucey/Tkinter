# Simple experiment with Tkinter text-highlighting capabilities
#
# Note: time.sleep and tkinter don't seem to work well together-
#       Quit doesn't work; suspect sleep makes event listeners
#       dormant.

from tkinter import *
import time
import sys

NORMALCOLOUR = "white"
HIGHLIGHTCOLOUR = "pink"

# Create and install the widgets
window = Tk()
cursor = Label(window, text = "")
text_box = Text(window, height = 20, width = 80)
quit_button = Button(window, text = "Quit", command = sys.exit)
cursor.pack()
text_box.pack()
quit_button.pack()

# Inject the text into text box
text = \
"""Oh jingle bells jingle bells
jingle all the way!
Oh what fun
it is to ride
In a one horse open sleigh, Hey!
Jingle bells jingle bells
Jingle all the way!
Oh what fun it is to ride
In a one horse open sleigh
"""
text_box.insert(END, text)

# Capture positions of the line breaks
line_breaks = []
for i in range(len(text)):
    if text[i] == "\n":
        line_breaks.append(i)

num_lines = len(line_breaks)

# Pre-pend dummy entry to index line numbers from one not zero
line_breaks = [-1] + line_breaks

# Add a tag to each line
for lineno in range(1, num_lines + 1):
    end = line_breaks[lineno]
    if lineno == 0:
        start = 0
    else:
        start = line_breaks[lineno-1] + 1
    tag = "line"+str(lineno)
    text_box.tag_add(tag, str(lineno)+".0", str(lineno)+".end")

while (True):
   cursor.configure(text = "One more time  . . .")
   cursor.update()
   time.sleep(2)

   # Cycle through lines, highlighting one at a time
   for curr_line_no in range(1, num_lines +1):
       # Show current line number
       cursor.configure(text = "Sing line: "+str(curr_line_no))
       curr_tag = "line"+str(curr_line_no)

       # Highlight current line
       text_box.tag_config(curr_tag, background = HIGHLIGHTCOLOUR)
       text_box.update()

       # Puase one second
       time.sleep(1)

       # Un-highlight line
       text_box.tag_config(curr_tag, background = NORMALCOLOUR)
       text_box.update()

   # Puase for two seconds before repeating
   cursor.configure(text = "Pause for breath  . . .")
   cursor.update()
   time.sleep(2)

mainloop()