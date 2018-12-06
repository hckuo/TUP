#!/bin/bash -e
videos=(uiuc fast nature)
dropnesses=(5000 10000 15000 20000 40000 80000 160000 320000)
udpflags=('--budp' '--pudp' '--budp --pudp' '--budp --pudp')
giveups=(" " "--giveup")
generate_videos() {
    for video in ${videos[*]}; do
        for dropness in ${dropnesses[*]}; do
            for flag in "${udpflags[@]}"; do
                for giveup in ${giveups[*]}; do
                    flagtrimmed=$(echo $flag.$giveup | tr -d ' ')
                    echo Processing $video $dropness $flagtrimmed
                    printf "$video $dropness $flagtrimmed" >> log
                    sender_opts="$giveup $flag -d $dropness -v videos/$video.mp4" \
                        client_opts="$giveup -o outputs/$video.$dropness.$flagtrimmed.mp4" \
                        make bench-tup >> log
                done
            done
        done
    done
}

generate_videos;
