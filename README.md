# Vehicle Counting and Flow Analysis

A computer vision system for detecting, tracking, and counting vehicles crossing a predefined virtual line in fixed-camera traffic video.

The system uses a pretrained YOLO model for detection, ByteTrack for object tracking, and a line-crossing algorithm to count each tracked vehicle once.

---

## Overview

This project implements an automated vehicle counting and flow analysis pipeline for fixed-camera traffic footage.

The system:

- Detects vehicles using YOLO
- Tracks vehicles using ByteTrack
- Filters detections to supported vehicle classes
- Uses the provided virtual counting line
- Counts vehicles moving from top to bottom across the line
- Prevents duplicate counting of the same tracked vehicle
- Records crossing events with timestamps
- Generates an annotated output video
- Provides a Streamlit-based user interface

---

## Features

### Vehicle Detection

A pretrained YOLO model is used to detect objects in each video frame.

Supported vehicle classes:

- Car
- Truck
- Bus
- Motorcycle

Non-vehicle objects such as people and bicycles are ignored.

### Object Tracking

ByteTrack is used to maintain tracking IDs for detected vehicles across video frames.

Tracking IDs are used internally by the counting system to determine whether a vehicle has already been counted.

### Line Crossing Detection

The provided virtual line is used for counting.

For the evaluation video:

```text
Start: (220, 420)
End:   (1080, 420)
Direction: top_to_bottom