<p align="center"><img src="screenshots/reviewer.gif" height=500></p>

<h2 align="center">Puppy Reinforcement for Anki</h2>

<p align="center">
<a title="Latest (pre-)release" href="https://github.com/glutanimate/puppy-reinforcement/releases"><img src ="https://img.shields.io/github/release-pre/glutanimate/puppy-reinforcement.svg?colorB=brightgreen"></a>
<a title="License: GNU AGPLv3" href="https://github.com/glutanimate/puppy-reinforcement/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a title="Rate on AnkiWeb" href="https://ankiweb.net/shared/info/1722658993"><img src="https://glutanimate.com/logos/ankiweb-rate.svg"></a>
<br>
<a title="Buy me a coffee :)" href="https://ko-fi.com/X8X0L4YV"><img src="https://img.shields.io/badge/ko--fi-contribute-%23579ebd.svg"></a>
<a title="Support me on Patreon :D" href="https://www.patreon.com/bePatron?u=7522179"><img src="https://img.shields.io/badge/patreon-support-%23f96854.svg"></a>
<a title="Follow me on Twitter" href="https://twitter.com/intent/user?screen_name=glutanimate"><img src="https://img.shields.io/twitter/follow/glutanimate.svg"></a>
</p>

> Everything's better with puppies!

An add-on for the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/) that encourages learners with pictures of cute puppies, following the principles of intermittent positive reinforcement.

### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC levels="1,2,3" -->

- [Video](#video)
- [Installation](#installation)
- [Documentation](#documentation)
- [Building](#building)
- [Contributing](#contributing)
- [License and Credits](#license-and-credits)

<!-- /MarkdownTOC -->

###  Video

A quick demo of the add-on (alongside other similar add-ons related to gamification):

[![YouTube: Anki add-on guide: Gamify Your Reviews](https://i.ytimg.com/vi/UkveLkAgXiM/mqdefault.jpg)](https://youtu.be/UkveLkAgXiM)

### Installation

#### AnkiWeb <!-- omit in toc -->

The easiest way to install Puppy Reinforcement is through [AnkiWeb](https://ankiweb.net/shared/info/1722658993).

#### Manual installation <!-- omit in toc -->

Please click on the entry corresponding to your Anki version:

<details>

<summary><i>Anki 2.1</i></summary>

1. Make sure you have the [latest version](https://apps.ankiweb.net/#download) of Anki 2.1 installed. Earlier releases (e.g. found in various Linux distros) do not support `.ankiaddon` packages.
2. Download the latest `.ankiaddon` package from the [releases tab](https://github.com/glutanimate/puppy-reinforcement/releases) (you might need to click on *Assets* below the description to reveal the download links)
3. From Anki's main window, head to *Tools* → *Add-ons*
4. Drag-and-drop the `.ankiaddon` package onto the add-ons list
5. Restart Anki

</details>

<details>

<summary><i>Anki 2.0</i></summary>

1. Go to *Tools* → *Add-ons* → *Open add-ons folder*
2. Find and delete the `Puppy Reinforcement.py` file if it already exists.
3. See if you can find a `puppy_reinforcement` folder. If so:
    1. If the folder contains a `meta.json` file, copy the file to a safe location. This will allow you to preserve your current settings.
    2. Proceed to delete the `puppy_reinforcement` folder
4. Download and extract the latest Anki 2.0 add-on release from the [releases tab](https://github.com/glutanimate/puppy-reinforcement/releases) (you might need to click on *Assets* below the description to reveal the download links)
5. Move the extracted `Puppy Reinforcement.py` and `puppy_reinforcement` into the add-ons folder
6. Optional: Place the `meta.json` file back into the directory if you created a copy beforehand.
7. Restart Anki

</details>

### Documentation

For further information on the use of this add-on please check out [the description text](docs/description.md) for AnkiWeb.

### Building

With [Anki add-on builder](https://github.com/glutanimate/anki-addon-builder/) installed:

    git clone https://github.com/glutanimate/puppy-reinforcement.git
    cd puppy-reinforcement
    aab build

For more information on the build process please refer to [`aab`'s documentation](https://github.com/glutanimate/anki-addon-builder/#usage).

### Contributing

Contributions are welcome! Please review the [contribution guidelines](./CONTRIBUTING.md) on how to:

- Report issues
- File pull requests
- Support the project as a non-developer

### License and Credits

*Puppy Reinforcement* is *Copyright © 2016-2020 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

With code contributions from: [@zjosua](https://github.com/zjosua) (thanks!)

Puppy Reinforcement is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [LICENSE](https://github.com/glutanimate/puppy-reinforcement/blob/master/LICENSE) file that accompanied this program.

Please note that this program uses the [Libaddon](https://github.com/glutanimate/anki-libaddon/) library which comes with [its own additional terms extending the GNU AGPLv3 license](https://github.com/glutanimate/puppy-reinforcement/blob/master/src/puppy_reinforcement/libaddon/LICENSE). You may only copy, distribute, or modify the present compilation of this program with Libaddon under the combined licensing terms specified by both licenses.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

----

<b>
<div align="center">The continued development of this add-on is made possible <br>thanks to my <a href="https://www.patreon.com/glutanimate">Patreon</a> and <a href="https://ko-fi.com/X8X0L4YV">Ko-Fi</a> supporters.
<br>You guys rock ❤️ !</div>
</b>