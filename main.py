import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import ifcopenshell.util.element
from routers import projects,tasks,task_activities, task_approver, issues, issue_activities,issue_approver
from fastapi.staticfiles import StaticFiles
import os


# Di awal aplikasi (global)
# connection_pool = pool.SimpleConnectionPool(
#     1, 10,
#     dbname="bim",
#     user="odoo16",
#     password="PG0doo16SQL",
#     host="103.127.139.73",
#     port="5432"
# )

connection_pool = pool.SimpleConnectionPool(
    1, 10,
    dbname="bim",
    user="openpg",
    password="openpgpwd",
    host="localhost",
    port="5432"
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# mount uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(projects.router, prefix="/project", tags=["project"])

app.include_router(tasks.router, prefix="/task", tags=["task"])
app.include_router(task_activities.router, prefix="/task/activity", tags=["task_activity"])
app.include_router(task_approver.router, prefix="/task/approver", tags=["task_approver"])

app.include_router(issues.router, prefix="/issue", tags=["issue"])
app.include_router(issue_activities.router, prefix="/issue/activity", tags=["issue_activity"])
app.include_router(issue_approver.router, prefix="/issue/approver", tags=["issue_approver"])


ifc_file = ifcopenshell.open("sample.ifc")

def get_db_connection():
    return connection_pool.getconn()  # dapatkan koneksi dari pool

def release_db_connection(conn):
    connection_pool.putconn(conn)  # kembalikan koneksi ke pool

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

# get_properties(1225)
# get_properties(936)

@app.get("/")
async def getRoot():
    return {"message": "Welcome to the API"}

@app.get("/id/{expressID}")
async def getIfcWithExpressID(expressID: int):
    slab = ifc_file.by_id(expressID)

    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, slab)
    footprint_area = round(ifcopenshell.util.shape.get_footprint_area(shape.geometry),2)
    footprint_perimeter = round(ifcopenshell.util.shape.get_footprint_perimeter(shape.geometry),2)
    volume = round(ifcopenshell.util.shape.get_volume(shape.geometry),2)
    side_area = round(ifcopenshell.util.shape.get_side_area(shape.geometry),2)
    height = round(ifcopenshell.util.shape.get_z(shape.geometry),2)
    length = round(ifcopenshell.util.shape.get_x(shape.geometry),2)
    width = round(ifcopenshell.util.shape.get_y(shape.geometry),2)

    globalId = slab.GlobalId
    name = slab.Name
    description = slab.Description
    objctType = slab.ObjectType
    if hasattr(slab, "ObjectPlacement"):
        placement = slab.ObjectPlacement


    # Get geometric representation
    if hasattr(slab, "Representation"):
        representation = slab.Representation


    result = {
    "bimfile": "JHSModern56.ifc",
    "globaid": str(globalId),
    "name": str(name),
    "representation": str(representation) if representation else None,
    "placement": str(placement) if placement else None,
    "description": str(description) if description else None,
    "objctType": str(objctType) if objctType else None,
    "length": length,
    "width": width,
    "height": height,
    "area": side_area,
    "volume": volume,
    "footprintarea": footprint_area,
    "footprintperimeter": footprint_perimeter
}
    return result

@app.get("/type/{type}")
async def getIfcType(type: str):
    # Get all IfcWall entities
    walls = ifc_file.by_type(type)

    # Extract and print GlobalId for each wall
    for wall in walls:
        global_id = wall.GlobalId
        ifclabel = wall.Name
        return {"globalid": global_id,"ifclabel": ifclabel}

@app.get("/globalid/{globalid}")
async def getPropGlobalId(globalid: str):

    # Iterate through all entities in the IFC file
    for entity in ifc_file:
        if hasattr(entity, "GlobalId") and entity.GlobalId == globalid:
            print("Entity found:", entity)

            # Extract properties from IfcPropertySet
            property_sets = entity.IsDefinedBy
            for prop_set in property_sets:
                if prop_set.is_a("IfcRelDefinesByProperties"):
                    property_set = prop_set.RelatingPropertyDefinition
                    if property_set.is_a("IfcPropertySet"):
                        print(f"Property Set: {property_set.Name}")
                        for prop in property_set.HasProperties:
                            print(f"  {prop.Name}: {prop.NominalValue.wrappedValue}")

            # Extract quantities from IfcElementQuantity
            quantities = entity.IsDefinedBy
            for quantity in quantities:
                if quantity.is_a("IfcRelDefinesByProperties"):
                    element_quantity = quantity.RelatingPropertyDefinition
                    if element_quantity.is_a("IfcElementQuantity"):
                        print(f"Quantity Set: {element_quantity.Name}")
                        for qty in element_quantity.Quantities:
                            print(f"  {qty.Name}: {qty.Value.wrappedValue}")
        break
    else:
        print("Entity with GlobalId not found.")

@app.get("/uuid")
def getUUID():
    return str(uuid.uuid4())

@app.get("/users")
# def getAllUsers():
    # sql_command="""
    # select * from users
    # """
    # cursor.execute(sql_command)
    # record = cursor.fetchall()
    # return record

def getAllUsers():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command = "SELECT * FROM users;"  # ganti sesuai query kamu
        cursor.execute(sql_command)
        results = cursor.fetchall()
        return results

    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection


@app.get("/tasks/done/{id}")
def getAllTasksDone(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        sql_command="""
        select t.project_id, t.name, t.id, t.globalid, t.expressid,t.value,t.start_date,t.end_date,u.name as assign_to,u2.name as issued_by,t.location
        from tasks t
        left join users u on t.user_assign_id = u.id
        left join users u2 on t.user_issued_id = u2.id
        where t.status ='done' and t.project_id=%s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data task selesai","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data task selesai","result":""}
        return response

    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/tasks/all/{id}")
def getAllTasks(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql_command="""
        select t.project_id, t.status, t.name, t.id, t.globalid, t.expressid,t.value,t.start_date,t.end_date,u.name as assign_to,u2.name as issued_by,t.location
        from tasks t
        left join users u on t.user_assign_id = u.id
        left join users u2 on t.user_issued_id = u2.id
        where t.project_id=%s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data task","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data task","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/issues/done/{id}")
def getAllIsseuesDone(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql_command="""
        select i.project_id, i.name, i.id,i.globalid, i.expressid, i.location, i.description, i.photo, i.date_issued, i.closed_date, u.name as user_assign_to, u2.name as user_issued_by
        from issues i
        left join users u on u.id = i.user_assign_id
        left join users u2 on u2.id = i.user_issued_id
        where i.status ='done' and i.project_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data issue selesai","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data issue selesai","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/issues/all/{id}")
def getAllIsseuesDone(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql_command="""
        select i.project_id, i.status, i.name, i.id,i.globalid, i.expressid, i.location, i.description, i.photo, i.date_issued, i.closed_date, u.name as user_assign_to, u2.name as user_issued_by
        from issues i
        left join users u on u.id = i.user_assign_id
        left join users u2 on u2.id = i.user_issued_id
        where i.project_id = %s
        """
        cursor.execute(sql_command,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data issue","result":record};
        else:
            response = {"status":"nok","message":"gagal dapat data issue","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/polygon/{id}")
def getDataPolygon(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
        select * from polygon p where project_id =%s
        """
        cursor.execute(sql,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data polygon","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data polygon","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/task/activities/{id}")
def getDataTaskActivity(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select ta.id, ta.photo, ta.date_activity, ta.activity, u.name, u.photo as photo_user from task_activities ta
            left join tasks t on ta.task_id = t.id
            left join users u on ta.user_task_activities_id = u.id
            where t.expressid = %s
            """
        cursor.execute(sql,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data task activity","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data task activity","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/issue/activities/{id}")
def getDataIssueActivity(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select ia.id, ia.date_activity, ia.photo, ia.activity, u.name, u.photo as photo_user from issue_activities ia
            left join issues i   on ia.issue_id = i.id
            left join users u on ia.user_issue_activities_id = u.id
            where i.expressid = %s
            """
        cursor.execute(sql,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data issue activity","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data issue activity","result":""}
        return response

    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/wall/all")
def getWallType() :
    all_wall =[]
    for wall_type in ifc_file.by_type("IfcWallType"):
        all_wall.append(wall_type)
        response = {"status":"ok","message":"berhasil dapat data IFCWall","result":all_wall}
        return response

@app.get("/door/all")
def getDoorAllOccur() :
    all_doors = []
    try :
        for door_type in ifc_file.by_type("IfcDoorType"):
            doorTypeName = door_type.Name
            doors = ifcopenshell.util.element.get_types(door_type)
            lenDoor = len(doors)
            for door in doors:
                doorName = door.attribute_name
                doorData = {"type_name": doorTypeName, "quantity": lenDoor, "door_name": doorName}
                all_doors.append(doorData)
                return {"status":"ok","message":"berhasil dapat data IFCDoor","result":doorData}
    except Exception as e:
        return {"status":"nok","message":"gagal dapat data IFCDoor","result":e}

@app.get("/wall/type")
def getTypeWall() :
    all_wall_type = []
    wall = ifc_file.by_type("IfcWall")[0]
    wall_type = ifcopenshell.util.element.get_type(wall)
    all_wall_type.append(wall_type)
    return {"status":"ok","message":"berhasil dapat data IFCWall","result":all_wall_type}

@app.get("/document/all/{id}")
def getDocumentAll(id: str) :
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql ="""
            select u2.name as user_upload, td.url, u.photo, md.id,md.date_modified_document, md.modified_document, u.name as user, td.name as document, p.name as project from modified_documents md
            left join track_documents td  on td.id = md.track_document_id
            left join users u on u.id = md.user_modified_id
            left join projects p on p.id = td.project_id
            left join users u2 on u2.id = td.upload_user_id
            where td.project_id = %s
            """
        cursor.execute(sql,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data modified document","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data modified document","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/document/profile/{id}")
def getDocProfile(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select td.url, td.id, td.name, td.description, td.date_document, u.name as user, u.photo from track_documents td
            left join users u on u.id = td.upload_user_id
            left join projects p on p.id = td.project_id
            where td.project_id = %s
            """
        cursor.execute(sql,(id,))
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data profile document","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data profile document","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection

@app.get("/library")
def getLibrary():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select l.id, l.name, l.date_library, l.description, l.url, u.name as user, u.photo from library l
            left join users u on u.id = l.upload_library_user_id
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data library","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data library","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 


@app.get("/project/list")
def getProjectList():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select p.id,p.name,td.url, u.name as user, u.photo, p.start_date, p.end_date, p.value, p.description from projects p
            left join track_documents td on td.project_id = p.id
            left join users u on u.id = td.upload_user_id
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data project","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data project","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.get("/rab/product")
def getProductList():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select p.id, p.product_name, pt.type_name, pc.category_name,u.uom, p.tariff from products p
            left join product_category pc on pc.id = p.product_category_id
            left join product_type pt on pt.id = p.product_type_id 
            left join uom u on u.id = p.uom_id
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data product","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data product","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.get("/rab/{id}")
def getProduct(id: str):
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select p.id, p.product_name, pt.type_name, pc.category_name,u.uom, p.tariff from products p
            left join product_category pc on pc.id = p.product_category_id
            left join product_type pt on pt.id = p.product_type_id 
            left join uom u on u.id = p.uom_id
            where p.id=%s
            """
        cursor.execute(sql, (id,))
        record = cursor.fetchone()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data product","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data product","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.get("/rab/product/type")
def getProductType():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select pt.id, pt.type_name from product_type pt
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data product_type","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data product_type","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.get("/rab/product/category")
def getProductCategory():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select pc.id, pc.category_name  from product_category pc
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data product category","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data product category","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.get("/rab/product/uom")
def getProductUom():
    try:
        connection = get_db_connection()  # atau koneksi dari pool
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        sql="""
            select u.id, u.uom  from uom u
            """
        cursor.execute(sql)
        record = cursor.fetchall()
        if (record):
            response = {"status":"ok","message":"berhasil dapat data product uom","result":record}
        else:
            response = {"status":"nok","message":"gagal dapat data product uom","result":""}
        return response
    except psycopg2.Error as e:
        connection.rollback()  # penting! reset transaksi
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)  # karena kamu pakai connection 

@app.on_event("shutdown")
def shutdown_event():
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed.")

@app.delete("/delete-file/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "success", "message": f"{filename} deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
