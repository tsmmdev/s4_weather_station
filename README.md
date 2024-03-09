### This is sketch notes not final README

# The Galaxy S4 Weather Station Project

I'm working on a project that's not exactly straightforward but has its own charm. It's about repurposing the Samsung Galaxy S4 into a local weather station. Remember the S4? Turns out, it's equipped with a set of sensors that are actually perfect for monitoring the weather—barometer, temperature, humidity sensors, you name it. It's an old phone, but here's where it gets interesting.

### Why the S4?

Not many apps out there make use of these sensors, and that's where the opportunity lies. The idea is to fully utilize these capabilities, which most new phones overlook.
### Getting Started

The process kicks off with the Weather Station Pro app. It's one of the few apps that taps into the S4's sensor suite for weather data logging. The catch? The paid version is necessary for comprehensive logging.

Next up is tackling Termux. Given the S4's outdated Android 5.0.1 OS, the latest Termux isn't compatible straight off the bat. The workaround? Start with an older version of Termux and then update. It's a bit of a workaround but nothing too daunting.
### The Technical Bits

With Termux sorted, the next steps involve setting up Python, SSH, and cron jobs for automation. It's pretty much straight-up tech setup from here.

The plan includes using a VPN for secure data transmission. The S4's older OS complicates automatic VPN connections, so manual setup is in the cards. It's an extra step but a manageable one.
### Bringing It All Together

The end goal is to gather the weather data, send it to a server, and then use Grafana for visualization. It's about making sense of the data in a visually appealing way.

As a side note, there's also the possibility of adding the AlfredCamera app to turn the phone into a makeshift security camera. It's a nice touch to squeeze more utility out of the device.
### In Conclusion

So, that's the gist of it. The project is about giving a second life to an old piece of technology, making it useful in a new way. It's not just about nostalgia; it's about practicality and making the most of what we already have. There's a bit more to iron out, but it's shaping up nicely.
<br>
<img src="/var/www/weatherstation/res/termux.png" width="200"/>
<img src="/var/www/weatherstation/res/ws1.jpg" width="200"/>
<img src="/var/www/weatherstation/res/ws2.png" width="200"/>
<img src="/var/www/weatherstation/res/ws3.png" width="200"/>
<br>
<img src="/var/www/weatherstation/res/gr1.jpg" width="200"/>
<img src="/var/www/weatherstation/res/gr2.jpg" width="200"/>
<img src="/var/www/weatherstation/res/gr3.jpg" width="200"/>
<img src="/var/www/weatherstation/res/gr4.jpg" width="200"/>
<br>

# TODO #
- Create Readme with full instructions ... 
- deploy.sh for client and server
- certificate instructions 
```text
Here's a basic example of how you can generate a self-signed certificate using OpenSSL:
openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -days 365 -nodes
This command generates a self-signed certificate (server_cert.pem) along with its private key (server_key.pem).
```

Sketch notes/steps
------------

1.  Install Anydesk on phone
    1.  set unattended access:  
        Settings→Security→Permission Profiles  
         
2.  install: Navigation Bar For Android  
    [https://play.google.com/store/apps/details?id=nu.nav.bar](https://play.google.com/store/apps/details?id=nu.nav.bar)
3.  Install Restart Button - to be able to restart phone from anydesk
4.  Install Total Commander  
     
5.  install Weather Station Pro and setup logging  
    ![](api/attachments/N2rJuenOi2zd/image/Screenshot from 2023-05-09 20-57-24.png)  
    setup widget  
     
6.  Install old Termux:
    1.  [https://archive.org/download/termux-repositories-legacy/termux-v0.79-offline-bootstraps.apk](https://archive.org/download/termux-repositories-legacy/termux-v0.79-offline-bootstraps.apk)  
        see attachment  
         
    2.  `vi /data/data/com.termux/files/usr/etc/apt/sources.list`  
        remove all repos and add only:  
        _**deb https://packages.termux.dev/termux-main-21 stable main**_  
        _**deb https://termux.dev/termux-root-packages-21-bin root stable**_
    3.  `vi /data/data/com.termux/files/usr/etc/apt/sources.list.d/science.list`  
        remove all repos
    4.  `vi /data/data/com.termux/files/usr/etc/apt/sources.list.d/game.list`  
        remove all repos
    5.  **update**  
        `apt update`  
        `apt upgrade`
    6.  **optional:**  
        `apt install mc`  
        `apt install nano`  
         
7.  SSH server
    1.  `pkg install openssh`
    2.  Set up a password:   
        `passwd`
    3.  Find your username by running this in Termux:   
        `whoami`
    4.  Start the server  
        `sshd`  
        ~Verify that it’s running with:~  
        `~logcat -s ‘ssh:*’~`  
        **!!! default port is 8022**
8.  Install Openvpn and setup profile  
     
9.  Setup ~/cronner.sh responsible for starting cron jobs

```text-plain
#!/bin/bash
num_procs=$(ps aux | grep -c [c]rond)
# Check if there is no process running
if [ $num_procs -eq 0 ]; then
  #Start the process
  crond
  echo "CROND started"
fi
```

7.  Setup ~/.bashrc

```text-plain
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w \$\[\033[00m\] '

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac


# some more ls aliases
alias ls='ls -las'
#alias la='ls -A'
#alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

export VISUAL=nano
export EDITOR=nano

#### AUTOSTARTS
sshd
~/cronner.sh
```

8.  `apt install busybox`  
     

7.  `apt install python`  
     
8.  `pip install --upgrade pip`  
     
9.  `pip install PyJWT`  
     
10.  `**mkdir storage**`  
    `**ln -s /sdcard/weather_station ~/storage/weather_station**`  
     
11.  `~mkdir ~/weather_station/client/log/~`
    1.  **TODO: set this in project to skip this step**
    
    3.    
         
12.  deploy project in ~/weather\_station
    1.  remove server folder from project  
         
13.  crontab -e

```text-plain
*/5 * * * * python /data/data/com.termux/files/home/weather_station/client/main.py >> /data/data/com.termux/files/home/weather_station/client/log/weather_station.log 2>&1 
```

15.  edit client ~/weather\_station/client/config.json  
    "device\_id": “whatever\_unique\_id”

You should see something like “Server listening on port 8022”