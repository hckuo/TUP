#!/bin/bash -e
videos=(uiuc fast nature)
dropnesses=(5000 10000 15000 20000 40000 80000 160000 320000)
udpflags=('--budp' '--pudp' '--budp --pudp')
giveups=("--nogiveup" "--giveup")
generate_videos() {
    for video in ${videos[*]}; do
        for dropness in ${dropnesses[*]}; do
            for flag in "${udpflags[@]}"; do
                for giveup in ${giveups[*]}; do
                    flagtrimmed=$(echo $flag.$giveup | tr -d ' ')
                    echo Processing $video $dropness $flagtrimmed
                    printf "$video $dropness $flagtrimmed" >> log
                    file="outputs/$video.$dropness.$flagtrimmed.mp4"
                    sender_opts="$giveup $flag -d $dropness -v videos/$video.mp4" \
                        client_opts="$giveup -o $file" \
                        make bench-tup >> log;
                    echo -n $video $dropness $flagtrimmed, >> result.csv
                    ffmpeg -i $file -i videos/$video.mp4 -filter_complex psnr -f null - |& grep average >> result.csv &
                done
            done
        done
    done
    wait
}

run_psnr() {
    for video in ${videos[*]}; do
        for dropness in ${dropnesses[*]}; do
            for flag in "${udpflags[@]}"; do
                for giveup in ${giveups[*]}; do
                    flagtrimmed=$(echo $flag.$giveup | tr -d ' ')
                    echo -n $video $dropness $flagtrimmed, >> test.csv
                    input_file="../outputs2/$video.$dropness.$flagtrimmed.mp4"
                done
            done
        done
    done
    sed -i -e 's/:/,/g' test.csv
    sed -i -e 's/0 -/0,-/g' test.csv
    sed -i -e 's/\[[^]]*\]//g' test.csv
}
generate_videos
