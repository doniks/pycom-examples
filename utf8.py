# y += 40
# disp.draw_text(x,y, "field equation: G(μ,ν) + Λ g(μ,ν) = κ T(μ,ν)",
#
# print("Image drawing")
# disp = EPaperDisplay(clear=False)
# # disp.draw_text(0,0, "😶😐😯😮😨😰😱🤢🤮😵🤯🥵💥",arial_35)
# disp.draw_text(0,0, "😐",arial_35)
# disp.scan_out()
#
# print(" 😀 😁 " )

for e in """
😂
😃
😄
😅
😆
😇
😈
😉
😊
😋
😌
😍
😎
😏
😐
😑
😒
😓
😔
😕
😖
😗
😘
😙
😚
😛
😜
😝
😞
😟
😠
😡
😢
😣
😤
😥
😦
😧
😨
😩
😪
😫
😬
😭
😮
😯
😰
😱
😲
😳
😴
😵
😶
😷
😸
😹
😺
😻
😼
😽
😾
😿
🙀
🙁
🙂
🙃
🙄
🙅
🙆
🙇
🙈
🙉
🙊
🙋
🙌
🙍
🙎
🙏
""" :
    if ord(e) != ord('\n'):
        print(hex(ord(e)), e)
