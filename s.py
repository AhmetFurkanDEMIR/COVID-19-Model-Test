from PyQt5.QtWidgets import QWidget,QApplication,QLineEdit,QTextEdit,QLabel,QPushButton,QVBoxLayout,QFileDialog,QHBoxLayout,QComboBox
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from PyQt5 import QtWidgets,QtGui
from PyQt5 import QtWidgets
import numpy as np
import argparse
import imutils
import cv2
import sys
import os


class Pencere(QWidget):

    def __init__(self):
        super().__init__()

        self.main()


    def main(self):

        self.modela = QPushButton("Eğitilmiş Modeli Açın ")

        self.veri = QPushButton("COVID-19 Şüpheli veriyi Açın")

        self.calistir = QPushButton("Modeli çalıştır")

        self.etiket = QtWidgets.QLabel()

        self.etiket.setPixmap(QtGui.QPixmap("demir.png"))


        v_box = QtWidgets.QVBoxLayout()

        v_box.addStretch()

        v_box.addWidget(self.etiket)

        v_box.addStretch()

        v_box.addWidget(self.modela)

        v_box.addStretch()

        v_box.addWidget(self.veri)

        v_box.addStretch()

        v_box.addWidget(self.calistir)

        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()

        h_box.addStretch()

        h_box.addLayout(v_box)

        h_box.addStretch()

        self.setLayout(h_box)

        self.modela.clicked.connect(self.modele)

        self.veri.clicked.connect(self.image)

        self.calistir.clicked.connect(self.calistirr)

        self.setGeometry(400,150,600,600)
        self.setWindowTitle('demir.ai')
        self.show()



    def modele(self):

        print(os.getcwd())
        self.dosya_ismi = QFileDialog.getOpenFileName(self,"dosya aranıyor",os.getenv("Masaüstü"))
        
        try:

            self.model = load_model(self.dosya_ismi[0])
            self.modela.setText("Model Keras 'a dahil edildi")

        except:

            self.modela.setText("HATA!! Model Keras Tarafından Tanımlanamadı!! - Lütfen tekrar seçiniz.")



    def image(self):

        print(os.getcwd())
        self.dosya_ismi2 = QFileDialog.getOpenFileName(self,"dosya aranıyor",os.getenv("Masaüstü"))

        try:

            self.image = cv2.imread(self.dosya_ismi2[0])
            self.orig = self.image.copy()

            self.image = cv2.resize(self.image, (150, 150))
            self.image = self.image.astype("float") / 255.0
            self.image = img_to_array(self.image)
            self.image = np.expand_dims(self.image, axis=0)

            self.veri.setText("COVID-19 Şüpheli veri dahil edildi - Yeni veri için tıklayın")


        except:

            self.veri.setText("HATA!! COVID-19 Şüpheli veri dahil edilemedi")

        
    def calistirr(self):

        if self.veri.text() == "COVID-19 Şüpheli veri dahil edildi - Yeni veri için tıklayın" and self.modela.text() == "Model Keras 'a dahil edildi":

            kontrol = None

            if self.model.predict(self.image) >=0.5:

                self.label = "COVID-19"
                self.a = 100 * self.model.predict(self.image)[0][0]

                kontrol = True

            else:

                kontrol = False
                self.label = "HEALTY"
                self.a = (1-self.model.predict(self.image)[0][0]) * 100


            super().__init__()

            self.setWindowTitle('demir.ai - TEST')

            self.setGeometry(200,200,500,500)
            
            self.etiket1 = QtWidgets.QLabel()

            self.etiket1.setPixmap(QtGui.QPixmap(self.dosya_ismi2[0]))

            self.sonuc = QLabel("")

            v_box = QtWidgets.QVBoxLayout()
        
            v_box.addStretch()
        
            v_box.addWidget(self.sonuc)

            v_box.addStretch()

            v_box.addWidget(self.etiket1)

            v_box.addStretch()

            v_box.addStretch()
        
            h_box = QtWidgets.QHBoxLayout()
        
            h_box.addStretch()
        
            h_box.addLayout(v_box)
        
            h_box.addStretch()
        
            self.setLayout(h_box)

            self.sonuc.setText("{} : {}".format(self.label,self.a))

            if kontrol == True:

                self.sonuc.setStyleSheet("color: red;")

            else:

                self.sonuc.setStyleSheet("color: green;")

        
            self.show()





uygulama = QApplication(sys.argv)

QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
pencere = Pencere()

uygulama.exec_()