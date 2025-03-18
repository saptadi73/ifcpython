import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape

ifc_file = ifcopenshell.open("sample.ifc")


# slabs = ifc_file.by_type("IfcSlab")
def get_properties(expressID):
    print(f'Property expressID: {expressID}')
    slab = ifc_file.by_id(expressID)

    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, slab)

    # bottom_elevation = ifcopenshell.util.shape.get_bottom_elevation(shape.geometry)
    # print(f'Bottom elevation: {bottom_elevation}')

    # top_elevation = ifcopenshell.util.shape.get_top_elevation(shape.geometry)
    # print(f'Top elevation: {top_elevation}')

    footprint_area = round(ifcopenshell.util.shape.get_footprint_area(shape.geometry),2)
    print(f'Footprint area: {footprint_area} m2')

    footprint_perimeter = round(ifcopenshell.util.shape.get_footprint_perimeter(shape.geometry),2)
    print(f'Footprint perimeter: {footprint_perimeter} m2')

    # area = round(ifcopenshell.util.shape.get_area(shape.geometry),2)
    # print(f'Total area: {area} m2')

    volume = round(ifcopenshell.util.shape.get_volume(shape.geometry),2)
    print(f'Volume: {volume} m3')

    side_area = round(ifcopenshell.util.shape.get_side_area(shape.geometry),2)
    print(f'Side Gross area: {side_area} m2')

    # x = ifcopenshell.util.shape.get_x(shape.geometry)
    # y = ifcopenshell.util.shape.get_y(shape.geometry)
    # z = ifcopenshell.util.shape.get_z(shape.geometry)
    # print(f'Facade position: x = {x}, y = {y}, z = {z}')

    # height = ifcopenshell.util.shape.get_top_elevation(shape.geometry)
    height = round(ifcopenshell.util.shape.get_z(shape.geometry),2)
    print(f'Height: {height} m')

    length = round(ifcopenshell.util.shape.get_x(shape.geometry),2)
    print(f'Length: {length} m')

    width = round(ifcopenshell.util.shape.get_y(shape.geometry),2)
    print(f'Width: {width} m\n')

get_properties(1225)
get_properties(936)