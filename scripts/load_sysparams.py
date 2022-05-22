#!/usr/bin/env python3

"""
Written by Haowen Shi <shi@mach9.io>, Mar 2022

Parameter loading

Copyright (C) Mach9 Robotics, Inc - All Rights Reserved
Open release
"""

import sys
import rospy
import yaml
from rosparam import upload_params
from m9_sysparam.sysparam import SystemParameters, SensorType

def load_gnss_params(gnss):
    rospy.loginfo("Overriding GNSS->LIDAR extrinsics")
    extrinsic_T = gnss.extrinsic_T
    # assuming transform lidar->imu << imu->gnss
    rospy.set_param(
        "mapping/extrinsic_T",
        [
            float(extrinsic_T[0][0]),
            float(extrinsic_T[1][0]),
            float(extrinsic_T[2][0])
        ]
    )

def load_fastlio_params(fastlio_filepath):
    with open(fastlio_filepath) as f:
        yamlfile = yaml.safe_load(f)
        upload_params("", yamlfile)
        rospy.loginfo("Loaded FAST-LIO config params from " + fastlio_filepath)

def main(args):
    cfgpath = args[1]
    syspath = args[2]
    params = SystemParameters(syspath)

    gnss = None
    # assuming only one GNSS onboard
    for sensor in params.sensors:
        if sensor.type == SensorType.GNSS:
            gnss = sensor
            break

    load_fastlio_params(cfgpath)

    # override gnss->lidar extrinsics
    if gnss:
        load_gnss_params(gnss)

if __name__ == "__main__":
    rospy.init_node("load_sysparams_node")
    if (len(sys.argv) < 3):
        print("usage: load_sysparam.py <cfg_filepath> <sysparam_filepath>")
        exit(1)
    main(sys.argv)
