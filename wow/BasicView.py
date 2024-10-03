import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QDialog,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
)


class BasicView:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BasicView, cls).__new__(cls)
        return cls._instance

    def __init__(self, custom_property=None):
        if not hasattr(self, "initialized"):
            self.__app = QApplication(sys.argv)
            self.initialized = True

    def exec_(self):
        return self.__app.exec_()

    @staticmethod
    def grid_arguments():
        return {
            "visible": True,
            "linestyle": "--",
            "linewidth": 0.5,
            "alpha": 0.7,
            "color": "gray",
            "which": "both",
        }

    @staticmethod
    def basic_view(title, mosaic, width_ratios, height_ratios, unwanted_buttons=[]):
        plt.ion()
        plt.switch_backend("qtagg")
        fig, ax = plt.subplot_mosaic(
            constrained_layout=True,
            mosaic=mosaic,
            empty_sentinel=None,
            width_ratios=width_ratios,
            height_ratios=height_ratios,
        )
        fig.canvas.manager.set_window_title(title=title)

        mng = plt.get_current_fig_manager()
        mng.window.setWindowTitle(title)
        mng.window.showMaximized()

        for x in mng.toolbar.actions():
            if x.text() in unwanted_buttons:
                mng.toolbar.removeAction(x)

        return fig, ax

    @staticmethod
    def basic_view_show_message(title, message, icon):
        """
        Instantiate a popup to show a message

        Parameters:
        title: The title of the popup
        message: The message you want to show
        icon:
            0: no icon
            1: information
            2: warning
            3: critical
            4: question
        """

        class MainWindow(QWidget):
            def __init__(self):
                super().__init__()
                msg_box = QMessageBox()
                msg_box.setWindowTitle(title)
                msg_box.setText(message)
                msg_box.setIcon(icon)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

        window = MainWindow()

    @staticmethod
    def basic_view_file_dialog():
        class FileDialogView(QWidget):
            def __init__(self):
                super().__init__()

                self.selected_file = None
                self.setWindowTitle("Select a file")
                self.setGeometry(500, 500, 500, 100)

                layout = QVBoxLayout()
                self.button = QPushButton("Open File", self)
                self.button.clicked.connect(self.show_file_dialog)
                layout.addWidget(self.button)

                self.setLayout(layout)

            def show_file_dialog(self):
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getOpenFileName(
                    self,
                    "Open File",
                    "",
                    "All Files (*);;csv Files (*.csv)",
                    options=options,
                )

                self.selected_file = file_name
                self.close()

        BasicView()
        dialog = FileDialogView()
        dialog.show()
        BasicView().exec_()
        return dialog.selected_file

    @staticmethod
    def basic_view_text_input(title, message):
        class TextInputDialogView(QDialog):
            def __init__(self, title=title, label_text=message):
                super().__init__()

                self.setWindowTitle(title)
                self.setGeometry(500, 500, 500, 100)

                layout = QVBoxLayout()
                h_layout = QHBoxLayout()

                self.label = QLabel(label_text, self)
                h_layout.addWidget(self.label)

                self.text_input = QLineEdit(self)
                h_layout.addWidget(self.text_input)

                layout.addLayout(h_layout)

                self.ok_button = QPushButton("OK", self)
                self.ok_button.clicked.connect(self.on_ok_clicked)
                layout.addWidget(self.ok_button)

                self.setLayout(layout)

                layout.setSpacing(10)
                layout.addStretch()

            def on_ok_clicked(self):
                self.entered_text = self.text_input.text()
                self.accept()

            def get_text(self):
                if self.exec_() == QDialog.Accepted:
                    return self.entered_text
                return None

        BasicView()
        dialog = TextInputDialogView()
        input_text = dialog.get_text()
        return input_text

    @staticmethod
    def basic_view_checkbox_list(title, message, items):
        class CheckBoxListDialog(QDialog):
            def __init__(self, items):
                super().__init__()

                self.setWindowTitle("Checkbox List Popup")
                self.setGeometry(100, 100, 300, 300)

                # Create layout
                layout = QVBoxLayout()

                # Create a QListWidget to hold the items
                self.list_widget = QListWidget()

                # Populate the list widget with items and checkboxes
                for item in items:
                    list_item = QListWidgetItem(item)
                    checkbox = QCheckBox(item)  # Create a checkbox for each item
                    checkbox.setChecked(False)  # Default state is unchecked
                    list_item.setSizeHint(
                        checkbox.sizeHint()
                    )  # Adjust item size to checkbox size
                    self.list_widget.addItem(
                        list_item
                    )  # Add the list item to the widget
                    self.list_widget.setItemWidget(
                        list_item, checkbox
                    )  # Set the checkbox as the widget for the item

                layout.addWidget(self.list_widget)

                # Create OK and Cancel buttons
                button_layout = QHBoxLayout()
                ok_button = QPushButton("OK")
                cancel_button = QPushButton("Cancel")

                # Connect buttons to functions
                ok_button.clicked.connect(self.on_ok)
                cancel_button.clicked.connect(self.reject)

                button_layout.addWidget(ok_button)
                button_layout.addWidget(cancel_button)
                layout.addLayout(button_layout)

                self.setLayout(layout)

            def on_ok(self):
                selected_items = []
                for index in range(self.list_widget.count()):
                    item = self.list_widget.item(index)
                    checkbox = self.list_widget.itemWidget(item)
                    if checkbox.isChecked():
                        selected_items.append(checkbox.text())

                self.selected_items = selected_items
                self.accept()

        BasicView()
        dialog = CheckBoxListDialog(items)
        dialog.show()
        dialog.exec_()
        return dialog.selected_items
