#Module importieren
import sys,sqlite3,random,glob 
from PyQt4 import QtGui, uic

class VerbenDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.change = ""
        self.ui = uic.loadUi("Verbendialog.ui",self)
        self.setWindowIcon(QtGui.QIcon('franzflagge.png'))
        self.setWindowTitle("Verben")
        self.setModal(1)
        self.con = sqlite3.connect("franzverben.db")
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM verb")
        self.anzahl = 1
        self.varNamen = ["selbst_1","selbst_2","selbst_3","selbst_4","selbst_5","selbst_6","selbst_7"]
        for i in range(1,8):
            exec("self.ui.selbst_{}.hide()".format(i))
        for element in self.cur:
            if element[9] == "E":
                print("Element Aufruf:",element)
                try:
                    self.varNamen.remove(element[13])
                except ValueError:
                    pass
                exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(element[13]))
                exec("self.ui.{}.show()".format(element[13]))
                exec("self.ui.{}.setText('{}')".format(element[13],element[0]))
                if element[11] == "2":
                    exec("self.ui.{}.setChecked(True)".format(element[13]))
                    self.ui.selbstdefinierteVerben.setChecked(True)
                elif element[11] == "0":
                    exec("self.ui.{}.setChecked(False)".format(element[13]))
                self.anzahl += 1
        if self.anzahl != 1:
            self.ui.selbstdefinierteVerben.setEnabled(True)
            self.ui.loeschenEingabe.setEnabled(True)
            self.ui.loeschenInfo.setText("")
        self.cur.execute("SELECT * FROM verb WHERE NOT unite='E'")
        for d in self.cur:
            if d[11] == "0":
                exec("self.ui.{}.setChecked(False)".format(d[13]))
        self.cur.execute("SELECT * FROM verb WHERE NOT unite='E'")
        for dsatz in self.cur:
            exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(dsatz[13]))

        self.cur.execute("SELECT * FROM unit")
        for element in self.cur:
            if element[1] == 0:
                exec("self.ui.{}.setChecked(False)".format(element[0]))
            else:
                exec("self.ui.{}.setChecked(True)".format(element[0]))
            
        
        self.ui.StandardVerben.stateChanged.connect(self.headingChange)
        self.ui.Unite1Verben.stateChanged.connect(self.headingChange)
        self.ui.Unite2Verben.stateChanged.connect(self.headingChange)
        self.ui.Unite3Verben.stateChanged.connect(self.headingChange)
        self.ui.Unite4Verben.stateChanged.connect(self.headingChange)
        self.ui.Unite5Verben.stateChanged.connect(self.headingChange)
        self.ui.Unite6Verben.stateChanged.connect(self.headingChange)
        self.ui.selbstdefinierteVerben.stateChanged.connect(self.headingChange)
                
        self.ui.defi.clicked.connect(self.neues_Verb)
        self.ui.zurueckDef.clicked.connect(self.zurueck_clicked)
        self.ui.loeschenButton.clicked.connect(self.loeschen_clicked)
        self.ui.loeschenEingabe.textChanged.connect(self.loeschen_changed)
        
        self.ui.infinitifS.textChanged.connect(self.textChange)
        self.ui.jeS.textChanged.connect(self.textChange)
        self.ui.tuS.textChanged.connect(self.textChange)
        self.ui.ilS.textChanged.connect(self.textChange)
        self.ui.nousS.textChanged.connect(self.textChange)
        self.ui.vousS.textChanged.connect(self.textChange)
        self.ui.ilsS.textChanged.connect(self.textChange)
        self.ui.participeS.textChanged.connect(self.textChange)
        self.ui.hilfsverbS.textChanged.connect(self.textChange)

        self.finished.connect(self.schliessen)

    def neues_Verb(self):
        infinitif = self.ui.infinitifS.text().lower()
        je = self.ui.jeS.text().lower()
        tu = self.ui.tuS.text().lower()
        il = self.ui.ilS.text().lower()
        nous = self.ui.nousS.text().lower()
        vous = self.ui.vousS.text().lower()
        ils = self.ui.ilsS.text().lower()
        participe = self.ui.participeS.text().lower()
        hilfsverb = self.ui.hilfsverbS.text().lower()
        buch = "0"
        unite = "E"
        eingeschaltet = "2"
        sonstiges = "r"
        sonstiges1 = self.varNamen[0]
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM verb")
        sql = "INSERT INTO verb VALUES('"+infinitif+"','"+je+"','"+tu+"','"+il+"','"+nous+"','"+vous+"','"+ils+"','"\
              +participe+"','"+hilfsverb+"','"+unite+"','"+buch+"','"+eingeschaltet+"','"+sonstiges+"','"+sonstiges1+"')"
        cursor.execute(sql)
        self.con.commit()
        self.ui.loeschenEingabe.setEnabled(True)
        self.ui.loeschenInfo.setText("")
        self.zurueck_clicked()
        self.ui.infoDef.setText("Das Verb wurde eingelesen")
        exec("self.ui.{}.show()".format(sonstiges1))
        exec("self.ui.{}.setText('{}')".format(sonstiges1,infinitif))
        self.ui.selbstdefinierteVerben.setEnabled(True)

    def textChange(self):
        for element in [self.ui.infinitifS.text().lower(),self.ui.jeS.text().lower(),self.ui.tuS.text().lower(),self.ui.ilS.text().lower(),\
                        self.ui.nousS.text().lower(),self.ui.vousS.text().lower(),self.ui.ilsS.text().lower(),self.ui.participeS.text().lower(),\
                        self.ui.hilfsverbS.text().lower()]:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM verb")
            if element == "":
                self.ui.defi.setEnabled(False)
                for dsatz in cur:
                    if self.ui.infinitifS.text().lower() == dsatz[0]:
                        self.ui.infoDef.setText("Das Verb ist schon vorhanden")
                        break
                else:
                    self.ui.infoDef.setText("Geben Sie alle Formen an")
                    break
        else:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM verb")
            for dsatz in cur:
                if self.ui.infinitifS.text().lower() == dsatz[0]:
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

    def zurueck_clicked(self):
        self.ui.infinitifS.setText("")
        self.ui.jeS.setText("")
        self.ui.tuS.setText("")
        self.ui.ilS.setText("")
        self.ui.nousS.setText("")
        self.ui.vousS.setText("")
        self.ui.ilsS.setText("")
        self.ui.participeS.setText("")
        self.ui.hilfsverbS.setText("")
        
    def loeschen_clicked(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM verb WHERE infinitif='"+self.ui.loeschenEingabe.text()+"'")
        for element in cur:
            exec("self.ui.{}.hide()".format(element[13]))
        cur.execute("DELETE FROM verb WHERE infinitif='"+self.ui.loeschenEingabe.text()+"'")
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
        
        
        

    def loeschen_changed(self):
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
            
            
    def stateChange(self,zustand):
        cur = self.con.cursor()
        if zustand == 0:
            zustand1 = "False"
        else:
            zustand1 = "True"
        if self.change == "mehrere":
            sql = "UPDATE verb SET eingeschaltet='"+str(zustand)+"' WHERE sonst='"+self.cursorinhalt[0][13]+"'"
            entfernt = self.cursorinhalt[0]
            self.cursorinhalt.pop(0)
            for element in self.cursorinhalt:
                sql += " OR sonst='"+element[13]+"'"
                exec("self.ui.{}.stateChanged.disconnect(self.stateChange)".format(element[13]))
                exec("self.ui.{}.setChecked({})".format(element[13],zustand1))
            exec("self.ui.{}.stateChanged.disconnect(self.stateChange)".format(entfernt[13]))
            exec("self.ui.{}.setChecked({})".format(entfernt[13],zustand1))         
            cur.execute(sql)
            self.con.commit()
            for element in self.cursorinhalt:
                exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(element[13]))
            exec("self.ui.{}.stateChanged.connect(self.stateChange)".format(entfernt[13]))
            self.cursorinhalt = []
        else:
            sql = "UPDATE verb SET eingeschaltet='"+str(zustand)+"' WHERE sonst='"+self.sender().objectName()+"'"
            cur.execute(sql)
            self.con.commit()
        dialog.ui.VerbenInfo.setText("")
        self.change = ""

    def headingChange(self,zustand):
        self.change = "mehrere"
        headings = ["StandardVerben","Unite1Verben","Unite2Verben","Unite3Verben","Unite4Verben","Unite5Verben","Unite6Verben","selbstdefinierteVerben"]
        heading = ""
        for element in headings:
            if element == self.sender().objectName():
                heading = element
                break
        heading1 = heading[5:6]
        heading2 = heading[0:-6]+"Box"
        if heading1 not in ["1","2","3","4","5","6"] and heading1 != "t":
            heading1 = "S"
        elif heading1 not in ["1","2","3","4","5","6"]:
            heading1 = "E"
        self.cursorinhalt = []
        cur = self.con.cursor()
        if zustand != 0:
            cur.execute("SELECT * FROM verb WHERE unite='"+heading1+"'")
            for element in cur:
                self.cursorinhalt.append(element)
            exec("self.ui.{}.setChecked(True)".format(heading))
            cur.execute("UPDATE unit SET zustand='1' WHERE name='"+heading+"'")
            self.stateChange(2)

        elif zustand == 0:
            cur.execute("SELECT * FROM verb WHERE unite='"+heading1+"'")
            for element in cur:
                self.cursorinhalt.append(element)
            exec("self.ui.{}.setChecked(False)".format(heading))
            cur.execute("UPDATE unit SET zustand='0' WHERE name='"+heading+"'")
            self.stateChange(0)

    def schliessen(self):
        dialog.ui.verbenliste.clear()
        cur = self.con.cursor()
        sql = "SELECT * FROM verb WHERE eingeschaltet='2'"
        cur.execute(sql)
        #ComboBox 'verbenliste' füllen
        dialog.ComboBox = []
        for element in cur:
            dialog.ComboBox.append(element[0])
        dialog.ComboBox.sort()
        dialog.ui.verbenliste.addItems(dialog.ComboBox)

class MeinDialog(QtGui.QMainWindow): #Neue Klasse erstellen
    def __init__(self): #Klasse initialisieren
        QtGui.QMainWindow.__init__(self) #QDialog initialisieren
        self.ui = uic.loadUi("VerbenBar.ui",self) #Ui laden

        self.setWindowIcon(QtGui.QIcon('franzflagge.png'))
        self.setWindowTitle("VPVerbprogramm 1.0")
        self.ui.actionVerben.triggered.connect(self.openVD)
        self.richtigeallg = []
        self.falscheallg = []
        self.ges = 0
        self.formzahl = 1
        self.con = ""
        self.sql = ""
        self.cursor = None
        self.cursorinhalt = []
        self.richtigeVerben = 0
        self.falscheVerben = 0
        self.prozentsatzVerben = 0
        self.gesamtrichtige = "1"
        self.gesamtfalsche = "0"
        if not glob.glob("verbdaten.txt"):
            d = open("verbdaten.txt","w")
            d.write("1|0")
            d.close()
        with open("verbdaten.txt") as gesamt:
            for line in gesamt:
                line = line.strip()
                zuordnung = line.split("|")
                self.gesamtrichtige = zuordnung[0]
                self.gesamtfalsche = zuordnung[1]
        self.gesamtprozente = self.gesamt()        

        #Slots verbinden
        self.ui.buttonAEnde.clicked.connect(self.onEnde)
        self.ui.buttonAOK.clicked.connect(self.eingabe)
        self.ui.einzel.clicked.connect(self.einzel_clicked)
        self.ui.zufall.clicked.connect(self.zufallsabfrage_clicked)
        self.ui.senden.clicked.connect(self.senden_clicked)
        self.ui.formabfrage.clicked.connect(self.formabfrage_clicked)

        self.ui.gesamtrichtig.setText("Richtig: "+self.gesamtrichtige)
        self.ui.gesamtfalsch.setText("Falsch: "+self.gesamtfalsche)
        self.ui.gesamtprozent.setText(str(self.gesamtprozente)+"% richtig")
        
        self.ComboBox = []
        con = sqlite3.connect("franzverben.db")
        cursor = con.cursor()
        self.curfrage = con.cursor()
        sql = "SELECT * FROM verb WHERE eingeschaltet='2'"
        cursor.execute(sql)
        #ComboBox 'verbenliste' füllen
        for element in cursor:
            self.ComboBox.append(element[0])
        self.ComboBox.sort()
        self.ui.verbenliste.addItems(self.ComboBox)
        self.curfrage.execute("SELECT * FROM fragen")
        self.fragen = self.curfrage.fetchall()
        self.fragezahl = 0
        self.ausfragen = self.fragen[0][0]
        self.ui.frage.setText(self.ausfragen)
        self.ui.allgaus.setText(self.fragen[0][2])
        self.ui.allgloesung.setText("")
        con.close()
        self.paare = []
        self.antwort = self.fragen[0][1].strip()
        zuordnung = self.antwort.split(",")
        for element in zuordnung:
            zu = element.split("|")
            self.paare.append(zu[0])
            self.paare.append(zu[1])        

        self.eformen = ["Infinitif: ","Je: ","Tu: ","Il/Elle/On: ","Nous: ","Vous: ","Ils/Elles: ","Participe: ","Hilfsverb: "]
        self.formen = ["Je","Tu","Il/Elle/On","Nous","Vous","Ils/Elles","Participe passé","Hilfsverb für participe passé"]
        #Das List-Objekt 'formart' mit den Formen füllen
        self.ui.formart.addItems(self.formen)
        self.ui.formart.setCurrentItem(self.ui.formart.item(0))
        
        
    def onEnde(self): #Wird abgerufen, wenn auf den 'Ende'-Button geklickt wird.
        #Setzt das Abfagefeld wieder in seinen Ursprungszustand zurück
        self.ui.abfrage.setEnabled(False)
        self.ui.label.setText("")
        self.ui.infinitif.setText("")
        self.ui.abfrageart.setText("")
        self.ui.label1.setText("")
        self.ui.verben.setEnabled(True)
        self.ui.eingabe1.setText("")
        self.ges = 1
        self.cursorinhalt = []
        self.ges = 0
        self.formzahl = 1
        self.richtigeVerben = 0
        self.falscheVerben = 0
        self.prozentsatzVerben = 0
        self.ui.richtig.setText("Richtig: ")
        self.ui.falsch.setText("Falsch: ")
        self.ui.prozent.setText("      % richtig")
        
    def einzel_clicked(self): #Wird abgerufen, wenn auf den 'Einzelabfrage'-Button geklickt wird
        self.ausgewählt = self.ui.verbenliste.currentText()
        self.con = sqlite3.connect("franzverben.db")
        self.cursor = self.con.cursor()
        self.sql = "SELECT * FROM verb WHERE infinitif='"+self.ausgewählt+"'"
        self.cursor.execute(self.sql)
        einzel = ""
        for element in self.cursor:
            self.cursorinhalt.append(element)
            einzel = element[0]
        if einzel:
            self.ui.infinitif.setText(self.ausgewählt)
            self.ui.abfrage.setEnabled(True)
            self.ui.abfrageart.setText("Verben")
            self.ui.label.setText("Geben Sie die konjugierte Verbform ein")
            self.ui.label1.setText(self.eformen[1])
            self.ui.verben.setEnabled(False)
            self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
            self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
            self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
            self.ges = 1
            self.ui.VerbenInfo.setText("")
        elif not einzel:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")
        
    def zufallsabfrage_clicked(self): #Wird ausgeführt, wenn der 'Zufallsabfrage'-Button geklickt wird
        self.cursorinhalt = []
        random.seed()
        self.conz = sqlite3.connect("franzverben.db")
        self.cursorz = self.conz.cursor()
        self.sqlz = "SELECT * FROM verb WHERE eingeschaltet='2'"
        self.cursorz.execute(self.sqlz)
        for element in self.cursorz:
            for i in range(0,8):
                self.cursorinhalt.append((self.eformen[i],element[i],i))
        if self.cursorinhalt:
            self.ui.verben.setEnabled(False)
            self.ui.abfrage.setEnabled(True)
            self.zufall = random.randint(0,int(len(self.cursorinhalt)-1))
            self.infinitife = []
            for i in range(0,(int(len(self.cursorinhalt)/8)-1)):
                self.infinitife.append(i*8)
            if self.zufall in self.infinitife:
                self.zufall += 1
            self.ui.abfrageart.setText("Verben")
            self.ui.label.setText("Geben Sie die konjugierte Verbform ein")
            self.ui.label1.setText(self.cursorinhalt[self.zufall][0])
            self.ui.infinitif.setText(self.cursorinhalt[self.zufall-self.cursorinhalt[self.zufall][2]][1])
            self.ges = 2
            self.ui.VerbenInfo.setText("")
        elif not self.cursorinhalt:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")

    def eingabe(self): #Wird ausgeführt, wenn auf den 'OK'-Button geklickt wird.
        self.ui.eingabe1.setFocus()
        if self.ges == 1:
            self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
            self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
            self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
            #Liest den Inhalt des Cursors aus
            for verbform in self.cursor:
                self.cursorinhalt.append(verbform)
            #Vergleicht die Eingabe mit der Lösung
            if self.ui.eingabe1.text().strip() == self.cursorinhalt[0][self.formzahl]:
                self.ui.label.setText("*** RICHTIG ***")
                self.ui.richtigeVerben += 1
                self.gesamtrichtige = str(int(self.gesamtrichtige) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()
                #Text aktuallisieren
                self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
                if self.formzahl < 8:
                    self.ui.label1.setText(self.eformen[self.formzahl+1])
                    self.formzahl += 1
                    self.ui.eingabe1.setText("")
                else:
                    self.ui.label1.setText(self.eformen[1])
                    self.formzahl = 1
                    self.ui.eingabe1.setText("")
                    
            else:
                self.falscheVerben += 1
                self.gesamtfalsche = str(int(self.gesamtfalsche) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()
                #Text aktuallisieren
                self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
                self.ui.label.setText("Falsch.Richtig wäre gewesen:"+self.eformen[self.formzahl]+self.cursorinhalt[0][self.formzahl])                
                if self.formzahl < 8:
                    self.ui.label1.setText(self.eformen[self.formzahl+1])
                    self.formzahl += 1
                    self.ui.eingabe1.setText("")
                else:
                    self.ui.label1.setText(self.eformen[1])
                    self.formzahl = 1
                    self.ui.eingabe1.setText("")

        elif self.ges == 2:
            self.infinitife = []
            self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
            self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
            if self.ui.eingabe1.text().strip() == self.cursorinhalt[self.zufall][1]:
                self.richtigeVerben += 1
                self.gesamtrichtige = str(int(self.gesamtrichtige) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()                
                self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
                self.ui.label.setText("*** RICHTIG ***")
            else:
                self.falscheVerben += 1
                self.gesamtfalsche = str(int(self.gesamtfalsche) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()
                self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
                self.ui.label.setText("Falsch.Richtig wäre gewesen:"+self.cursorinhalt[self.zufall][0]+self.cursorinhalt[self.zufall][1])
                
            for element in self.cursorz:
                for i in range(0,8):
                    self.cursorinhalt.append((self.eformen[i],element[i],i))
            for i in range(0,(int(len(self.cursorinhalt)/8)-1)):
                self.infinitife.append(i*8)
            
            self.ui.eingabe1.setText("")
            self.zufall = random.randint(1,int(len(self.cursorinhalt)-1))
            if self.zufall in self.infinitife:
                self.zufall += 1
            self.ui.label1.setText(self.cursorinhalt[self.zufall][0])
            self.ui.infinitif.setText(self.cursorinhalt[self.zufall-self.cursorinhalt[self.zufall][2]][1])

        elif self.ges == 3:
            if self.ui.eingabe1.text().strip() == self.formabfrageform[self.formnummer]:
                self.ui.label.setText("*** RICHTIG ***")
                self.ui.richtigeVerben += 1
                self.gesamtrichtige = str(int(self.gesamtrichtige) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()
                #Text aktuallisieren
                self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
            else:
                self.falscheVerben += 1
                self.gesamtfalsche = str(int(self.gesamtfalsche) + 1)
                self.schreiben()
                self.prozentsatzVerben = self.prozentsatz()
                self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
                self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
                self.ui.label.setText("Falsch.Richtig wäre gewesen:"+self.formabfrageform[self.formnummer])
            try:
                self.formnummer += 1
                self.ui.infinitif.setText(self.formabfrageinf[self.formnummer])
            except IndexError:
                self.formnummer = 0
                self.ui.infinitif.setText(self.formabfrageinf[self.formnummer])
            self.ui.eingabe1.setText("")
            
    def senden_clicked(self):
        self.richtigeallg = []
        self.falscheallg = []
        allgeingabe = self.ui.allgemein.toPlainText()
        self.gefehlt = self.paare[:]
        line = allgeingabe
        zu = line.split("\n")
        for zeile in zu:
            zuordnung = zeile.split(",")
            for element in zuordnung:
                element.strip()
                while element.startswith(" "):
                    element = element[1:]
                while element.endswith(" "):
                    element = element[0:-1]
                if element in self.paare:
                    if element not in self.richtigeallg:
                        self.richtigeallg.append(element)
                        self.gefehlt.remove(element)
                        
                elif element == "":
                    continue
                else:
                    if element not in self.falscheallg:
                        self.falscheallg.append(element)
        self.falscheallgsch = ""
        self.richtigeallgsch = ""
        self.gefehltsch = ""
        for element in self.gefehlt:
            self.gefehltsch += element+", "
        for element in self.falscheallg:
            self.falscheallgsch += element+", "
        for element in self.richtigeallg:
            self.richtigeallgsch += element+", "
        if self.gefehltsch == "":
            self.gefehltsch = " - "
        if self.falscheallgsch == "":
            self.falscheallgsch = " - "
        if self.richtigeallgsch == "":
            self.richtigeallgsch = " - "
        self.ui.allgloesung.setText("{} von {} richtig. Richtig waren: {} Falsch waren: {} Gefehlt haben: {}".format(str(len(self.richtigeallg)),str(len(self.paare))
                                                                                                          ,self.richtigeallgsch,self.falscheallgsch,self.gefehltsch))
        if len(self.richtigeallg) == len(self.paare) and not self.falscheallg:
            self.gesamtrichtige = str(int(self.gesamtrichtige) + 1)
            self.schreiben()
        else:
            self.gesamtfalsche = str(int(self.gesamtfalsche) + 1)
            self.schreiben()
        self.ui.allgemein.setText("")
        

    def formabfrage_clicked(self):
        self.formabfrageinf = []
        self.formabfrageform = []
        self.formnummer = 0
        self.formarten = ["je","tu","il","nous","vous","ils","participe","hilfsverb"]
        self.formarten1 = ["je","tu","il","nous","vous","ils","participe","hilfsverb"]
        for element in self.formarten:
            if self.ui.formart.currentItem().text().lower()[0:2] != element[0:2]:
                self.formarten1.remove(element)
            else:
                try:
                    if self.ui.formart.currentItem().text().lower()[2] == "/":
                        raise IndexError

                except IndexError:
                    try:
                        if element[2]:
                            self.formarten1.remove(element)
                    except:
                        continue
                else:
                    if self.ui.formart.currentItem().text().lower()[-1:] == "s" and element[-1:] == "l":
                        self.formarten1.remove(element)
        
        self.conne = sqlite3.connect("franzverben.db")
        self.curs = self.conne.cursor()
        self.sqls = "SELECT infinitif,"+self.formarten1[0]+" FROM verb WHERE eingeschaltet='2'"
        self.curs.execute(self.sqls)
        self.ges = 3
        for element in self.curs:
            self.formabfrageinf.append(element[0])
            self.formabfrageform.append(element[1])
        try:
            self.ui.infinitif.setText(self.formabfrageinf[self.formnummer])
            self.ui.abfrageart.setText("Verben")
            self.ui.label1.setText(self.ui.formart.currentItem().text()+": ")
            self.ui.abfrage.setEnabled(True)
            self.ui.verben.setEnabled(False)
            self.ui.richtig.setText("Richtig: "+str(self.richtigeVerben))
            self.ui.falsch.setText("Falsch: "+str(self.falscheVerben))
            self.ui.prozent.setText(str(self.prozentsatzVerben)+"% richtig")
        except IndexError:
            self.ui.VerbenInfo.setText("Sie haben kein Verb eingeschaltet")
        else:self.ui.VerbenInfo.setText("")
            
    def prozentsatz(self):
        hallo = self.richtigeVerben / (self.richtigeVerben + self.falscheVerben) * 100
        hallo = round(hallo,2)
        return hallo
                    
    def gesamt(self):
        hallo = int(self.gesamtrichtige) / (int(self.gesamtrichtige) + int(self.gesamtfalsche)) * 100
        hallo = round(hallo,2)
        return hallo

    def schreiben(self):
        with open("verbdaten.txt","w") as d:
            self.gesamtprozente = self.gesamt()
            d.write(self.gesamtrichtige+"|"+self.gesamtfalsche)
        self.ui.gesamtrichtig.setText("Richtig :"+self.gesamtrichtige)
        self.ui.gesamtfalsch.setText("Falsch :"+self.gesamtfalsche)
        self.ui.gesamtprozent.setText(str(self.gesamtprozente)+"% richtig")
            
    def openVD(self):
        VD = VerbenDialog()
        VD.show()
                       
app = QtGui.QApplication(sys.argv) #Hauptfenster öffnen
dialog = MeinDialog()
dialog.show()
sys.exit(app.exec_())

