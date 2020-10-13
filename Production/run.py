import paramiko
import socket
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QProgressBar, QLabel, QMessageBox
from PyQt5 import uic
from dateutil.parser import parse
from pathlib import Path

class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('POSLogDownloaderWindow.ui', self)

        self.search_dir = r'C:\Centric\Backup'

        self.success = []
        self.failed = []
        self.file = ''

        self.input_file = self.findChild(QPushButton, 'InputFile')
        self.download = self.findChild(QPushButton, 'Download')
        self.failed_label = self.findChild(QLabel, 'Failed')
        self.msg = QMessageBox()
        self.msg.Title = '!'
        self.pbar = self.findChild(QProgressBar, 'ProgressBar')
        self.pbar.setHidden(True)
        self.failed_label.setHidden(True)

        self.input_file.clicked.connect(self.openFileNameDialog)
        self.download.clicked.connect(self.download_files)


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
        if fileName:
            self.file = fileName


    def fetch_from_file(self):

        if self.file == '':
            return []
        else:
            with open(self.file, 'r+') as f:
                self.lines = [line.split() for line in f]
                return [i for i in self.lines]


    def get_pwd(self, host):

        result_list = []
        numbers = '0123456789'

        for i in host:
            if i in numbers:
                result_list.append(i)
        return 'admin' + ''.join(result_list[:4])


    def download_files(self):


        self.files = self.fetch_from_file()
        out_file = os.getcwd() + '\output.txt'

        if len(self.files) > 0:

            self.pbar.setHidden(False)
            self.pbar.setMaximum(len(self.lines))

            count = 0

            try:
                os.makedirs(os.getcwd() + '\Copied', exist_ok=True)
                self.destination_path = os.getcwd() + '\Copied'
            except OSError:
                self.msg.setText('Creation of directory within current directory failed.')
                self.msg.exec_()
                sys.exit()


            for pair in self.files:

                hour = pair[3]
                date = pair[2]
                remote_host = pair[1]
                filename = pair[0]

                # Define Year, Month, Day and Hour
                year_timestamp = parse(date).year
                day_timestamp = parse(date).day
                hr_timestamp = parse(hour).hour
                month_timestamp = parse(date).month 

                if month_timestamp < 10:
                    month_timestamp = '0' + str(month_timestamp) # Month < 10 is parsed as two digits

                destination_file = os.path.join(self.destination_path, filename)
                filepath = os.path.join(self.search_dir, str(year_timestamp), str(month_timestamp), str(day_timestamp), str(hr_timestamp), str(filename))

                try:
                    ssh = paramiko.SSHClient()
                    ssh.load_system_host_keys()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # refrain from using this in PROD environment
                    ssh.connect(hostname=remote_host, username='root', password=self.get_pwd(remote_host), timeout=4)

                except paramiko.SSHException as e:
                    self.failed.append(f'{filepath} --- {e}')
                    self.failed_label.setText('Failed: %s' %len(self.failed))
                    self.failed_label.setHidden(False)
                    count += 1
                    self.pbar.setValue(count)
                    continue

                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    self.failed.append(f'{filepath} --- {e}')
                    self.failed_label.setText('Failed: %s' %len(self.failed))
                    self.failed_label.setHidden(False)
                    count += 1
                    self.pbar.setValue(count)
                    continue

                except socket.timeout as e:
                    self.failed.append(f'{filepath} --- {e}')
                    self.failed_label.setText('Failed: %s' %len(self.failed))
                    self.failed_label.setHidden(False)
                    count += 1
                    self.pbar.setValue(count)
                    continue

                except socket.error as e:
                    self.failed.append(f'{filepath} --- {e}')
                    self.failed_label.setText('Failed: %s' %len(self.failed))
                    self.failed_label.setHidden(False)
                    count += 1
                    self.pbar.setValue(count)
                    continue


                ftp_conn = ssh.open_sftp()

                try:
                    ftp_conn.get(filepath, destination_file)
                    self.success.append(filepath)
                except IOError as e:
                    self.failed.append(f'{filepath} --- {e}')


                ftp_conn.close()
                ssh.close()

                count += 1
                self.pbar.setValue(count)

            # Write output to file
            with open(out_file, 'w+') as f:
                        f.write('--- COPIED FILES ---' + '\n' + '\n')
                        if len(self.success) > 0:
                            f.write('\n'.join(self.success) + '\n' + '\n' + 'PLEASE CHECK DESTINATION FOLDER --- ' + self.destination_path + '\n' )
                        f.write('\n' + '--- FAILED FILES ---' + '\n' + '\n')
                        if len(self.failed) > 0:
                            f.write('\n'.join(self.failed))
                            self.failed_label.setText('Failed: %s' %len(self.failed))
                            self.failed_label.setHidden(False)

            self.msg.setText('Please check output.txt file.')
            self.msg.exec_()

            os.startfile(out_file)

        else:
            self.msg.setText('Please select input file.')
            self.msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
