import sys, sqlite3, random, glob
from PyQt4 import QtGui, uic


class VerbsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.change = ""
        self.ui = uic.loadUi("verbsdialog.ui", self)
        self.setWindowIcon(QtGui.QIcon('frenchflag.png'))
        self.setWindowTitle("Verben")
        self.setModal(1)
        self.con = sqlite3.connect("frenchverbs.db")
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM verb")
        self.count = 1
        self.var_names = ["selbst_1", "selbst_2", "selbst_3", "selbst_4", "selbst_5", "selbst_6", "selbst_7"]
        for i in range(1, 8):
            exec("self.ui.selbst_{}.hide()".format(i))
        for element in self.cur:
            if element[9] == "E":
                print("Element called:", element)
                try:
                    self.var_names.remove(element[13])
                except ValueError:
                    pass
                exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(element[13]))
                exec("self.ui.{}.show()".format(element[13]))
                exec("self.ui.{}.setText('{}')".format(element[13], element[0]))
                if element[11] == "2":
                    exec("self.ui.{}.setChecked(True)".format(element[13]))
                    self.ui.selbstdefinierteVerben.setChecked(True)
                elif element[11] == "0":
                    exec("self.ui.{}.setChecked(False)".format(element[13]))
                self.count += 1
        if self.count != 1:
            self.ui.selbstdefinierteVerben.setEnabled(True)
            self.ui.loeschenEingabe.setEnabled(True)
            self.ui.loeschenInfo.setText("")
        self.cur.execute("SELECT * FROM verb WHERE NOT unite='E'")
        for d in self.cur:
            if d[11] == "0":
                exec("self.ui.{}.setChecked(False)".format(d[13]))
        self.cur.execute("SELECT * FROM verb WHERE NOT unite='E'")
        for element in self.cur:
            exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(element[13]))

        self.cur.execute("SELECT * FROM unit")
        for element in self.cur:
            if element[1] == 0:
                exec("self.ui.{}.setChecked(False)".format(element[0]))
            else:
                exec("self.ui.{}.setChecked(True)".format(element[0]))

        self.ui.StandardVerben.stateChanged.connect(self.heading_change)
        self.ui.Unite1Verben.stateChanged.connect(self.heading_change)
        self.ui.Unite2Verben.stateChanged.connect(self.heading_change)
        self.ui.Unite3Verben.stateChanged.connect(self.heading_change)
        self.ui.Unite4Verben.stateChanged.connect(self.heading_change)
        self.ui.Unite5Verben.stateChanged.connect(self.heading_change)
        self.ui.Unite6Verben.stateChanged.connect(self.heading_change)
        self.ui.selbstdefinierteVerben.stateChanged.connect(self.heading_change)

        self.ui.defi.clicked.connect(self.new_verb)
        self.ui.zurueckDef.clicked.connect(self.back_clicked)
        self.ui.loeschenButton.clicked.connect(self.delete_clicked)
        self.ui.loeschenEingabe.textChanged.connect(self.delete_changed)

        self.ui.infinitifS.textChanged.connect(self.text_change)
        self.ui.jeS.textChanged.connect(self.text_change)
        self.ui.tuS.textChanged.connect(self.text_change)
        self.ui.ilS.textChanged.connect(self.text_change)
        self.ui.nousS.textChanged.connect(self.text_change)
        self.ui.vousS.textChanged.connect(self.text_change)
        self.ui.ilsS.textChanged.connect(self.text_change)
        self.ui.participeS.textChanged.connect(self.text_change)
        self.ui.hilfsverbS.textChanged.connect(self.text_change)

        self.finished.connect(self.close_clicked)

    def new_verb(self):
        infinitive = self.ui.infinitifS.text().lower()
        je = self.ui.jeS.text().lower()
        tu = self.ui.tuS.text().lower()
        il = self.ui.ilS.text().lower()
        nous = self.ui.nousS.text().lower()
        vous = self.ui.vousS.text().lower()
        ils = self.ui.ilsS.text().lower()
        participle = self.ui.participeS.text().lower()
        auxiliary_verb = self.ui.hilfsverbS.text().lower()
        book = "0"
        unit = "E"
        enabled = "2"
        others = "r"
        others1 = self.var_names[0]
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM verb")
        sql = "INSERT INTO verb VALUES('" + infinitive + "','" + je + "','" + tu + "','" + il + "','" + nous + "','" + vous + "','" + ils + "','" \
              + participle + "','" + auxiliary_verb + "','" + unit + "','" + book + "','" + enabled + "','" + others + "','" + others1 + "')"
        cursor.execute(sql)
        self.con.commit()
        self.ui.loeschenEingabe.setEnabled(True)
        self.ui.loeschenInfo.setText("")
        self.back_clicked()
        self.ui.infoDef.setText("Das Verb wurde eingelesen")
        exec("self.ui.{}.show()".format(others1))
        exec("self.ui.{}.setText('{}')".format(others1, infinitive))
        self.ui.selbstdefinierteVerben.setEnabled(True)

    def text_change(self):
        for element in [self.ui.infinitifS.text().lower(), self.ui.jeS.text().lower(), self.ui.tuS.text().lower(),
                        self.ui.ilS.text().lower(), \
                        self.ui.nousS.text().lower(), self.ui.vousS.text().lower(), self.ui.ilsS.text().lower(),
                        self.ui.participeS.text().lower(), \
                        self.ui.hilfsverbS.text().lower()]:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM verb")
            if element == "":
                self.ui.defi.setEnabled(False)
                for verb in cur:
                    if self.ui.infinitifS.text().lower() == verb[0]:
                        self.ui.infoDef.setText("Das Verb ist schon vorhanden")
                        break
                else:
                    self.ui.infoDef.setText("Geben Sie alle Formen an")
                    break
        else:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM verb")
            for verb in cur:
                if self.ui.infinitifS.text().lower() == verb[0]:
                    self.ui.infoDef.setText("Das Verb ist schon vorhanden")
                    self.ui.defi.setEnabled(False)
                    break
                else:
                    if self.ui.hilfsverbS.text().lower() == "avoir" or self.ui.hilfsverbS.text().lower() == "être":
                        self.ui.infoDef.setText("Sie können das Verb jetzt definieren")
                        self.ui.defi.setEnabled(True)
                    else:
                        self.ui.infoDef.setText("Das Hilfsverb muss avoir oder être sein")
                        self.ui.defi.setEnabled(False)

    def back_clicked(self):
        self.ui.infinitifS.setText("")
        self.ui.jeS.setText("")
        self.ui.tuS.setText("")
        self.ui.ilS.setText("")
        self.ui.nousS.setText("")
        self.ui.vousS.setText("")
        self.ui.ilsS.setText("")
        self.ui.participeS.setText("")
        self.ui.hilfsverbS.setText("")

    def delete_clicked(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM verb WHERE infinitif='" + self.ui.loeschenEingabe.text() + "'")
        for element in cur:
            exec("self.ui.{}.hide()".format(element[13]))
        cur.execute("DELETE FROM verb WHERE infinitif='" + self.ui.loeschenEingabe.text() + "'")
        self.con.commit()
        cur.execute("SELECT * FROM verb WHERE unite='E'")
        self.ui.loeschenButton.setEnabled(False)
        self.ui.loeschenEingabe.setText("")
        for element in cur:
            self.ui.loeschenEingabe.setFocus()
            break
        else:
            self.ui.loeschenEingabe.setEnabled(False)
            self.ui.selbstdefinierteVerben.setEnabled(False)
            self.ui.loeschenInfo.setText("Sie haben noch kein eigenes Verb definiert")

    def delete_changed(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM verb WHERE unite='E'")
        for element in cur:
            if element[0] == self.ui.loeschenEingabe.text().lower():
                self.ui.loeschenInfo.setText("Sie können das verb jetzt löschen")
                self.ui.loeschenButton.setEnabled(True)
                break
        else:
            self.ui.loeschenInfo.setText("Das Verb ist nicht vorhanden")
        if not self.ui.loeschenEingabe.text().lower():
            self.ui.loeschenInfo.setText("")

    def state_change(self, state):
        cur = self.con.cursor()
        if state == 0:
            state1 = "False"
        else:
            state1 = "True"
        if self.change == "mehrere":
            sql = "UPDATE verb SET eingeschaltet='" + str(state) + "' WHERE sonst='" + self.cursorcontent[0][13] + "'"
            entfernt = self.cursorcontent[0]
            self.cursorcontent.pop(0)
            for element in self.cursorcontent:
                sql += " OR sonst='" + element[13] + "'"
                exec("self.ui.{}.stateChanged.disconnect(self.stateChange)".format(element[13]))
                exec("self.ui.{}.setChecked({})".format(element[13], state1))
            exec("self.ui.{}.stateChanged.disconnect(self.stateChange)".format(entfernt[13]))
            exec("self.ui.{}.setChecked({})".format(entfernt[13], state1))
            cur.execute(sql)
            self.con.commit()
            for element in self.cursorcontent:
                exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(element[13]))
            exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(entfernt[13]))
            self.cursorcontent = []
        else:
            sql = "UPDATE verb SET eingeschaltet='" + str(
                state) + "' WHERE sonst='" + self.sender().objectName() + "'"
            cur.execute(sql)
            self.con.commit()
        dialog.ui.VerbenInfo.setText("")
        self.change = ""

    def heading_change(self, state):
        self.change = "mehrere"
        headings = ["StandardVerben", "Unite1Verben", "Unite2Verben", "Unite3Verben", "Unite4Verben", "Unite5Verben",
                    "Unite6Verben", "selbstdefinierteVerben"]
        heading = ""
        for element in headings:
            if element == self.sender().objectName():
                heading = element
                break
        heading1 = heading[5:6]
        heading2 = heading[0:-6] + "Box"
        if heading1 not in ["1", "2", "3", "4", "5", "6"] and heading1 != "t":
            heading1 = "S"
        elif heading1 not in ["1", "2", "3", "4", "5", "6"]:
            heading1 = "E"
        self.cursorcontent = []
        cur = self.con.cursor()
        if state != 0:
            cur.execute("SELECT * FROM verb WHERE unite='" + heading1 + "'")
            for element in cur:
                self.cursorcontent.append(element)
            exec("self.ui.{}.setChecked(True)".format(heading))
            cur.execute("UPDATE unit SET zustand='1' WHERE name='" + heading + "'")
            self.state_change(2)

        elif state == 0:
            cur.execute("SELECT * FROM verb WHERE unite='" + heading1 + "'")
            for element in cur:
                self.cursorcontent.append(element)
            exec("self.ui.{}.setChecked(False)".format(heading))
            cur.execute("UPDATE unit SET zustand='0' WHERE name='" + heading + "'")
            self.state_change(0)

    def close_clicked(self):
        dialog.ui.verbenliste.clear()
        cur = self.con.cursor()
        sql = "SELECT * FROM verb WHERE eingeschaltet='2'"
        cur.execute(sql)
        # ComboBox 'verbenliste' füllen
        dialog.ComboBox = []
        for element in cur:
            dialog.ComboBox.append(element[0])
        dialog.ComboBox.sort()
        dialog.ui.verbenliste.addItems(dialog.ComboBox)


class MainDialog(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("verbs_bar.ui", self)

        self.setWindowIcon(QtGui.QIcon('frenchflag.png'))
        self.setWindowTitle("VPVerbprogramm 1.0")
        self.ui.actionVerben.triggered.connect(self.open_verbs_dialog)
        self.right_general = []
        self.wrong_general = []
        self.total = 0
        self.form_number = 1
        self.con = ""
        self.sql = ""
        self.cursor = None
        self.cursor_content = []
        self.verbs_right = 0
        self.verbs_wrong = 0
        self.percent_verbs = 0
        self.right_total = "1"
        self.wrong_total = "0"
        if not glob.glob(".verbdata.txt"):
            d = open(".verbdata.txt", "w")
            d.write("1|0")
            d.close()
        with open(".verbdata.txt") as total:
            for line in total:
                line = line.strip()
                split = line.split("|")
                self.right_total = split[0]
                self.wrong_total = split[1]
        self.percent_total = self.total_in_percent()

        # Slots verbinden
        self.ui.buttonAEnde.clicked.connect(self.on_finished)
        self.ui.buttonAOK.clicked.connect(self.input)
        self.ui.einzel.clicked.connect(self.single_clicked)
        self.ui.zufall.clicked.connect(self.random_clicked)
        self.ui.senden.clicked.connect(self.send_clicked)
        self.ui.formabfrage.clicked.connect(self.query_form_clicked)

        self.ui.gesamtrichtig.setText("Richtig: " + self.right_total)
        self.ui.gesamtfalsch.setText("Falsch: " + self.wrong_total)
        self.ui.gesamtprozent.setText(str(self.percent_total) + "% richtig")

        self.ComboBox = []
        con = sqlite3.connect("frenchverbs.db")
        cursor = con.cursor()
        self.cur_question = con.cursor()
        sql = "SELECT * FROM verb WHERE eingeschaltet='2'"
        cursor.execute(sql)
        # Fill ComboBox 'verbenliste'
        for element in cursor:
            self.ComboBox.append(element[0])
        self.ComboBox.sort()
        self.ui.verbenliste.addItems(self.ComboBox)
        self.cur_question.execute("SELECT * FROM fragen")
        self.questions = self.cur_question.fetchall()
        self.question_count = 0
        self.cur_question = self.questions[0][0]
        self.ui.frage.setText(self.cur_question)
        self.ui.allgaus.setText(self.questions[0][2])
        self.ui.allgloesung.setText("")
        con.close()
        self.pairs = []
        self.answer = self.questions[0][1].strip()
        split = self.answer.split(",")
        for element in split:
            assignment = element.split("|")
            self.pairs.append(assignment[0])
            self.pairs.append(assignment[1])

        self.eforms = ["Infinitif: ", "Je: ", "Tu: ", "Il/Elle/On: ", "Nous: ", "Vous: ", "Ils/Elles: ", "Participe: ",
                        "Hilfsverb: "]
        self.forms = ["Je", "Tu", "Il/Elle/On", "Nous", "Vous", "Ils/Elles", "Participe passé",
                       "Hilfsverb für participe passé"]
        # Fill List Object 'formart' with forms
        self.ui.formart.addItems(self.forms)
        self.ui.formart.setCurrentItem(self.ui.formart.item(0))

    def on_finished(self):
        # Resets the query field
        self.ui.abfrage.setEnabled(False)
        self.ui.label.setText("")
        self.ui.infinitif.setText("")
        self.ui.abfrageart.setText("")
        self.ui.label1.setText("")
        self.ui.verben.setEnabled(True)
        self.ui.eingabe1.setText("")
        self.total = 1
        self.cursor_content = []
        self.total = 0
        self.form_number = 1
        self.verbs_right = 0
        self.verbs_wrong = 0
        self.percent_verbs = 0
        self.ui.richtig.setText("Richtig: ")
        self.ui.falsch.setText("Falsch: ")
        self.ui.prozent.setText("      % richtig")

    def single_clicked(self):  # Wird abgerufen, wenn auf den 'Einzelabfrage'-Button geklickt wird
        self.selected = self.ui.verbenliste.currentText()
        self.con = sqlite3.connect("frenchverbs.db")
        self.cursor = self.con.cursor()
        self.sql = "SELECT * FROM verb WHERE infinitif='" + self.selected + "'"
        self.cursor.execute(self.sql)
        single = ""
        for element in self.cursor:
            self.cursor_content.append(element)
            single = element[0]
        if single:
            self.ui.infinitif.setText(self.selected)
            self.ui.abfrage.setEnabled(True)
            self.ui.abfrageart.setText("Verben")
            self.ui.label.setText("Geben Sie die konjugierte Verbform ein")
            self.ui.label1.setText(self.eforms[1])
            self.ui.verben.setEnabled(False)
            self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
            self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
            self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
            self.total = 1
            self.ui.VerbenInfo.setText("")
        elif not single:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")

    def random_clicked(self):  # Wird ausgeführt, wenn der 'Zufallsabfrage'-Button geklickt wird
        self.cursor_content = []
        random.seed()
        self.conz = sqlite3.connect("frenchverbs.db")
        self.cursorz = self.conz.cursor()
        self.sqlz = "SELECT * FROM verb WHERE eingeschaltet='2'"
        self.cursorz.execute(self.sqlz)
        for element in self.cursorz:
            for i in range(0, 8):
                self.cursor_content.append((self.eforms[i], element[i], i))
        if self.cursor_content:
            self.ui.verben.setEnabled(False)
            self.ui.abfrage.setEnabled(True)
            self.random = random.randint(0, int(len(self.cursor_content) - 1))
            self.infinitive = []
            for i in range(0, (int(len(self.cursor_content) / 8) - 1)):
                self.infinitive.append(i * 8)
            if self.random in self.infinitive:
                self.random += 1
            self.ui.abfrageart.setText("Verben")
            self.ui.label.setText("Geben Sie die konjugierte Verbform ein")
            self.ui.label1.setText(self.cursor_content[self.random][0])
            self.ui.infinitif.setText(self.cursor_content[self.random - self.cursor_content[self.random][2]][1])
            self.total = 2
            self.ui.VerbenInfo.setText("")
        elif not self.cursor_content:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")

    def input(self):  # Wird ausgeführt, wenn auf den 'OK'-Button geklickt wird.
        self.ui.eingabe1.setFocus()
        if self.total == 1:
            self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
            self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
            self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
            # Liest den Inhalt des Cursors aus
            for verbform in self.cursor:
                self.cursor_content.append(verbform)
            # Vergleicht die Eingabe mit der Lösung
            if self.ui.eingabe1.text().strip() == self.cursor_content[0][self.form_number]:
                self.ui.label.setText("*** RICHTIG ***")
                self.ui.verbs_right += 1
                self.right_total = str(int(self.right_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                # Text aktuallisieren
                self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
                if self.form_number < 8:
                    self.ui.label1.setText(self.eforms[self.form_number + 1])
                    self.form_number += 1
                    self.ui.eingabe1.setText("")
                else:
                    self.ui.label1.setText(self.eforms[1])
                    self.form_number = 1
                    self.ui.eingabe1.setText("")

            else:
                self.verbs_wrong += 1
                self.wrong_total = str(int(self.wrong_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                # Text aktuallisieren
                self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
                self.ui.label.setText(
                    "Falsch.Richtig wäre gewesen:" + self.eforms[self.form_number] + self.cursor_content[0][self.form_number])
                if self.form_number < 8:
                    self.ui.label1.setText(self.eforms[self.form_number + 1])
                    self.form_number += 1
                    self.ui.eingabe1.setText("")
                else:
                    self.ui.label1.setText(self.eforms[1])
                    self.form_number = 1
                    self.ui.eingabe1.setText("")

        elif self.total == 2:
            self.infinitive = []
            self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
            self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
            if self.ui.eingabe1.text().strip() == self.cursor_content[self.random][1]:
                self.verbs_right += 1
                self.right_total = str(int(self.right_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
                self.ui.label.setText("*** RICHTIG ***")
            else:
                self.verbs_wrong += 1
                self.wrong_total = str(int(self.wrong_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
                self.ui.label.setText(
                    "Falsch.Richtig wäre gewesen:" + self.cursor_content[self.random][0] + self.cursor_content[self.random][
                        1])

            for element in self.cursorz:
                for i in range(0, 8):
                    self.cursor_content.append((self.eforms[i], element[i], i))
            for i in range(0, (int(len(self.cursor_content) / 8) - 1)):
                self.infinitive.append(i * 8)

            self.ui.eingabe1.setText("")
            self.random = random.randint(1, int(len(self.cursor_content) - 1))
            if self.random in self.infinitive:
                self.random += 1
            self.ui.label1.setText(self.cursor_content[self.random][0])
            self.ui.infinitif.setText(self.cursor_content[self.random - self.cursor_content[self.random][2]][1])

        elif self.total == 3:
            if self.ui.eingabe1.text().strip() == self.query_form_form[self.form_number]:
                self.ui.label.setText("*** RICHTIG ***")
                self.ui.verbs_right += 1
                self.right_total = str(int(self.right_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                # Text aktuallisieren
                self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
            else:
                self.verbs_wrong += 1
                self.wrong_total = str(int(self.wrong_total) + 1)
                self.schreiben()
                self.percent_verbs = self.percents()
                self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
                self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
                self.ui.label.setText("Falsch.Richtig wäre gewesen:" + self.query_form_form[self.form_number])
            try:
                self.form_number += 1
                self.ui.infinitif.setText(self.query_form_inf[self.form_number])
            except IndexError:
                self.form_number = 0
                self.ui.infinitif.setText(self.query_form_inf[self.form_number])
            self.ui.eingabe1.setText("")

    def send_clicked(self):
        self.right_general = []
        self.wrong_general = []
        general_input = self.ui.allgemein.toPlainText()
        self.missing = self.pairs[:]
        line = general_input
        split = line.split("\n")
        for line in split:
            assignment = line.split(",")
            for element in assignment:
                element.strip()
                while element.startswith(" "):
                    element = element[1:]
                while element.endswith(" "):
                    element = element[0:-1]
                if element in self.pairs:
                    if element not in self.right_general:
                        self.right_general.append(element)
                        self.missing.remove(element)

                elif element == "":
                    continue
                else:
                    if element not in self.wrong_general:
                        self.wrong_general.append(element)
        self.wrong_general_str = ""
        self.right_general_str = ""
        self.missing_general_str = ""
        for element in self.missing:
            self.missing_general_str += element + ", "
        for element in self.wrong_general:
            self.wrong_general_str += element + ", "
        for element in self.right_general:
            self.right_general_str += element + ", "
        if self.missing_general_str == "":
            self.missing_general_str = " - "
        if self.wrong_general_str == "":
            self.wrong_general_str = " - "
        if self.right_general_str == "":
            self.right_general_str = " - "
        self.ui.allgloesung.setText("{} von {} richtig. Richtig waren: {} Falsch waren: {} Gefehlt haben: {}".format(
            str(len(self.right_general)), str(len(self.pairs))
            , self.right_general_str, self.wrong_general_str, self.missing_general_str))
        if len(self.right_general) == len(self.pairs) and not self.wrong_general:
            self.right_total = str(int(self.right_total) + 1)
            self.schreiben()
        else:
            self.wrong_total = str(int(self.wrong_total) + 1)
            self.schreiben()
        self.ui.allgemein.setText("")

    def query_form_clicked(self):
        self.query_form_inf = []
        self.query_form_form = []
        self.form_number = 0
        self.form_types = ["je", "tu", "il", "nous", "vous", "ils", "participe", "hilfsverb"]
        self.form_types1 = ["je", "tu", "il", "nous", "vous", "ils", "participe", "hilfsverb"]
        for element in self.form_types:
            if self.ui.formart.currentItem().text().lower()[0:2] != element[0:2]:
                self.form_types1.remove(element)
            else:
                try:
                    if self.ui.formart.currentItem().text().lower()[2] == "/":
                        raise IndexError

                except IndexError:
                    try:
                        if element[2]:
                            self.form_types1.remove(element)
                    except:
                        continue
                else:
                    if self.ui.formart.currentItem().text().lower()[-1:] == "s" and element[-1:] == "l":
                        self.form_types1.remove(element)

        self.conne = sqlite3.connect("frenchverbs.db")
        self.curs = self.conne.cursor()
        self.sqls = "SELECT infinitif," + self.form_types1[0] + " FROM verb WHERE eingeschaltet='2'"
        self.curs.execute(self.sqls)
        self.total = 3
        for element in self.curs:
            self.query_form_inf.append(element[0])
            self.query_form_form.append(element[1])
        try:
            self.ui.infinitif.setText(self.query_form_inf[self.form_number])
            self.ui.abfrageart.setText("Verben")
            self.ui.label1.setText(self.ui.formart.currentItem().text() + ": ")
            self.ui.abfrage.setEnabled(True)
            self.ui.verben.setEnabled(False)
            self.ui.richtig.setText("Richtig: " + str(self.verbs_right))
            self.ui.falsch.setText("Falsch: " + str(self.verbs_wrong))
            self.ui.prozent.setText(str(self.percent_verbs) + "% richtig")
        except IndexError:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")
        else:
            self.ui.VerbenInfo.setText("")

    def percents(self):
        percent = self.verbs_right / (self.verbs_right + self.verbs_wrong) * 100
        percent = round(percent, 2)
        return percent

    def total_in_percent(self):
        percent = int(self.right_total) / (int(self.right_total) + int(self.wrong_total)) * 100
        percent = round(percent, 2)
        return percent

    def schreiben(self):
        with open(".verbdata.txt", "w") as d:
            self.percent_total = self.total_in_percent()
            d.write(self.right_total + "|" + self.wrong_total)
        self.ui.gesamtrichtig.setText("Richtig :" + self.right_total)
        self.ui.gesamtfalsch.setText("Falsch :" + self.wrong_total)
        self.ui.gesamtprozent.setText(str(self.percent_total) + "% richtig")

    def open_verbs_dialog(self):
        vd = VerbsDialog()
        vd.show()


app = QtGui.QApplication(sys.argv)
dialog = MainDialog()
dialog.show()
sys.exit(app.exec_())
