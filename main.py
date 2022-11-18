import os
from CloverHacker import CloverHacker

# for LA-352
ch = CloverHacker(IP="192.168.39.208")
ch.default_sampling_Hz = 200
ch.default_time_source = "GPS"
ch.default_file_interval = 10
ch.default_file_interval_flag = "Minute"
ch.default_ClkCalInterval = 0
ch.default_sensor_type = "M-A352"

if ch.is_connected():
    print("Logger is connected!")
    
    # SD内部のディレクトリ構造をとってくる
    print(ch.show_directory() )

    # 計測前チェックリストを実行する
    ret = ch.run_preflight_checklist()

    # データのモニタリング
    ch.monitor(dt=10.0, repeat=1)

else:
    print("Logger is NOT connected!")