Python

from tkinter import Tk, Label, Frame, Button, StringVar
from tkinter import ttk

class OrderView:
    def __init__(self, root):
        self.root = root
        self.root.title("Order View")
        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.order_id = StringVar()
        self.cake_type = StringVar()
        self.cake_size = StringVar()
        self.special_instructions = StringVar()

        self.order_id_label = Label(self.frame, text="Order ID:")
        self.order_id_label.pack()
        self.order_id_value = Label(self.frame, textvariable=self.order_id)
        self.order_id_value.pack()

        self.cake_type_label = Label(self.frame, text="Cake Type:")
        self.cake_type_label.pack()
        self.cake_type_value = Label(self.frame, textvariable=self.cake_type)
        self.cake_type_value.pack()

        self.cake_size_label = Label(self.frame, text="Cake Size:")
        self.cake_size_label.pack()
        self.cake_size_value = Label(self.frame, textvariable=self.cake_size)
        self.cake_size_value.pack()

        self.special_instructions_label = Label(self.frame, text="Special Instructions:")
        self.special_instructions_label.pack()
        self.special_instructions_value = Label(self.frame, textvariable=self.special_instructions)
        self.special_instructions_value.pack()

        self.update_order_button = Button(self.frame, text="Update Order")
        self.update_order_button.pack()

        self.cancel_order_button = Button(self.frame, text="Cancel Order")
        self.cancel_order_button.pack()