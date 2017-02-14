from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *
import sys
import os


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  About Dialog Class ~~~~~~~~~~~~~~~~~~~~~~
class AboutDialog(QDialog):

    def __init__(self,*args,**kwargs):
        super(AboutDialog,self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # no Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)    # Not connected

        layout = QVBoxLayout()

        #Adding The title
        title = QLabel("ChadwickBrowser Limited Edition")
        font = title.font()
        font.setPointSize(12)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter) # to Center the title
        layout.addWidget(title)

        # The CHadwick Logo
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join("James_Chadwick.jpg")))
        logo.setAlignment(Qt.AlignHCenter)
        layout.addWidget(logo)

        # Other Widgets
        version=QLabel("Version 1.0 ")
        version.setAlignment(Qt.AlignHCenter)
        layout.addWidget(version)

        copyright=QLabel("Copyright 2016 Benabderrahmane Inc ")
        copyright.setAlignment(Qt.AlignHCenter)
        layout.addWidget(copyright)

        layout.addWidget(self.buttonBox)


        self.setLayout(layout)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~








#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Window Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MainWindow(QMainWindow):


    def __init__(self,*args ,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        # Tabbed webView
        self.tabs = QTabWidget()    # Hold all the tabs
        self.tabs.setDocumentMode(True) # To change the layout for the tabs ...
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick) # open new tab by double clicking
        self.tabs.setTabsClosable(True) # Allow closing tabs
        self.tabs.tabCloseRequested.connect(self.close_current_tab )

        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.current_tab_changed)



        #~~~~~~~~ To set without tabs ~~~~~~~~~~~~~~~~~~~~~~~~
        #self.browser= QWebView()
        #self.browser.setUrl(QUrl("http://www.google.fr"))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # We create our Toolbar~~~~~~~~~~~~~~~~~~~~~~~~
        toolBar = QToolBar("Nav")
        toolBar.setIconSize(QSize(18,18))
        self.addToolBar(toolBar)


        # back button :~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        back = QAction(QIcon(os.path.join('back_2.png')),"Back",self)
        back.setStatusTip("Back to previous page")
        # Using a Lambda i connect back signal to the widget saved in self.tabs.currentWidget()
        back.triggered.connect(lambda: self.tabs.currentWidget().back())
        toolBar.addAction(back)
        ###############################################################

        # Forward Button ###############################################
        F = QAction(QIcon(os.path.join('forward_2.png')),"Forward",self)
        F.setStatusTip("Next page")
        F.triggered.connect(lambda: self.tabs.currentWidget().forward())
        toolBar.addAction(F)
        ##################################################################

        # Stop Button #######################################################
        stop = QAction(QIcon(os.path.join('stop-red.png')),"Stop",self)
        stop.setStatusTip("Stop")
        stop.triggered.connect(lambda: self.tabs.currentWidget().stop())
        toolBar.addAction(stop)
        ####################################################################


        # Reload Button  #####################################################
        rload  = QAction(QIcon(os.path.join('reload.png')),"Reload",self)
        rload.setStatusTip("Reload")
        rload.triggered.connect(lambda: self.tabs.currentWidget().reload())
        toolBar.addAction(rload)
        #####################################################################



        # Add a UrlBar####################################################
        self.urlbar=QLineEdit()
        toolBar.addSeparator()
        self.urlbar.returnPressed.connect(self.nav_to)
        toolBar.addWidget(self.urlbar)

        self.httpsicon=QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('Olock.png')))
        toolBar.addWidget(self.httpsicon)
        ##################################################################


        #self.menuBar().setNativeMenuBar(False)


        #~~~~~~~~~~~~~~~~menuBar~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Creating the File Menu
        file_menu = self.menuBar().addMenu("&File")

        # Create new tab
        new_tab_action = QAction( QIcon(os.path.join("add_tab.png") ) , "Open new tab ... " , self )
        new_tab_action.setStatusTip("Open new tab ")
        # I use a lambda here again because add new tab expectx to receive a QUrl
        # for the new page to open
        new_tab_action.triggered.connect(lambda x :  self.add_new_tab() )
        file_menu.addAction(new_tab_action)


        # Open File
        open_file_action = QAction( QIcon(os.path.join("folder-open.png") ) , "Open File ... " , self )
        open_file_action.setStatusTip("Open From File")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Save File
        save_file_action = QAction( QIcon(os.path.join("save-file.png") ) , "Save page as ..." , self )
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # Print
        print_action = QAction(QIcon(os.path.join("print.png")),"Print ... ",self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Help Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction(QIcon(os.path.join("about.png") ) , "About..." , self )
        about_action.setStatusTip("Find out more about ChadwickBrowser")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)


        #~~~~~~~~~~~~~~~~~~~~~~~~ Go to My HomePage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        go_home_page = QAction(QIcon(os.path.join("home.png") ) , "Chadwick Browser HomePage..." , self )
        go_home_page.setStatusTip("Visit the ChadwickBrowser HomePage")
        go_home_page.triggered.connect(self.go_home_page)
        help_menu.addAction(go_home_page)



        self.add_new_tab(QUrl('http://www.google.fr'), 'HomePage')



        #~~~~~~~~~~~~~~~~~~~~~~~~~ Title and Icon~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.show()
        self.setWindowTitle("Chadwick Browser")
        self.setWindowIcon(QIcon(os.path.join('James_Chadwick.jpg') ) )
        ##################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_new_tab(self,qurl=None,label='Blank'):

        if qurl is None:
            qurl = QUrl('')

        browser = QWebView()
        browser.setUrl(qurl)


        i = self.tabs.addTab(browser,label)

        self.tabs.setCurrentIndex(i)    # The current tab is the newly created


        # More Difficult! :)   We only want to update the url when it's from the
        # Correct tab
        browser.urlChanged.connect(lambda qurl, browser = browser:
            self.update_url(qurl,browser) )
        browser.loadFinished.connect(lambda _, i = i , browser=browser:
            self.tabs.setTabText (i,browser.page().mainFrame().title() ) )

    def tab_open_doubleclick(self, i ):
        if i == -1 :    # No tab under the click
            self.add_new_tab()


    def current_tab_changed(self, i ):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget() )


    def close_current_tab(self,i):
        if self.tabs.count() < 2 :  # Don't close the last tab ...
            return
        self.tabs.removeTab(i)


    def go_home_page(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.mohammed-benabderrahmane.com"))


    def update_url(self,q,browser=None):
        # Here i test if the browser have been passed from a lambda function and
        # the signal is equal to the current Widget
        if browser != self.tabs.currentWidget():
            # if this signal is not from the current tab , ignore !
            return

        self.urlbar.setText(q.toString())   # Show the URL
        self.urlbar.setCursorPosition(0)    # TO show the begining of the URL

        # To see if THe URL is Secured or not
        if(q.scheme()=='https'):
            self.httpsicon.setPixmap(QPixmap(os.path.join('Lock.png') ))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('Olock.png') ))


    # Allow the user to navigate using the URL
    def nav_to(self):
        a = QUrl(self.urlbar.text())
        if a.scheme() == "":
            a.setScheme("http")
        self.tabs.currentWidget().setUrl(a)

    #"Prinintg function"
    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect( self.tabs.currentWidget().print_ )
        dlg.exec_()


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self,"Open File", "" , "Hypertext Markup Language(*.htm,*.html);;" "All files(*.*)" )

        if filename:
            with open(filename,'r') as f :
                html = f.read()
            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)


    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self,"Save page as ", "" , "Hypertext Markup Language(*.htm,*.html);;" "All files(*.*)" )

        if filename:
            html = self.tabs.currentWidget().page().mainFrame().toHtml() # Each page has a mainFrame ...
            with open(filename,'w') as f :
                f.write(html)
            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)


    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END OF MainWindow Class ~~~~~~~~~~~~~~~~~~~~~~




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~RUN the APP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app=QApplication(sys.argv)
app.setApplicationName("ChadwickBrowser")
app.setOrganizationName("ChadwickBros")
app.setOrganizationDomain("http://www.mohammed-benabderrahmane.com")

window = MainWindow()

app.exec_()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
