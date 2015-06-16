Extending Pylease
=================

Although Pylease is an Open Source project, it is impossible to consider and include all possible features at once. Moreover, one may
want a particular feature urgently. Even after sending a feature request, he may have no time to wait for confirmation, implementation
and release of that feature. On the other hand, Pylease may get too much loaded with features that does not get used by everyone.

For this reason, one of the major parts of Pylease is its extension system. It allows to develop a separate Python pakage and optionally
plug it into Pylease.

So basically there are two ways to extend Pylease:

 - Add new commands
 - Add before and after tasks for existing commands

