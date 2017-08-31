# AudioQuranBot

بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

AudioQuranBot is a bot on Telegram that shares audio recitations of the Holy
Qur'an. [Talk with it][AudioQuranBot] to request audio tracks of surahs recited
by [Shaykh Mahmoud Khalil al-Husary][qari].

[AudioQuranBot]: https://telegram.me/AudioQuranBot
[qari]: https://en.wikipedia.org/wiki/Mahmoud_Khalil_Al-Hussary


# Installation

Get the code and dependencies:

``` shell
sudo apt install redis-server git python3-pip python3-dev virtualenv
git clone https://github.com/rahiel/AudioQuranBot.git
cd AudioQuranBot/
virtualenv -p python3 venv
. venv/bin/activate
pip install --upgrade git+https://github.com/rahiel/BismillahBot.git
pip install -r requirements.txt --upgrade
```

Put the bot's API token in a `secret.py` file:

```python
token = "<your-token-here>"
```

## Data

Download [this torrent][torrent] with the audio files and save the data in the
bot's main directory.

Get Quran metadata:

``` shell
wget 'http://tanzil.net/res/text/metadata/quran-data.xml'
```

Telegram bots are currently only allowed to send files up to 50 MB. Some audio
tracks are bigger, so they need to be split. In the directory with the audio,
split them with ffmpeg:

``` shell
ffmpeg -t 46:41 -i 002.mp3 -codec:a copy -vn -metadata title="Al-Baqarah (part 1/4)" 002_1.mp3              # ayah 1 - 86
ffmpeg -ss 46:41 -t 49:57 -i 002.mp3 -codec:a copy -vn -metadata title="Al-Baqarah (part 2/4)" 002_2.mp3    # ayah 87 - 167
ffmpeg -ss 1:36:38 -t 50:26 -i 002.mp3 -codec:a copy -vn -metadata title="Al-Baqarah (part 3/4)" 002_3.mp3  # ayah 168 - 231
ffmpeg -ss 2:27:04 -i 002.mp3 -codec:a copy -vn -metadata title="Al-Baqarah (part 4/4)" 002_4.mp3           # ayah 232 - end

ffmpeg -t 38:09 -i 003.mp3 -codec:a copy -vn -metadata title="Al-Imran (part 1/3)" 003_1.mp3                # ayah 1 - 71
ffmpeg -ss 38:09 -t 39:01 -i 003.mp3 -codec:a copy -vn -metadata title="Al-Imran (part 2/3)" 003_2.mp3      # ayah 72 - 143
ffmpeg -ss 1:17:10 -i 003.mp3 -codec:a copy -vn -metadata title="Al-Imran (part 3/3)" 003_3.mp3             # ayah 144 - end

ffmpeg -t 40:48 -i 004.mp3 -codec:a copy -vn -metadata title="An-Nisa' (part 1/3)" 004_1.mp3                # ayah 1 - 59
ffmpeg -ss 40:48 -t 34:54 -i 004.mp3 -codec:a copy -vn -metadata title="An-Nisa' (part 2/3)" 004_2.mp3      # ayah 60 - 112
ffmpeg -ss 1:15:42 -i 004.mp3 -codec:a copy -vn -metadata title="An-Nisa' (part 3/3)" 004_3.mp3             # 113 - end

ffmpeg -t 43:44.7 -i 005.mp3 -codec:a copy -vn -metadata title="Al-Ma'idah (part 1/2)" 005_1.mp3            # ayah 1 - 50
ffmpeg -ss 43:44.7 -i 005.mp3 -codec:a copy -vn -metadata title="Al-Ma'idah (part 2/2)" 005_2.mp3           # ayah 51 - end

ffmpeg -t 50:04 -i 006.mp3 -codec:a copy -vn -metadata title="Al-An'am (part 1/2)" 006_1.mp3                # ayah 1 - 90
ffmpeg -ss 50:04 -i 006.mp3 -codec:a copy -vn -metadata title="Al-An'am (part 2/2)" 006_2.mp3               # ayah 91 - end

ffmpeg -t 53:44 -i 007.mp3 -codec:a copy -vn -metadata title="Al-A'raf (part 1/2)" 007_1.mp3                # ayah 1 - 100
ffmpeg -ss 53:44 -i 007.mp3 -codec:a copy -vn -metadata title="Al-A'raf (part 2/2)" 007_2.mp3               # ayah 101 - end

ffmpeg -t 44:48 -i 009.mp3 -codec:a copy -vn -metadata title="At-Taubah (part 1/2)" 009_1.mp3               # ayah 1 - 66
ffmpeg -ss 44:48 -i 009.mp3 -codec:a copy -vn -metadata title="At-Taubah (part 2/2)" 009_2.mp3              #  ayah 67 - end

ffmpeg -t 34:32 -i 010.mp3 -codec:a copy -vn -metadata title="Yunus (part 1/2)" 010_1.mp3                   # ayah 1 - 60
ffmpeg -ss 34:32 -i 010.mp3 -codec:a copy -vn -metadata title="Yunus (part 2/2)" 010_2.mp3                  # ayah 61 - end

ffmpeg -t 26:49 -i 011.mp3 -codec:a copy -vn -metadata title="Hood (part 1/2)" 011_1.mp3                    # ayah 1 - 60
ffmpeg -ss 26:49 -i 011.mp3 -codec:a copy -vn -metadata title="Hood (part 2/2)" 011_2.mp3                   # ayah 61 - end

ffmpeg -t 27:02.3 -i 012.mp3 -codec:a copy -vn -metadata title="Yusuf (part 1/2)" 012_1.mp3                 # ayah 1 - 49
ffmpeg -ss 27:02.3 -i 012.mp3 -codec:a copy -vn -metadata title="Yusuf (part 2/2)" 012_2.mp3                # ayah 50 - en

ffmpeg -t 27:19 -i 016.mp3 -codec:a copy -vn -metadata title="An-Nahl (part 1/2)" 016_1.mp3                 # ayah 1 - 65
ffmpeg -ss 27:19 -i 016.mp3 -codec:a copy -vn -metadata title="An-Nahl (part 2/2)" 016_2.mp3                # ayah 66 - end
```

[torrent]: http://torrent.mp3quran.net/details.php?id=3f2404b9cc6dfb5ccf70580a149fd8b87de0d8f1

# License

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
