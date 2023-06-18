# i am lazy programmer

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QFileDialog, QProgressBar , QVBoxLayout, QCheckBox, QBoxLayout, QLineEdit
from datetime import datetime
import shutil

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Map Copier")
        self.resize(840, 600)
        #fix window size
        self.setMaximumSize(840, 600)
        self.setMinimumSize(840, 600)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        #make window dark mode
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        self.vb = QVBoxLayout(self)
        
        #add 3 clicklable emoji on top right corner.
        #location origin is top right corner
        #grid layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        #place grid layout on top right corner
        self.grid.setAlignment(Qt.AlignTop)

        #add 2 clicklable emoji and 1 long box on top.
        
        #close button
        self.closeButton = QPushButton("x")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.clicked.connect(self.close)
        #remove border
        self.closeButton.setStyleSheet("border: 0px;")
        self.closeButton.enterEvent = lambda event: self.btn_hovered_brighter(self.closeButton)
        self.closeButton.leaveEvent = lambda event: self.btn_hovered_restore(self.closeButton)

        #minimize button
        self.minimizeButton = QPushButton("-")
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.clicked.connect(self.showMinimized)
        #remove border
        self.minimizeButton.setStyleSheet("border: 0px;")
        self.minimizeButton.enterEvent = lambda event: self.btn_hovered_brighter(self.minimizeButton)
        self.minimizeButton.leaveEvent = lambda event: self.btn_hovered_restore(self.minimizeButton)

        #long box
        self.longBox = QPushButton("")
        #it should fill the rest of the space
        self.longBox.setFixedSize(780, 35)
        #add text
        self.longBox.setText("Map Copier by ssapgosu")
        #remove border
        self.longBox.setStyleSheet("border: 0px;")
        #make it moveable
        self.longBox.mousePressEvent = self.mousePressEvent
        self.longBox.mouseMoveEvent = self.mouseMoveEvent

        #locate them on top right corner
        self.grid.addWidget(self.longBox, 0, 0)
        self.grid.addWidget(self.minimizeButton, 0, 1)
        self.grid.addWidget(self.closeButton, 0, 2)
        
        self.vb.addLayout(self.grid)
        self.shenani = QLabel("Made by ssapgosu \nauto select one diff from folder.(excluding .osb) \nDM me for bugs and suggestions")
        self.lay5 = QBoxLayout(QVBoxLayout.Direction.LeftToRight, self)
        self.lay5.setSpacing(0)
        self.lay5.setContentsMargins(90, 30, 0, 0)
        self.lay5.addWidget(self.shenani)
        self.vb.addLayout(self.lay5)
        #add title
        self.title = QLabel("Map Copier")

        #get folder path
        self.folderPath = QPushButton("Select Folder")
        self.folderPath.clicked.connect(self.getFolderPath)
        #size of button
        self.folderPath.setFixedSize(200, 30)
        #remove border
        self.folderPath.setStyleSheet("border: 0px;")
        self.folderPath.enterEvent = lambda event: self.btn_hovered_brighter(self.folderPath)
        self.folderPath.leaveEvent = lambda event: self.btn_hovered_restore(self.folderPath)
        
        #label for folder path
        self.folderPathLabel = QLabel("Selected Folder: ")
        self.folderPathLabel.setFixedSize(600, 20)
        self.folderPathLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        #ask for name
        self.askName = QLabel("Enter creator name: ")
        self.askName.setFixedSize(400, 20)
        self.askName.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        #get name
        self.name = QLineEdit()
        self.name.setFixedSize(200, 30)


        #checkboxes
        #checkbox for copying non-bpm SVs
        self.copyNonBpmSV = QCheckBox("Copy non-bpm SVs")
        self.copyNonBpmSV.setChecked(True)

        #checkbox for copying original background
        self.copyOriginalBG = QCheckBox("Copy original background")
        self.copyOriginalBG.setChecked(True)

        self.copyTags = QCheckBox("Copy tag + source")
        self.copyTags.setChecked(True)

        self.copyDifficulty = QCheckBox("Copy difficulty settings (HP, OD, CS, AR) + keymodes")
        self.copyDifficulty.setChecked(False)
        
        #make empty box space
        self.emptyBox = QLabel("")
        self.emptyBox.setFixedSize(300, 30)

        self.lay2 = QBoxLayout(QBoxLayout.Direction.TopToBottom, self)
        self.lay2.setSpacing(0)
        self.lay2.setContentsMargins(100, 30, 0, 0)
        self.lay2.addWidget(self.copyNonBpmSV)
        self.lay2.addWidget(self.copyOriginalBG)
        self.lay2.addWidget(self.copyTags)
        self.lay2.addWidget(self.copyDifficulty)
        self.lay2.addWidget(self.emptyBox)

        self.lay3 = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)
        self.lay3.setSpacing(0)
        self.lay3.setContentsMargins(20, 30, 0, 0)
        self.lay3.addWidget(self.askName)
        self.lay3.addWidget(self.name)


        #make new grid for actual content
        self.grid2 = QGridLayout()
        self.grid2.setSpacing(0)
        self.grid2.setContentsMargins(90, 0, 75, 0)
        self.grid2.addWidget(self.folderPathLabel, 0, 0)
        self.grid2.addWidget(self.folderPath, 0, 1)
        
        
        
        self.vb.addLayout(self.grid2)
        self.vb.addLayout(self.lay3)
        self.vb.addLayout(self.lay2)
        self.vb.setContentsMargins(0, 0, 0, 20)

        self.convertButton = QPushButton("Convert to empty map")
        self.convertButton.setFixedSize(600, 30)
        self.convertButton.clicked.connect(self.convert)
        self.convertButton.setStyleSheet("background-color: #1e1e1e; color: #ffffff;border: 0px;")
        self.convertButton.enterEvent = lambda event: self.btn_hovered_brighter(self.convertButton)
        self.convertButton.leaveEvent = lambda event: self.btn_hovered_restore(self.convertButton)
        
        self.lay4 = QBoxLayout(QBoxLayout.Direction.TopToBottom, self)
        self.lay4.setSpacing(0)
        self.lay4.setContentsMargins(120, 0, 0, 0)
        self.lay4.addWidget(self.convertButton)

        self.conditions = QLabel("")
        self.conditions.setFixedSize(600, 30)
        self.conditions.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.lay4.addWidget(self.conditions)
        
        self.vb.addLayout(self.lay4)

        

        
    def convert(self):
        creator = self.name.text()
        try:
            songDir = "/".join(self.folderDir.split("/")[0:-1])
            file_list = os.listdir(self.folderDir)
            for file in file_list:
                if file.endswith(".osu"):
                    osb = file
                    break
                
            rosb = open(self.folderDir + "/" + osb, "r")
            lines = rosb.readlines()
            rosb.close()
            self.conditions.setText("File found. Converting...")
        except:
            self.conditions.setText("No (.osu) file found")
            return

        for i in range(len(lines)):
            if lines[i].startswith("AudioFilename: "):
                audio = lines[i].split(": ")[1].rstrip()
            if lines[i].startswith("Title:"):
                title = lines[i].split(":")[1].rstrip()
            if lines[i].startswith("TitleUnicode:"):
                titleUnicode = lines[i].split(":")[1].rstrip()
            if lines[i].startswith("Artist:"):
                artist = lines[i].split(":")[1].rstrip()
            if lines[i].startswith("ArtistUnicode:"):
                artistUnicode = lines[i].split(":")[1].rstrip()
            if lines[i].startswith("PreviewTime:"):
                previewTime = lines[i].split(": ")[1].rstrip()
            if self.copyTags.isChecked():
                if lines[i].startswith("Source:"):
                    source = lines[i].split(":")[1].rstrip()
                if lines[i].startswith("Tags:"):
                    tags = lines[i].split(":")[1].rstrip()
            if self.copyDifficulty.isChecked():
                if lines[i].startswith("HPDrainRate:"):
                    HP = lines[i].split(":")[1].rstrip()
                if lines[i].startswith("CircleSize:"):
                    CS = lines[i].split(":")[1].rstrip()
                if lines[i].startswith("OverallDifficulty:"):
                    OD = lines[i].split(":")[1].rstrip()
                if lines[i].startswith("ApproachRate:"):
                    AR = lines[i].split(":")[1].rstrip()
                if lines[i].startswith("Mode: "):
                    mode = lines[i].split(": ")[1].rstrip()
            
            if lines[i].startswith("[TimingPoints]"):
                timingPointsStart = i
                if self.copyNonBpmSV.isChecked():
                    for j in range(i, len(lines)):
                        if lines[j] == "\n":
                            timingPointsEnd = j
                            break
                    timingPoints = lines[timingPointsStart:timingPointsEnd]
                else:
                    timingPoints = lines[timingPointsStart:timingPointsStart+1]

            if self.copyOriginalBG.isChecked():
                if lines[i].startswith("0,0,\""):
                    bgline = lines[i]

        print(HP, OD, AR, CS, mode, source, tags, previewTime, timingPoints, bgline, audio, title, artist, creator)
        
        now = datetime.now()
        newdir = songDir+"/"+title+" - "+artist+" ("+creator+") " + now.strftime('%Y%m%d%H%M')
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        else:
            self.conditions.setText("Folder already exists")
            return

        shutil.copy(self.folderDir+"/"+audio, newdir+"/"+audio)
        if self.copyOriginalBG.isChecked():
            shutil.copy(self.folderDir+"/"+bgline.split("\"")[1], newdir+"/"+bgline.split("\"")[1])
        
        newosu = open(f'{newdir}/{artist} - {title} ({creator}) [converted to empty].osu', "w")
        newosu.write("osu file format v14\n\n")
        newosu.write("[General]\n")
        newosu.write("AudioFilename: " + audio + "\n")
        newosu.write("AudioLeadIn: 0\n")
        newosu.write("PreviewTime: " + previewTime + "\n")
        newosu.write("Countdown: 0\n")
        newosu.write("SampleSet: Soft\n")
        newosu.write("StackLeniency: 0\n")
        if self.copyDifficulty.isChecked():
            newosu.write("Mode: " + mode + "\n")
        else:
            newosu.write("Mode: " + "0" + "\n")
        newosu.write("LetterboxInBreaks: 0\n")
        newosu.write("SpecialStyle: 0\n")
        newosu.write("WidescreenStoryboard: 0\n\n")

        newosu.write("[Editor]\n")
        newosu.write("DistanceSpacing: 2.2\n")
        newosu.write("BeatDivisor: 4\n")
        newosu.write("GridSize: 4\n")
        newosu.write("TimelineZoom: 1\n\n")

        newosu.write("[Metadata]\n")
        newosu.write("Title:" + title + "\n")
        newosu.write("TitleUnicode:" + titleUnicode + "\n")
        newosu.write("Artist:" + artist + "\n")
        newosu.write("ArtistUnicode:" + artistUnicode + "\n")
        newosu.write("Creator:" + creator + "\n")
        newosu.write("Version:" + "converted to empty" + "\n")
        if self.copyTags.isChecked():
            newosu.write("Source:" + source + "\n")
            newosu.write("Tags:" + tags + "\n")
        else:
            newosu.write("Source:" + "\n")
            newosu.write("Tags:" + "\n")
        newosu.write("BeatmapID:0\n")
        newosu.write("BeatmapSetID:-1\n\n")

        newosu.write("[Difficulty]\n")
        if self.copyDifficulty.isChecked:
            newosu.write("HPDrainRate:" + HP + "\n")
            newosu.write("CircleSize:" + CS + "\n")
            newosu.write("OverallDifficulty:" + OD + "\n")
            newosu.write("ApproachRate:" + AR + "\n")
        else:
            newosu.write("HPDrainRate:5\n")
            newosu.write("CircleSize:5\n")
            newosu.write("OverallDifficulty:5\n")
            newosu.write("ApproachRate:5\n")
        newosu.write("SliderMultiplier:1.4\n")
        newosu.write("SliderTickRate:1\n\n")

        for i in range(len(timingPoints)):
            newosu.write(timingPoints[i])
        newosu.write("\n")
        
        newosu.write("[Events]\n")
        newosu.write("//Background and Video events\n")
        if self.copyOriginalBG.isChecked():
            newosu.write(bgline)
        newosu.write("//Break Periods\n")
        newosu.write("//Storyboard Layer 0 (Background)\n")
        newosu.write("//Storyboard Layer 1 (Fail)\n")
        newosu.write("//Storyboard Layer 2 (Pass)\n")
        newosu.write("//Storyboard Layer 3 (Foreground)\n")
        newosu.write("//Storyboard Layer 4 (Overlay)\n")
        newosu.write("//Storyboard Sound Samples\n\n")

        newosu.close()
        self.conditions.setText("Successfully converted to empty")
        
                
                
            

    def btn_hovered_brighter(self,btn):
        btn.setStyleSheet("background-color: #2e2e2e; color: #ffffff;border: 0px;")
    def btn_hovered_restore(self,btn):
        btn.setStyleSheet("background-color: #1e1e1e; color: #ffffff;border: 0px;")


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def getFolderPath(self):
        self.folderDir = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folderPathLabel.setText("Selected Folder: " + self.folderDir)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())