# InProcess Viewer

## Getting Started

### Installation

Start by downloading and extracting the latest release
```
mkdir ~/in-process-viewer
cd ~/in-process-viewer
wget https://github.com/lirwin3007/in-process-viewer/releases/latest/download/in-process-viewer.tar.gz
tar -xzvf in-process-viewer.tar.gz -C ~/in-process-viewer
rm in-process-viewer.tar.gz
```

Then test that everything work by running
```
cd dist
python3 server/server.py
```

If everything is working correctly, you should see an output similar to
```
IN_PROCESS_PORT not found. Using port 8000
Serving at port 8000
```

Hit `ctrl + c` to stop that, and now let's set up a service to start this server automatically.
This guide is designed for a raspberry pi - you may have to adapt these instructions to your OS.
```
sudo nano /lib/systemd/system/inProcessViewer.service
```
Populate that file with
```
[Unit]
Description=In Process Viewer
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi/in-process-viewer/dist
ExecStart=/usr/bin/python3 server/server.py > /home/pi/in-process-viewer/server.log 2>&1

[Install]
WantedBy=multi-user.target
```
And then `ctrl + x` then `y` to save.
```
sudo chmod 644 /lib/systemd/system/inProcessViewer.service
sudo systemctl daemon-reload
sudo systemctl enable inProcessViewer.service
sudo systemctl start inProcessViewer.service
```

We can check it is working by running
```
sudo systemctl status inProcessViewer.service
```
You should get an output similar to
```
● inProcessViewer.service - In Process Viewer
   Loaded: loaded (/lib/systemd/system/inProcessViewer.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2021-01-19 21:25:49 GMT; 2s ago
 Main PID: 1708 (python3)
    Tasks: 1 (limit: 2068)
   CGroup: /system.slice/inProcessViewer.service
           └─1708 /usr/bin/python3 server/server.py > /home/pi/in-process-viewer/server.log 2>&1

Jan 19 21:25:49 duet3 systemd[1]: Started In Process Viewer.
```

If you find that it complains about the port already being in use, this might be because we already ran the service on port 8000 before. This complaint should disappear after a while, but a reboot will always fix this issue.

Finally, try going to `<your-ip>:8000` to see it working! (Replacing `<your-ip>` with the IP address of whatever device we just set the service up on)

### Link

InProcess is most powerful when linked to your print controller software. Follow the guides below to link it to your favorite print controller software.

#### Duet

Navigate to Settings > General in the sidebar.

![image](https://user-images.githubusercontent.com/25307526/105096078-7c334700-5a9e-11eb-8a61-b5aa5a8a6d93.png)

Set 'Webcam URL' to `<your-ip>:8000` (Replacing `<your-ip>` with the IP address of whatever device is running this software) and check 'Embed webcam image in an iframe'

![image](https://user-images.githubusercontent.com/25307526/105096355-d7fdd000-5a9e-11eb-8acb-688924281749.png)

That's it! You should see the webcam option appear in the sidebar - click it and you're good to go!
