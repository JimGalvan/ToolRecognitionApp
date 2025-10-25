DARK_STYLE = """
    QWidget {
        background-color: #0f1115;
        color: #e8eefc;
        font-family: Segoe UI, sans-serif;
        font-size: 14px;
    }

    QLabel {
        color: #e8eefc;
    }

    QPushButton {
        background-color: #1a1d25;
        color: #e8eefc;
        border: 1px solid #2b3140;
        border-radius: 6px;
        padding: 6px 10px;
    }
    QPushButton:hover {
        background-color: #232733;
    }
    QPushButton:pressed {
        background-color: #2c3040;
    }

    QListWidget, QScrollArea, QGraphicsView {
        background-color: #141823;
        border: 1px solid #2b3140;
    }

    QListWidget::item {
        padding: 6px;
    }
    QListWidget::item:selected {
        background-color: #2b3550;
        border-left: 3px solid #5b8cff;
    }

    QScrollBar:vertical, QScrollBar:horizontal {
        background: #141823;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle {
        background: #2b3140;
        border-radius: 6px;
    }
    QScrollBar::handle:hover {
        background: #3a4152;
    }

    QSplitter::handle {
        background-color: #2b3140;
    }
    """