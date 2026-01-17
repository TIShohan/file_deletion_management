import sys
import os

# Ensure backend modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
