from database import CursorFromConnectionFromPool
from decimal import *


class CurrentStock:
    def __init__(self, smpl_no, customer, weight, numbers, thickness, width, length, status, grade, unit):
        self.smpl_no = smpl_no
        self.customer = customer
        self.weight = weight
        self.numbers = numbers
        self.thickness = thickness
        self.width = width
        self.length = length
        self.status = status
        self.grade = grade
        self.unit = unit

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into current_stock (smpl_no,weight,numbers,width,length,status,customer,thickness"
                           ",grade, unit) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.smpl_no, self.weight, self.numbers, self.width, self.length, self.status, self.customer,
                           self.thickness, self.grade, self.unit))

    def update_status(self, status):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("update current_stock set status = %s where smpl_no = %s and width = %s and length = %s",
                           (status, self.smpl_no, self.width, self.length))

    @classmethod
    def update_status_cls(cls,cs_id,status):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("update current_stock set status = %s where cs_id = %s",
                           (status, cs_id))

    @classmethod
    def smpl_list_for_modify_order(cls):
        user_data = []
        cs_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from current_stock where status= 'Order' order by smpl_no asc")
            user_data = cursor.fetchall()

            if user_data:
                for lst in user_data:
                    cs = CurrentStock(smpl_no=lst[1], weight=Decimal(lst[2]), numbers=int(lst[3]),
                                      width=Decimal(lst[4]),
                                      length=Decimal(lst[5]), status=lst[6], customer=lst[7], thickness=Decimal(lst[8]),
                                      grade=lst[9], unit=lst[10])
                    cs_lst.append(cs)

                return cs_lst
            else:
                return None


    @classmethod
    def smpl_list_for_place_order(cls, operation, unit):
        user_data = []
        cs_lst = []
        cs_id_lst = []
        if operation == "CTL" or operation == "Narrow CTL" or operation == "Slitting" or operation == "Mini Slitting":
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock where (status = 'RM' or status = 'HC' or status= 'WIP') and "
                               "length = 0 and unit = %s order by smpl_no asc", (str(unit),))
                user_data = cursor.fetchall()

        if operation == "Reshearing":
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock where (status = 'RM' or status = 'HC' or status= 'WIP') and "
                               "length > 0  order by smpl_no asc")
                user_data = cursor.fetchall()

        if user_data:
            for lst in user_data:
                cs = CurrentStock(smpl_no=lst[1], weight=Decimal(lst[2]), numbers=int(lst[3]), width=Decimal(lst[4]),
                                  length=Decimal(lst[5]), status=lst[6], customer=lst[7], thickness=Decimal(lst[8]),
                                  grade=lst[9], unit=lst[10])
                cs_lst.append(cs)

                cs_id_lst.append(lst[0])
            return zip(cs_id_lst, cs_lst)
        else:
            return None

    @classmethod
    def load_smpl_by_smplno(cls,smpl_no):
        user_data = []
        cs_lst = []
        cs_id_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from current_stock where smpl_no = %s",(smpl_no,))
            user_data = cursor.fetchall()

            for lst in user_data:
                cs = CurrentStock(smpl_no=lst[1], weight=Decimal(lst[2]), numbers=int(lst[3]), width=Decimal(lst[4]),
                                  length=Decimal(lst[5]), status=lst[6], customer=lst[7], thickness=Decimal(lst[8]),
                                  grade=lst[9], unit=lst[10])
                cs_lst.append(cs)
                cs_id_lst.append(lst[0])

            return zip(cs_id_lst, cs_lst)


    @classmethod
    def load_smpl_by_id(cls, cs_id):
        user_data = []
        cs_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from current_stock where cs_id = %s", (cs_id,))
            user_data = cursor.fetchone()

            if user_data:
                cs = CurrentStock(smpl_no=user_data[1], weight=Decimal(user_data[2]), numbers=int(user_data[3]),
                                  width=Decimal(user_data[4]), length=Decimal(user_data[5]), status=user_data[6],
                                  customer=user_data[7], thickness=Decimal(user_data[8]), grade=user_data[9],
                                  unit=user_data[10])

                return cs
            else:
                return None

    @classmethod
    def change_wt(cls, smpl_no, width, length, processed_wt, actual_no_of_pieces, sign):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select weight, numbers, unit from current_stock where smpl_no = %s and width = %s and length = %s",(smpl_no,width,length))
            user_data = cursor.fetchone()
            if user_data:
                weight = Decimal(user_data[0])
                numbers = Decimal(user_data[1])
                if sign == "minus":
                    new_weight = weight - Decimal(processed_wt)
                    new_weight = round(new_weight,3)
                    if Decimal(length) > 0:
                        new_numbers = numbers - Decimal(actual_no_of_pieces)
                    else:
                        new_numbers = numbers
                if sign == "plus":
                    new_weight = weight + Decimal(processed_wt)
                    new_weight = round(new_weight, 3)
                    if Decimal(length) > 0:
                        new_numbers = numbers + Decimal(actual_no_of_pieces)
                    else:
                        new_numbers = numbers
                if new_weight < 0.15:
                    cursor.execute("delete from current_stock where smpl_no = %s and width = %s and length = %s",(smpl_no,width,length))
                    return "complete"
                else:
                    cursor.execute("update current_stock set weight = %s, numbers = %s where smpl_no = %s and width = %s and length = %s",(new_weight,new_numbers,smpl_no,width,length))
                    return "continue"
            else:
                return "insert"


    @classmethod
    def delete_record(cls, cs_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('delete from current_stock where cs_id = %s',(cs_id,))

    @classmethod
    def get_stock(cls, stock_type):
        user_data = []
        cs_lst=[]
        cs_id_lst =[]

        if stock_type == 'All':
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock")
                user_data = cursor.fetchall()
        else:
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock where status = %s",(stock_type,))
                user_data = cursor.fetchall()

        for lst in user_data:
            cs = CurrentStock(smpl_no=lst[1],weight = Decimal(lst[2]),numbers=int(lst[3]),width=Decimal(lst[4]),
                              length=Decimal(lst[5]),status=lst[6],customer=lst[7], thickness=Decimal(lst[8]),grade=lst[9],unit=lst[10])
            cs_lst.append(cs)
            cs_id_lst.append(lst[0])
        return zip(cs_id_lst,cs_lst)

    @classmethod
    def rm_list_for_hold(cls):
        user_data = []
        cs_lst = []
        cs_id_lst =[]
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from current_stock where status = 'RM'")
            user_data = cursor.fetchall()
        for lst in user_data:
            cs = CurrentStock(smpl_no=lst[1],weight = Decimal(lst[2]),numbers=int(lst[3]),width=Decimal(lst[4]),
                              length=Decimal(lst[5]),status=lst[6],customer=lst[7], thickness=Decimal(lst[8]),grade=lst[9],unit=lst[10])
            cs_lst.append(cs)
            cs_id_lst.append(lst[0])
        return zip(cs_id_lst,cs_lst)

    @classmethod
    def rm_list_for_unhold(cls):
        user_data = []
        cs_lst = []
        cs_id_lst = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from current_stock where status = 'RM - On Hold'")
            user_data = cursor.fetchall()
        for lst in user_data:
            cs = CurrentStock(smpl_no=lst[1], weight=Decimal(lst[2]), numbers=int(lst[3]), width=Decimal(lst[4]),
                              length=Decimal(lst[5]), status=lst[6], customer=lst[7], thickness=Decimal(lst[8]),
                              grade=lst[9], unit=lst[10])
            cs_lst.append(cs)
            cs_id_lst.append(lst[0])
        return zip(cs_id_lst,cs_lst)

    @classmethod
    def transfer_material_cls(cls,cs_id, unit):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("update current_stock set unit = %s where cs_id = %s",
                           (unit, cs_id))

    @classmethod
    def customer_list_for_dispatch(cls):
        customer_lst = []
        user_data = []
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select distinct customer from current_stock  order by customer asc")
            user_data = cursor.fetchall()
        for lst in user_data:
            customer_lst.append(lst[0])
        return customer_lst


    @classmethod
    def get_stock_by_customer(cls, customer, display_type):
        user_data = []
        cs_lst = []
        cs_id_lst = []
        if display_type == 'FG':
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock where customer=%s and status = 'FG'",(customer,))
                user_data = cursor.fetchall()
        if display_type == 'FGandRM':
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute("select * from current_stock where customer=%s and (status = 'FG' or status = 'RM')", (customer,))
                user_data = cursor.fetchall()
        for lst in user_data:
            cs = CurrentStock(smpl_no=lst[1],weight = Decimal(lst[2]),numbers=int(lst[3]),width=Decimal(lst[4]),
                              length=Decimal(lst[5]),status=lst[6],customer=lst[7], thickness=Decimal(lst[8]),grade=lst[9],unit=lst[10])
            cs_lst.append(cs)
            cs_id_lst.append(lst[0])

        return zip(cs_id_lst, cs_lst)



