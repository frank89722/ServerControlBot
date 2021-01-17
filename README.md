# ServerControlBot

Require discord.py and Screen
```
pip install discord

#Arch 
sudo pacman -S screen

#Debian/Ubuntu
sudo apt-get install screen
```

***
* You hava to create a settings.json in bot directory like this
```
{
    "MC_DIR":"/home/user/MCServers",
    "TOKEN":"NzM4NzkwMDQzMTgyODI1NjIz.XyRB2A.ObUxHf-fZdjdGCsxcDWtqU1AULA",
    "CHANNEL":738672611846714950
}
```
Put your server folders under `"MC_DIR"`


* Put a json file named as same as each server folder that in your `"MC_DIR"`directory

```
{
    "JAVA_PARAMETERS":"-Xms2048M -Xmx3072M",
    "SERVER_JAR":"server.jar"
}
``` 

`!commands` in your discord chat to see the commands
