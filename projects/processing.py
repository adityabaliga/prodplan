from database import CursorFromConnectionFromPool


class Processing:
    def __init__(self, order_id, smpl_no, operation, processing_date, start_time, end_time, setting_start_time,
                 setting_end_time, processing_time, setting_time, no_of_qc, no_of_helpers, names_of_qc,
                 names_of_helpers, name_of_packer, stage_no):
        self.order_id = order_id
        self.smpl_no = smpl_no
        self.operation = operation
        self.processing_date = processing_date
        self.start_time = start_time
        self.end_time = end_time
        self.setting_start_time = setting_start_time
        self.setting_end_time = setting_end_time
        self.processing_time = processing_time
        self.setting_time = setting_time
        self.no_of_qc = no_of_qc
        self.no_of_helpers = no_of_helpers
        self.names_of_qc = names_of_qc
        self.names_of_helpers = names_of_helpers
        self.name_of_packer = name_of_packer
        self.stage_no = stage_no

    @classmethod
    def load_from_db(cls, smpl_no, operation):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from processing where smpl_no = %s and operation = %s', (smpl_no, operation))
            user_data = cursor.fetchall()
            processing_lst = []
            for lst in user_data:
                processing = Processing(smpl_no=lst[2],order_id=lst[1],operation=lst[3],processing_date=lst[4],start_time=lst[5],
                                        end_time=lst[6],processing_time=lst[7],setting_start_time=lst[8],setting_end_time=lst[9],
                                        setting_time=lst[10],no_of_qc=lst[11],no_of_helpers=lst[12],names_of_qc=lst[13],
                                        names_of_helpers=lst[14],name_of_packer=lst[14],stage_no=lst[15])
                processing_lst.append(processing)
        return processing_lst

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("insert into processing (order_id, smpl_no, operation, processing_date, start_time, "
                           "end_time, setting_start_time, setting_end_time, production_time, setting_time, no_of_qc, "
                           "no_of_helpers, names_of_qc, names_of_helpers,name_of_packer,stage_no) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,"
                           "%s,%s, %s, %s, %s, %s, %s)",
                           (self.order_id, self.smpl_no, self.operation, self.processing_date,
                            self.start_time, self.end_time, self.setting_start_time,
                            self.setting_end_time, self.processing_time, self.setting_time,
                            self.no_of_qc, self.no_of_helpers, self.names_of_qc,
                            self.names_of_helpers, self.name_of_packer, self.stage_no))

            cursor.execute("select processing_id from processing where oid= %s", (cursor.lastrowid,))
            data = cursor.fetchone()
            return data[0]

    @classmethod
    def load_history(cls, smpl_no):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from processing where smpl_no = %s', (smpl_no, ))
            user_data = cursor.fetchall()
            processing_lst = []
            for lst in user_data:
                processing = Processing(smpl_no=lst[2], order_id=lst[1], operation=lst[3], processing_date=lst[4],
                                        start_time=lst[5],
                                        end_time=lst[6], processing_time=lst[7], setting_start_time=lst[8],
                                        setting_end_time=lst[9],
                                        setting_time=lst[10], no_of_qc=lst[11], no_of_helpers=lst[12],
                                        names_of_qc=lst[13],
                                        names_of_helpers=lst[14], name_of_packer=lst[14], stage_no=lst[15])
                processing_lst.append(processing)
        return processing_lst