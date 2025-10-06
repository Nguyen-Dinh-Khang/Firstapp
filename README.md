- Dự án này dùng nhiều công cụ bên ngoài (cần tải về):
    + python-decouple==3.8
    + python-dotenv==1.1.1
    + redis==6.4.0
    + fastapi==0.118.0 (chỉ tải về để học cách dùng chứ chưa có làm gì liên quan đến nó)
    + djangorestframework==3.16.1
    + daphne==4.2.1
    + Django==5.2.5
    + channels==4.3.1
    + channels_redis==4.3.0
      
- Firstapp: là app giao diện chính kết nối đến hai app khác là blog và foodapp
  
- blog:
  Gồm 3 trang:
    + Page:
        > Dùng để tra bài viết và cả tác giả (giống youtube nhưng kém hiện đại hơn)
        > Khi tra tác giả thì sẽ hiện lên cái icon dẫn thẳng tới trang cá nhân (gồm tất cả bài đăng) của tác giả đó
        > Bên trong trang tác giả đó có nút chat kế bên để kích hoạt chat realtime cùng tác giả đó
    + Create:
        > Dùng khi muốn đăng bài
    + My page:
        > Trang cá nhân của riêng user sẽ hiện toàn bộ bài viết và nó nút 'update' để sửa bài đăng nếu cần

- foodapp:
  Gồm 4 trang:
    + Add new dish:
        > Dùng để thêm món ăn vào danh sách của riêng mình (thêm vào database)
        > Chia món ăn làm hai nhóm lớn là ăn chay và không ăn chay
        > Nếu các nguyện liệu của món vừa thêm không có nguyên liệu thuộc nhóm thịt thì sẽ được thêm vào database món chay và cả món không chay để tiện cho bước tiếp theo
        > Các nguyên liệu của món này được kiểm tra có kị nhau hay không trước khi được up lên database, sự kị này phụ thuộc vào database chưa thông tin kị
    + Create random:
        > Tạo một danh sách món ăn random cho những người không biết bữa nay ăn gì
        > Các món ăn được lấy theo số lượng người dùng muốn
        > Các món ăn tuyệt đối không có nguyên liệu kị nhau trong riêng món ăn và cả bữa ăn
        > Hiện danh sách nguyên liệu kế bên để tiện chuẩn bị
    + List:
        > Giúp người dùng quan sát số lượng món ăn mình đã thêm vào
    + Test:
        > Không có tính năng gì, chỉ sử dụng để kiểm tra template và code trước khi sử dụng diện rộng (trên một phạm vi app)
  
- Phụ lục:
    + Vì đây là app đầu được sinh ra để thực hành xong xong với kiến thức nên code chỉ chọn những tính năng có vẻ như mình có thể làm được cũng như khác nhau (không dồn hết thời gian vào một app cụ thể)
    + Những code trên đã được thông qua ChatGPT và Gemini để sửa bug và fix một số lỗi logic cũng như tối ưu hiệu suất
    + Với định hướng là backend developer nên chỉ học và tìm hiểu sâu về các code ở backend (toàn bộ đều hiểu rồi mới tự ghi lại, cũng có những phần tự nghỉ ra logic sau đó nhờ chat sửa)
    + Về phần frontend thì chỉ có thể thiết kế những giao diện được chia hàng chia cột rõ ràng, phần lớn chức năng nằm ở mức hiểu tính năng chứ chưa thể tự viết vì chưa nhớ hết mấy cái kiểu dáng hay lớp CSS 
        
