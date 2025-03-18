import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QTextEdit, QPushButton, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QKeySequence
import tweepy
from dotenv import load_dotenv

class XPosterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("X Poster")
        self.setFixedSize(400, 200)

        # Load environment variables
        load_dotenv()

        # Initialize Twitter client
        self.client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create text area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("What's on your mind?")
        layout.addWidget(self.text_area)

        # Create character counter
        self.char_counter = QPushButton("0/280")
        self.char_counter.setEnabled(False)
        layout.addWidget(self.char_counter)

        # Create post button
        self.post_button = QPushButton("Post (⌘+Return)")
        self.post_button.clicked.connect(self.post_tweet)
        layout.addWidget(self.post_button)

        # Connect text area to update counter
        self.text_area.textChanged.connect(self.update_counter)

        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)

        # Find app icon path
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "X Poster.app/Contents/Resources/AppIcon.icns")
        app_path = "/Applications/X Poster.app/Contents/Resources/applet.icns"

        # Try to use app icon, fall back to system icon
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        elif os.path.exists(app_path):
            self.tray_icon.setIcon(QIcon(app_path))
        else:
            self.tray_icon.setIcon(QIcon.fromTheme("document-edit"))

        # Make the tray icon visible
        self.tray_icon.setVisible(True)

        # Create tray menu
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # Connect tray icon activation
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Create keyboard shortcut for posting
        post_shortcut = QAction("Post", self)
        post_shortcut.setShortcut(QKeySequence("Ctrl+Return"))
        post_shortcut.triggered.connect(self.post_tweet)
        self.addAction(post_shortcut)

        # Create Command+Return shortcut for macOS users
        post_shortcut_mac = QAction("Post Mac", self)
        post_shortcut_mac.setShortcut(QKeySequence("Meta+Return"))
        post_shortcut_mac.triggered.connect(self.post_tweet)
        self.addAction(post_shortcut_mac)

        # Hide window when closed
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

    def update_counter(self):
        text = self.text_area.toPlainText()
        count = len(text)
        self.char_counter.setText(f"{count}/280")

        # Limit text to 280 characters
        if count > 280:
            cursor = self.text_area.textCursor()
            cursor.deletePreviousChar()
            self.text_area.setTextCursor(cursor)

    def post_tweet(self):
        tweet_content = self.text_area.toPlainText()
        if not tweet_content:
            return

        try:
            self.client.create_tweet(text=tweet_content)
            self.text_area.clear()
            self.tray_icon.showMessage(
                "Success",
                "Tweet posted successfully!",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        except Exception as e:
            self.tray_icon.showMessage(
                "Error",
                f"Failed to post tweet: {str(e)}",
                QSystemTrayIcon.MessageIcon.Critical,
                2000
            )

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "X Poster",
            "App minimized to tray. Click the tray icon to show the window.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

def main():
    app = QApplication(sys.argv)
    window = XPosterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
