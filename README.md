# CDJ1000-Nexus-MOD
This is a on-going project to create a skin for DJ software "MIXXX" to make a CDJ1000mk3 MIDI moded work as a Nexus CDJ2000 model

Pioneer inspired theme for smaller screen resolutions. It has been designed to 'extend' a MIDI controller.

This project is being developed using ChatGPT as im not a poeficient coder/programmer so bear in mind that the code may seam weird for a professional programmer.

This repository contains the source code for "My Nexus App," a Python application built using the PyQt5 framework. The application serves as a digital DJ tool with MIDI integration, waveform visualization, music track management, and extended functionalities.

Features
** MIDI Integration
The application leverages the mido library to handle MIDI input and output. The MidiThread class manages MIDI ports, allowing communication with external MIDI devices. MIDI messages are received in real-time, enabling seamless integration with MIDI controllers.

** Waveform Visualization
The ExtendedWaveformFrame class provides an extended waveform display with various features:

** Fixed Needle: Represents a specific position within the waveform.
** Loop Markers: Display customizable loop start and end points.
** Slip Function Needle: Indicates a slip function position.
** Zoom In/Out: Allows users to zoom in and out of the waveform for detailed analysis.
** Music Track Management

The MyNexusApp class serves as the main application window and includes features such as:

Music Loading: Displays information about the currently playing track, including title, artist, album, and artwork.
Music List: Populates a list of tracks, allowing users to select and load them into the player.
Extended Functionalities
The application includes additional functionalities:

Looping: Provides loop division options with a customizable menu.
Beat Jump: Offers beat jump options for quick navigation within the track.
Customizable Colors: Allows users to customize needle and marker colors using a color dialog.
Menu System: Implements a menu bar with options for file management, extended configurations, and music sources.
User Interface
The user interface is designed with a top bar for general information, waveform displays, a position slider, artwork display, track information, music list, and various buttons for controls.

Usage
Installation: Ensure you have Python and PyQt5 installed. You may also need to install the mido library for MIDI support.

bash
Copy code
pip install PyQt5 mido
Run the Application:

bash
Copy code
python my_nexus_app.py
Interact:

Load music tracks, customize colors, and explore waveform features.
Utilize MIDI controllers for real-time interaction.


![Alt text](https://github.com/freddykat/CDJ1000-Nexus-MOD/blob/main/images.jpg)

## Features
* Tabbed view: Main Menu
* Fully scalable to use a 6.1" screen
* Inspired by the Pioneer CDJ2000NSX interface
* Small waveform overviews at the bottom and big extended RGB overview waveform
* Keylock/Quantize/Slip buttons 
* Beatjump/Loop size on screen button (popup as factory Pioneer product)
* MIDI handling
* Barely any resources = Rpi4b or Rpi5!
