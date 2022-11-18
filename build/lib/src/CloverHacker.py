import subprocess
from subprocess import PIPE
import datetime
import numpy as np


class CloverHacker:
    def __init__(self,IP):
        self.ip_addr = IP
        self.port = 50000

        self.default_sampling_Hz = 200
        self.default_time_source = "GPS"
        self.default_file_interval = 10
        self.default_file_interval_flag = "Minute"
        self.default_ClkCalInterval = 0
        self.default_sensor_type = "M-A352"
        self.serial_number = -1

    def monitor(self,dt,repeat):

        csv_name = "log_"+self.ip_addr+".csv"

        gp_name = "log_"+self.ip_addr+".gp"
        gp= open(gp_name,"w")
        gp.write("set datafile separator ','\n")
        gp.write('set terminal pdf\n')
        gp.write('set output "log_'+self.ip_addr+'.pdf"\n')
        gp.write('set datafile separator ","\n')
        gp.write('set grid\n')
        gp.write("set timefmt '%Y/%m/%"+"d %H:%M:%S'\n")
        gp.write('Vsize = 210.0 \n') # A4
        gp.write('Hsize = 297.0 \n') # A4
        gp.write('set size Vsize, Hsize\n')

        gp.write('set multiplot layout 3,1 rowsfirst title "Wave (x,y,z) " font "Times,9"\n')
        gp.write('set bmargin 1.00\n')
        gp.write('set tmargin 1.00\n')
        gp.write('set lmargin 5.00\n')
        gp.write('set xtics font "Times,9" \n')
        gp.write('set ytics font "Times,9" \n')
        gp.write('set title font "Times,9"\n')
        gp.write('unset key\n')

        gp.write("set xdata time\n")
        gp.write("set format x '%H:%M:%S'\n")

        gp.write('set ylabel "Accel. (mg) " font "Times,9"\n')
        gp.write('plot "'+csv_name+'" u 1:2 w l\n')
        gp.write('plot "'+csv_name+'" u 1:3 w l\n')
        gp.write('plot "'+csv_name+'" u 1:4 w l\n')
        gp.write("unset multiplot\n")
        gp.write("exit\n")
        gp.close()

        f = open(csv_name,"w")
        for i in range(repeat):
            result = self.monitor_time(dt)
            f.write(result)
            f.flush()
            proc = subprocess.Popen("gnuplot "+gp_name,shell=True, text=True)
        f.close()

    def monitor_time(self,duration):
        telnet_command = "(echo 'N'; sleep 0.01; echo 'MON'; sleep "+str(duration)+"; echo '!'; sleep 0.001; exit;)|telnet " + self.ip_addr + " "+str(self.port)
        
        #target_from=">Monitoring Mode."
        #target_to="--- Finish Monitoring. ---"
        #idx_from = telnet_command.find(target_from)
        #idx_to = telnet_command.find(target_to)
        #telnet_command = telnet_command[:idx_to]

        try :
            proc = subprocess.run(telnet_command,shell=True, stdout=PIPE, stderr=PIPE, text=True)
            proc.stdout =proc.stdout.replace("C\n\n","C")
            proc.stdout =proc.stdout.replace("\n-","")
            proc.stdout =proc.stdout.replace("\nC","")
            proc.stdout =proc.stdout.replace("\nE","")
            proc.stdout =proc.stdout.replace("\nS","")
            proc.stdout =proc.stdout.replace("\n>","")
            proc.stdout =proc.stdout.replace("\nG","")
            proc.stdout =proc.stdout+"\n"
            proc.stdout =proc.stdout+"\n"
            proc.stdout =proc.stdout+"\n"
            return proc.stdout
        except:
            return "[ERROR] No data"

    def is_connected(self):
        telnet_command = "(echo 'Y'; sleep 0.5;exit)|telnet " + self.ip_addr + " "+str(self.port)
        
        try :
            proc = subprocess.run(telnet_command,shell=True, stdout=PIPE, stderr=PIPE, text=True)
            succ_connected = ("Connected to" in proc.stdout) and ("Show Help ? (Y/N)" in proc.stdout)
            return succ_connected
        except:
            return False

    def show_directory(self):
        telnet_command = "(echo 'N'; sleep 0.5; echo 'DIR'; sleep 1; exit)|telnet " + self.ip_addr + " "+str(self.port)
        
        try :
            proc = subprocess.run(telnet_command,shell=True, stdout=PIPE, stderr=PIPE, text=True)
            return proc.stdout
        except:
            return "[ERROR] No data"

    def show_setting(self):
        telnet_command = "(echo 'N'; sleep 0.5; echo 'i'; sleep 0.3;echo 'STAT'; sleep 0.3;echo 'SET'; sleep 0.3;echo 'SHWSET'; sleep 0.5;echo 'GPSCHK';sleep 1.0; exit)|telnet " + self.ip_addr + " "+str(self.port)
        
        try :
            proc = subprocess.run(telnet_command,shell=True, stdout=PIPE, stderr=PIPE, text=True)
            return proc.stdout
        except:
            return "[ERROR] No data"

    def run_preflight_checklist(self):
        set_info = self.show_setting()
        score = np.ones(11)
        fname = "PreFlight_"+self.ip_addr+"_"+ str(datetime.datetime.now().isoformat() ) +".log"
        f = open(fname ,"w")
        f.write(set_info)
        f.close()


        with open(fname,"r") as f:
            for line in f:
                if ("Sampling" in line) and ("Rate" in line) and ("[" in line) :
                    
                    line = line.split("[")
                    line = line[1].split("]")
                    if int(line[0]) == self.default_sampling_Hz:
                        print("[OK] Sampling Rate (Hz): "+str(self.default_sampling_Hz) )
                        score[0] = 0
                    else:
                        print("[ERROR] Sampling Rate (Hz): "+line[0]+" , Expected : "+str(self.default_sampling_Hz) )

                if ("Time" in line) and ("Source" in line) and ("[" in line) :
                    line = line.split("[")
                    line = line[1].split("]")
                    if line[0] == self.default_time_source:
                        print("[OK] Time source: "+str(self.default_time_source) )
                        score[1] = 0
                    else:
                        print("[ERROR] Time source : "+line[0]+" , Expected : "+str(self.default_time_source) )

                if ("GPS" in line) and ("Power" in line) and not("[" in line) and not("OfsErrCnt" in line):
                    
                    if ("On" in line) :
                        print("[OK] GPS Power: On")
                        score[2] = 0
                    else:
                        print("[ERROR] GPS Power: Off")

                if ("GPS" in line) and ("Status" in line) :
                    
                    if ("Ready" in line) :
                        print("[OK] GPS Power: Ready")
                        score[3] = 0
                    else:
                        print("[ERROR] GPS Power: not Ready")

                if ("Time " in line) and ("Set              " in line) :
                    
                    if ("OK" in line) :
                        print("[OK] Time Set: OK")
                        score[4] = 0
                    else:
                        print("[ERROR] Time Set: Not Yet")

                if ("File " in line) and ("Interval " in line) and ("Flag " in line) :
                    line = line.split("[")
                    line = line[1].split("]")

                    if (self.default_file_interval_flag in line[0]) :
                        print("[OK] File Interval Flag : "+self.default_file_interval_flag)
                        score[5] = 0
                    else:
                        print("[ERROR] File Interval Flag: "+line[0]+", expected"+self.default_file_interval_flag)

                if ("File " in line) and ("Interval     " in line) and ("[" in line) :
                    line = line.split("[")
                    line = line[1].split("]")

                    if self.default_file_interval == int(line[0]) :
                        print("[OK] File Interval is : " +str(self.default_file_interval) )
                        score[6] = 0
                    else:
                        print("[ERROR] File Interval : " +line[0]+" , expected :"+ str(self.default_file_interval) )

                if ("ClkCal" in line) and ("Interval " in line) and ("[" in line) :
                    line = line.split("[")
                    line = line[1].split("]")

                    if self.default_ClkCalInterval == int(line[0]) :
                        print("[OK] Clock calibration interval : " +str(self.default_ClkCalInterval) )
                        score[7] = 0
                    else:
                        print("[ERROR] Clock calibration interval : " +line[0]+" , expected : "+ str(self.default_ClkCalInterval) )

                if ("Sensor " in line) and ("Type " in line) and ("[" in line) :
                    line = line.split("[")
                    line = line[1].split("]")

                    if (self.default_sensor_type in line[0] ):
                        print("[OK] Sensor type : " +str(self.default_sensor_type) )
                        score[8] = 0
                    else:
                        print("[ERROR] Sensor type : " +line[0]+" , expected : "+ str(self.default_sensor_type) )

                if ("Server " in line) and ("Time " in line) :
                    line = line.split(" : ")
                    mytime =str(datetime.datetime.now(datetime.timezone.utc).isoformat() )
                    line[1] = line[1].replace("/","-")
                    line[1] = line[1].replace(" ","T")
                    line[1] = line[1].replace("\n","")
                    print("Current Time: "+ mytime)
                    print("Server Time : "+ line[1] )

                if ("Own " in line) and ("Time " in line) :
                    line = line.split(" : ")
                    line[1] = line[1].replace("/","-")
                    line[1] = line[1].replace(" ","T")
                    line[1] = line[1].replace("\n","")
                    print("Own Time    : "+ line[1] )

                if ("Serial " in line) and ("No " in line) :
                    line = line.split(" : ")
                    line[1] = line[1].replace(".","")
                    line[1] = line[1].replace("\n","")
                    line[1] = line[1].replace("[","")
                    line[1] = line[1].replace("]","")
                    self.serial_number = int(str(line[1]))
                    print("[OK] Serial number    : "+ line[1] )

                if ("SD          " in line) and (" : " in line) :
                    line = line.split(" : ")
                    #line[1] = line[1].replace(",","")
                    line[1] = line[1].replace(".","")
                    line[1] = line[1].replace("\n","")
                    if ("No" in line[1]):
                        print("[WARNING] SD card is not installed! ")
                    else:
                        print("[OK] SD card is installed. Size is "+line[1])
                        score[9] = 0

                if ("Offset : " in line) and ("ClkCalVal " in line) :
                    line = line.split(" : ")
                    line = line[1].split(",")
                    if abs(int( line[0] )) < 5:
                        print("[OK] Offset is small : "+ line[0] )
                        score[10] = 0
                    elif abs(int( line[0] )) < 10:
                        print("[Caution] Offset is significant : "+ line[0] )
                    else:
                        print("[WARNING] Offset is too Large : "+ line[0] )
        
        if np.max(score) == 0:
            print("[OK] TEST PASSED. READY FOR FLIGHT. ")
            return True
        else:
            print("[NOT PASSED] ERROR EXISTS. NOT READY FOR FLIGHT. ")
            return False

    def is_ready(self):
        telnet_command = "telnet " + self.ip_addr + " "+str(self.port)
        
        try :
            print(telnet_command)

            return True
        except:
            return False
