# Blender "Edit Instanced Collection" Addon
An add-on for Blender that allows quickly editing Collection Instance source collections.

This came about as the result of making Asset Library files that used Collection Instances to house multiple-Object assets.
Upon importing them into another file, they would be seemingly uneditable, as Blender would link the Collection Instances to
the current Scene, but not the Collection itself.

Since it was a relatively reproducible process to find and link the Collections, I created this addon that allows quickly
dropping in to edit the underlying Collection of a Collection Instance, and then dropping out.

## To Install

It's an ordinary Blender addon. You can either install the ZIP release and install it, or clone/copy this into your
Blender addons directory.

## To Use

1. Select a Collection Instance. (Selecting multiple Collection Instances is not supported.)
2. Either from the Object menu or the spacebar/W context menu, select "Edit Instanced Collection", or use the hotkey (Ctrl+Alt+C)
   in Object Mode.
3. You will be dropped into a newly-created Scene containing nothing but the Collection. Edit the collection, and your
   edits will be reflected in all instances of the Collection.
4. Once you are done editing (ensure that all new objects are within the Collection) delete the temporary Scene (named
   "temp(name-of-collection)").

You can drill down to multiple levels, though you will have to be sure to clean up any temporary Scenes
made by the addon.
