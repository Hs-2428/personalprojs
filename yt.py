import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl


class YouTubeUnliker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Unliker")
        self.setGeometry(200, 100, 1200, 800)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://www.youtube.com/playlist?list=LL"))
        self.layout.addWidget(self.webview)

        self.auto_channel_checkbox = QCheckBox("Only remove videos from the first visible channel")
        self.layout.addWidget(self.auto_channel_checkbox)

        self.unlike_button = QPushButton("Start Unliking")
        self.unlike_button.clicked.connect(self.start_unliking)
        self.layout.addWidget(self.unlike_button)

    def start_unliking(self):
        script = f"""
        (async () => {{
            function sleep(ms) {{
                return new Promise(resolve => setTimeout(resolve, ms));
            }}

            const scrollAndLoad = async () => {{
                for (let i = 0; i < 15; i++) {{
                    window.scrollTo(0, document.body.scrollHeight);
                    await sleep(1500);
                }}
            }};

            const unlikeVideos = async (filterChannel) => {{
                await scrollAndLoad();
                const videos = document.querySelectorAll("ytd-playlist-video-renderer");
                if (filterChannel && videos.length > 0) {{
                    var channelName = videos[0].querySelector("#byline a")?.textContent.trim().toLowerCase();
                }}

                let removed = 0;
                for (const video of videos) {{
                    try {{
                        if (filterChannel) {{
                            const thisChannel = video.querySelector("#byline a")?.textContent.trim().toLowerCase();
                            if (thisChannel !== channelName) continue;
                        }}

                        const menuBtn = video.querySelector("ytd-menu-renderer yt-icon-button");
                        menuBtn.click();
                        await sleep(1000);

                        const options = [...document.querySelectorAll("ytd-menu-service-item-renderer yt-formatted-string")];
                        const removeOption = options.find(o => o.textContent.trim() === "Remove from Liked videos");

                        if (removeOption) {{
                            removeOption.click();
                            removed++;
                            await sleep(1500);
                        }}
                    }} catch (e) {{
                        console.error("Error unliking:", e);
                    }}
                }}

                alert(`Unliked ${{removed}} videos${{filterChannel ? " from channel " + channelName : ""}}.`);
            }};

            unlikeVideos({str(self.auto_channel_checkbox.isChecked()).lower()});
        }})();
        """
        self.webview.page().runJavaScript(script)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeUnliker()
    window.show()
    sys.exit(app.exec_())
