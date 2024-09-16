# text_edit_logger.py

import logging
from PySide6.QtGui import QTextCursor

class QTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        self.widget.moveCursor(QTextCursor.MoveOperation.End)
