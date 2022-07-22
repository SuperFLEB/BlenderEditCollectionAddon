import bpy

bl_info = {
    "name": "Edit Instanced Collection",
    "author": "FLEB",
    "version": (0, 1, 0),
    "blender": (3, 2, 0),
    "category": "Object"
}

addon_keymaps = []

print("HELLLOOOOOO EIC!")


class EditCollection(bpy.types.Operator):
    """Edit the Collection referenced by this Collection Instance in a new Scene"""
    bl_idname = "object.edit_collection"
    bl_label = "Edit Instanced Collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        coll = bpy.context.active_object.instance_collection

        if not coll:
            print("Active item is not a collection instance")
            self.report({"WARNING"}, "Active item is not a collection instance")
            return {"CANCELLED"}

        scene_name = f"temp:{coll.name}"
        bpy.ops.scene.new(type="EMPTY")
        new_scene = bpy.context.scene
        new_scene.name = scene_name
        bpy.context.window.scene = new_scene
        new_scene.collection.children.link(coll)
        # Select the collection
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[coll.name]

        def message(self_2, _):
            self_2.layout.label(text=f"When you're done, simply delete the scene using the X "
                                     "in the Scene selector on the right side of the main menu bar.")
            self_2.layout.label(
                text=f"Be sure to keep all changes you wish to apply within the \"{coll.name}\" collection.")

        bpy.context.window_manager.popup_menu(message, title=f"Temporary Scene \"{scene_name}\" Created", icon='INFO')

        return {"FINISHED"}


def menu_function(self, context):
    if bpy.context.active_object.instance_collection:
        self.layout.operator(EditCollection.bl_idname)


def register():
    bpy.utils.register_class(EditCollection)
    bpy.types.VIEW3D_MT_object.append(menu_function)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_function)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(EditCollection.bl_idname, 'C', 'PRESS', ctrl=True, alt=True)
        # kmi.properties.total = 4
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(EditCollection)
    bpy.types.VIEW3D_MT_object.remove(menu_function)
