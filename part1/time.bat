powershell -command "Measure-Command {python get_stat.py --fig_location test/figure.png}|Select -Exp TotalSeconds" >> timing.txt
