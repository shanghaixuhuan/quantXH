from QUANTAXIS.QASU.main import (QA_SU_save_index_day, QA_SU_save_index_list,
                                 QA_SU_save_stock_block, QA_SU_save_stock_day,
                                 QA_SU_save_stock_info, QA_SU_save_stock_list,
                                 QA_SU_save_stock_xdxr)

if __name__ == "__main__":
    QA_SU_save_index_day('tdx')
    QA_SU_save_index_list('tdx')
    QA_SU_save_stock_block('tdx')
    QA_SU_save_stock_day('tdx')
    QA_SU_save_stock_info('tdx')
    QA_SU_save_stock_list('tdx')
    QA_SU_save_stock_xdxr('tdx')