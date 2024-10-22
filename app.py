import sys

#from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from view import Ui_MainWindow
from Algorithm import BinomialDistribution
from nvidiaLlamaPrommpting import EvaluateConvenience


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnGenerateProbability.clicked.connect(self.handleGenerateProbability)

        self.ui.btnGenerateResponse.clicked.connect(self.handleResponse)



    def handleGenerateProbability(self):

        n = int(self.ui.txtAllUsers.text())
        p = float(self.ui.txtActivepPercentage.text()) / 100

        k = 0

        try:
            bandwidth = 0
            bandwidthPerUser = 0

            if self.ui.txtBandwidth.text() != "" and self.ui.txtBandwidthPerUser.text() != "":
                bandwidth = float(self.ui.txtBandwidth.text())
                bandwidthPerUser = float(self.ui.txtBandwidthPerUser.text())

            targetUsers = self.ui.txtTargetUsers.text().strip()

            if targetUsers != "":
                k = int(targetUsers)
            else:

                k = int((bandwidth * 1000) // bandwidthPerUser)
                self.ui.txtTargetUsers.setText(str(k))

        except ValueError:
            print("Error: Invalid input. Please enter numeric values for bandwidth and bandwidth per user.")
            self.ui.txtTargetUsers.setText("Invalid input")

        mode = self.ui.comboBox.currentText()


        if mode == "Equal ( = )":
                mode = "="
        elif mode == "More ( > )":
                mode = ">"
        elif mode == "More or equal ( >= )":
                mode = ">="
        elif mode == "Less ( < )":
                mode = "<"
        elif mode == "Less or equal ( <= )":
                mode = "<="


        probability = BinomialDistribution.probability(n, k, p, mode)

        rez = f"{float(probability) * 100:.10f}"

        self.ui.txtGenerateProbability.setText(rez)



    def handleResponse(self):

        print("Here")

        environment = self.ui.txtEnvironment.text()

        txtLanguage = self.ui.comboLanguage.currentText()

        language = True
        if txtLanguage != "English":
            language = False

        #probability = float(self.ui.txtGenerateProbability.text())

        prob_text = self.ui.txtGenerateProbability.text()
        print("Raw probability text:", prob_text)  # Print raw text

        try:
            probability = float(prob_text)
            print("Prob:", probability)  # Only prints if conversion is successful
        except ValueError:
            print("Invalid probability value")
            self.ui.txtResponse.setText("Invalid probability value.")
            return

        print("Prob:", probability)
        response = EvaluateConvenience.evaluate(probability, environment, language)
        print(response)


        if response < 3:
            responseText = f"{response} - Extremely Risky!"
        elif response < 5:
            responseText = f"{response} - Risky"
        elif response < 7:
            responseText = f"{response} - Moderate Risk"
        elif response < 9:
            responseText = f"{response} - Safe"
        else:
            responseText = f"{response} - Perfectly Safe"

        self.ui.txtResponse.setText(responseText)







if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()