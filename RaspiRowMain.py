# Allow access to command-line arguments
import sys
import pyrow
 
# Import the core and GUI elements of Qt
from PyQt4.Qt import *
class PM3(QWidget):
    def __init__(self):
        super(PM3,self).__init__()
        self.pmCount = 0
        self.strokeCount = 0
        self.display = ""
        self.distance =0
    def paintEvent(self, event):
        qp = QPainter()
        font = QFont("times")
        fm = QFontMetrics(font)
        qp.begin(self)

        wnd = qp.window()
        w = wnd.width()
        h = wnd.height()
        qp.setBrush(QColor(127,127,192 ))
        qp.drawRect(0,0,w-1,h-1)
        qp.drawText(10, 10, self.display)
        bw = w /6 # 6 buoys on the screen
        dw = self.distance % 10
        offset = (dw/10) *bw
        for ix in range(0,10):
            qp.drawEllipse(ix * bw +offset, h/4, 5,5)
            qp.drawEllipse(ix * bw +offset, h/2, 5,5)
            qp.drawText(ix * bw +offset, h/4-20, str(10* ((ix -3) + int(self.distance/10))))


        qp.end()
class RaspiRowMain(QMainWindow):
    def __init__(self, parent = None):
        super(RaspiRowMain, self).__init__(parent)
        ergs = pyrow.find()
        if len(ergs) == 0: exit("No ergs found.")
        self.erg = pyrow.pyrow(ergs[0])
        self.initUI()
    def onStrokeTime(self):
        self.pm3.strokeCount = self.pm3.strokeCount +1
    def onPmRefresh(self):
        results = self.erg.getMonitor(True)
        cstate = results['strokestate'] & 0xF
        s = "Stroke : " + str(results['spm']) + "\r\n"
        s = s+ "Distance : " + str(results['distance']) + "\r\n"
        s = s + "Time : " + str(results['time']) + "\r\n"
        s = s + "Power : " + str(results['power']) +"\r\n"
        s = s + "Calories/hour : " + str(results['calhr'])+"\r\n"
        s = s + "Calories : " + str(results['calories'])+"\r\n"
        s = s + "Pace : " + str(results['pace'])+"\r\n"
        self.pm3.distance = results['distance']
        self.pm3.display = s
        self.pm3.pmCount = self.pm3.pmCount +1
        self.pm3.update()
    def initUI(self):
        openUserAction = QAction('&Open user', self)
        openUserAction.setShortcut('Ctrl+O')
        openUserAction.setStatusTip('CHoose or create a user')

#        openUserAction.triggered.connect(qApp.quit)

        exitAction = QAction('E&xit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openUserAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        self.toolbar = self.addToolBar('Main')
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(openUserAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(exitAction)
        self.statusBar().showMessage('Ready')

        self.mainBody = QVBoxLayout()
        self.pm3 = PM3()
        self.pm3.setGeometry(10,10,100,100)
        self.mainBody.addWidget(self.pm3)
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainBody)
        self.setCentralWidget(centralWidget)

        
        self.setGeometry(50,50,640,480)
        self.setWindowTitle('RaspiRow')
        # Add some timers

        self.strokeTime = QTimer(self)
        self.strokeTime.timeout.connect(self.onStrokeTime)
        self.strokeTime.start(2000)

        self.pmRefresh = QTimer(self)
        self.pmRefresh.timeout.connect(self.onPmRefresh)
        self.pmRefresh.start(50)

        self.show()
        print "after the show"
        print self.rect()
def main():
    app = QApplication(sys.argv)
    mw = RaspiRowMain()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
