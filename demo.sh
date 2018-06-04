#!/bin/bash

curl -i http://localhost:5000/network/api/actors?\'Jack\'INnameOR\'James\'INname
curl -i http://localhost:5000/network/api/actors?\'Willis\'INnameANDage=61
