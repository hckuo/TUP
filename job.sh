#!/bin/bash -e
videos=(uiuc rabbit fast nature)
dropnesses=(10 100 1000 10000 100000 100000)
udpflags=('--budp --pudp' '--budp --pudp --audp' '--budp --pudp --audp --iudp')

generate_videos() {
    for video in ${videos[*]}; do
        for dropness in ${dropnesses[*]}; do
            for flag in "${udpflags[@]}"; do
                flagtrimmed=$(echo $flag | tr -d ' ')
                echo Processing $video $dropness $flagtrimmed
                printf "$video $dropness $flagtrimmed" >> log
                sender_opts="$flag -d $dropness -v videos/$video.mp4" \
                    client_opts="-o outputs/$video.$dropness.$flagtrimmed.mp4" \
                    make bench-tup >> log
            done
        done
    done
}

run_psnr() {
    #TODO
}
generate_videos;
