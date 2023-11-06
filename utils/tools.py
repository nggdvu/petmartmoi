from enum import Enum
class MessageType(Enum):
    LOADING = 'Đang lấy dữ liệu'
    SUCCESS = 'Thành công'
    ERROR = 'Lỗi'

def format_currency(value):
    return "{:,.0f} VND".format(value).replace(',', '.')