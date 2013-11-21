Scumbot
=======

Description:

IRC Bot that hosts Mafia games (also known as werewolf)
This simple bot can currently host a vanilla only version of the party game Mafia. It is in very early development.

=======

Note: Current Issues

Too much stuff is hardcoded. The Main class is being rewritten, if anyone wants to actually use the bot, please run
objectmafiaplayer.py instead of main.py. The old main class will soon be removed from the project and replaced with
the new better written one.

=======


Current Tasklist:

- Rewrite the Main class to be less awful
- Move the initialization variablers to a configuration file

Longer Term:

- Add roles (cop, doctor, etc)
- Add a database for stats
- Allow the Bot to run it's own channel (+m and manage channel chat)
- Handle errors better, make sure the bot doesn't crash
