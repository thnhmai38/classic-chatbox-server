<h1 align="center">classic-chatbox-server</h1>

<p align="center">Một chatbox đơn giản sử dụng WebSocket. Là một phiên bản nâng cấp của <a href="https://github.com/thanhgaming5550/classic-chatbox-server/tree/api"> Bản API </a> để cập nhật theo thời gian thực.</p>
<p align="center">Đây là Server của <b>classic-chatbox</b>. Tạm thời chưa có Client thích hợp.

<!-- Click vào <a href="https://github.com/thanhgaming5550/classic-chatbox-client">đây</a> để chuyển sang Client</p> -->
#### Có gì mới?
Ở phiên bản v2, mình (thực ra là chờ teacher dạy WebSocket) đã sử dụng WebSocket để thay thế cho API ở v1, giúp cập nhật theo thời gian thực với lượng tài nguyên sử dụng rất ít. Cũng qua đó mình cũng thêm vào **"Hệ thống Chống lặp Biệt danh"** (**ARNS**: **Anti-Repeat Nickname System**) *(đặt tên cho nó sang)*, tức là mỗi kết nối chỉ được sử dụng 1 biệt danh (có thể thay đổi) và không được lặp với biệt danh của người trước đó. 

Ngoài ra còn có:
- "**get**" ngoài cung cấp tin nhắn ra thì nó sẽ cung cấp cho Client Biệt danh những người đã kết nối tới Server.

#### Yêu cầu:
- <a href="https://pypi.org/project/Flask/">Flask</a>
- <a href="https://pypi.org/project/flask-sock/">Flask-Sock</a>
- <a href="https://www.python.org/">Python 3</a>

#### Hướng dẫn sử dụng:
  Chạy file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/main/index.py">`index.py`</a> (`python index.py`)

#### Tài liệu
Đang trong quá trình code rất đau đầu và rối nơ-ron thần kinh nên sẽ cập nhật sau nha :3

#### Lưu trữ:
  Lịch sử chat sẽ được lưu trong file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/main/data.json">`data.json`</a> để lưu trữ và thực hiện các hành động liên quan. Rất cổ điển.
#### Thông tin khác:
- **#study**: Đây là repo được tạo ra nhằm mục đích để hoàn thành Bài tập về nhà hoặc tựa tựa thế.

Đây là dự án rất tâm huyết của mình :v Mong mọi người thích nó :3