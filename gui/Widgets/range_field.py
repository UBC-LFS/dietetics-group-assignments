import os
from styles import *
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QLineEdit, QPushButton, QScrollArea, QCheckBox, QWidget, QLabel 

class RangeField(QWidget):
    changed = Signal(dict)


    def __init__(self, default_min=0, default_max=100):
        super().__init__()

        self.min_entry = None
        self.max_entry = None
        self.default_min = default_min
        self.default_max = default_max

        layout = QHBoxLayout()
        self.setLayout(layout)

        min_label = QLabel("Min:")
        min_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        layout.addWidget(min_label)

        self.min_entry = QLineEdit(str(self.default_min))
        self.min_entry.setMaximumWidth(80)
        self.min_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.min_entry.textEdited.connect(self._signal_change)
        layout.addWidget(self.min_entry)

        layout.addSpacing(15)

        max_label = QLabel("Max:")
        max_label .setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        layout.addWidget(max_label)

        self.max_entry = QLineEdit(str(self.default_max))
        self.max_entry.setMaximumWidth(80)
        self.max_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.max_entry.textEdited.connect(self._signal_change)
        layout.addWidget(self.max_entry)

        layout.addStretch()


    def values(self):
        return { "min": int(self.min_entry.text()), "max": int(self.max_entry.text()) }


    def reset(self):
        self.min_entry.setText(str(self.default_min))
        self.max_entry.setText(str(self.default_max))


    def _signal_change(self):
        list_range = self.values()
        self.changed.emit(list_range)
