<h1 align="center">classic-chatbox-server</h1>

<p align="center">Một chatbox đơn giản sử dụng WebSocket. Là một phiên bản nâng cấp của <a href="https://github.com/thanhgaming5550/classic-chatbox-server/tree/v1"> Bản API </a> để cập nhật theo thời gian thực.</p>
<p align="center">Đây là Server của <b>classic-chatbox</b>. Click vào <a href="https://github.com/thanhgaming5550/classic-chatbox-client/tree/v2">đây</a> để chuyển sang bản Client.

<!-- Click vào <a href="https://github.com/thanhgaming5550/classic-chatbox-client">đây</a> để chuyển sang Client</p> -->
### Có gì mới?
Ở phiên bản v2, mình (thực ra là chờ teacher dạy WebSocket) đã sử dụng WebSocket để thay thế cho API ở v1, giúp cập nhật theo thời gian thực với lượng tài nguyên sử dụng rất ít. Cũng qua đó mình cũng thêm vào **"Hệ thống Chống lặp Biệt danh"** (**ARNS**: **Anti-Repeat Nickname System**) *(đặt tên cho nó sang)*, tức là mỗi kết nối chỉ được sử dụng 1 biệt danh (có thể thay đổi) và không được lặp với biệt danh hiện tại của người trước đó. 

Ngoài ra còn có:
- "**get**" ngoài cung cấp tin nhắn ra thì nó sẽ cung cấp cho Client cái Biệt danh của những người đã kết nối tới Server.
- Để sử dụng các tính năng trên Server (trừ "**register**"), bạn sẽ phải Đăng ký cho mình một cái Biệt danh trước ("**register**"), hoặc là Server chỉ đưa cho bạn đúng mỗi cái nịt `status: false` cho bạn muốn làm gì thì làm.
- Thông báo cho bạn nguyên nhân gây lỗi yêu cầu của bạn ("**reason**" và "**error**")
- Log tại Console đã được phân rõ ràng
- ...

và nhiều tính năng mới mà cơ bản mình lười nên không ghi, với lại không nhớ mình đã update những gì

### Yêu cầu:
- <a href="https://pypi.org/project/Flask/">Flask</a>
- <a href="https://pypi.org/project/flask-sock/">Flask-Sock</a>
- <a href="https://www.python.org/">Python 3</a>

### Hướng dẫn sử dụng:
  Chạy file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/v2/index.py">`index.py`</a> (`python index.py`)

### Tài liệu
Tóm gọn lại là thế này:

**```Mỗi Client sau khi kết nối phải gửi lệnh (tin) đăng ký để đăng ký cho mình 1 biệt danh, có thể thay đổi nhưng phải khác với các biệt danh hiện tại của người khác, bằng không thì các chức năng chính (trừ chức năng đăng ký) sẽ không được thực thi. Biệt danh giống như tên của Client, dùng làm tên để đại diện trò chuyện với các Client khác.```**

**Khi Client gửi cho Server 1 message:**
- `{"data":"name", "name":"`<i>`Tên_người_dùng`</i>`"}`
  - TH1: Chưa đăng ký
    - Server sẽ gửi cho Client đó:
        - **`{"type":"name", "action":"register", "name":"`*`Tên_Người_dùng`*`", "status":true, "timestamp":"`*`Thời_gian`*`"}` và đăng ký Biệt danh *`Tên_người_dùng`* cho Client (vào lúc *`Thời_gian`*) (Thành công)**
        - `{"type":"name", "action":"register", "name":"`*`Tên_Người_dùng`*`", "status":false, "reason":"NameAlreadyUsed"}` nếu Biệt danh đã *`Tên_Người_dùng`* bị ai đó sử dụng/đăng ký (Thất bại)
        - `{"type":"name", "action":"register", "name":"`*`Tên_Người_dùng`*`", "status":false, "reason":"WrongFormatName"}` nếu Biệt danh *`Tên_Người_dùng`* không đúng quy chuẩn (Thất bại)
        - `{"type":"name", "action":"register", "name":"`*`Tên_Người_dùng`*`", "status":false, "reason":"ErrorWhenRegister", "error":"`*`Lỗi_Trên_Server`*`"}` nếu đã xảy ra lỗi *`Lỗi_Trên_Server`* khi thực hiện đăng ký biệt danh *`Tên_Người_dùng`* cho Client trên Server (Thất bại)
    - Server sẽ gửi cho các Client khác:
      - **`{"type": "receive", "datatype": "register", "name":"`*`Tên_người_dùng`*`", "timestamp":"`*`Thời_gian`*`"}` nếu việc đăng ký Biệt danh *`Tên_người_dùng`* cho Client trên thành công vào lúc *`Thời_gian`*`**
  - TH2: Đã đăng ký
    - Server sẽ gửi cho Client đó:
        - **`{"type":"name", "action":"change", "oldname":"`*`Tên_Người_dùng_cũ`*`", "newname":"`*`Tên_Người_dùng_mới`*`",  "status":true, "timestamp":"`*`Thời_gian`*`"` và đổi Biệt danh cho Client từ *`Tên_Người_dùng_cũ`* thành *`Tên_Người_dùng_mới`* vào lúc *`Thời_gian`* (Thành công)**
        - `{"type":"name", "action":"change", "oldname":"`*`Tên_Người_dùng_cũ`*`", "newname":"`*`Tên_Người_dùng_mới`*`",  "status":false, "reason":"NameAlreadyUsed"}` nếu không thể đổi Biệt danh cho Client từ *`Tên_Người_dùng_cũ`* thành *`Tên_Người_dùng_mới`* do Biệt danh *`Tên_Người_dùng_mới`* đã được sử dụng/đăng ký (Thất bại)
        - `{"type":"name", "action":"change", "oldname":"`*`Tên_Người_dùng_cũ`*`", "newname":"`*`Tên_Người_dùng_mới`*`",  "status":false, "reason":"WrongFormatName"}` nếu không thể đổi Biệt danh cho Client từ *`Tên_Người_dùng_cũ`* thành *`Tên_Người_dùng_mới`* do Biệt danh *`Tên_Người_dùng_mới`* không đúng quy chuẩn (Thất bại)
        - `{"type":"name", "action":"change", "oldname":"`*`Tên_Người_dùng_cũ`*`", "newname":"`*`Tên_Người_dùng_mới`*`",  "status":false, "reason":"ErrorWhenChange", "error":"`*`Lỗi_Trên_Server`*`"}` nếu đã xảy ra lỗi *`Lỗi_Trên_Server`* khi thực hiện thao tác đổi Biệt danh cho Client từ *`Tên_Người_dùng_cũ`* thành *`Tên_Người_dùng_mới`* trên Server (Thất bại)
    - Server sẽ gửi cho các Client khác:
      - **`{"type": "receive", "datatype": "change", "oldname":"`*`Tên_người_dùng_cũ`*`", "newname":"`*`Tên_người_dùng_mới`*`", "timestamp":"`*`Thời_gian`*`"}` nếu việc đổi Biệt danh cho Client trên từ *`Tên_Người_dùng_cũ`* thành *`Tên_Người_dùng_mới`* vào lúc *`Thời_gian`* thành công**
- `{"data":"get"}`
    - Server sẽ gửi cho Client đó:
      - **`{"type":"get", "status":true, "name":"`*`Tên_Người_dùng`*`", "timestamp":"`*`Thời_gian`*`", "data": {"message": `*`[Dãy_Tin_nhắn]`*`, "online":`*`[Dãy_Người_dùng]`*`}}` cho Client mình (Biệt danh: *`Tên_Người_dùng`*), lấy dữ liệu vào lúc *`Thời_gian`* (Thành công)**
        - ***`[Dãy_Tin_nhắn]`*** là tập hợp tất cả **tin nhắn (Object)**, sắp xếp theo Cũ đến mới nhất. Đây là đại diện 1 tin nhắn có nội dung *`Nội_dung`* được gửi bởi *`Tên_Người_dùng`* lúc *`Thời_gian`*:
          - `{"name":"`*`Tên_Người_dùng`*`", "content":"`*`Nội_dung`*`", "timestamp":"`*`Thời_gian`*`"}`
        - `***[Dãy_Người_dùng]***` là tập hợp tất cả **xâu** là những biệt danh đang được sử dụng/đăng ký (Kể cả của bạn).
      - `{"type":"get", "status":false, "reason":"UnknownRegister"}` nếu Client chưa đăng ký biệt danh (Thất bại)
      - `{"type":"get", "name":"`*`Tên_Người_dùng`*`", "status":false, "reason":"ErrorWhenGet", "error":"`*`Lỗi_trên_Server`*`"}` nếu đã xảy ra lỗi *`Lỗi_Trên_Server`* khi thực hiện thao tác trên Server cho Client đó (biệt danh *`Tên_Người_dùng`*) (Thất bại)
- `{"data":"send", "content":"`*`Nội_dung`*`"}`
  - Server sẽ gửi cho Client đó:
    - **`{"type":"send", "name":"`*`Tên_Người_dùng`*`", "content":"`*`Nội_dung`*`", "status":true, "timestamp":"`*`Thời_gian`*`"}` và lưu tin nhắn lại, gửi bởi Client đó (biệt danh: *`Tên_Người_dùng`*) với nội dung *`Nội_dung`* vào lúc *`Thời_gian`* (Thành công)**
    - `{"type":"send", "status":false, "reason":"UnknownRegister"}` nếu Client đó chưa đăng ký biệt danh (Thất bại)
    - `{"type":"send", "username":"`*`Tên_Người_dùng`*`", "content":"`*`Nội_dung`*`", "status":false, "reason":"WrongFormatContent"}` nếu *`Nội_dung`* không đúng quy chuẩn (Gửi tin nhắn cho Client đó (Biệt danh: *`Tên_Người_dùng`*)) (Thất bại)
    - `{"type":"send", "username":"`*`Tên_Người_dùng`*`", "content":"`*`Nội_dung`*`", "status":false, "reason":"ErrorWhenSend", "error":"`*`Lỗi_trên_Server`*`"}` nếu đã xảy ra lỗi *`Lỗi_Trên_Server`* khi thực hiện thao tác gửi tin nhắn cho Client đó (Biệt danh: *`Tên_Người_dùng`*) với nội dung *`Nội_dung`* trên Server (Thất bại)
  - Server sẽ gửi cho các Client khác:
    - **`{"type":"receive", "datatype":"message", "name":"`*`Tên_người_dùng`*`", "content":"`*`Nội_dung`*`", "timestamp":"Thời_gian"}` nếu việc gửi tin nhắn có nội dung *`Nội_dung`* cho Client trên (Biệt danh: *`Tên_người_dùng`*) thành công**


**Tại sự kiện:**
  - Có 1 client đã đăng ký biệt danh *`Tên_người_dùng`* Ngắt kết nối khỏi Server vào lúc *`Thời_gian`*:
    - Server sẽ gửi cho các Client khác: `{"type":"receive", "datatype":"leave", "name":"`*`Tên_người_dùng`*`", "timestamp":"`*`Thời_gian`*`"}` và xóa biệt danh *`Tên_người_dùng`*  khỏi danh sách biệt danh đã đăng ký
  - Client gửi cho Server tin nhắn không thuộc dạng JSON:
    - Server sẽ gửi cho Client đó: `{"status":false, "reason":"WrongFormatJSON"}`
  - Client gửi cho Server một trong 2 *`Loại_Yêu_cầu`* trên (*`name`* hoặc *`send`*) nhưng không có key *`Key_cần`* được yêu cầu
    - Server sẽ gửi cho Client đó: `{"type":"`*`Loại_Yêu_cầu`*`", "status":false, "reason":"NotEnoughKey", "need":"`*`Key_cần`*`}`
  - Client gửi cho Server tin nhắn không thuộc một trong 3 Loại yêu cầu trên (*`name`*, *`send`*, *`get`*):
    - Server sẽ gửi cho Client đó: `{"type":null, "status":false, "reason":"UnknownType"}`

**Server sẽ kiểm tra Client đã Ngắt kết nối chưa** mỗi 5s bằng cách cứ mối 5s sẽ gửi cho các Client tin nhắn `{"type":"ping", "timeout":"`*`Delay_mỗi_lần_ping`*`"}`. Phải kiểm tra như vậy vì <a href="https://github.com/thanhgaming5550/classic-chatbox-server/issues/1">#1</a>. *`Delay_mỗi_lần_ping`* hiện tại là số 5.

**Quy chuẩn:**
  - *``Tên_Người_dùng``*, *`Tên_Người_dùng_mới`* có ít nhất 1 ký tự và nhiều nhất 100 ký tự
  - *`Nội_dung`* có ít nhất 1 ký tự và nhiều nhất 100 ký tự
  - *`Thời_gian`* là một **xâu** có dạng `{`*`Ngày`*`}/{`*`Tháng`*`}/{`*`Năm`*`} {`*`Giờ`*`}/{`*`Phút`*`}{`*`Giây`*`}`

### Lưu trữ:
  Lịch sử chat sẽ được lưu trong file <a href="https://github.com/thanhgaming5550/classic-chatbox-server/blob/v2/data.json">`data.json`</a> để lưu trữ và thực hiện các hành động liên quan. Rất cổ điển.
### Thông tin khác:
- **#study**: Đây là repo được tạo ra nhằm mục đích để hoàn thành Bài tập về nhà hoặc tựa tựa thế.

Đây là dự án rất tâm huyết của mình :v Mong mọi người thích nó :3
