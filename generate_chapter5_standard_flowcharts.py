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


def figure_5_4() -> None:
    c = SvgCanvas(860, 1120)
    c.terminator(370, 45, 120, 42, "开始")
    c.manual_input(290, 120, 280, 66, "用户进入登录页面")
    c.manual_input(260, 235, 340, 78, "选择密码登录\n验证码登录或第三方登录")
    c.io_box(270, 360, 320, 72, "输入表单或跳转 OAuth 页面")
    c.subprocess(290, 485, 280, 76, "后端校验并返回 token")
    c.process(250, 615, 360, 82, "前端保存登录信息\n并初始化 Socket")
    c.document(290, 760, 280, 82, "进入聊天主界面")
    c.terminator(370, 915, 120, 42, "结束")

    c.arrow(430, 87, 430, 120)
    c.arrow(430, 186, 430, 235)
    c.arrow(430, 313, 430, 360)
    c.arrow(430, 432, 430, 485)
    c.arrow(430, 561, 430, 615)
    c.arrow(430, 697, 430, 760)
    c.arrow(430, 842, 430, 915)

    write_svg("图5_4_1.svg", c)


def figure_5_8() -> None:
    c = SvgCanvas(900, 1140)
    c.terminator(390, 45, 120, 42, "开始")
    c.manual_input(300, 120, 300, 66, "用户进入主界面")
    c.subprocess(240, 235, 420, 82, "加载用户资料\n好友列表和房间列表")
    c.manual_input(240, 360, 420, 78, "根据导航切换\n聊天、联系人或聊天室")
    c.manual_input(300, 485, 300, 66, "点击某个会话或房间")
    c.process(240, 600, 420, 82, "写入当前会话上下文\n并跳转详情页")
    c.document(260, 740, 380, 86, "详情页继续拉取消息记录")
    c.terminator(390, 910, 120, 42, "结束")

    c.arrow(450, 87, 450, 120)
    c.arrow(450, 186, 450, 235)
    c.arrow(450, 317, 450, 360)
    c.arrow(450, 438, 450, 485)
    c.arrow(450, 551, 450, 600)
    c.arrow(450, 682, 450, 740)
    c.arrow(450, 826, 450, 910)

    write_svg("图5_8_1.svg", c)


def figure_5_11() -> None:
    c = SvgCanvas(920, 1060)
    c.terminator(400, 45, 120, 42, "开始")
    c.manual_input(230, 120, 460, 78, "用户打开 AI 面板\n或在聊天室中输入 @AI")
    c.io_box(250, 245, 420, 72, "前端提交问题并附带当前上下文")
    c.subprocess(220, 365, 480, 84, "后端查询最近消息\n并执行 RAG 检索")
    c.process(300, 500, 320, 76, "调用模型生成回答")
    c.document(250, 625, 420, 86, "前端渲染答案并展示来源信息")
    c.terminator(400, 800, 120, 42, "结束")

    c.arrow(460, 87, 460, 120)
    c.arrow(460, 198, 460, 245)
    c.arrow(460, 317, 460, 365)
    c.arrow(460, 449, 460, 500)
    c.arrow(460, 576, 460, 625)
    c.arrow(460, 711, 460, 800)

    write_svg("图5_11_1.svg", c)


def figure_5_15() -> None:
    c = SvgCanvas(920, 1080)
    c.terminator(400, 45, 120, 42, "开始")
    c.subprocess(240, 120, 440, 82, "加载最近会话\n和未读数")
    c.manual_input(310, 245, 300, 66, "用户点击某个会话")
    c.subprocess(220, 360, 480, 84, "拉取完整历史消息\n并渲染消息列表")
    c.process(210, 500, 500, 90, "执行搜索、收藏、删除\n或已读更新操作")
    c.document(210, 650, 500, 90, "刷新当前会话状态\n和左侧列表摘要")
    c.terminator(400, 830, 120, 42, "结束")

    c.arrow(460, 87, 460, 120)
    c.arrow(460, 202, 460, 245)
    c.arrow(460, 311, 460, 360)
    c.arrow(460, 444, 460, 500)
    c.arrow(460, 590, 460, 650)
    c.arrow(460, 740, 460, 830)

    write_svg("图5_15_1.svg", c)


def figure_5_17() -> None:
    c = SvgCanvas(980, 1120)
    c.terminator(430, 45, 120, 42, "开始")
    c.manual_input(320, 120, 340, 66, "用户打开设置弹窗")
    c.manual_input(260, 235, 460, 78, "修改头像、用户名\n或主题")
    c.io_box(290, 360, 400, 72, "调用上传或资料更新接口")
    c.process(260, 485, 460, 82, "本地刷新用户资料\n并保存主题状态")
    c.decision(490, 690, 230, 130, "是否需要同步\n其他在线用户")
    c.subprocess(350, 845, 280, 76, "通过 Socket 同步")
    c.terminator(430, 995, 120, 42, "结束")

    c.arrow(490, 87, 490, 120)
    c.arrow(490, 186, 490, 235)
    c.arrow(490, 313, 490, 360)
    c.arrow(490, 432, 490, 485)
    c.arrow(490, 567, 490, 625)
    c.polyarrow([(490, 755), (490, 800), (490, 845)])
    c.text(530, 798, "是", size=13, weight="700", klass="note")
    c.polyarrow([(605, 690), (760, 690), (760, 1016), (550, 1016)])
    c.text(680, 672, "否", size=13, weight="700", klass="note")
    c.arrow(490, 921, 490, 995)

    write_svg("图5_17_1.svg", c)


def figure_5_20() -> None:
    c = SvgCanvas(1100, 1380)
    c.terminator(490, 35, 120, 42, "开始")
    c.manual_input(320, 105, 460, 76, "客户端（Vue 3）\n发送 @AI 提问")
    c.subprocess(360, 225, 380, 76, "API 网关与鉴权\n验证 JWT Token")
    c.process(330, 350, 440, 84, "ChatRoomAIController\n接收流式请求")
    c.subprocess(340, 490, 420, 82, "VectorSearchTool\n检索 Top-K 语料")
    c.process(330, 620, 440, 84, "Prompt 构建引擎\n注入上下文与历史")
    c.process(330, 760, 440, 84, "DeepSeek API\n模型流式推理（SSE）")
    c.subprocess(330, 900, 440, 82, "Socket.IO 广播\nai-stream-chunk 事件")
    c.document(320, 1040, 460, 90, "客户端增量渲染答案\n并回显引用来源")
    c.terminator(490, 1220, 120, 42, "结束")
    c.note_box(800, 215, 220, 98, "POST /api/chatroom-ai\n携带 JWT 与会话上下文")
    c.note_box(800, 600, 220, 98, "组合 Context\n补充历史讨论与检索结果")
    c.note_box(800, 880, 220, 98, "Chunk 回调解析\n并推送到房间")

    c.arrow(550, 77, 550, 105)
    c.arrow(550, 181, 550, 225)
    c.arrow(550, 301, 550, 350)
    c.arrow(550, 434, 550, 490)
    c.arrow(550, 572, 550, 620)
    c.arrow(550, 704, 550, 760)
    c.arrow(550, 844, 550, 900)
    c.arrow(550, 982, 550, 1040)
    c.arrow(550, 1130, 550, 1220)
    c.polyarrow([(740, 263), (800, 263)], dashed=True)
    c.polyarrow([(770, 662), (800, 662)], dashed=True)
    c.polyarrow([(770, 940), (800, 940)], dashed=True)

    write_svg("图5_20_1.svg", c)


def figure_5_21() -> None:
    c = SvgCanvas(1140, 1180)
    c.terminator(510, 35, 120, 42, "开始")
    c.database(380, 115, 380, 104, "MongoDB 聚合查询\n近 30 分钟消息与提问")
    c.subprocess(120, 320, 300, 86, "未解决问题过滤\nquestionStatus = open")
    c.subprocess(720, 320, 300, 86, "热门话题聚类\n按频率聚合 Top-3")
    c.process(380, 500, 380, 86, "状态分析引擎\n生成 Insights 与 AI Can Help")
    c.process(380, 650, 380, 86, "播报与建议生成\n组装 aiSpeech 与 suggestions")
    c.document(380, 810, 380, 86, "客户端侧边栏\n动态渲染分析组件")
    c.terminator(510, 965, 120, 42, "结束")
    c.note_box(110, 460, 230, 90, "紧急程度、未解状态\n作为重点分析输入")
    c.note_box(800, 460, 230, 90, "活跃度排序\n识别近期热点主题")

    c.arrow(570, 77, 570, 115)
    c.polyarrow([(500, 219), (270, 219), (270, 320)])
    c.polyarrow([(640, 219), (870, 219), (870, 320)])
    c.polyarrow([(270, 406), (270, 450), (570, 450), (570, 500)])
    c.polyarrow([(870, 406), (870, 450), (570, 450), (570, 500)])
    c.arrow(570, 586, 570, 650)
    c.arrow(570, 736, 570, 810)
    c.arrow(570, 896, 570, 965)
    c.polyarrow([(420, 500), (340, 500)], dashed=True)
    c.polyarrow([(720, 500), (800, 500)], dashed=True)

    write_svg("图5_21_1.svg", c)


if __name__ == "__main__":
    figure_5_4()
    figure_5_8()
    figure_5_11()
    figure_5_15()
    figure_5_17()
    figure_5_20()
    figure_5_21()
    print("Generated: 图5_4_1.svg, 图5_8_1.svg, 图5_11_1.svg, 图5_15_1.svg, 图5_17_1.svg, 图5_20_1.svg, 图5_21_1.svg")
