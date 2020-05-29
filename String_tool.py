bl_info = {
    "name": "STRING",
    "blender": (2, 80, 0),
    "category": "Object",
    'Author' : 'Vibhor Gupta'
}

import bpy
import bmesh


class STRING(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.stringtool_ot"        # Unique identifier for buttons and menu items to reference.
    bl_label = "String"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    
    bdepth: bpy.props.FloatProperty(name = "String Thickness", min = 0.1, max = 5, precision = 2 )

    def execute(self, context):
       # The original script
       ####################
       #to create an edge between two given objects            
        def Edgify(ob1,ob2):
            loc1 = ob1.location
            loc2 = ob2.location
            verts = [loc1,loc2]
            bpy.ops.mesh.primitive_plane_add(location = (0,0,0))
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete(type='VERT')

            #creating the vertices using the current mesh data into bmesh 
            pipe = bpy.context.object.data
            bm = bmesh.new()
            
            for v in verts:
                bm.verts.new(v)
                
            bpy.ops.object.editmode_toggle()
            bm.to_mesh(pipe)
            bm.free() 
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            

        def string(olist):
            edges = []
            l = len(olist)
            for x in range(l):
                for y in range(l):
                    if y != x and x < y :
                        Edgify(olist[x], olist[y])
                        edges.append(bpy.context.active_object)
            return edges


        def piper(xlist):
            bpy.ops.object.select_all(action='DESELECT')
            for x in xlist:
                x.select_set(True)
            bpy.ops.object.join()
            bpy.ops.object.convert(target='CURVE')
            
        def check(olist):
            if len(olist) == 0:
                self.report({'INFO'},'NONE SELECTED OBJECTS')
                return 0
            else:
                return 1 
            
                    
        
        oblist = bpy.context.selected_objects     
        
        Edgelist = string(oblist)

        piper(Edgelist)
        
        actob = bpy.context.active_object
        actob.data.bevel_depth = self.bdepth
        bpy.ops.object.shade_smooth()

            
            
        ########################
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


            
def register():
    bpy.utils.register_class(STRING)


def unregister():
    bpy.utils.unregister_class(STRING)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
    
    
    
    
