fliki
=====

This is fork of [fdb/fliki](https://github.com/fdb/fliki).  The itch it
was originally trying to scratch was small, self-contained,
possibly-throwaway wiki notebooks, only those tend not to have revision
control.  When you clone this and `pip install -r`, you get a microwiki
pretty much like any other, but with the benefits of git.  That's how
I've been using it, anyway.

It has the following changes from the base version of fliki:
* uses creole instead of markdown
* version control via git
* ajax preview
* better (though still crappy) handling of page titles
* ʇɹoddns ǝpoɔıun

It's possible it will spiral out of control and turn into a real
(non-micro) wiki though...

### TODO
* separate page repos from code repo
* support multiple page repos
* multiple and pluggable parsers

### MAYBES
These things either require careful design, or I don't know if I want
them badly enough, or both
* a way to do entity relationships (yeah weird, huh?)
* hooks and plugins and whatnot
* some kind of virtualenv management
