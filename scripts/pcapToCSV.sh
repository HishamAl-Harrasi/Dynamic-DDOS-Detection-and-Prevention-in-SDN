#!/bin/sh

tshark -r $1 -T fields -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e frame.len -e frame.time -e frame.time_delta -e frame.time_delta_displayed -e frame.time_relative -E header=y -E separator=, -E quote=d -E occurrence=f > $2
