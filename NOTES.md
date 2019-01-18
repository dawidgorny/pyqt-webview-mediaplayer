$ pipenv shell
$ pipenv run python main.py

## VIDEO
https://pythonprogramminglanguage.com/pyqt5-video-widget/

https://github.com/baoboa/pyqt5/blob/master/examples/multimediawidgets/videowidget.py

## JS callback
https://stackoverflow.com/questions/45230931/qwebengineview-javascript-callback

view.runJavaScript("document.getElementsByName('email')[0].value", self.store_value)

intercept navigation links clicked
https://stackoverflow.com/questions/3188513/catch-link-clicks-in-qtwebview-and-open-in-default-browser

use QWebChannel to export a QObject and call the function
https://stackoverflow.com/questions/52197927/how-to-detect-button-click-inside-qwebengine-in-pyside2

http://doc.qt.io/qt-5/qtwebchannel-javascript.html

https://stackoverflow.com/questions/39544089/how-can-i-access-python-code-from-javascript-in-pyqt-5-7

Signals
https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal

WebSocket?

## Debuging js
https://stackoverflow.com/questions/28681141/qtwebengine-debugging

QTWEBENGINE_REMOTE_DEBUGGING=<port>

```
class WebPage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    @pyqtSlot(str)
    def print(self, text):
        print('From JS:', text)

```

https://riverbankcomputing.com/pipermail/pyqt/2015-August/036346.html





