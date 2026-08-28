import sys
from PySide6.QtWidgets import QApplication
from project_matching import ProjectMatchingGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        import pyi_splash
        if pyi_splash.is_alive():
            pyi_splash.close()
    except ImportError:
        pass

    project_matching = ProjectMatchingGUI()
    project_matching.show()
    sys.exit(app.exec())
