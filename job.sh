#!/bin/bash
videos=(uiuc rabbit fast nature)
dropnesses=(100 1000 10000 100000 100000)
udpflags=('--budp --pudp' '--budp --pudp --audp' '--budp --pudp --audp --iudp')

for video in ${videos[*]}; do
    for dropness in ${dropnesses[*]}; do
        for flag in "${udpflags[@]}"; do
            echo $video $dropness $flag
                
        done
    done
done
