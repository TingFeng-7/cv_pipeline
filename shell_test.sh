#!/bin/bash
# echo "Hello World !"
# your_name="runoob.com"
# echo $your_name
# my_array=(A B "C" D)

for ((i=8; i<= 8; i+=1))
do
    echo "i: $i"
    # echo "python tools/demo.py image-full -f my/fpn4_nano_re_bs8.py #配置文件
    # --path /data/screen_analysis/0001_sa_v1/ 
    # --ckpt YOLOX_outputs/fpn4_nano_re_bs8/last_epoch_ckpt.pth #pt文件
    # --json_folder 20221103_yolox-nano-fpn4_conf_0.$i  --nms 0.45 
    # --conf 0.$i"
    # python tools/demo.py image-full -f my/fpn4_nano_re_bs8.py --path /data/screen_analysis/0001_sa_v1/  --ckpt YOLOX_outputs/fpn4_nano_re_bs8/last_epoch_ckpt.pth --json_folder 20221115_yolox-nano-fpn4_conf_0.$i  --nms 0.45 --conf 0.$i
done
