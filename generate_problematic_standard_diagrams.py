# -*- coding: utf-8 -*-
from __future__ import annotations

from html import escape
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parents[1] / "img"
FONT_STACK = '"Microsoft YaHei", "Noto Sans SC", "PingFang SC", sans-serif'


class SvgCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.parts: list[str] = []

    def add(self, item: str) -> None:
        self.parts.append(item)

    def text(self, x: float, y: float, text: str, *, size: int = 14, weight: str = "500",
             anchor: str = "middle", klass: str = "label") -> None:
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" class="{klass}">{escape(text)}</text>'
        )

    def text_block(self, x: float, y: float, text: str, *, size: int = 14,
                   weight: str = "500", anchor: str = "middle", klass: str = "label",
                   line_gap: float | None = None) -> None:
        lines = text.split("\n")
        if line_gap is None:
            line_gap = size * 1.4
        start_y = y - ((len(lines) - 1) * line_gap) / 2 + size * 0.34
        tspans = []
        for idx, line in enumerate(lines):
            tspans.append(f'<tspan x="{x}" y="{start_y + idx * line_gap}">{escape(line)}</tspan>')
        self.add(
            f'<text text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" class="{klass}">'
            + "".join(tspans)
            + "</text>"
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False,
             marker: str = "arrow") -> None:
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        self.add(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line"{dash} marker-end="url(#{marker})"/>'
        )

    def polyline(self, pts: list[tuple[float, float]], *, dashed: bool = False,
                 marker: str = "arrow") -> None:
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        points = " ".join(f"{x},{y}" for x, y in pts)
        self.add(f'<polyline points="{points}" fill="none" class="line"{dash} marker-end="url(#{marker})"/>')

    def entity(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="entity"/>')
        self.text_block(x + w / 2, y + h / 2, title, size=16, weight="700")

    def relation(self, cx: float, cy: float, w: float, h: float, title: str) -> None:
        pts = [
            (cx, cy - h / 2),
            (cx + w / 2, cy),
            (cx, cy + h / 2),
            (cx - w / 2, cy),
        ]
        self.add(
            '<polygon points="'
            + " ".join(f"{x},{y}" for x, y in pts)
            + '" class="relation"/>'
        )
        self.text_block(cx, cy, title, size=13, weight="700")

    def attribute(self, cx: float, cy: float, rx: float, ry: float, title: str, *, pk: bool = False) -> None:
        self.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="attribute"/>')
        self.text_block(cx, cy, title, size=12, weight="600" if pk else "500")
        if pk:
            title_width = min(rx * 1.35, max(len(title) * 6.3, 34))
            self.add(
                f'<line x1="{cx - title_width / 2}" y1="{cy + 9}" '
                f'x2="{cx + title_width / 2}" y2="{cy + 9}" class="entity-line"/>'
            )

    def note_box(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            'fill="#fafafa" stroke="#111111" stroke-width="1.6" stroke-dasharray="7 5" rx="6"/>'
        )
        self.text_block(x + w / 2, y + h / 2, text, size=12, weight="600")

    def participant(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="entity"/>')
        self.text_block(x + w / 2, y + h / 2, title, size=14, weight="700")

    def lifeline(self, x: float, y1: float, y2: float) -> None:
        self.add(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="lifeline"/>')

    def activation(self, x: float, y: float, w: float, h: float) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="activation"/>')

    def render(self) -> str:
        header = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
  <defs>
    <marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 12 6 L 0 12 z" fill="#111111"/>
    </marker>
    <marker id="open-arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 1 1 L 11 6 L 1 11" fill="none" stroke="#111111" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <style>
      .label, .note {{
        fill: #111111;
        font-family: {FONT_STACK};
      }}
      .line {{
        stroke: #111111;
        stroke-width: 2.0;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .entity {{
        fill: #ffffff;
        stroke: #111111;
        stroke-width: 2.1;
      }}
      .entity-line {{
        fill: none;
        stroke: #111111;
        stroke-width: 1.5;
      }}
      .relation {{
        fill: #ffffff;
        stroke: #111111;
        stroke-width: 2.0;
        stroke-linejoin: round;
      }}
      .attribute {{
        fill: #ffffff;
        stroke: #111111;
        stroke-width: 1.8;
      }}
      .lifeline {{
        stroke: #111111;
        stroke-width: 1.4;
        stroke-dasharray: 7 5;
      }}
      .activation {{
        fill: #ffffff;
        stroke: #111111;
        stroke-width: 1.6;
      }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#ffffff"/>
'''
        return header + "\n".join(self.parts) + "\n</svg>\n"


def write_svg(name: str, canvas: SvgCanvas) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(canvas.render(), encoding="utf-8")


def draw_er_diagram() -> None:
    c = SvgCanvas(1500, 980)

    # Entities
    c.entity(620, 90, 170, 60, "Users")
    c.entity(1040, 90, 170, 60, "Room")
    c.entity(210, 260, 190, 60, "AIConversation")
    c.entity(600, 330, 210, 60, "Messages")
    c.entity(1020, 330, 220, 60, "GroupMessage")
    c.entity(250, 640, 170, 60, "Summary")
    c.entity(980, 640, 170, 60, "Favorite")

    # Attributes
    c.attribute(565, 65, 70, 24, "uID", pk=True)
    c.attribute(565, 145, 70, 24, "uName")
    c.attribute(845, 120, 82, 24, "provider")

    c.attribute(1000, 55, 82, 24, "RoomID", pk=True)
    c.attribute(1280, 70, 90, 24, "RoomName")
    c.attribute(1290, 135, 78, 24, "joinType")

    c.attribute(155, 235, 92, 24, "conversationId", pk=True)
    c.attribute(145, 315, 64, 24, "role")
    c.attribute(465, 240, 70, 24, "updatedAt")

    c.attribute(530, 305, 70, 24, "messageId", pk=True)
    c.attribute(535, 385, 60, 24, "time")
    c.attribute(885, 360, 70, 24, "type")

    c.attribute(995, 295, 80, 24, "groupMsgId", pk=True)
    c.attribute(1315, 300, 72, 24, "roomId")
    c.attribute(1325, 380, 84, 24, "isQuestion")

    c.attribute(155, 625, 76, 24, "summaryId", pk=True)
    c.attribute(155, 705, 70, 24, "chatType")
    c.attribute(505, 675, 70, 24, "createdAt")

    c.attribute(920, 625, 76, 24, "favoriteId", pk=True)
    c.attribute(1245, 625, 88, 24, "messageId")
    c.attribute(1240, 705, 56, 24, "tags")

    # Attribute connectors
    c.add('<line x1="620" y1="120" x2="565" y2="89" class="line"/>')
    c.add('<line x1="620" y1="120" x2="565" y2="145" class="line"/>')
    c.add('<line x1="790" y1="120" x2="845" y2="120" class="line"/>')

    c.add('<line x1="1040" y1="120" x2="1082" y2="79" class="line"/>')
    c.add('<line x1="1210" y1="120" x2="1280" y2="85" class="line"/>')
    c.add('<line x1="1210" y1="120" x2="1290" y2="135" class="line"/>')

    c.add('<line x1="210" y1="290" x2="247" y2="259" class="line"/>')
    c.add('<line x1="210" y1="290" x2="209" y2="315" class="line"/>')
    c.add('<line x1="400" y1="290" x2="465" y2="264" class="line"/>')

    c.add('<line x1="600" y1="360" x2="600" y2="329" class="line"/>')
    c.add('<line x1="600" y1="360" x2="535" y2="385" class="line"/>')
    c.add('<line x1="810" y1="360" x2="885" y2="360" class="line"/>')

    c.add('<line x1="1020" y1="360" x2="1075" y2="319" class="line"/>')
    c.add('<line x1="1240" y1="360" x2="1315" y2="324" class="line"/>')
    c.add('<line x1="1240" y1="360" x2="1325" y2="380" class="line"/>')

    c.add('<line x1="250" y1="670" x2="231" y2="649" class="line"/>')
    c.add('<line x1="250" y1="670" x2="231" y2="705" class="line"/>')
    c.add('<line x1="420" y1="670" x2="505" y2="675" class="line"/>')

    c.add('<line x1="980" y1="670" x2="996" y2="649" class="line"/>')
    c.add('<line x1="1150" y1="670" x2="1245" y2="649" class="line"/>')
    c.add('<line x1="1150" y1="670" x2="1240" y2="705" class="line"/>')

    # Relationships
    c.relation(925, 120, 110, 60, "创建")
    c.relation(925, 195, 110, 60, "加入")
    c.relation(500, 210, 110, 60, "拥有")
    c.relation(705, 250, 120, 62, "发送")
    c.relation(925, 365, 120, 62, "包含")
    c.relation(705, 445, 150, 70, "收藏来源")
    c.relation(500, 555, 120, 62, "生成")
    c.relation(925, 555, 120, 62, "收藏")

    # Relationship connectors
    c.add('<line x1="790" y1="120" x2="870" y2="120" class="line"/>')
    c.add('<line x1="980" y1="120" x2="1040" y2="120" class="line"/>')
    c.text(830, 104, "1", size=13, weight="700")
    c.text(1010, 104, "N", size=13, weight="700")

    c.add('<line x1="790" y1="135" x2="860" y2="180" class="line"/>')
    c.add('<line x1="1040" y1="135" x2="980" y2="180" class="line"/>')
    c.text(842, 170, "M", size=13, weight="700")
    c.text(997, 170, "N", size=13, weight="700")

    c.add('<line x1="400" y1="290" x2="445" y2="226" class="line"/>')
    c.add('<line x1="620" y1="120" x2="555" y2="194" class="line"/>')
    c.text(442, 248, "N", size=13, weight="700")
    c.text(567, 172, "1", size=13, weight="700")

    c.add('<line x1="705" y1="281" x2="705" y2="330" class="line"/>')
    c.add('<line x1="705" y1="281" x2="705" y2="390" class="line"/>')
    c.text(690, 302, "1", size=13, weight="700")
    c.text(690, 404, "N", size=13, weight="700")

    c.add('<line x1="985" y1="365" x2="1020" y2="365" class="line"/>')
    c.add('<line x1="865" y1="365" x2="810" y2="365" class="line"/>')
    c.text(833, 349, "1", size=13, weight="700")
    c.text(1005, 349, "N", size=13, weight="700")

    c.add('<line x1="925" y1="395" x2="925" y2="524" class="line"/>')
    c.add('<line x1="1020" y1="390" x2="760" y2="438" class="line"/>')
    c.add('<line x1="810" y1="390" x2="640" y2="438" class="line"/>')
    c.add('<line x1="705" y1="480" x2="705" y2="520" class="line"/>')
    c.text(892, 430, "N", size=13, weight="700")
    c.text(809, 430, "N", size=13, weight="700")
    c.text(689, 505, "1", size=13, weight="700")
    c.note_box(805, 445, 210, 74, "Favorite 可溯源私聊消息\n也可溯源群消息")

    c.add('<line x1="400" y1="670" x2="445" y2="571" class="line"/>')
    c.add('<line x1="335" y1="700" x2="445" y2="572" class="line"/>')
    c.text(410, 603, "1", size=13, weight="700")
    c.text(372, 661, "N", size=13, weight="700")

    c.add('<line x1="980" y1="670" x2="980" y2="585" class="line"/>')
    c.add('<line x1="790" y1="120" x2="870" y2="530" class="line"/>')
    c.text(960, 617, "N", size=13, weight="700")
    c.text(845, 454, "1", size=13, weight="700")

    c.note_box(1120, 145, 250, 84, "标准化说明：\n采用实体（矩形）-关系（菱形）-\n属性（椭圆）的 ER 表达")

    write_svg("图4_10_系统数据库E_R图_1.svg", c)


def draw_socket_sequence() -> None:
    c = SvgCanvas(1100, 780)

    headers_y = 40
    lifeline_top = 82
    lifeline_bottom = 720
    xs = {
        "a": 120,
        "http": 330,
        "socket": 560,
        "db": 790,
        "b": 990,
    }

    c.participant(xs["a"] - 55, headers_y, 110, 42, "客户端 A")
    c.participant(xs["http"] - 70, headers_y, 140, 42, "HTTP 业务服务")
    c.participant(xs["socket"] - 80, headers_y, 160, 42, "Socket.IO 服务器")
    c.participant(xs["db"] - 60, headers_y, 120, 42, "MongoDB")
    c.participant(xs["b"] - 55, headers_y, 110, 42, "客户端 B")

    for x in xs.values():
        c.lifeline(x, lifeline_top, lifeline_bottom)

    # Activation bars
    c.activation(xs["http"] - 5, 118, 10, 70)
    c.activation(xs["socket"] - 5, 235, 10, 395)
    c.activation(xs["db"] - 5, 460, 10, 80)
    c.activation(xs["b"] - 5, 590, 10, 60)
    c.activation(xs["a"] - 5, 610, 10, 40)

    # Note for client B precondition
    c.note_box(865, 115, 200, 70, "前置条件：\n客户端 B 已完成连接\n并已加入目标 Room")

    # Messages
    c.line(xs["a"], 130, xs["http"] - 5, 130, marker="arrow")
    c.text(225, 120, "1. POST /login", size=12)

    c.line(xs["http"] - 5, 165, xs["a"], 165, dashed=True, marker="open-arrow")
    c.text(225, 155, "2. 返回 JWT Token", size=12)

    c.line(xs["a"], 260, xs["socket"] - 5, 260, marker="arrow")
    c.text(340, 250, "3. connect(token)", size=12)

    c.line(xs["a"], 310, xs["socket"] - 5, 310, marker="arrow")
    c.text(340, 300, "4. emit join-room(roomId)", size=12)

    c.line(xs["socket"] - 5, 350, xs["a"], 350, dashed=True, marker="open-arrow")
    c.text(345, 340, "5. join-room ack", size=12)

    c.line(xs["a"], 410, xs["socket"] - 5, 410, marker="arrow")
    c.text(340, 400, "6. emit group-message(payload)", size=12, weight="700")

    c.line(xs["socket"] - 5, 460, xs["db"] - 5, 460, marker="arrow")
    c.text(675, 450, "7. 校验并写入消息", size=12)

    c.line(xs["db"] - 5, 510, xs["socket"] - 5, 510, dashed=True, marker="open-arrow")
    c.text(675, 500, "8. 持久化完成", size=12)

    c.line(xs["socket"] - 5, 560, xs["b"] - 5, 560, marker="arrow")
    c.text(775, 550, "9. io.to(roomId).emit(new-message)", size=12, weight="700")

    c.line(xs["b"] - 5, 610, xs["socket"] - 5, 610, dashed=True, marker="open-arrow")
    c.text(775, 600, "10. delivered ack", size=12)

    c.line(xs["socket"] - 5, 640, xs["a"], 640, dashed=True, marker="open-arrow")
    c.text(340, 630, "11. 返回发送成功状态", size=12)

    c.note_box(160, 680, 250, 70, "标准化说明：\n实线实心箭头表示调用消息，\n虚线开口箭头表示返回消息")

    write_svg("图4_6_Socket即时通信底层时序图_1.svg", c)


if __name__ == "__main__":
    draw_er_diagram()
    draw_socket_sequence()
    print("Generated: 图4_10_系统数据库E_R图_1.svg, 图4_6_Socket即时通信底层时序图_1.svg")
