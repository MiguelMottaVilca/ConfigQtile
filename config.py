from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen , Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os

mod = "mod4"
#terminal = guess_terminal()
terminal = "alacritty"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),


    # rofi
    Key([mod], "m", lazy.spawn("rofi -show run")),
    Key([mod, 'shift'], "m", lazy.spawn("rofi -show")),
    # alacritty
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # firefox
    Key([mod], "f", lazy.spawn("firefox")),
    # thunar
    Key([mod], "e", lazy.spawn("dolphin")),
    # spotify
    Key([mod], "s", lazy.spawn("spotify")),



    # Brillo
    Key([] , "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    Key([] , "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    
    # Volume
    #Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    #Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    #Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Volume pamixer
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),

]

__groups = {
    1:Group("" , matches = [Match(wm_class=["firefox"])]),
    2:Group("" , matches = [Match(wm_class=["alacritty"])]),
    3:Group("" , matches = [Match(wm_class=["Thunar"])]),
    4:Group("" , matches = [Match(wm_class=["spotify"])]),
    5:Group(""),
}

groups = [__groups[i] for i in __groups]

def get_group_key(name):
    return [k for k , g in __groups.items() if g.name == name ][0]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(get_group_key(i.name)) ,lazy.group[i.name].toscreen() , 
            desc="Switch to group {}".format(i.name)),

        Key([mod,"shift"],str(get_group_key(i.name)) ,lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])
#ventanas
layouts = [
    layout.Max(),
    layout.MonadTall(
        border_width = 2 ,
        border_focus = "#ffffff" ,
        single_border_width = 0 ,
        margin = 4 ,
    ),
]

widget_defaults = dict(
    font='sans',
    #font = "UbuntuMono Nerd Font Bold",
    fontsize=18,
    padding=1,
)
extension_defaults = widget_defaults.copy()
#00ffe8
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout( 
                    foreground = "#ffffff" ,
                    fontsize = 15
                ),
                widget.GroupBox(
                    highlight_color=["#333948"] , # caja
                    highlight_method = "line" ,
                    active="#ffffff" ,
                    inactive="#485267",
                    block_highlight_text_color = "#ffffff", # icons
                    spacing = 10 ,
                    panddind = 10 ,
                    border_width = 10 ,
                    fontsize = 42 
                ),
                #widget.Prompt(),
                widget.WindowName(
                    foreground = "#ffffff" ,
                    fontsize = 15
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CheckUpdates(
                    #foreground = "#ffffff",
                    custom_command = "checkupdates",
                    update_interval = 1800 ,
                    display_format = " {updates}" ,
                    execute = "alacritty -e sudo pacman -Syyu" ,
                    #padding = 10 ,
                ),
                widget.TextBox("", fontsize = 30 ),
                widget.TextBox("Miguel", name="user"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.TextBox("", fontsize = 35 ),
                widget.Clock(format="%Y/%m/%d %a %I:%M:%S %p "),
                #widget.QuickExit(),
                widget.Systray(), # batery , wifi , ....
            ],
            26,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "LG3D"

autostart = [
    "setxkbmap latam",
    "feh --bg-fill /home/miguel/Pictures/wallpaper.jpg",
    "nm-applet &",
    "volumeicon &"
    "cbatticon &",
    "udiskie -t &",
]

for x in autostart:
    os.system(x)
