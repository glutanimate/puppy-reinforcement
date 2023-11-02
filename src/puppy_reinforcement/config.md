**Puppy Reinforcement** supports the following config values:

<div style="color: #ff8080; font-weight: bold;">Please note that you will have to restart Anki for some of these options to apply (e.g. toggling the add-on for reviews / adding cards)</div>

- **count_adding** [true/false]: count added cards towards puppy tally; default: `false`
- **count_reviewing** [true/false]: count reviews towards puppy tally; default: `true`
- **duration** [integer]: duration in msec; default: `3000`
- **encourage_every** [integer]: show encouragement about every n cards; default: `10`
- **encouragements** [dict]: encouragements by level
- **image_height** [integer]: image height in px, tooltip is automatically scaled; default: `128`
- **limit_high** [integer]: lower card limit for high encouragement level; defaults: `50`
- **limit_max** [integer]: lower card limit for max encouragement level; defaults: `100`
- **limit_middle** [integer]: lower card limit for middle encouragement level; defaults: `25`
- **max_spread** [integer]: max spread around interval; default: `5`
- **tooltip_color** [string]: HTML color code; default: `#AFFFC5` (light green)
- **tooltip_align_vertical** [enum]: controls vertical screen position at which tooltips will pop up. You can select between: `top`, `center` and `bottom`. Default: `bottom`.
- **tooltip_align_horizontal** [enum]: controls vertical screen position at which tooltips will pop up. You can select between: `right`, `center` and `left`. Default: `left`.
- **tooltip_space_vertical** [integer]: allows you to fine-tune the tooltip position by specifying a distance between the tooltip and the top/bottom edge of Anki. Only applies when selecting `top` or `bottom` as `tooltip_align_vertical`. Default: `100`.
- **tooltip_space_horizontal** [integer]: allows you to fine-tune the tooltip position by specifying a distance between the tooltip and the left/right edge of Anki. Only applies when selecting `left` or `right` as `tooltip_align_horizontal`. Default: `0`.

---

Created with ❤️ by [Glutanimate](https://glutanimate.com). If you enjoy this add-on, please consider supporting my work by **[pledging your support on Patreon](https://www.patreon.com/bePatron?u=7522179)** or by **[buying me a coffee](https://ko-fi.com/X8X0L4YV)**. Thanks!
