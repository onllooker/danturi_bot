# Перенаправление вывода консоли в текстовое поле
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.insert("end", string)
        self.widget.see("end")

    def flush(self):
        pass

