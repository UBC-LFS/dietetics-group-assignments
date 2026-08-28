import os
from styles import *
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QWidget, QLabel 
from widgets.checkable_combo_box import CheckableComboBox

class ListField(QWidget):

    changed = Signal(list)

    def __init__(self, row_template):

        self.selected_fields = []
        self.row_template = row_template

        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # Button frame
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 2, 0, 2)

        add_button = QPushButton("+")
        add_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_BACKGROUND_COLOR};
                color: {BUTTON_TEXT_COLOR};
                padding: 4px 12px;
                border-width: 2px;
                border-color: {BUTTON_BORDER_COLOR};
                border-style: solid;
                border-radius: 4px;
            }}
        """)

        row_fields = list(self.row_template.values())
        add_button.clicked.connect(lambda _1=0, lf=layout, _2=0: self._add_row(lf, row_fields[0], row_fields[1]))
        button_layout.addWidget(add_button)

        remove_button = QPushButton("-")
        remove_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_BACKGROUND_COLOR};
                color: {BUTTON_TEXT_COLOR};
                padding: 4px 12px;
                border-width: 2px;
                border-color: {BUTTON_BORDER_COLOR};
                border-style: solid;
                border-radius: 4px;
            }}
        """)
        remove_button.clicked.connect(self._remove_row)
        button_layout.addWidget(remove_button)

        button_layout.addStretch()
        layout.addWidget(button_widget)


    def values(self):
        return self.selected_fields


    def clear(self):
        while self.selected_fields:
            self._remove_row()


    def _signal_change(self):
        self.changed.emit(self.selected_fields)

    # If you need to add new code field type you can do it here
    def _add_row(self, layout, val1_field, val2_field):
        val1 = val1_field["dropdown_options"] if "dropdown_options" in val1_field else ""
        val2 = val2_field["dropdown_options"] if "dropdown_options" in val2_field else ""

        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 2, 0, 2)
        
        if val1_field["type"] == "dropdown":
            first_entry = QComboBox()
            first_entry.addItems(val1)
            first_entry.currentIndexChanged.connect(self._signal_change)
            row_layout.addWidget(first_entry)

        elif val1_field["type"] == "multiselect":
            first_entry = CheckableComboBox() 
            first_entry.addItems(val1)
            first_entry.checkedItemsChanged.connect(self._signal_change)
            row_layout.addWidget(first_entry)
            
        else:
            first_entry = QLineEdit(val1)
            first_entry.setMaximumWidth(200)
            first_entry.textEdited.connect(self._signal_change)
            row_layout.addWidget(first_entry)
        
        colon_label = QLabel(":")
        colon_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        row_layout.addWidget(colon_label)

        if val2_field["type"] == "dropdown":
            second_entry = QComboBox()
            second_entry.addItems(val2)
            second_entry.currentIndexChanged.connect(self._signal_change)
            row_layout.addWidget(second_entry)

        elif val2_field["type"] == "multiselect":
            second_entry  = CheckableComboBox() 
            second_entry.addItems(val2)
            second_entry.checkedItemsChanged.connect(self._signal_change)
            row_layout.addWidget(second_entry)

        else:
            second_entry = QLineEdit(val2)
            second_entry.setMaximumWidth(200)
            second_entry.textEdited.connect(self._signal_change)
            row_layout.addWidget(second_entry)

        row_layout.addStretch()
        layout.insertWidget(layout.count() - 1, row_widget)
        self.selected_fields.append((first_entry, second_entry))
        self._signal_change()


    def _remove_row(self):
        first_entry, second_entry = self.selected_fields.pop()
        row_widget = first_entry.parent()
        row_widget.deleteLater()
        self._signal_change()