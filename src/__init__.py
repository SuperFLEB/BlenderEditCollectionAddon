import bpy
from mathutils import Vector

bl_info = {
    "name": "Edit Instanced Collection",
    "description": "Edit a Collection Instance's source Collection (even if it is not in the Scene).",
    "author": "FLEB",
    "version": (0, 2, 1),
    "blender": (3, 1, 0),
    "location": "Object > Edit Instanced Collection",
    "doc_url": "https://github.com/SuperFLEB/BlenderEditCollectionAddon",
    "tracker_url": "https://github.com/SuperFLEB/BlenderEditCollectionAddon/issues",
    "support": "COMMUNITY",
    "category": "Object",
}

addon_keymaps = []
package_name = __package__
seen_popup = False


class EditCollection(bpy.types.Operator):
    """Edit the Collection referenced by this Collection Instance in a new Scene"""
    bl_idname = "object.edit_collection"
    bl_label = "Edit Instanced Collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        prefs = context.preferences.addons[package_name].preferences
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

        if prefs.world_texture != "none":
            world = bpy.data.worlds.new(bpy.context.scene.name)
            new_scene.world = world
            world.use_nodes = True
            tree = world.node_tree

            if prefs.world_texture in ["checker", "checker_view"]:
                checker_texture = tree.nodes.new("ShaderNodeTexChecker")
                checker_texture.inputs["Scale"].default_value = 20
                checker_texture.location = Vector((-250, 0))
                if prefs.world_texture == "checker_view":
                    coord = tree.nodes.new("ShaderNodeTexCoord")
                    coord.location = Vector((-500, 0))
                    for op in coord.outputs:
                        op.hide = True
                    tree.links.new(coord.outputs["Window"], checker_texture.inputs["Vector"])
                tree.links.new(checker_texture.outputs["Color"], tree.nodes["Background"].inputs["Color"])
            elif prefs.world_texture == "gray":
                tree.nodes["Background"].inputs["Color"].default_value = (.3, .3, .3, 1)

        # Select the collection
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[coll.name]

        def message(self_2, _):
            global seen_popup

            self_2.layout.label(text="When you're done, simply delete the scene using the X")
            self_2.layout.label(text="and run File > Clean Up > Unused Data Blocks to clean up")
            self_2.layout.label(
                text=f"Be sure to keep all changes you wish to apply within the \"{coll.name}\" collection.")
            # Only show the message about it being able to be turned off the first time
            if not seen_popup:
                seen_popup = True
                self_2.layout.separator()
                self_2.layout.label(
                    text=f"(This message can be turned off in the {bl_info['name']} addon preferences panel.)",
                    icon="INFO"
                )

        if not prefs.hide_scene_popup:
            bpy.context.window_manager.popup_menu(message,
                                                  title=f"Temporary Scene \"{scene_name}\" Created",
                                                  icon="COLLECTION_NEW")

        return {"FINISHED"}


class EditInstancedCollectionPreferences(bpy.types.AddonPreferences):
    bl_idname = package_name
    hide_scene_popup: bpy.props.BoolProperty(
        name="Don't show instructional popup message",
        description="Do not show the informational pop-up when editing a Collection",
        default=False
    )
    world_texture: bpy.props.EnumProperty(
        name="Background",
        description="Background (World) texture of the temporary scene",
        items=[
            ("checker", "Checker (generated map)", "Checker-like texture using a Generated map"),
            ("checker_view", "Checker (view aligned)", "Checkerboard texture aligned to the view"),
            ("gray", "Gray", "Solid Gray Background"),
            ("none", "None", "No World/background (black)")
        ]
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "world_texture")
        layout.prop(self, "hide_scene_popup")


def menu_function(self, context):
    if bpy.context.active_object.instance_collection:
        self.layout.operator(EditCollection.bl_idname)


def register():
    global seen_popup
    seen_popup = False

    # Register classes
    bpy.utils.register_class(EditCollection)
    bpy.utils.register_class(EditInstancedCollectionPreferences)

    # Add menu items
    bpy.types.VIEW3D_MT_object.append(menu_function)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_function)

    # Add keymaps
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")
        kmi = km.keymap_items.new(EditCollection.bl_idname, "C", "PRESS", ctrl=True, alt=True)
        # kmi.properties.total = 4
        addon_keymaps.append((km, kmi))


def unregister():
    # Unregister classes
    bpy.utils.unregister_class(EditCollection)
    bpy.utils.unregister_class(EditInstancedCollectionPreferences)

    # Remove menu items
    bpy.types.VIEW3D_MT_object.remove(menu_function)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_function)

    # Clear keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
