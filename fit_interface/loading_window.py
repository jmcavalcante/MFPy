from PyQt5.QtWidgets import QDialog, QVBoxLayout,QLabel,QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class LoadingWindow(QDialog):
    def __init__(self, gif_path=r"fit_interface/design/loading.gif", parent=None):
        super().__init__(parent)

        # Configure the dialog window
        self.setWindowTitle("Loading fit")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 300)

        # Layout
        layout = QVBoxLayout(self)

        # Label to show the GIF
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Load the GIF
        self.loading_gif = QMovie(gif_path)
        self.gif_label.setMovie(self.loading_gif)
        self.loading_gif.start()  # Start playing the GIF

        # Button to close the window
        self.stop_button = QPushButton("Stop fit", self)
        self.stop_button.clicked.connect(self.close_window)

        # Add widgets to layout
        layout.addWidget(self.gif_label)
        layout.addWidget(self.stop_button)

    def close_window(self):
        """Stop the GIF and close the window."""
        self.close()