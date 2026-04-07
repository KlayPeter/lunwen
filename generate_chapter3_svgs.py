from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"


def wrap_text(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            if len(current) >= width:
                lines.append(current)
                current = ch
            else:
                current += ch
        if current:
            lines.append(current)
    return lines or [""]


class SvgCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.elements: list[str] = []

    def add(self, element: str) -> None:
        self.elements.append(element)

    def rect(self, x: float, y: float, w: float, h: float, text: str | None = None,
             rx: float = 14, cls: str = "box", font_size: int = 24, wrap: int = 11) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'
        )
        if text is not None:
            self.text_block(x + w / 2, y + h / 2, wrap_text(text, wrap), font_size=font_size)

    def header_rect(self, x: float, y: float, w: float, h: float, text: str,
                    font_size: int = 26, wrap: int = 14) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="header"/>'
        )
        self.text_block(x + w / 2, y + h / 2, wrap_text(text, wrap), font_size=font_size, weight="700")

    def boundary(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="boundary"/>'
        )
        self.text(label, x + 18, y + 32, anchor="start", font_size=24, weight="700")

    def lane(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="lane"/>'
        )
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="64" class="lane-header"/>'
        )
        self.text(label, x + w / 2, y + 38, font_size=24, weight="700")

    def ellipse(self, cx: float, cy: float, rx: float, ry: float, text: str,
                font_size: int = 22, wrap: int = 9, cls: str = "usecase") -> None:
        self.add(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="{cls}"/>'
        )
        self.text_block(cx, cy, wrap_text(text, wrap), font_size=font_size)

    def diamond(self, cx: float, cy: float, w: float, h: float, text: str,
                font_size: int = 24, wrap: int = 8) -> None:
        half_w = w / 2
        half_h = h / 2
        points = [
            (cx, cy - half_h),
            (cx + half_w, cy),
            (cx, cy + half_h),
            (cx - half_w, cy),
        ]
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polygon points="{pts}" class="decision"/>')
        self.text_block(cx, cy, wrap_text(text, wrap), font_size=font_size)

    def actor(self, x: float, y: float, label: str) -> None:
        self.add(f'<circle cx="{x}" cy="{y}" r="22" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y + 22}" x2="{x}" y2="{y + 88}" class="actor-line"/>')
        self.add(f'<line x1="{x - 32}" y1="{y + 42}" x2="{x + 32}" y2="{y + 42}" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y + 88}" x2="{x - 28}" y2="{y + 130}" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y + 88}" x2="{x + 28}" y2="{y + 130}" class="actor-line"/>')
        self.text_block(x, y + 170, wrap_text(label, 6), font_size=24, weight="700")

    def line(self, x1: float, y1: float, x2: float, y2: float,
             dashed: bool = False, arrow: bool = False, cls: str = "line") -> None:
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        dash = ' stroke-dasharray="10 8"' if dashed else ""
        self.add(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{dash}{marker}/>'
        )

    def polyline(self, points: list[tuple[float, float]], dashed: bool = False,
                 arrow: bool = False, cls: str = "line") -> None:
        pts = " ".join(f"{x},{y}" for x, y in points)
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        dash = ' stroke-dasharray="10 8"' if dashed else ""
        self.add(
            f'<polyline points="{pts}" fill="none" class="{cls}"{dash}{marker}/>'
        )

    def text(self, text: str, x: float, y: float, anchor: str = "middle",
             font_size: int = 22, weight: str = "500", cls: str = "label") -> None:
        esc = escape(text)
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{font_size}" '
            f'font-weight="{weight}" class="{cls}">{esc}</text>'
        )

    def text_block(self, x: float, y: float, lines: list[str], font_size: int = 22,
                   line_height: int | None = None, anchor: str = "middle",
                   weight: str = "500", cls: str = "label") -> None:
        if line_height is None:
            line_height = int(font_size * 1.35)
        start_y = y - ((len(lines) - 1) * line_height) / 2 + font_size * 0.35
        tspans = []
        for idx, line in enumerate(lines):
            esc = escape(line)
            tspans.append(
                f'<tspan x="{x}" y="{start_y + idx * line_height}">{esc}</tspan>'
            )
        self.add(
            f'<text text-anchor="{anchor}" font-size="{font_size}" font-weight="{weight}" class="{cls}">'
            + "".join(tspans)
            + "</text>"
        )

    def note(self, x: float, y: float, text: str, font_size: int = 20,
             anchor: str = "middle") -> None:
        self.text(text, x, y, anchor=anchor, font_size=font_size, weight="600", cls="note")

    def render(self) -> str:
        header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#111111"/>
  </marker>
  <style>
    .label {{
      font-family: "Microsoft YaHei", "Noto Sans SC", "PingFang SC", sans-serif;
      fill: #111111;
    }}
    .note {{
      font-family: "Microsoft YaHei", "Noto Sans SC", "PingFang SC", sans-serif;
      fill: #111111;
    }}
    .box {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.2;
    }}
    .subbox {{
      fill: #fafafa;
      stroke: #111111;
      stroke-width: 1.9;
    }}
    .header {{
      fill: #ececec;
      stroke: #111111;
      stroke-width: 2.2;
    }}
    .boundary {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.4;
    }}
    .lane {{
      fill: #ffffff;
      stroke: #777777;
      stroke-width: 1.4;
      stroke-dasharray: 9 6;
    }}
    .lane-header {{
      fill: #efefef;
      stroke: #111111;
      stroke-width: 1.6;
    }}
    .usecase {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.0;
    }}
    .decision {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.2;
    }}
    .line {{
      stroke: #111111;
      stroke-width: 2.2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .actor-line {{
      stroke: #111111;
      stroke-width: 2.2;
      fill: none;
      stroke-linecap: round;
    }}
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>
'''
        return header + "\n".join(self.elements) + "\n</svg>\n"


def figure_3_1() -> str:
    c = SvgCanvas(1500, 760)
    c.actor(75, 260, "技术交流用户")
    c.line(110, 282, 140, 260, arrow=True)
    c.rect(140, 220, 180, 84, "登录并进入系统", wrap=8)
    c.rect(350, 220, 180, 84, "选择技术交流空间\n（群聊/专题聊天室）", wrap=9)
    c.rect(560, 212, 200, 100, "提交问题上下文\n（文本、代码、日志、文件）", wrap=12)
    c.rect(790, 212, 200, 100, "协同讨论与引用回复\n（成员参与、问题标记）", wrap=12)
    c.diamond(1060, 262, 150, 118, "是否获得\n可行方案", wrap=6)
    c.rect(1170, 220, 210, 84, "标记解决方案\n或最佳答案", wrap=8)
    c.rect(1030, 500, 210, 84, "收藏关键内容\n补充标签与备注", wrap=8)
    c.rect(760, 500, 210, 84, "生成阶段总结\n沉淀讨论结论", wrap=8)
    c.rect(490, 500, 210, 84, "通过搜索与收藏\n再次复用经验", wrap=8)
    c.rect(790, 372, 200, 90, "请求 AI 辅助\n（RAG 检索 / 代码分析）", wrap=12)

    c.line(320, 262, 350, 262, arrow=True)
    c.line(530, 262, 560, 262, arrow=True)
    c.line(760, 262, 790, 262, arrow=True)
    c.line(990, 262, 985, 262, arrow=True)
    c.line(1135, 262, 1170, 262, arrow=True)

    c.note(1110, 235, "是", font_size=20)
    c.note(1005, 355, "否", font_size=20)
    c.polyline([(1060, 321), (1060, 417), (990, 417)], arrow=True)
    c.polyline([(790, 417), (740, 417), (740, 312), (790, 312)], arrow=True)
    c.polyline([(1275, 304), (1275, 420), (1135, 420), (1135, 500)], arrow=True)
    c.line(1030, 542, 970, 542, arrow=True)
    c.line(760, 542, 700, 542, arrow=True)
    c.note(1050, 654, "问题解决后形成知识沉淀闭环", font_size=20)
    return c.render()


def figure_3_2() -> str:
    c = SvgCanvas(1600, 980)
    lanes = [
        (20, 20, 250, 940, "用户"),
        (270, 20, 340, 940, "Web / Electron 客户端"),
        (610, 20, 500, 940, "业务服务层"),
        (1110, 20, 470, 940, "AI / RAG 服务"),
    ]
    for lane in lanes:
        c.lane(*lane)

    c.rect(50, 110, 190, 76, "登录并选择交流空间", wrap=8)
    c.rect(305, 110, 270, 92, "加载会话列表、历史消息\n在线状态与公告", wrap=12)
    c.rect(675, 108, 360, 96, "认证身份并返回消息上下文\n成员信息、未读数与房间状态", wrap=14)

    c.rect(50, 270, 190, 84, "发送文本 / 代码 / 文件", wrap=10)
    c.rect(305, 262, 270, 100, "发起 HTTP 请求并触发\nSocket 发送事件", wrap=12)
    c.rect(675, 252, 360, 120, "校验消息内容\n持久化消息与附件元数据\n更新房间状态并广播", wrap=14)

    c.rect(305, 438, 270, 108, "渲染新消息、引用回复\n支持问题标记、最佳答案\n与表情反馈", wrap=12)
    c.diamond(860, 620, 170, 126, "人工回复是否\n已经解决问题", wrap=7)

    c.rect(1170, 470, 350, 88, "检索历史讨论与相似问题", wrap=12)
    c.rect(1170, 610, 350, 108, "生成 AI 问答 / 代码分析\n并输出阶段总结或提示建议", wrap=13)
    c.rect(675, 740, 360, 96, "将 AI 结果写入消息流\n并再次广播给当前空间", wrap=14)

    c.rect(50, 820, 190, 88, "收藏关键消息", wrap=8)
    c.rect(305, 812, 270, 104, "查看阶段总结\n搜索历史讨论与附件资料", wrap=12)
    c.rect(675, 814, 360, 100, "为后续复用保留收藏、标签\n备注与聊天总结记录", wrap=14)

    c.polyline([(240, 148), (305, 148)], arrow=True)
    c.polyline([(575, 148), (675, 148)], arrow=True)

    c.polyline([(240, 312), (305, 312)], arrow=True)
    c.polyline([(575, 312), (675, 312)], arrow=True)
    c.polyline([(855, 372), (855, 438)], arrow=True)
    c.polyline([(575, 492), (700, 492), (700, 620), (775, 620)], arrow=True)

    c.note(930, 585, "是", font_size=20)
    c.note(1075, 650, "否", font_size=20)
    c.polyline([(945, 620), (1035, 620), (1035, 864), (675, 864)], arrow=True)
    c.polyline([(945, 620), (1170, 620)], dashed=True, arrow=True)
    c.polyline([(1345, 558), (1345, 610)], arrow=True)
    c.polyline([(1170, 664), (1110, 664), (1110, 788), (1035, 788)], arrow=True)

    c.polyline([(675, 864), (575, 864)], arrow=True)
    c.polyline([(305, 864), (240, 864)], arrow=True)
    c.note(790, 945, "核心业务闭环：消息协同 -> AI 补位 -> 结果沉淀与复用", font_size=20)
    return c.render()


def module_block(c: SvgCanvas, x: float, y: float, w: float, h: float, title: str, items: list[str]) -> None:
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" class="box"/>')
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="16" class="header"/>')
    c.text(title, x + w / 2, y + 36, font_size=24, weight="700")
    inner_y = y + 76
    item_h = 42
    for idx, item in enumerate(items):
        box_y = inner_y + idx * (item_h + 12)
        c.add(f'<rect x="{x + 18}" y="{box_y}" width="{w - 36}" height="{item_h}" rx="10" class="subbox"/>')
        c.text(item, x + w / 2, box_y + 27, font_size=20)


def figure_3_3() -> str:
    c = SvgCanvas(1600, 980)
    c.header_rect(620, 60, 360, 72, "智能聊天室系统功能结构")
    module_positions = [30, 340, 650, 960, 1270]
    modules = [
        ("用户与认证", ["邮箱注册 / 登录", "验证码登录", "OAuth 第三方登录", "资料维护与联系人管理"]),
        ("实时通信", ["私聊与群聊", "文本 / 代码 / 文件 / 音频消息", "搜索、未读与在线状态", "引用回复与消息转发"]),
        ("技术聊天室", ["创建专题聊天室", "公开 / 邀请码 / 密码加入", "公告、成员与时效控制", "问题标记与最佳答案"]),
        ("AI 辅助", ["AI 问答与文本解释", "RAG 聊天记录检索", "代码分析与相似问题", "阶段总结与智能提示"]),
        ("知识沉淀", ["收藏关键消息", "标签与备注", "收藏统计", "历史检索与经验复用"]),
    ]
    for x, (title, items) in zip(module_positions, modules):
        module_block(c, x, 220, 280, 310, title, items)
        c.polyline([(800, 132), (800, 180), (x + 140, 180), (x + 140, 220)], arrow=True)

    c.rect(390, 640, 820, 170, "业务主线：用户在交流空间中提出问题，经由即时通信与技术聊天室完成协同讨论；当人工反馈不足时，AI 模块提供问答、检索和总结能力，最终通过收藏与检索机制完成知识沉淀。", wrap=28, font_size=24, cls="subbox")
    c.note(800, 900, "功能模块之间并非孤立存在，而是围绕“提出问题、协同解决、沉淀复用”统一服务。", font_size=20)
    return c.render()


def relation_label(c: SvgCanvas, x: float, y: float, text: str) -> None:
    c.add(f'<rect x="{x - 52}" y="{y - 18}" width="104" height="28" rx="8" fill="#ffffff"/>')
    c.text(text, x, y + 2, font_size=16, weight="700")


def figure_3_4() -> str:
    c = SvgCanvas(1380, 900)
    c.actor(110, 280, "技术交流用户")
    c.actor(1260, 300, "AI 服务")
    c.boundary(270, 70, 860, 740, "智能聊天室系统")

    cases = {
        "help": (500, 180, "发起技术求助"),
        "context": (840, 180, "发送代码 / 日志 / 文件"),
        "room": (500, 330, "创建专题聊天室"),
        "question": (840, 330, "标记问题 / 最佳答案"),
        "search": (500, 500, "检索历史讨论"),
        "ai": (840, 500, "请求 AI 辅助"),
        "summary": (500, 670, "生成讨论总结"),
        "favorite": (840, 670, "收藏关键结论"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 138, 42, label)

    user_lines = ["help", "room", "search", "summary", "favorite", "question"]
    for key in user_lines:
        cx, cy, _ = cases[key]
        c.line(142, 322, cx - 138, cy, cls="line")
    c.line(978, 500, 1228, 500, cls="line")
    c.line(638, 670, 1228, 334, cls="line")

    c.polyline([(638, 180), (730, 180), (730, 180), (702, 180)], dashed=True, arrow=True)
    relation_label(c, 730, 160, "<<include>>")
    c.polyline([(500, 542), (500, 600), (500, 628)], dashed=True, arrow=True)
    relation_label(c, 500, 580, "<<extend>>")
    c.polyline([(840, 542), (840, 600), (840, 628)], dashed=True, arrow=True)
    relation_label(c, 840, 580, "<<extend>>")
    return c.render()


def figure_3_5() -> str:
    c = SvgCanvas(1380, 900)
    c.actor(110, 300, "个人开发者")
    c.actor(1260, 280, "AI 服务")
    c.boundary(270, 70, 860, 740, "智能聊天室系统")

    cases = {
        "ask": (500, 180, "咨询代码 / 框架问题"),
        "rag": (840, 180, "开启 RAG 上下文问答"),
        "explain": (500, 360, "解释选中文本"),
        "analyze": (840, 360, "请求代码分析"),
        "fav": (500, 560, "收藏关键消息"),
        "tag": (840, 560, "添加标签与备注"),
        "search": (670, 710, "检索收藏记录"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 142, 44, label)

    for key in ["ask", "explain", "fav", "search"]:
        cx, cy, _ = cases[key]
        c.line(142, 342, cx - 142, cy, cls="line")
    c.line(142, 342, 698, 710, cls="line")
    c.line(1228, 322, 982, 180, cls="line")
    c.line(1228, 322, 982, 360, cls="line")
    c.line(1228, 322, 642, 360, cls="line")

    c.polyline([(642, 180), (698, 180)], dashed=True, arrow=True)
    relation_label(c, 698, 160, "<<include>>")
    c.polyline([(642, 560), (698, 560)], dashed=True, arrow=True)
    relation_label(c, 698, 540, "<<include>>")
    c.polyline([(840, 222), (840, 302), (840, 318)], dashed=True, arrow=True)
    relation_label(c, 840, 270, "<<extend>>")
    return c.render()


def figure_3_6() -> str:
    c = SvgCanvas(1380, 900)
    c.actor(110, 320, "普通交流用户")
    c.boundary(270, 70, 860, 740, "智能聊天室系统")

    cases = {
        "join": (500, 180, "加入聊天室 / 群聊"),
        "browse": (840, 180, "浏览公告与消息"),
        "send": (500, 360, "发送文本 / 附件"),
        "search": (840, 360, "搜索历史消息"),
        "download": (500, 560, "下载共享资料"),
        "summary": (840, 560, "查看阶段总结"),
        "fav": (670, 710, "收藏重要内容"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 142, 44, label)

    for key in cases:
        cx, cy, _ = cases[key]
        c.line(142, 362, cx - 142, cy, cls="line")

    c.polyline([(642, 180), (700, 180)], dashed=True, arrow=True)
    relation_label(c, 700, 160, "<<include>>")
    c.polyline([(982, 360), (1035, 360), (1035, 560), (982, 560)], dashed=True, arrow=True)
    relation_label(c, 1040, 460, "<<extend>>")
    c.polyline([(500, 602), (500, 660), (528, 710)], dashed=True, arrow=True)
    relation_label(c, 500, 650, "<<extend>>")
    return c.render()


FIGURES = {
    "figure3-1.svg": figure_3_1,
    "figure3-2.svg": figure_3_2,
    "figure3-3.svg": figure_3_3,
    "figure3-4.svg": figure_3_4,
    "figure3-5.svg": figure_3_5,
    "figure3-6.svg": figure_3_6,
}


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for name, builder in FIGURES.items():
        path = FIG_DIR / name
        path.write_text(builder(), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
