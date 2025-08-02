from ga_parser.clean_product_composition.main import process_excel_and_fill_composition

if __name__ == '__main__':
    process_excel_and_fill_composition(
        file_path_tools='00_base/Средства_АКТУАЛЬНАЯ.xlsx',
        sheet_name='Средства',
        source_column_name='Состав',
        target_column_name='Элементы состава списком',
        target_len_column_name='Количество элементов состава',
    )
