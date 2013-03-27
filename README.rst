cclib for IOS
============

(This is a work in progress. The goal is to have an easy-to-use version
of cclib/Python for iOS.

#. This is based on kivy-ios. You need developer tools like autoconf,
   automake, libtool, etc.

#. For now, only a trimmed-down version of cclib will be attempted. This is
   because cross-compiling numpy is not straight-foward. It should, however,
   be possible to compile multiarray (old Numeric) support directly into the 
   Python interpreter.

