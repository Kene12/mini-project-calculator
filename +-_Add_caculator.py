import tkinter as tk

# คลาสแม่ที่รับผิดชอบการแสดงผล
class Display:
    def __init__(self, root):
        self.root = root
        self.display = tk.Text(root, font=('Arial', 20), bd=10, insertwidth=4, width=14, height=2, borderwidth=4)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")
    
    # ฟังก์ชันในการแสดงผลบนหน้าจอ
    def insert_text(self, text):
        self.display.insert(tk.END, text)
    
    # ฟังก์ชันในการลบข้อมูลในหน้าจอ
    def clear_display(self):
        self.display.delete('1.0', tk.END)
    
    # ฟังก์ชันในการดึงข้อมูลจากหน้าจอแสดงผล
    def get_display_content(self):
        return self.display.get('1.0', tk.END).strip()

# คลาสลูกที่สืบทอดจาก Display และจัดการเฉพาะปุ่ม "."
class DotButton(Display):
    def __init__(self, root):
        super().__init__(root)
        self.dot_pressed = False

    # ฟังก์ชันในการจัดการปุ่ม "."
    def handle_dot(self):
        self.dot_pressed = True
        self.insert_text('.')

# คลาสลูกที่สืบทอดจาก Display และจัดการปุ่มตัวเลข 0-9
class NumberButton(Display):
    def __init__(self, root):
        super().__init__(root)

    # ฟังก์ชันในการจัดการปุ่มตัวเลข
    def handle_number(self, number):
        self.insert_text(str(number))

# คลาสลูกที่สืบทอดจาก Display และจัดการปุ่มการดำเนินการทางคณิตศาสตร์
class OperatorButton(Display):
    def __init__(self, root):
        super().__init__(root)

    # ฟังก์ชันในการจัดการปุ่มการดำเนินการทางคณิตศาสตร์
    def handle_operator(self, operator):
        self.insert_text(operator)

# คลาสหลักของเครื่องคิดเลข
class Calculator(NumberButton, DotButton, OperatorButton):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("KentaZad Calculator")
        
        # สร้างปุ่มเครื่องคิดเลข
        self.create_buttons()

        # ปรับขนาดของแถวและคอลัมน์ให้ยืดหยุ่นเท่ากัน
        for i in range(4):  # ปรับขนาดคอลัมน์ 4 คอลัมน์ให้เท่ากัน
            self.root.grid_columnconfigure(i, weight=1, uniform="equal")
        for i in range(6):  # ปรับขนาดแถว 6 แถวให้เท่ากัน
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")

    def create_buttons(self):
        # สร้างปุ่มและวางบน grid layout
        button_texts = [
            '(', ')', '=', 'C',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'DEL', '+'
        ]
        
        row_val = 1  # ปรับเป็น row 1 เนื่องจาก row 0 ใช้สำหรับจอแสดงผล
        col_val = 0
        
        for text in button_texts:
            if text == '.':
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5,
                                   command=self.handle_dot)  # ปุ่ม .
            elif text == '=':
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5,
                                   command=self.calculate)  # ปุ่ม =
            elif text == 'C':
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5,
                                   command=self.clear_display)  # ปุ่มล้างจอ
            elif text.isdigit():  # ตรวจสอบว่าถ้าเป็นตัวเลข
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5,
                                   command=lambda t=text: self.handle_number(t))  # ปุ่มตัวเลข
            elif text in ['+', '-', '*', '/']:  # ปุ่มเครื่องหมายการดำเนินการ
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5,
                                   command=lambda t=text: self.handle_operator(t))  # ปุ่มเครื่องหมาย
            else:
                button = tk.Button(self.root, text=text, font=('Arial', 16), padx=5, pady=5)
            
            button.grid(row=row_val, column=col_val, sticky="nsew")  # ปรับขนาดให้ขยายเท่ากัน
            col_val += 1

            if col_val > 3:  # ปรับเป็น 3 เพราะเรามี 4 คอลัมน์
                col_val = 0
                row_val += 1

    # ฟังก์ชันในการคำนวณนิพจน์ทางคณิตศาสตร์
    def calculate(self):
        try:
            expression = self.get_display_content()
            # ตรวจสอบว่าลงท้ายด้วยเครื่องหมายการดำเนินการหรือไม่
            if expression[-1] in ['+', '-', '*', '/']:
                expression = expression[:-1]  # ลบเครื่องหมายออก และใช้ตัวเลขที่เหลือ
            result = eval(expression)  # ใช้ eval() เพื่อคำนวณนิพจน์
            self.clear_display()  # ล้างหน้าจอแสดงผลก่อนแสดงผลลัพธ์
            self.insert_text(result)  # แสดงผลลัพธ์
        except Exception as e:
            self.clear_display()
            self.insert_text('Error')  # แสดงข้อความ Error หากเกิดข้อผิดพลาดในการคำนวณ

# สร้างหน้าต่างหลักของ tkinter
root = tk.Tk()

# สร้างวัตถุของคลาส Calculator
calc = Calculator(root)

# เริ่ม loop ของ tkinter
root.mainloop()
