set datafile separator ','
set terminal pdf
set output "log_192.168.39.208.pdf"
set datafile separator ","
set grid
set timefmt '%Y/%m/%d %H:%M:%S'
Vsize = 210.0 
Hsize = 297.0 
set size Vsize, Hsize
set multiplot layout 3,1 rowsfirst title "Wave (x,y,z) " font "Times,9"
set bmargin 1.00
set tmargin 1.00
set lmargin 5.00
set xtics font "Times,9" 
set ytics font "Times,9" 
set title font "Times,9"
unset key
set xdata time
set format x '%H:%M:%S'
set ylabel "Accel. (mg) " font "Times,9"
plot "log_192.168.39.208.csv" u 1:2 w l
plot "log_192.168.39.208.csv" u 1:3 w l
plot "log_192.168.39.208.csv" u 1:4 w l
unset multiplot
exit
