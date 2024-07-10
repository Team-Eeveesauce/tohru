# Tohru
Tohru is a little Discord bot that doesn't do anything remotely useful.  
Mostly just designed to be used in the DTAG server, it can do certain things that are largely unrelated.

## Features
  * PING the bot to make sure it's online.
  * CONNECT to check if Kanna is awake.
  * GAMING will ask Kanna to open the Epic Games Launcher.
  * UPLOAD images to then be horribly compressed and stored in the archives.
  * TIPS AND QUOTES system for random advice and inspiration on command.

## Installation (Tohru)
You'll need to install Python 3 onto your machine to use either of these. The exact version probably doesn't matter, but I use 3.11.

Next, there's a few packages that you'll need to install from pip, which you can do by running this: `pip3 install py-cord mysql-connector-python python-dotenv pymagick colorthief pillow`

You'll also need a MariaDB or MySQL installation setup on one of your computers. It doesn't have to be on the same machine as Tohru, but it should be locally available.

After those are installed, you just need to copy `.env.template` to `.env` and open it in your favourite text editor. You'll know what to do.

Finally, run the bot by typing `python3 tohru.py`. If that doesn't work, try `python tohru.py`. And if *THAT* doesn't work, then you found a new bug! Report it please!!

## Installation (Kanna)
You'll still need Python 3 on your machine, and you should probably use the same version as you used for Tohru.

You can skip most of the pip packages, but you'll still need dotenv, so just run this: `pip3 install python-dotenv`

All you have to do now is copy `.env.template` to `.env` and open it in your text editor. You should instantly know what must be done.

At last, you can run the service by typing `python3 kanna.py` in your terminal. If Windows says Python isn't installed, try `python kanna.py` instead.

## Kanna
Kanna is Tohru's Windows-based friend who does stuff that Tohru can't do, since Tohru is designed to run on Linux and not Windows.
So, unless you run Tohru on a Linux system and also have a Windows system that you wanna use the same features as Kanna supports... it might not be entirely useful.

## FAQ
**Q.** Why is it named Tohru?  
**A.** Tohru is a dragon maid from the hit anime series Miss Kobayashi's Dragon Maid. This has many layers:
  * Miss Kobayashi's Dragon Maid was the first show to be added to the DTAG anime section.
  * The codename for the redesign of the DTAG website is "dragon".
  * Maids are supposed to do stuff for you.
  * Kanna is Tohru's little also-dragon friend.

**Q.** Nerd.  
**A.** Hey, you don't have to use it if you don't want to.

**Q.** What if I only want to run Tohru and not Kanna?  
**A.** Tohru will become emotionally unstable and may threaten to kill you.

**Q.** How do I run Tohru/Kanna automatically in the background?  
**A.** For Windows, the [Non-Sucking Service Manager](http://nssm.cc/) works. For Linux, [Supervisor](http://supervisord.org/) is pretty good.
