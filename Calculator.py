import customtkinter as ctk
from ctypes import windll, c_int, byref, sizeof
from cal_setting import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLACK_)
        self.geometry("400x700+0+0")
        self.resizable(False, False)
        HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(BLACK)), sizeof(c_int))

        #layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

        #DATA
        self.number = ctk.StringVar(value=str(0))
        self.sequence = ctk.StringVar(value="")
        self.result = ctk.BooleanVar(value=False)

        #Button
        Number1(self, self.number, self.sequence, self.result)
        Number2(self, self.number, self.sequence, self.result)
        Number3(self, self.number, self.sequence, self.result)
        Number4(self, self.number, self.sequence, self.result)
        Number5(self, self.number, self.sequence, self.result)
        Number6(self, self.number, self.sequence, self.result)
        Number7(self, self.number, self.sequence, self.result)
        Number8(self, self.number, self.sequence, self.result)
        Number9(self, self.number, self.sequence, self.result)
        Number0(self, self.number, self.sequence, self.result)
        DotSign(self, self.number, self.sequence, self.result)
        EqualSign(self, self.number, self.sequence, self.result)
        PlusSign(self, self.number, self.sequence, self.result)
        MinusSign(self, self.number, self.sequence, self.result)
        MultiplySign(self, self.number, self.sequence, self.result)
        DivideSign(self, self.number, self.sequence, self.result)
        PercentSign(self, self.number, self.sequence, self.result)
        InvertSign(self, self.number, self.sequence, self.result)
        ACSign(self, self.number, self.sequence)
        # Display
        OutPut(self, self.number)
        Display(self, self.sequence)


        self.mainloop()


class Display(ctk.CTkLabel):
    def __init__(self, parent, sequence):
        self.sequence = sequence
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, textvariable=self.sequence, text_color=WHITE
                         , font=font, anchor="e")
        self.grid(column=0, row=0, columnspan=4, sticky="news")


class OutPut(ctk.CTkLabel):
    def __init__(self, parent, number):
        self.number = number
        font = ctk.CTkFont(family="Calibri", size=100)
        super().__init__(master=parent, textvariable=self.number, font=font, anchor="e",
                         text_color=WHITE)
        self.grid(column=0, columnspan=4, row=1, sticky="news", padx=10)

class PercentSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, text="%", text_color=WHITE, fg_color=DARK_GREY,
                         hover_color=DARK_GREY_HOVER, corner_radius=0, font=font, command=self.update)
        self.grid(row=2, column=2, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        new_number = float(self.number.get())/100
        new_sequence = self.sequence.get()[:-len(self.number.get())]
        if len(str(new_number)) >= 6:
            new_number = round(new_number, 6)
        new_sequence += str(new_number)
        if self.equal.get() is False:
            self.sequence.set(new_sequence)
            self.number.set(new_number)
        else:
            self.number.set(f"{new_number}")
            self.sequence.set(f"{new_number}")
            self.equal.set(False)



class InvertSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, text="±", text_color=WHITE, fg_color=DARK_GREY,
                         hover_color=DARK_GREY_HOVER, corner_radius=0,font=font, command=self.update)
        self.grid(row=2, column=1, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.number.get()[0] == "-":
            if self.equal.get():
                self.sequence.set("")
            new_sequence = self.sequence.get()[:-len(self.number.get())]
            new_sequence += self.number.get()[1:]
            self.sequence.set(new_sequence)
            self.number.set(self.number.get()[1:])
        else:
            if self.equal:
                self.sequence.set("")
            new_sequence = self.sequence.get()[:-len(self.number.get())]
            self.number.set(f"-{self.number.get()}")
            new_sequence += self.number.get()
            self.sequence.set(new_sequence)

class ACSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        super().__init__(master=parent, text="AC", text_color=WHITE, fg_color=DARK_GREY,
                         hover_color=DARK_GREY_HOVER, corner_radius=0,font=font, command=self.update)
        self.grid(row=2, column=0, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        self.number.set("0")
        self.sequence.set("")


class EqualSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, fg_color=ORANGE, text_color=WHITE, corner_radius=0
                         , font=font, text="=", hover_color=ORANGE_HOVER, command=self.result)
        self.grid(row=6, column=3, padx=0.5, pady=0.5, sticky="news")

    def result(self):
        self.equal.set(True)
        s = list(self.sequence.get().split())
        if s[-1] in ['+', '-', 'x', '÷']:
            self.number.set("Error")
        else:
            result = float(s[0])
            for x in range(1, len(s), 2):
                if s[x] == "+":
                    result += float(s[x+1])
                elif s[x] == "-":
                    result -= float(s[x+1])
                elif s[x] == "x":
                    result *= float(s[x+1])
                else:
                    result /= float(s[x+1])

            if len(str(result)) > 6:
                if result >= 0:
                    result = round(float(result), 6)
                else:
                    result = round(float(result), 5)
            elif str(result)[-2:] == ".0":
                result = int(result)
            self.number.set(str(result))




class PlusSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=30)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, command=self.update, fg_color=ORANGE, text_color=WHITE, corner_radius=0
                         , font=font, text="+", hover_color=ORANGE_HOVER)
        self.grid(row=5, column=3, padx=0.5, pady=0.5, sticky="news")

    def update(self):
        if self.sequence.get() == "":
            self.sequence.set(f"0 + ")
        elif (len(self.sequence.get()) >= 3 and\
              self.sequence.get()[-2:] in ["+ ", "- ", "x ", "÷ "]):
            pass
        else:
            self.sequence.set(f"{self.sequence.get()} + ")
        self.number.set("")
        if self.equal.get():
            self.equal.set(False)


class MinusSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, command=self.update, fg_color=ORANGE, text_color=WHITE, corner_radius=0
                         , font=font, text="-", hover_color=ORANGE_HOVER)
        self.grid(row=4, column=3, padx=0.5, pady=0.5, sticky="news")

    def update(self):
        if self.sequence.get() == "":
            self.sequence.set(f"0 - ")
        elif (len(self.sequence.get()) >= 3 and \
                self.sequence.get()[-2:] in ["+ ", "- ", "x ", "÷ "]):
            pass
        else:
            self.sequence.set(f"{self.sequence.get()} - ")
        self.number.set("")
        if self.equal.get():
            self.equal.set(False)


class MultiplySign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, command=self.update, fg_color=ORANGE, text_color=WHITE, corner_radius=0
                         , font=font, text="x", hover_color=ORANGE_HOVER)
        self.grid(row=3, column=3, padx=0.5, pady=0.5, sticky="news")

    def update(self):
        if self.sequence.get() == "":
            self.sequence.set(f"0 x ")
        elif (len(self.sequence.get()) >= 3 and\
              self.sequence.get()[-2:] in ["+ ", "- ", "x ", "÷ "]):
            pass
        else:
            self.sequence.set(f"{self.sequence.get()} x ")
        self.number.set("")
        if self.equal.get():
            self.equal.set(False)


class DivideSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.sequence = sequence
        self.equal = equal
        super().__init__(master=parent, command=self.update, fg_color=ORANGE, text_color=WHITE, corner_radius=0
                         , font=font, text="÷", hover_color=ORANGE_HOVER)
        self.grid(row=2, column=3, padx=0.5, pady=0.5, sticky="news")

    def update(self):
        if self.sequence.get() == "":
            self.sequence.set(f"0 ÷ ")
        elif (len(self.sequence.get()) >= 3 and\
              self.sequence.get()[-2:] in ["+ ", "- ", "x ", "÷ "]):
            pass
        else:
            self.sequence.set(f"{self.sequence.get()} ÷ ")
        self.number.set("")
        if self.equal.get():
            self.equal.set(False)


class Number1(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.sequence = sequence
        self.equal = equal
        self.number = number
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="1", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=5, column=0, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("1")
            else:
                a = f"{self.number.get()}1"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}1")
        self.equal.set(False)


class Number2(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        font = ctk.CTkFont(family="Calibri", size=50)
        self.sequence = sequence
        self.equal = equal
        self.number = number
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="2", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=5, column=1, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("2")
            else:
                a = f"{self.number.get()}2"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}2")
        self.equal.set(False)

class Number3(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="3", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=5, column=2, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("3")
            else:
                a = f"{self.number.get()}3"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}3")
        self.equal.set(False)

class Number4(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="4", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=4, column=0, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("4")
            else:
                a = f"{self.number.get()}4"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}4")
        self.equal.set(False)

class Number5(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="5", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=4, column=1, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("5")
            else:
                a = f"{self.number.get()}5"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}5")
        self.equal.set(False)

class Number6(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="6", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=4, column=2, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("6")
            else:
                a = f"{self.number.get()}6"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}6")
        self.equal.set(False)

class Number7(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="7", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=3, column=0, sticky="news",padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("7")
            else:
                a = f"{self.number.get()}7"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}7")
        self.equal.set(False)

class Number8(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="8", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=3, column=1, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("8")
            else:
                a = f"{self.number.get()}8"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}8")
        self.equal.set(False)

class Number9(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="9", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=3, column=2, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("9")
            else:
                a = f"{self.number.get()}9"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}9")
        self.equal.set(False)

class Number0(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.number = number
        self.sequence = sequence
        self.equal = equal
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text="0", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=6, column=0, sticky="news", columnspan=2, padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get():
            self.sequence.set("")
            self.number.set("")
        if len(self.number.get()) <= 6:
            if self.number.get() == "0":
                self.number.set("0")
            else:
                a = f"{self.number.get()}0"
                self.number.set(a)
            self.sequence.set(f"{self.sequence.get()}0")
        self.equal.set(False)

class DotSign(ctk.CTkButton):
    def __init__(self, parent, number, sequence, equal):
        self.sequence = sequence
        font = ctk.CTkFont(family="Calibri", size=50)
        self.number = number
        self.equal = equal
        super().__init__(master=parent, corner_radius=0, fg_color=LIGHT_GREY, text_color=BLACK_,
                         text=".", font=font, hover_color=LIGHT_GREY_HOVER, command=self.update)
        self.grid(row=6, column=2, sticky="news", padx=0.5, pady=0.5)

    def update(self):
        if self.equal.get() is False:
            if len(self.number.get()) <= 6:
                if "." not in self.number.get():
                    a = f"{self.number.get()}."
                    self.number.set(a)
                    self.sequence.set(f"{self.sequence.get()}.")
        else:
            if "." not in self.number.get():
                self.number.set(f"{self.number.get()}.")
                self.sequence.set(f"{self.number.get()}")
                self.equal.set(False)

if __name__ == "__main__":
    App()