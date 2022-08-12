<h1 align="center">classic-chatbox-server</h1>

<p align="center">Một chatbox đơn giản sử dụng WebSocket. Là một phiên bản nâng cấp của <a href="https://github.com/thanhgaming5550/classic-chatbox-server/tree/api"> Bản API </a> để cập nhật theo thời gian thực.</p>
<p align="center">Đây là Server của <b>classic-chatbox</b>. Tạm thời chưa có Client thích hợp.

<!-- Click vào <a href="https://github.com/thanhgaming5550/classic-chatbox-client">đây</a> để chuyển sang Client</p> -->

#### Yêu cầu:
- <a href="https://pypi.org/project/Flask/">Flask</a>
- <a href="https://pypi.org/project/flask-sock/">Flask-Sock</a>
- <a href="https://www.python.org/">Python 3</a>

#### Hướng dẫn sử dụng:
  Chạy file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/main/index.py">`index.py`</a> (`python index.py`)

#### Đầu vào và đầu ra:
Kết nối và gửi tin nhắn:
  - Gửi: `{"type":"send", "data":{"name":"Tên_Người_Gửi", "content":"Nội_dung"}}`
    - Thành công: 
      - `{"type":"send", "status": true, "timestamp":"Xâu_thời_gian"}` cho client đã gửi tin
      - `{"name":"Tên_Người_Gửi", "content":"Nội_dung", "timestamp":"Xâu_thời_gian}` cho các client khác

      <b>CHÚ Ý: `Tên_Người_Gửi` từ 1 đến 100 ký tự, `Nội_dung` từ 1 đến 4000 ký tự</b>
    - Thất bại:
      - `{"type":"send", "status": false}` cho client đã gửi tin
  - Lấy: `{"type":"get"}`
    - Thành công: 
      - `{"type":"get", "status": true, "data":[Tất cả tin nhắn]}` cho client đã gửi tin
        - Đại diện 1 object trong `"data"`: 
          `{"name":"Tên_Người_Gửi", "content":"Nội_dung", "timestamp":"Xâu_thời_gian"}`
    - Thất bại: 
      `{"type":"get", "status": false}`cho client đã gửi tin

Nếu gửi tin không đúng định dạng, tự động ngắt kết nối WebSocket.

#### Lưu trữ:
  Lịch sử chat sẽ được lưu trong file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/main/data.json">`data.json`</a> để lưu trữ và thực hiện các hành động liên quan. Rất cổ điển.
#### Thông tin khác:
- **#study**: Đây là repo được tạo ra nhằm mục đích để hoàn thành Bài tập về nhà hoặc tựa tựa thế.
