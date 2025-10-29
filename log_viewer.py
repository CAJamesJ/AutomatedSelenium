from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QListWidget, QSlider, QLabel, QLineEdit, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, QTimer
import sys
import os

class CommentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Comment")
        self.setGeometry(150, 150, 300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Add Comment")
        self.text_field = QLineEdit()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)

        layout.addWidget(self.label)
        layout.addWidget(self.text_field)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_comment(self):
        return self.text_field.text()

class SeleniumRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selenium Script Recorder")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()
        self.log_list = QListWidget()
        main_layout.addWidget(self.log_list)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.record_btn = QPushButton("Record")
        self.pause_btn = QPushButton("Pause")
        self.send_key_btn = QPushButton("Send Key")
        self.slider_label = QLabel("Implicit Pause: 1 sec")
        self.implicit_slider = QSlider(Qt.Horizontal)

        self.implicit_slider.setMinimum(1)
        self.implicit_slider.setMaximum(10)
        self.implicit_slider.setValue(1)
        self.implicit_slider.valueChanged.connect(self.update_slider_label)

        self.implicit_pause_btn = QPushButton("Implicit Pause")
        self.remove_line_btn = QPushButton("Remove a Line")
        self.add_comment_btn = QPushButton("Add Comment")
        self.submit_btn = QPushButton("Submit")

        button_layout.addWidget(self.record_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.send_key_btn)
        button_layout.addWidget(self.slider_label)
        button_layout.addWidget(self.implicit_slider)
        button_layout.addWidget(self.implicit_pause_btn)
        button_layout.addWidget(self.remove_line_btn)
        button_layout.addWidget(self.add_comment_btn)
        button_layout.addWidget(self.submit_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.record_btn.clicked.connect(self.start_recording)
        self.pause_btn.clicked.connect(self.pause_recording)
        self.implicit_pause_btn.clicked.connect(self.add_implicit_pause)
        self.remove_line_btn.clicked.connect(self.remove_selected_line)
        self.add_comment_btn.clicked.connect(self.show_comment_dialog)
        self.submit_btn.clicked.connect(self.convert_log_to_selenium_code)
        self.send_key_btn.clicked.connect(self.send_key_action)

        self.click_count = 0
        self.is_recording = False
        self.last_line_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_log)
        self.timer.start(1000)

    
    def send_key_action(self):
        selected_items = self.log_list.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        original_text = item.text()

        if "[R] ID:" in original_text or "[R] XPath:" in original_text:
            dialog = CommentDialog()
            dialog.label.setText("Enter key to send:")
            dialog.text_field.setText("")  # Clear previous text
            if dialog.exec():
                key = dialog.get_comment()
                if key:
                    updated_text = f"{original_text}'->'{key}"
                    item.setText(updated_text)
        else:
            # Optional: show a message box if the selected line isn't a valid record
            pass


    def update_slider_label(self, value):
        self.slider_label.setText(f"Implicit Pause: {value} sec")

    def start_recording(self):
        self.is_recording = True
        with open("recording_flag.txt", "w") as f:
            f.write("True")
        self.record_btn.setStyleSheet("background-color: green")
        self.pause_btn.setStyleSheet("")

    def pause_recording(self):
        self.is_recording = False
        with open("recording_flag.txt", "w") as f:
            f.write("False")
        self.pause_btn.setStyleSheet("background-color: orange")
        self.record_btn.setStyleSheet("")

    def add_implicit_pause(self):
        seconds = self.implicit_slider.value()
        self.click_count += 1
        self.log_list.addItem(f"[{self.click_count}] [P] {seconds} sec wait is added")

    def remove_selected_line(self):
        selected_items = self.log_list.selectedItems()
        for item in selected_items:
            self.log_list.takeItem(self.log_list.row(item))

    def show_comment_dialog(self):
        dialog = CommentDialog()
        if dialog.exec():
            comment = dialog.get_comment()
            if comment:
                self.click_count += 1
                self.log_list.addItem(f"[{self.click_count}] [C] \"{comment}\"")

    def update_log(self):
        if not os.path.exists("click_log.txt"):
            return

        with open("click_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = lines[self.last_line_count:]
        for line in new_lines:
            self.click_count += 1
            self.log_list.addItem(f"[{self.click_count}] [R] {line.strip()}")

        self.last_line_count = len(lines)
    
    def convert_log_to_selenium_code(self):
        import re

        selenium_script = [
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC",
            "import time",
            "",
            "driver = webdriver.Edge()",
            "driver.maximize_window()",
            "driver.get(\"https://www.google.com\")  # Replace with your target URL",
            "wait = WebDriverWait(driver, 10)",
            ""
        ]

        for i in range(self.log_list.count()):
            line = self.log_list.item(i).text()
            send_keys_match = re.match(r"\[\d+\] \[R\] (ID|XPath): (.+?)'->'(.*?)$", line)
            record_match = re.match(r"\[\d+\] \[R\] (ID|XPath): (.+)", line)
            comment_match = re.match(r'\[\d+\] \[C\] "(.*)"', line)
            pause_match = re.match(r"\[\d+\] \[P\] (\d+) sec wait is added", line)

            if send_keys_match:
                locator_type, locator_value, key = send_keys_match.groups()
                if locator_type == "ID":
                    selenium_script.append(
                        f'wait.until(EC.presence_of_element_located((By.ID, "{locator_value}"))).send_keys({key})'
                    )
                else:
                    selenium_script.append(
                        f'wait.until(EC.presence_of_element_located((By.XPATH, "{locator_value}"))).send_keys({key})'
                    )
            elif record_match:
                locator_type, locator_value = record_match.groups()
                if locator_type == "ID":
                    selenium_script.append(f'wait.until(EC.element_to_be_clickable((By.ID, "{locator_value}"))).click()')
                else:
                    selenium_script.append(f'wait.until(EC.element_to_be_clickable((By.XPATH, "{locator_value}"))).click()')
            elif comment_match:
                comment = comment_match.group(1)
                selenium_script.append(f'# Comment: {comment}')
            elif pause_match:
                seconds = pause_match.group(1)
                selenium_script.append(f'time.sleep({seconds})')
                selenium_script.append(f'')

        selenium_script.append("time.sleep(1000)")
        selenium_script.append("driver.quit()")

        with open("generated_selenium_script.py", "w", encoding="utf-8") as f:
            f.write("\n".join(selenium_script))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeleniumRecorderApp()
    window.show()
    sys.exit(app.exec())

# from PySide6.QtWidgets import (
#     QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
#     QListWidget, QSlider, QLabel, QLineEdit, QDialog, QDialogButtonBox
# )
# from PySide6.QtCore import Qt, QTimer
# import sys
# import os

# class CommentDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Add Comment")
#         self.setGeometry(150, 150, 300, 150)
#         layout = QVBoxLayout()

#         self.label = QLabel("Add Comment")
#         self.text_field = QLineEdit()
#         self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)

#         layout.addWidget(self.label)
#         layout.addWidget(self.text_field)
#         layout.addWidget(self.button_box)
#         self.setLayout(layout)

#         self.button_box.accepted.connect(self.accept)
#         self.button_box.rejected.connect(self.reject)

#     def get_comment(self):
#         return self.text_field.text()

# class SeleniumRecorderApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Selenium Script Recorder")
#         self.setGeometry(100, 100, 600, 400)

#         main_layout = QHBoxLayout()
#         self.log_list = QListWidget()
#         main_layout.addWidget(self.log_list)

#         button_layout = QVBoxLayout()
#         button_layout.setSpacing(15)

#         self.record_btn = QPushButton("Record")
#         self.pause_btn = QPushButton("Pause")
#         self.slider_label = QLabel("Implicit Pause: 1 sec")
#         self.implicit_slider = QSlider(Qt.Horizontal)
#         self.implicit_slider.setMinimum(1)
#         self.implicit_slider.setMaximum(10)
#         self.implicit_slider.setValue(1)
#         self.implicit_slider.valueChanged.connect(self.update_slider_label)

#         self.implicit_pause_btn = QPushButton("Implicit Pause")
#         self.remove_line_btn = QPushButton("Remove a Line")
#         self.add_comment_btn = QPushButton("Add Comment")
#         self.submit_btn = QPushButton("Submit")

#         button_layout.addWidget(self.record_btn)
#         button_layout.addWidget(self.pause_btn)
#         button_layout.addWidget(self.slider_label)
#         button_layout.addWidget(self.implicit_slider)
#         button_layout.addWidget(self.implicit_pause_btn)
#         button_layout.addWidget(self.remove_line_btn)
#         button_layout.addWidget(self.add_comment_btn)
#         button_layout.addWidget(self.submit_btn)
#         button_layout.addStretch()

#         main_layout.addLayout(button_layout)
#         self.setLayout(main_layout)

#         self.record_btn.clicked.connect(self.start_recording)
#         self.pause_btn.clicked.connect(self.pause_recording)
#         self.implicit_pause_btn.clicked.connect(self.add_implicit_pause)
#         self.remove_line_btn.clicked.connect(self.remove_selected_line)
#         self.add_comment_btn.clicked.connect(self.show_comment_dialog)

#         self.click_count = 0
#         self.is_recording = False
#         self.last_line_count = 0

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_log)
#         self.timer.start(1000)

#     def update_slider_label(self, value):
#         self.slider_label.setText(f"Implicit Pause: {value} sec")

#     def start_recording(self):
#         self.is_recording = True
#         self.record_btn.setStyleSheet("background-color: green")
#         self.pause_btn.setStyleSheet("")
#         self.click_count += 1
#         locator = f"ID: button{self.click_count}" if self.click_count % 2 == 1 else f"XPath: //button[{self.click_count}]"
#         self.log_list.addItem(f"[{self.click_count}] [R] {locator}")

#     def pause_recording(self):
#         self.is_recording = False
#         self.pause_btn.setStyleSheet("background-color: orange")
#         self.record_btn.setStyleSheet("")

#     def add_implicit_pause(self):
#         seconds = self.implicit_slider.value()
#         self.click_count += 1
#         self.log_list.addItem(f"[{self.click_count}] [P] {seconds} sec wait is added")

#     def remove_selected_line(self):
#         selected_items = self.log_list.selectedItems()
#         for item in selected_items:
#             self.log_list.takeItem(self.log_list.row(item))

#     def show_comment_dialog(self):
#         dialog = CommentDialog()
#         if dialog.exec():
#             comment = dialog.get_comment()
#             if comment:
#                 self.click_count += 1
#                 self.log_list.addItem(f"[{self.click_count}] [C] \"{comment}\"")

#     def update_log(self):
#         if not os.path.exists("click_log.txt"):
#             return

#         with open("click_log.txt", "r", encoding="utf-8") as f:
#             lines = f.readlines()

#         new_lines = lines[self.last_line_count:]
#         for line in new_lines:
#             self.click_count += 1
#             self.log_list.addItem(f"[{self.click_count}] [L] {line.strip()}")

#         self.last_line_count = len(lines)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = SeleniumRecorderApp()
#     window.show()
#     sys.exit(app.exec())