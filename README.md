# Tohru
![Tohru](tohru.png)

Tohru is a little Discord bot that doesn't do anything remotely useful.  
Mostly just designed to be used in the DTAG server, it can do certain things that are largely unrelated.

## Features
  * PING the bot to make sure it's online.
  * CONNECT to check if Kanna is awake.
  * UPLOAD images to then be horribly compressed and stored in the archives.
  * TIPS AND QUOTES system for random advice and inspiration on command.
  * CRYPTO integration (the [secret message tool](https://github.com/Team-Eeveesauce/crypto), not the currency.)

## Manual Installation
You'll need to install Python 3 onto your machine to use either of these. The exact version probably doesn't matter, but I'm using 3.12.

Next, there's a few packages that you'll need to install from pip, which you can do by running this: `pip3 install -r requirements.txt`

You'll also need a MariaDB or MySQL installation setup on one of your computers. It doesn't have to be on the same machine as Tohru, but it should be locally available.

After those are installed, you just need to copy `.env.template` to `.env` and open it in your favourite text editor. You'll know what to do.

Finally, run the bot by typing `python3 tohru.py`. If that doesn't work, try `python tohru.py`. And if *THAT* doesn't work, then you found a new bug! Report it please!!

## Docker Installation
If you're into that sort of thing, you can just run the docker container. It's really convenient!
1. Clone the repository however you want to.
2. Create your .env file using the provided template.
3. Run `docker-compose up --build` in your favourite console, and voila!

Like Todd Howard once said, "It just works".

## Kanna
Kanna is Tohru's Windows-based friend who does stuff that Tohru can't do, since Tohru is designed to run on Linux and not Windows.
So, unless you run Tohru on a Linux system and also have a Windows system that you wanna use the same features as Kanna supports... it might not be entirely useful.

Communication with the pair is quite limited, but it's not meant to be a deep integration, just like calling someone to do your work for you.
I can't stop you, but please refrain from using Kanna over the internet. She may be a dragon, but she's not very secure.

## Installation (Kanna)
You'll still need Python 3 on your machine, and you should probably use the same version as you used for Tohru.

You can skip most of the pip packages, but you'll still need dotenv and the toast notification handler, so just run this: `pip3 install python-dotenv win11toast`

All you have to do now is copy `.env.template` to `.env` and reconfigure, or copy the one from when you were setting up Tohru.

At last, you can run the service by typing `python3 kanna.py` or `python kanna.py` in your terminal, or by double-clicking on it.

## P.A.Q. (Potentially Asked Questions)
**Q.** Why is it named Tohru?  
**A.** Tohru is a dragon maid from the hit anime series Miss Kobayashi's Dragon Maid. This has many layers:
  * Miss Kobayashi's Dragon Maid was the first show to be added to the DTAG anime section.
  * The codename for the redesign of the DTAG website is "dragon".
  * Maids are supposed to do stuff for you.
  * Kanna is one Tohru's dragon friends.

**Q.** Nerd.  
**A.** Hey, you asked the question.

**Q.** What if I only want to run Tohru and not Kanna?  
**A.** Tohru will become emotionally unstable and may threaten to kill you.

**Q.** How do I run Tohru/Kanna automatically in the background?  
**A.** For Windows, the [Non-Sucking Service Manager](http://nssm.cc/) works. For Linux, [Supervisor](http://supervisord.org/) is pretty good.
Alternatively, the Docker container can be configured to run whenever Docker is running, but that only works with Tohru for now.

**Q.** How do I set up the MariaDB/MySQL for Tohru?  
**A.** I've provided a very neat (and convenient!!) `init.sql` file for your convenience. Just import it, create a user to access it, and profit!

**Q.** How do I moderate whatever enters the database?  
**A.** There's an Update command for the Stuffpile, but everyone can access that. You'll just have to plunge into the database itself with HeidiSQL or phpMyAdmin, whatever suits you.
