import sys
import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineScript
from PyQt5.QtCore import QDir, Qt, QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon


class MediaPlayerBridge(QObject):
  positionChanged = pyqtSignal(int)

  def __init__(self, mediaPlayer):
    super(MediaPlayerBridge, self).__init__()
    self.mediaPlayer = mediaPlayer
    self.mediaPlayer.positionChanged.connect(self.onPositionChanged)

  def onPositionChanged(self, position):
    self.positionChanged.emit(position)
  
  @pyqtSlot()
  def playStop(self):
      print("playStop")
      if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
          self.mediaPlayer.pause()
      else:
          self.mediaPlayer.play()


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)
        self.loadFinished.connect(self.onLoadFinished)
    
    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    def onLoadFinished(self, ok):
        print("Finished loading: ", ok)
        if ok:
            self.load_qwebchannel()
            self.run_scripts_on_load()

    def load_qwebchannel(self):
        file = QtCore.QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            self.runJavaScript(content.data().decode())
        if self.webChannel() is None:
            channel = QtWebChannel.QWebChannel(self)
            self.setWebChannel(channel)

    def add_objects(self, objects):
        if self.webChannel() is not None:
            initial_script = ""
            end_script = ""
            # self.webChannel().registerObjects(objects)
            for name, obj in objects.items():
                self.webChannel().registerObject(name, obj)
                initial_script += "var {helper};".format(helper=name)
                end_script += "{helper} = channel.objects.{helper};".format(helper=name)
                end_script += "window.{helper} = {helper};".format(helper=name)
            js = initial_script + \
                 "new QWebChannel(qt.webChannelTransport, function (channel) {" + \
                 end_script + \
                 " if (window.onwebchannel) window.onwebchannel.call(this) } );"
            self.runJavaScript(js)

    def run_scripts_on_load(self):
        pass


class WebRTCPageView(WebEnginePage):
    objects = {}

    def __init__(self, *args, **kwargs):
        super(WebRTCPageView, self).__init__(*args, **kwargs)
        # self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)
        self.load(QtCore.QUrl.fromLocalFile(os.path.abspath('index.html')))

    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QtWebEngineWidgets.QWebEnginePage.MediaAudioCapture,
                       QtWebEngineWidgets.QWebEnginePage.MediaVideoCapture,
                       QtWebEngineWidgets.QWebEnginePage.MediaAudioVideoCapture):
            self.setFeaturePermission(url, feature, QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, QtWebEngineWidgets.WebEnginePage.PermissionDeniedByUser)

    def run_scripts_on_load(self):
      if self.url() == QtCore.QUrl.fromLocalFile(os.path.abspath('index.html')):
        self.add_objects(self.objects)
        # self.add_objects({"jshelper": self})
    
        
 
class App(QWidget):
  
  def __init__(self):
    super().__init__()
    self.title = 'Main'
    self.left = 10
    self.top = 10
    self.width = 640
    self.height = 480

    self.setWindowTitle(self.title)
    # self.setGeometry(self.left, self.top, self.width, self.height)

    # Create video widget
    self.videoWidget = QVideoWidget()
    self.videoWidget.setMinimumSize(320, 320)
    # Create Media player
    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    self.mediaPlayer.setVideoOutput(self.videoWidget)
    # self.mediaPlayer.positionChanged.connect(self.positionChanged)

    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath('sample2.mov'))))

    # Create media player bridge
    self.mediaPlayerBridge = MediaPlayerBridge(self.mediaPlayer)

    # Create Web View
    self.webView = QtWebEngineWidgets.QWebEngineView()
    self.page = WebRTCPageView()
    self.page.objects = {"mediaPlayerBridge": self.mediaPlayerBridge}
    self.page.profile().clearHttpCache()
    self.webView.setPage(self.page)
    
    # Create layout
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(self.videoWidget)
    layout.addWidget(self.webView)

    self.setLayout(layout)
    self.resize(640, 800)
    self.show()
    
    self.mediaPlayer.play()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
