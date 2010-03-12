CMYKProjectManager
==================

This plugin provides a TextMate-Like project manager.
This is the first version (0.1) and allows to add projects (folders)
using drag & drop over its left panel.
To remove a project simply right-click on it and select 'Delete'

Installation
------------

1. Copy the `CMYKProjectManager.gedit-plugin` and the `CMYKProjectManager`
   into your `~/.gnome2/gedit/plugins/`
2. Open gedit and click `Edit -> Preferences -> Plugins`
3. Check the `CMYKProject Manager 0.1` and hit `Close`
4. Restart Gedit and use the plugin dragging your first project (a folder )
   over his left panel

Features
-------
 Current version:  
  - Adds a project via drag & drop  
  - Right clicking on the Project root allows the user to open the corrispective directory  
  - Basic files sorting

 In Development:  
  - Visualize icons of the files  
  - Compress the project directory in an archive (for backup purposes)
  - Gedit Menus integration (adding a project, remove projects etc..)  

License
-------

Copyright (C) 2009 [Michael Cereda](http://cmyklover.com/)

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

Credits
-------

Thanks to all the creators of gedit plugins, i've used pieces of code from:
 * Class Browser Plugin, Frederic Back
 * scratchTab, Rui Nibau


Changes
-------
> @2010-02-15  -  thanks ukanga [http://github.com/ukanga]
> Added basic sorting
> Fixed the "Can't create a project" error

> @2010-02-15
> Fixed the "Click on directory" error, now clicking on a directory just open the Treeview

> @2009-08-06
> Added Show in default file browser.
> Now you can "jump" directly to the project folder in your default file browser
> right-clicking on the project browser folder and selecting 'Open'

> @2009-07-27
> First commit.
> The plugin is not yet optimized and is only a beta-version, new features will
> be added as soon as possible

