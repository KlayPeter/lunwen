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
                   weight: str = "500", anchor: str = "middle", klass: str = "label") -> None:
        lines = text.split("\n")
        line_gap = size * 1.45
        start_y = y - ((len(lines) - 1) * line_gap) / 2 + size * 0.35
        tspans = []
        for idx, line in enumerate(lines):
            tspans.append(f'<tspan x="{x}" y="{start_y + idx * line_gap}">{escape(line)}</tspan>')
        self.add(
            f'<text text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" class="{klass}">'
            + "".join(tspans)
            + "</text>"
        )

    def terminator(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" class="symbol"/>')
        self.text_block(x + w / 2, y + h / 2, text, size=14, weight="700")

    def process(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="symbol"/>')
        self.text_block(x + w / 2, y + h / 2, text, size=14, weight="600")

    def subprocess(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="symbol"/>')
        self.add(f'<line x1="{x + 14}" y1="{y}" x2="{x + 14}" y2="{y + h}" class="symbol-line"/>')
        self.add(f'<line x1="{x + w - 14}" y1="{y}" x2="{x + w - 14}" y2="{y + h}" class="symbol-line"/>')
        self.text_block(x + w / 2, y + h / 2, text, size=14, weight="600")

    def manual_input(self, x: float, y: float, w: float, h: float, text: str) -> None:
        points = f"{x + 22},{y} {x + w},{y} {x + w - 18},{y + h} {x},{y + h}"
        self.add(f'<polygon points="{points}" class="symbol"/>')
        self.text_block(x + w / 2 - 6, y + h / 2, text, size=14, weight="600")

    def io_box(self, x: float, y: float, w: float, h: float, text: str) -> None:
        points = f"{x + 24},{y} {x + w},{y} {x + w - 24},{y + h} {x},{y + h}"
        self.add(f'<polygon points="{points}" class="symbol"/>')
        self.text_block(x + w / 2, y + h / 2, text, size=14, weight="600")

    def decision(self, cx: float, cy: float, w: float, h: float, text: str) -> None:
        points = [
            (cx, cy - h / 2),
            (cx + w / 2, cy),
            (cx, cy + h / 2),
            (cx - w / 2, cy),
        ]
        self.add(
            '<polygon points="'
            + " ".join(f"{x},{y}" for x, y in points)
            + '" class="symbol"/>'
        )
        self.text_block(cx, cy, text, size=14, weight="700")

    def document(self, x: float, y: float, w: float, h: float, text: str) -> None:
        path = (
            f'M {x} {y} H {x + w} V {y + h - 18} '
            f'Q {x + w * 0.75} {y + h - 34} {x + w * 0.5} {y + h - 18} '
            f'Q {x + w * 0.25} {y + h - 2} {x} {y + h - 18} Z'
        )
        self.add(f'<path d="{path}" class="symbol"/>')
        self.text_block(x + w / 2, y + h / 2 - 4, text, size=14, weight="600")

    def database(self, x: float, y: float, w: float, h: float, text: str) -> None:
        rx = w / 2
        ry = 15
        cx = x + w / 2
        self.add(f'<ellipse cx="{cx}" cy="{y + ry}" rx="{rx}" ry="{ry}" class="symbol"/>')
        self.add(f'<line x1="{x}" y1="{y + ry}" x2="{x}" y2="{y + h - ry}" class="symbol-line"/>')
        self.add(f'<line x1="{x + w}" y1="{y + ry}" x2="{x + w}" y2="{y + h - ry}" class="symbol-line"/>')
        self.add(f'<path d="M {x} {y + h - ry} A {rx} {ry} 0 0 0 {x + w} {y + h - ry}" class="symbol-line"/>')
        self.text_block(cx, y + h / 2 + 10, text, size=14, weight="600")

    def note_box(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            'fill="#fafafa" stroke="#111111" stroke-width="1.8" stroke-dasharray="7 5"/>'
        )
        self.text_block(x + w / 2, y + h / 2, text, size=13, weight="600")

    def arrow(self, x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False) -> None:
        cls = "flow-dash" if dashed else "flow"
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>')

    def polyarrow(self, points: list[tuple[float, float]], *, dashed: bool = False) -> None:
        cls = "flow-dash" if dashed else "flow"
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polyline points="{pts}" fill="none" class="{cls}"/>')

    def render(self) -> str:
        header = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
  <defs>
    <marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 12 6 L 0 12 z" fill="#111111"/>
    </marker>
    <style>
      .label, .note {{
        fill: #111111;
        font-family: {FONT_STACK};
      }}
      .symbol {{
        fill: #ffffff;
        stroke: #111111;
        stroke-width: 2.2;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .symbol-line {{
        fill: none;
        stroke: #111111;
        stroke-width: 2.2;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .flow {{
        fill: none;
        stroke: #111111;
        stroke-width: 2.4;
        stroke-linecap: round;
        stroke-linejoin: round;
        marker-end: url(#arrow);
      }}
      .flow-dash {{
        fill: none;
        stroke: #111111;
        stroke-width: 2.4;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-dasharray: 8 6;
        marker-end: url(#arrow);
      }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#ffffff"/>
'''
        return header + "\n".join(self.parts) + "\n</svg>\n"


def write_svg(name: str, canvas: SvgCanvas) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(canvas.render(), encoding="utf-8")


def figure_4_4() -> None:
    c = SvgCanvas(980, 1040)
    c.terminator(430, 55, 120, 42, "开始")
    c.manual_input(375, 140, 230, 66, "选择认证方式\n邮箱密码 / 验证码 / OAuth")
    c.decision(490, 330, 210, 130, "是否为\n本地认证")
    c.manual_input(120, 445, 240, 82, "邮箱密码登录\n或验证码登录")
    c.process(620, 448, 240, 76, "跳转 OAuth 平台\n并接收回调")
    c.subprocess(380, 620, 220, 74, "统一生成 JWT")
    c.database(390, 745, 200, 96, "写入用户身份信息")
    c.process(380, 890, 220, 74, "访问受保护资源")
    c.terminator(430, 980, 120, 42, "结束")

    c.arrow(490, 97, 490, 140)
    c.arrow(490, 206, 490, 265)
    c.polyarrow([(385, 330), (240, 330), (240, 445)])
    c.polyarrow([(595, 330), (740, 330), (740, 448)])
    c.text(315, 314, "是", size=13, weight="700", klass="note")
    c.text(664, 314, "否", size=13, weight="700", klass="note")
    c.polyarrow([(240, 527), (240, 575), (490, 575), (490, 620)])
    c.polyarrow([(740, 524), (740, 575), (490, 575), (490, 620)])
    c.arrow(490, 694, 490, 745)
    c.arrow(490, 841, 490, 890)
    c.arrow(490, 964, 490, 980)

    write_svg("图4_4_1.svg", c)


def figure_4_5() -> None:
    c = SvgCanvas(1100, 1100)
    c.terminator(470, 50, 160, 44, "开始发送消息")
    c.io_box(430, 145, 240, 72, "前端组织消息体")
    c.subprocess(430, 270, 240, 74, "区分私聊 / 群聊 / 聊天室")
    c.process(410, 395, 280, 84, "服务端校验权限\n与消息类型")
    c.process(110, 545, 260, 78, "Socket.IO 实时广播")
    c.database(730, 525, 260, 100, "写入 Messages /\nGroupMessage")
    c.subprocess(730, 680, 260, 74, "加入 MessageIndexer\n索引队列")
    c.process(410, 820, 280, 82, "更新在线状态\n未读 / 已读")
    c.document(410, 950, 280, 82, "客户端刷新消息区")
    c.terminator(470, 1040, 160, 44, "结束")

    c.arrow(550, 94, 550, 145)
    c.arrow(550, 217, 550, 270)
    c.arrow(550, 344, 550, 395)
    c.polyarrow([(550, 479), (550, 515), (240, 515), (240, 545)])
    c.polyarrow([(550, 479), (550, 505), (860, 505), (860, 525)])
    c.text(330, 500, "推送链路", size=13, weight="700", klass="note")
    c.text(790, 490, "持久化链路", size=13, weight="700", klass="note")
    c.arrow(860, 625, 860, 680)
    c.polyarrow([(240, 623), (240, 780), (550, 780), (550, 820)])
    c.polyarrow([(860, 754), (860, 780), (550, 780), (550, 820)])
    c.arrow(550, 902, 550, 950)
    c.arrow(550, 1032, 550, 1040)

    write_svg("图4_5_1.svg", c)


def figure_4_6() -> None:
    c = SvgCanvas(1240, 1160)
    c.terminator(550, 50, 140, 42, "开始")
    c.manual_input(530, 125, 180, 62, "创建聊天室")
    c.manual_input(430, 240, 380, 96, "填写房间名称、技术方向\n加入方式与有效时长")
    c.process(450, 390, 340, 92, "生成 RoomID\n初始化成员与系统消息")
    c.decision(620, 585, 220, 130, "加入方式")
    c.process(100, 700, 260, 90, "公开加入\n自动进入房间")
    c.process(490, 700, 260, 90, "邀请码加入\n校验 inviteCode")
    c.process(880, 700, 260, 90, "密码加入\n校验 password")
    c.subprocess(460, 860, 320, 84, "同步在线人数与成员状态")
    c.process(470, 990, 300, 78, "到期清理与自动失效")
    c.terminator(550, 1095, 140, 42, "结束")

    c.arrow(620, 92, 620, 125)
    c.arrow(620, 187, 620, 240)
    c.arrow(620, 336, 620, 390)
    c.arrow(620, 482, 620, 520)
    c.polyarrow([(510, 585), (230, 585), (230, 700)])
    c.polyarrow([(620, 650), (620, 700)])
    c.polyarrow([(730, 585), (1010, 585), (1010, 700)])
    c.text(365, 568, "公开", size=13, weight="700", klass="note")
    c.text(620, 685, "邀请码", size=13, weight="700", klass="note")
    c.text(875, 568, "密码", size=13, weight="700", klass="note")
    c.polyarrow([(230, 790), (230, 830), (620, 830), (620, 860)])
    c.arrow(620, 790, 620, 860)
    c.polyarrow([(1010, 790), (1010, 830), (620, 830), (620, 860)])
    c.arrow(620, 944, 620, 990)
    c.arrow(620, 1068, 620, 1095)

    write_svg("图4_6_1.svg", c)


def figure_4_8() -> None:
    c = SvgCanvas(1080, 1180)
    c.terminator(470, 45, 140, 42, "开始")
    c.manual_input(420, 120, 240, 64, "发起收藏")
    c.process(430, 235, 220, 74, "读取原始消息")
    c.process(430, 340, 220, 74, "读取发送者信息")
    c.document(410, 450, 260, 90, "构造收藏快照\n正文 / 代码 / 附件信息")
    c.note_box(730, 435, 250, 102, "保存的是快照\n不是单纯引用\n避免源消息变更影响收藏")
    c.manual_input(420, 585, 240, 64, "补充标签与备注")
    c.database(430, 690, 220, 98, "保存 Favorite 记录")
    c.manual_input(390, 845, 300, 64, "按关键词 / 标签筛选")
    c.document(410, 930, 260, 86, "打开收藏详情")
    c.process(430, 1045, 220, 74, "回溯消息来源")
    c.terminator(470, 1130, 140, 42, "结束")

    c.arrow(540, 87, 540, 120)
    c.arrow(540, 184, 540, 235)
    c.arrow(540, 309, 540, 340)
    c.arrow(540, 414, 540, 450)
    c.polyarrow([(670, 495), (730, 495)], dashed=True)
    c.arrow(540, 540, 540, 585)
    c.arrow(540, 649, 540, 690)
    c.polyarrow([(540, 788), (540, 820), (540, 845)], dashed=True)
    c.text(620, 828, "后续查阅", size=13, weight="700", klass="note")
    c.arrow(540, 909, 540, 930)
    c.arrow(540, 1016, 540, 1045)
    c.arrow(540, 1119, 540, 1130)

    write_svg("图4_8_1.svg", c)


if __name__ == "__main__":
    figure_4_4()
    figure_4_5()
    figure_4_6()
    figure_4_8()
    print("Generated: 图4_4_1.svg, 图4_5_1.svg, 图4_6_1.svg, 图4_8_1.svg")
