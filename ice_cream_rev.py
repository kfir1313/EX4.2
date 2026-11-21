import sys
from pathlib import Path
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    """
    A PySide6 graphical user interface with file selection,
    a zoomable Matplotlib canvas (without toolbar), and graph export capability.
    """

    def __init__(self, stylesheet_path: str = "styles.qss") -> None:
        super().__init__()

        self.setWindowTitle("Data Plotter & Visualizer")
        self.resize(900, 650)
        self.setMinimumSize(700, 500)

        self.selected_file_path: str = ""

        # Tracking state for drag-to-pan & zoom reset
        self._pan_start = None
        self._initial_xlim = None
        self._initial_ylim = None

        # Load external QSS styling
        self.load_stylesheet(stylesheet_path)

        # Build interface
        self._setup_ui()

        # Display sine wave on the graph at startup
        self.plot_sine()

        self.statusBar().showMessage(
            "Ready. Zoom: Scroll wheel | Pan: Click & drag | Reset view: Double-click"
        )

    def load_stylesheet(self, stylesheet_path: str) -> None:
        """Load and apply QSS stylesheet from a file."""
        qss_file = Path(stylesheet_path)
        if not qss_file.is_absolute():
            qss_file = Path(__file__).resolve().parent / stylesheet_path

        if qss_file.exists():
            with open(qss_file, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Warning: Stylesheet file not found at: {qss_file}")

    def _setup_ui(self) -> None:
        """Set up UI layout and widgets."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # --- Top Controls Bar ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # Select file button
        self.select_file_btn = QPushButton("Select File...")
        self.select_file_btn.setCursor(Qt.PointingHandCursor)
        self.select_file_btn.clicked.connect(self.select_file)
        controls_layout.addWidget(self.select_file_btn)

        # File path display
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("No file selected...")
        controls_layout.addWidget(self.file_path_edit, stretch=1)

        # Save graph button
        self.save_graph_btn = QPushButton("Save Graph...")
        self.save_graph_btn.setCursor(Qt.PointingHandCursor)
        self.save_graph_btn.clicked.connect(self.save_graph)
        controls_layout.addWidget(self.save_graph_btn)

        main_layout.addLayout(controls_layout)

        # --- Matplotlib Canvas (No Toolbar) ---
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        main_layout.addWidget(self.canvas, stretch=1)

        # Connect canvas events for zooming, panning, and resetting view
        self.canvas.mpl_connect("scroll_event", self._on_scroll_zoom)
        self.canvas.mpl_connect("button_press_event", self._on_button_press)
        self.canvas.mpl_connect("button_release_event", self._on_button_release)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion_notify)

        # Status Bar
        self.setStatusBar(QStatusBar(self))

    def plot_sine(self) -> None:
        """Plot a sine function on the zoomable graph."""
        self.ax.clear()
        self.figure.set_facecolor("#f3f5f9")
        self.ax.set_facecolor("#ffffff")

        # Generate sine wave data points
        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        # Plot the sine curve
        self.ax.plot(x, y, label=r"$y = \sin(x)$", color="#1f77b4", linewidth=2)
        self.ax.set_title("Sine Function", fontsize=13, pad=10)
        self.ax.set_xlabel("x (radians)", fontsize=10)
        self.ax.set_ylabel("sin(x)", fontsize=10)
        self.ax.grid(True, linestyle="--", color="#dce3ed", alpha=0.9)
        self.ax.tick_params(colors="#526176")
        self.ax.title.set_color("#202b3c")
        self.ax.xaxis.label.set_color("#526176")
        self.ax.yaxis.label.set_color("#526176")
        for spine in self.ax.spines.values():
            spine.set_color("#cbd3df")

        self.figure.tight_layout()
        self.canvas.draw()

        # Store initial limits for double-click reset
        self._initial_xlim = self.ax.get_xlim()
        self._initial_ylim = self.ax.get_ylim()

    def select_file(self) -> None:
        """Allow user to select a file via a file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Supported Files (*.csv *.txt *.dat);;CSV Files (*.csv);;All Files (*.*)",
        )

        if file_path:
            self.selected_file_path = file_path
            self.file_path_edit.setText(file_path)
            self.statusBar().showMessage(f"Selected file: {Path(file_path).name}")

    def save_graph(self) -> None:
        """Allow user to save the current graph to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Graph As",
            "plot.png",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;PDF Document (*.pdf);;SVG Vector (*.svg)",
        )

        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches="tight")
                self.statusBar().showMessage(f"Graph saved: {Path(file_path).name}")
            except Exception as e:
                self.statusBar().showMessage(f"Error saving graph: {e}")

    def _on_scroll_zoom(self, event) -> None:
        """Zoom in or out using the mouse scroll wheel centered on cursor."""
        if event.inaxes != self.ax:
            return

        base_scale = 1.2
        if event.button == "up":
            scale_factor = 1 / base_scale
        elif event.button == "down":
            scale_factor = base_scale
        else:
            scale_factor = 1.0

        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        xdata = event.xdata
        ydata = event.ydata

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.canvas.draw_idle()

    def _on_button_press(self, event) -> None:
        """Handle mouse clicks: double-click to reset, drag to pan."""
        if event.inaxes != self.ax:
            return

        # Double-click resets view to initial limits
        if event.dblclick and self._initial_xlim and self._initial_ylim:
            self.ax.set_xlim(self._initial_xlim)
            self.ax.set_ylim(self._initial_ylim)
            self.canvas.draw_idle()
            self.statusBar().showMessage("View reset to original limits.")
            return

        # Start panning on left or middle button click
        if event.button in (1, 2):
            self._pan_start = (event.x, event.y, self.ax.get_xlim(), self.ax.get_ylim())

    def _on_button_release(self, event) -> None:
        """End panning on button release."""
        self._pan_start = None

    def _on_motion_notify(self, event) -> None:
        """Handle mouse drag to pan across axes."""
        if self._pan_start is None or event.inaxes != self.ax:
            return

        start_x, start_y, xlim_orig, ylim_orig = self._pan_start
        dx_pixels = event.x - start_x
        dy_pixels = event.y - start_y

        # Convert pixel displacement to data coordinates
        bbox = self.ax.bbox
        dx_data = -dx_pixels * (xlim_orig[1] - xlim_orig[0]) / bbox.width
        dy_data = -dy_pixels * (ylim_orig[1] - ylim_orig[0]) / bbox.height

        self.ax.set_xlim([xlim_orig[0] + dx_data, xlim_orig[1] + dx_data])
        self.ax.set_ylim([ylim_orig[0] + dy_data, ylim_orig[1] + dy_data])
        self.canvas.draw_idle()


def main() -> None:
    """Application entry point."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    if not QApplication.instance().property("_is_interactive"):
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
