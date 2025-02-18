from ga_parser.main import start_parser

if __name__ == '__main__':
    start_parser(
        table_path='./00_base/Шампуни.xlsx',
        ws_title='Средства',
        image_dir_path='00_base/products/00_img/',
        base_delay=10,
    )
