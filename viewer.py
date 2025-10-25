import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QWidget, QLabel, QListWidget, QVBoxLayout, QScrollArea, \
    QListWidgetItem, QHBoxLayout, QFrame, QPushButton, QFileDialog, QApplication, QSplitter, QProgressBar, \
    QGraphicsPixmapItem

import themes
from tool_detector import ToolDetector


class ImageViewer(QGraphicsView):
    """Viewer widget that will later support zoom/pan/overlays."""

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        # self.setRenderHint(self.renderHints.)

    def set_image(self, pixmap: QPixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def get_image(self) -> QPixmap:
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                return item.pixmap()  # this is your QPixmap


class Sidebar(QWidget):
    """Right-hand panel showing detections and metadata."""

    def __init__(self):
        super().__init__()

        self.file_label = QLabel("File: —")
        self.size_label = QLabel("Size: —")
        self.dim_label = QLabel("Dimensions: —")

        self.detect_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.dim_label)

        title = QLabel("Detections")
        title.setStyleSheet("font-weight:bold; margin-top:10px;")
        layout.addWidget(title)
        layout.addWidget(self.detect_list)

        layout.addStretch()
        self.setLayout(layout)

    def update_info(self, filename, size_text, dims_text, detections):
        self.file_label.setText(f"File: {filename}")
        self.size_label.setText(f"Size: {size_text}")
        self.dim_label.setText(f"Dimensions: {dims_text}")

        self.detect_list.clear()
        for d in detections:
            QListWidgetItem(d, self.detect_list)


class ThumbnailBar(QScrollArea):
    """Horizontal thumbnail strip."""

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.thumb_container = QHBoxLayout()
        holder = QWidget()
        holder.setLayout(self.thumb_container)
        self.setWidget(holder)
        self.setFixedHeight(100)

    def add_thumbnail(self, pixmap, callback):
        label = QLabel()
        label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setFrameShape(QFrame.StyledPanel)
        label.setStyleSheet("border:1px solid #444; margin:4px;")
        label.mousePressEvent = lambda event: callback()
        self.thumb_container.addWidget(label)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unwanted Tool Detector - PySide Viewer")
        self.resize(1200, 700)

        # Top bar buttons
        self.btn_load = QPushButton("Select Images")
        self.btn_run = QPushButton("Run AI")
        self.btn_export = QPushButton("Export JSON")
        self.btn_clear = QPushButton("Clear")

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.btn_load)
        top_bar.addWidget(self.btn_run)
        top_bar.addWidget(self.btn_export)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_clear)

        # Main layout split view
        self.viewer = ImageViewer()
        self.sidebar = Sidebar()
        splitter = QSplitter()
        splitter.addWidget(self.viewer)
        splitter.addWidget(self.sidebar)
        splitter.setSizes([900, 300])

        # Thumbnails
        self.thumb_bar = ThumbnailBar()

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(splitter)
        layout.addWidget(self.thumb_bar)

        self.setLayout(layout)

        # Connect buttons
        self.btn_load.clicked.connect(self.load_images)
        self.btn_clear.clicked.connect(self.clear_photos)
        self.btn_run.clicked.connect(self.run_ai)

        self.images = {}
        self.tool_detector = None

    def load_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not files:
            return

        for path in files:
            pix = QPixmap(path)

            self.images[id(pix.__hash__())] = path
            self.thumb_bar.add_thumbnail(pix, lambda p=path, px=pix: self.show_image(p, px))

        # Auto-display first image
        if len(files) > 0:
            self.show_image(files[0], QPixmap(files[0]))

    def clear_photos(self):
        self.images.clear()
        self.viewer.set_image(QPixmap())
        # while len(self.thumb_bar.children()) > 0:
        #     self.thumb_bar.children().pop()

    def show_image(self, path, pixmap):
        self.viewer.set_image(pixmap)
        size_text = f"{pixmap.width()}×{pixmap.height()}"
        self.sidebar.update_info(path.split("/")[-1], "—", size_text, [])

    def get_image_in_pil(self):
        image_pixmap = self.viewer.get_image()
        path = self.images.get(image_pixmap.__hash__())
        # item1 = self.images[0]
        print("test")

    def run_ai(self):
        image = self.get_image_in_pil()
        # self.tool_detector.predict()
        print("test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    screens = app.screens()
    third_screen = screens[1]
    geometry = third_screen.geometry()

    window.move(geometry.left() + 100, geometry.top() + 100)
    window.showFullScreen()
    app.setStyleSheet(themes.DARK_STYLE)

    window.show()

    window.tool_detector = ToolDetector(model_path='model_local.pkl')

    sys.exit(app.exec())
