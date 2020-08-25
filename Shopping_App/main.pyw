# Shopping Basket with email
from tkinter import *
from tkinter import ttk
import os
from tkinter import messagebox, END
import string
# Email
import smtplib
from email.message import EmailMessage
import connect

# Root Window
app = Tk()
app_title = 'Shopping Basket'
win_size = '350x640-0+56'

# Page defaults
bg_color = '#FFFFFF'
fg_color = '#296296'
font_size = 'Arial, 12'
# Outbox Error Font
fg_error = '#A32627'
error_font = 'Arial, 10'
# Buttons
bg_close_btn = '#A32627'
entry_btn_font = 'Arial', 8


# Create List Title
def list_title(*args):
    global filename
    global get_title

    # Getter (get title)
    get_title = list_input.get()
    # Cap Words
    get_title = string.capwords(get_title)

    # If title entry is empty, show error
    if get_title == '':
        output_box['text'] = 'Please create a title for your shopping list.'
        output_box.config(fg=fg_error, font=error_font)
        list_entry.focus()
    else:
        # If error message exists, clear the output box
        output_box['text'] = ''
        output_box.config(fg=fg_color, font=font_size)

        # Directory for saved lists
        filename = f'My Lists/{get_title}'

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
                'Sorry!\n\nWe have experienced an issue\n'\
                'collecting your data\n\nPlease tyy again.')

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
        output_box['text'] = 'Add items field is empty!\n\n'\
                             f'Please add items to your\n{get_title} shopping basket.'
        output_box.config(fg=fg_error, font=error_font)
        list_entry.focus()
    else:
        # If error message exists, clear the output box
        output_box['text'] = ''
        output_box.config(fg=fg_color, font=font_size)

        # Getter (counter + get added)
        get_added = f'{counter+1}. {list_input.get()}'
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
                'Sorry!\n\nWe have experienced an issue\n'\
                'collecting your data\n\nPlease tyy again.')

        # Page settings
        # Clear list entry field
        list_entry.delete(0, END)
        # Add more items (if required)
        basket

        # Show hidden footer buttons
        new_list_btn['text'] = 'New List'
        new_list_btn.config(bg=fg_color, fg=bg_color)
        close_btn['text'] = 'Close'
        close_btn.config(bg=bg_close_btn, fg=bg_color)
        


# New List and send email (optional)
def new_list():
    global counter

    # Getter
    get_to = send_to.get()

    # Check if user is sending an email
    if get_to == '':
        messagebox.showinfo(f'New List: {get_title}',\
                            'Shopping list saved in:\n'\
                            f'"My Lists" folder as: {get_title}')

        reset_page()

    else:
        if get_to in mail_cb['values']:
            
            pass
            
        if get_to not in mail_cb['values']:

            file_name = 'Emails_Book/addresses'
        
            try:
                with open(file_name, 'a') as f_append:
                    f_append.write(get_to + '\n')


                with open(file_name) as f_read:
                    address_list = f_read.read()


                mail_cb['values'] = address_list
            
            except:
                pass

        send_mail()


# Send Mail
def send_mail():
    global counter

    # Getter
    get_to = send_to.get()
        
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
        messagebox.showinfo(f'New List: {get_title}',\
                            'Shopping list saved in:\n'\
                            f'"My Lists" folder\n\nEmail sent to:\n{get_to}')
    except:
        # Error message
        messagebox.showerror(\
                'Email Server Error', 'Sorry!\n\nWe have experienced a server issue.'\
                '\nPlease check your internet connection\nand try again.')
    
    # Reset counter
    counter = 0
    reset_page()
            

# Reset Page Settings
def reset_page():
    global counter
    
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
        messagebox.showinfo(f'New List: {get_title}',\
                            'Shopping list saved in:\n'\
                            f'"My Lists" folder as: {get_title}')

    else:
        
        if get_to in mail_cb['values']:
            
            pass
            
        if get_to not in mail_cb['values']:
            
            file_name = 'Emails_Book/addresses'
            
            try:
                with open(file_name, 'a') as f_append:
                    f_append.write(get_to + '\n')


                with open(file_name) as f_read:
                    address_list = f_read.read()


                mail_cb['values'] = address_list
            
            except:
                pass
        
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
            messagebox.showinfo(f'New List: {get_title}',\
                                'Shopping list saved in:\n'\
                                f'"My Lists" folder\n\nEmail sent to:\n{get_to}')
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
mail_cb['values'] = mail_cb['values']
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
    list_frame, text='Create', bg=fg_color, fg=bg_color, font=entry_btn_font, relief='flat', command=list_title)
app.bind('<Return>', list_title)
list_btn.pack(anchor='e')

# Output for Output to Screen _______________________________

# Frame
output_frame = Frame(app, bg=bg_color)
output_frame.pack(fill='x')

# Output Box Label
output_box = Label(output_frame, text='', justify='left', wrap=200, \
                   bg=bg_color, fg=fg_color, font=font_size)
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

# ______________________________________________________
# Auto Populate New Directoties and file (if not exists)

# Create My Lists Directory (if not exists)
dir_name = 'My Lists/'
if dir_name != os.path.basename(dir_name):
    try:
        os.mkdir(dir_name)
    except:
        pass

# Create Email Addresses Directory (if not exists)
dir_name = 'Emails_Book/'
if dir_name != os.path.basename(dir_name):
    try:
        os.mkdir(dir_name)
    except:
        pass

# Create Email Addresses File (if not exists)
new_file = 'addresses'
try:
    with open(f'Emails_Book/{new_file}', 'a'):
        os.path.isfile(new_file)


except:
    pass

# On load.. Display the content of the file in combobox
file_path = 'Emails_Book/addresses'
try:
    with open(file_path) as f_read:
        address_list = f_read.read()


    mail_cb['values'] = address_list
except:
    pass

# ______________________________________________________

# App defaults
if __name__ == '__main__':
    app.title(app_title)
    app.iconbitmap('icon/shopping.ico')
    app.geometry(win_size)
    app.resizable(width=False, height=False)
    app.configure(bg=bg_color)
    app.mainloop()
