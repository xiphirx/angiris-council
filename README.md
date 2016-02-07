# Angiris Council

A Python package of angiris council members to help moderate [r/Diablo](https://www.reddit.com/r/diablo)

## Itherael

_"Knowledge of the future grants power over the present. For this reason, Itherael, the archangel of Fate, is a vital member of the Council. He alone possesses the ability to decipher the threads of destiny woven in the celestial Scroll of Fate. His boundless sight grants him perspective others cannot fully comprehend."_

Itherael is responsible for tracking all Blizzard employees' postings on reddit and compiling that information into a "blue tracker."

This "blue tracker" is currently located [here](https://www.reddit.com/r/diablo/wiki/bluetracker)

### Usage

```python
import angiriscouncil
itherael = angiriscouncil.Itherael(reddit, 'subreddit')
itherael.track_blues()
```

## Tyrael

_"He has intervened for the sake of humankind time and again, for he sees the potential for heroism and selflessness in each of us. He has even acted against the mandates of his fellow Council members to fight on our behalf. For that alone I always have and always will believe in him."_

Tyrael is responsible for posting our weekly threads and updating the subreddit's top-bar links for said weekly threads.

### Usage

```python
import angiriscouncil
tyrael = angiriscouncil.Tyrael(reddit, 'subreddit')
tyrael.post_weekly_thread()
```

`post_weekly_thread` will determine the current weekday and post the corresponding thread(s) for that day.

## License
    Copyright (C) 2016 Hilal Alsibai

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
