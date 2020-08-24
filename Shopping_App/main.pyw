# Shopping Basket with email (version 0.1)
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, END
import string
# Email
import smtplib
from email.message import EmailMessage
import connect

# Root Window
app = Tk()

# Page defaults
bg_color = '#FFFFFF'
fg_color = '#296296'
font_size = 'Arial, 12'


# List Title
def list_title(*args):
    global filename
    global get_title

    # Getter (get title)
    get_title = list_input.get()
    # Cap Words
    get_title = string.capwords(get_title)

    # If title entry is empty, show error
    if get_title == '':
        output_box['text'] = 'Please create a title\nfor your shopping list.'
        output_box.config(fg='#A32627')
    else:
        # If error message exists, clear the output box
        output_box['text'] = ''
        output_box.config(fg=fg_color)

        # Directory for saved lists
        filename = 'My Lists/' + get_title

        try:
            # Write title to file
            with open(filename, 'w') as f_write:
                f_write.write('____  ' + get_title + '  ____\n\n')


            # Read file
            with open(filename) as f_read:
                show_content = f_read.read()


            # Output file content to screen
            output_box['text'] = show_content

        except:
            messagebox.showerror(\
                'Data Error',\
                'Sorry!\n\nWe have experienced an issue\ncollecting your data\n\nPlease tyy again.')

        # Page settings
        # Clear list entry field
        list_entry.delete(0, END)
        # Change list label, button text (for adding to basket)
        list_label['text'] = 'Add items:'
        list_btn['text'] = 'Add +'
        # List button function
        list_btn['command'] = basket
        app.bind('<Return>', basket)


# Counter for added items in basket
counter = 0

# List Title
def basket(*args):
    global counter
    global show_content

    # Getter (get added)
    get_added = list_input.get()

    # If title entry is empty, show error
    if get_added == '':
        output_box['text'] = 'Add items field is empty!\n\nPlease add items\nto your shopping basket.'
        output_box.config(fg='#A32627')
    else:
        # If error message exists, clear the output box
        output_box['text'] = ''
        output_box.config(fg=fg_color)

        # Getter (get added)
        get_added = str(counter+1) + '. ' + list_input.get()
        # Cap Words
        get_added = string.capwords(get_added)

        try:
            # Write added items to file
            with open(filename, 'a') as f_append:
                f_append.write(get_added + '\n')


            # Read file
            with open(filename) as f_read:
                show_content = f_read.read()


            # Counter plus one
            counter +=1
            # Output file content to screen
            output_box['text'] = show_content

        except:
            messagebox.showerror(\
                'Data Error',\
                'Sorry!\n\nWe have experienced an issue\ncollecting your data\n\nPlease tyy again.')

        # Page settings
        # Clear list entry field
        list_entry.delete(0, END)
        # Add more items (if required)
        basket

        # Show hidden footer buttons
        new_list_btn['text'] = 'New List'
        new_list_btn.config(bg=fg_color, fg=bg_color)
        close_btn['text'] = 'Close'
        close_btn.config(bg='#A32627', fg=bg_color)
        


# New List and send email (optional)
def new_list():
    global counter

    # Getter
    get_to = send_to.get()

    # Check if user is sending an email
    if get_to == '':
        messagebox.showinfo(\
            'New List: ' + get_title,\
            'Shopping list saved in:\n"My Lists" folder as: ' + get_title)
    else:
        # Get connect import
        e_a = connect.EMAIL_USER
        e_p = connect.EMAIL_PASS

        # Process Email
        msg = EmailMessage()
        msg['subject'] = get_title
        msg['From'] = e_a
        msg['To'] = get_to
        msg.set_content(show_content)

        # Send Email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(e_a, e_p)
                smtp.send_message(msg)


            # Saved successfully and email sent
            messagebox.showinfo(\
                'New List: ' + get_title,\
                'Shopping list saved in:\n"My Lists" folder\n\nEmail sent to:\n' + get_to)
        except :
            # Error message
            messagebox.showerror(\
                    'Email Server Error', 'Sorry!\n\nWe have experienced a server issue.'\
                    '\nPlease check your internet connection\nand try again.')
            

    # Reset Page Settings
    # Clear the screen
    mail_cb.delete(0, END)
    output_box['text'] = ''
    
    list_label['text'] = 'List title:'
    list_entry.delete(0, END)
    list_btn['text'] = 'Create'
    list_btn['command'] = list_title
    app.bind('<Return>', list_title)

    # Hide footer buttons
    new_list_btn['text'] = ''
    new_list_btn.config(bg=bg_color)
    close_btn['text'] = 'Close'
    close_btn.config(bg=bg_color)

    # Reset counter
    counter = 0


# Close Program and send email (optional)
def close_program():

    # Getter
    get_to = send_to.get()

    # Getter, check if user is sending an email
    if get_to == '':
        messagebox.showinfo(\
            'New List: ' + get_title,\
            'Shopping list saved in:\n"My Lists" folder as: ' + get_title)
    else:
        # Get connect import
        e_a = connect.EMAIL_USER
        e_p = connect.EMAIL_PASS

        # Process Email
        msg = EmailMessage()
        msg['subject'] = get_title
        msg['From'] = e_a
        msg['To'] = get_to
        msg.set_content(show_content)

        # Send Email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(e_a, e_p)
                smtp.send_message(msg)


            # Saved successfully and email sent
            messagebox.showinfo(\
                'New List: ' + get_title,\
                'Shopping list saved in:\n"My Lists" folder\n\nEmail sent to:\n' + get_to)
        except:
            # Error message
            messagebox.showerror(\
                    'Server Error', 'Sorry!\n\nWe have experienced a server issue.'\
                    '\nPlease check your internet connection\nand try again.')
    
    app.destroy()


# Getters
send_to = StringVar()
list_input = StringVar()

# Header for Combobox ______________________________________

# Frame
header_frame = Frame(app, bg=bg_color)
header_frame.pack(pady=(20, 0))

# Label for email To:
mail_label = Label(header_frame, text='Email To: (optional)', bg=bg_color, fg=fg_color)
mail_label.pack(anchor='w')

# Combobox for send email To: address
mail_cb = ttk.Combobox(header_frame, width=24, textvariable=send_to)
mail_cb['values'] = 'HomeOfCoding@outlook.com', 'johnsmith@example.com'
mail_cb.pack()

# List for User Input ________________________________________

# Frame
list_frame = Frame(app, bg=bg_color)
list_frame.pack(pady=20)

# Label for creating list title
list_label = Label(list_frame, text='List title:', bg=bg_color, fg=fg_color)
list_label.pack(anchor='w')

# List entry field
list_entry = Entry(list_frame, width=27, fg=fg_color, textvariable=list_input)
list_entry.focus()
list_entry.pack()

# List entry submit button
list_btn = Button(\
    list_frame, text='Create', bg=fg_color, fg=bg_color, font=('Arial', 8), relief='flat', command=list_title)
app.bind('<Return>', list_title)
list_btn.pack(anchor='e')

# Output for Output to Screen _______________________________

# Frame
output_frame = Frame(app, bg=bg_color)
output_frame.pack(fill='x')

# Output Box Label
output_box = Label(output_frame, text='', justify='left', bg=bg_color, fg=fg_color, font=font_size)
output_box.pack(side='left', padx=(90, 0))

# Footer for New Lis and Close Program Buttons ___________

# Frame
footer_frame = Frame(app, bg=bg_color)
footer_frame.pack(side='bottom', fill='x')

# New List Button
new_list_btn = Button(\
    footer_frame, text='', bg=bg_color, fg=bg_color, font=font_size, relief='flat', command=new_list)
new_list_btn.pack(side='left', fill='x', expand=True)

# Close Program Button
close_btn = Button(\
    footer_frame, text='', bg=bg_color, fg=bg_color, font=font_size, relief='flat', command=close_program)
close_btn.pack(side='left', fill='x', expand=True)

# App defaults
if __name__ == '__main__':
    app.title('Shopping Basket')
    app.iconbitmap('icon/shopping.ico')
    app.geometry('350x640-0+56')
    app.resizable(width=False, height=False)
    app.configure(bg=bg_color)
    app.mainloop()
