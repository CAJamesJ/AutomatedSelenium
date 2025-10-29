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

        self.click_count = 0
        self.is_recording = False
        self.last_line_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_log)
        self.timer.start(1000)

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