# Blender "Edit Instanced Collection" Addon
An add-on for Blender that allows quickly editing Collection Instance source collections

This came about as the result of making Asset Library files that used Collection Instances to house multiple-Object assets.
Upon importing them into another file, they would be seemingly uneditable, as Blender would link the Collection Instances to
the current Scene, but not the Collection itself.

After some searching around, I found that the collections were attached to the file (accessible via the Blender File view in
the outliner), but that was hidden away and difficult to work with (attaching them back to the Scene using "Link to Scene"
worked, but then you have an extra copy hanging around your scene).

Since it was a relatively reprocducible process to find and link the Collections, I created this addon that allows quickly
dropping in to edit the underlying Collection of a Collection Instance.

## To Use

Select a Collection Instance. Selecting multiple Collection Instances is not supported, and the active item must be a Collection
Instance to see the menu. Either from the Object menu or the spacebar/W menu, select "Edit Instanced Collection". You will be
dropped into a newly-created Scene containing nothing but the Collection. You can edit and add or remove items, which will be
reflected in all instances of the Collection. Once you are done editing (ensure that all new objects are within the Collection)
delete the temporary Scene (named "temp(name-of-collection)"). You can drill down to multiple levels, though you will have to be
sure to clean up any temporary Scenes made by the addon.
