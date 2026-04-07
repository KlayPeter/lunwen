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


class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.elements: list[str] = []

    def add(self, element: str) -> None:
        self.elements.append(element)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str | None = None,
        cls: str = "box",
        rx: float = 14,
        font_size: int = 20,
        wrap: int = 10,
    ) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')
        if text is not None:
            self.text_block(x + w / 2, y + h / 2, wrap_text(text, wrap), font_size=font_size)

    def header_rect(self, x: float, y: float, w: float, h: float, text: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="header"/>')
        self.text_block(x + w / 2, y + h / 2, wrap_text(text, 16), font_size=24, weight="700")

    def boundary(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="boundary"/>')
        self.text(label, x + 18, y + 30, anchor="start", font_size=22, weight="700")

    def lane(self, x: float, y: float, w: float, h: float, label: str) -> None:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="lane"/>')
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="56" class="lane-header"/>')
        self.text(label, x + w / 2, y + 34, font_size=22, weight="700")

    def ellipse(self, cx: float, cy: float, rx: float, ry: float, text: str, wrap: int = 8) -> None:
        self.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="usecase"/>')
        self.text_block(cx, cy, wrap_text(text, wrap), font_size=19)

    def diamond(self, cx: float, cy: float, w: float, h: float, text: str, wrap: int = 7) -> None:
        points = [
            (cx, cy - h / 2),
            (cx + w / 2, cy),
            (cx, cy + h / 2),
            (cx - w / 2, cy),
        ]
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polygon points="{pts}" class="decision"/>')
        self.text_block(cx, cy, wrap_text(text, wrap), font_size=19)

    def actor(self, x: float, y: float, label: str) -> None:
        self.add(f'<circle cx="{x}" cy="{y}" r="20" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y+20}" x2="{x}" y2="{y+82}" class="actor-line"/>')
        self.add(f'<line x1="{x-28}" y1="{y+40}" x2="{x+28}" y2="{y+40}" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y+82}" x2="{x-24}" y2="{y+118}" class="actor-line"/>')
        self.add(f'<line x1="{x}" y1="{y+82}" x2="{x+24}" y2="{y+118}" class="actor-line"/>')
        self.text_block(x, y + 155, wrap_text(label, 7), font_size=21, weight="700")

    def line(self, x1: float, y1: float, x2: float, y2: float, arrow: bool = False, dashed: bool = False) -> None:
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line"{dash}{marker}/>')

    def polyline(self, points: list[tuple[float, float]], arrow: bool = False, dashed: bool = False) -> None:
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polyline points="{pts}" fill="none" class="line"{dash}{marker}/>')

    def text(
        self,
        text: str,
        x: float,
        y: float,
        anchor: str = "middle",
        font_size: int = 18,
        weight: str = "500",
        cls: str = "label",
    ) -> None:
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{font_size}" '
            f'font-weight="{weight}" class="{cls}">{escape(text)}</text>'
        )

    def text_block(
        self,
        x: float,
        y: float,
        lines: list[str],
        font_size: int = 18,
        line_height: int | None = None,
        anchor: str = "middle",
        weight: str = "500",
        cls: str = "label",
    ) -> None:
        if line_height is None:
            line_height = int(font_size * 1.35)
        start_y = y - ((len(lines) - 1) * line_height) / 2 + font_size * 0.35
        tspans = []
        for idx, line in enumerate(lines):
            tspans.append(f'<tspan x="{x}" y="{start_y + idx * line_height}">{escape(line)}</tspan>')
        self.add(
            f'<text text-anchor="{anchor}" font-size="{font_size}" font-weight="{weight}" class="{cls}">'
            + "".join(tspans)
            + "</text>"
        )

    def card(self, x: float, y: float, w: float, title: str, items: list[str], item_h: int = 34) -> None:
        h = 60 + 22 + len(items) * item_h
        self.rect(x, y, w, h, cls="box")
        self.rect(x, y, w, 54, cls="header", rx=14)
        self.text(title, x + w / 2, y + 33, font_size=21, weight="700")
        current_y = y + 68
        for item in items:
            self.rect(x + 14, current_y, w - 28, 26, item, cls="subbox", rx=8, font_size=16, wrap=16)
            current_y += item_h

    def relation_label(self, x: float, y: float, text: str) -> None:
        self.add(f'<rect x="{x-58}" y="{y-16}" width="116" height="26" rx="8" fill="#ffffff"/>')
        self.text(text, x, y + 2, font_size=15, weight="700")

    def render(self) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#111111"/>
  </marker>
  <style>
    .label, .note {{
      font-family: "Microsoft YaHei", "Noto Sans SC", "PingFang SC", sans-serif;
      fill: #111111;
    }}
    .box {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.1;
    }}
    .subbox {{
      fill: #f7f7f7;
      stroke: #111111;
      stroke-width: 1.6;
    }}
    .header {{
      fill: #eaeaea;
      stroke: #111111;
      stroke-width: 2.1;
    }}
    .boundary {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.2;
    }}
    .lane {{
      fill: #ffffff;
      stroke: #8a8a8a;
      stroke-width: 1.4;
      stroke-dasharray: 8 6;
    }}
    .lane-header {{
      fill: #efefef;
      stroke: #111111;
      stroke-width: 1.4;
    }}
    .usecase {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.0;
    }}
    .decision {{
      fill: #ffffff;
      stroke: #111111;
      stroke-width: 2.0;
    }}
    .line {{
      stroke: #111111;
      stroke-width: 2.0;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .actor-line {{
      stroke: #111111;
      stroke-width: 2.0;
      fill: none;
      stroke-linecap: round;
    }}
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>
{''.join(self.elements)}
</svg>
'''


def lifeline(c: Canvas, x: float, y1: float, y2: float, label: str) -> None:
    c.rect(x - 80, y1, 160, 48, label, cls="header", font_size=18, wrap=10)
    c.line(x, y1 + 48, x, y2, dashed=True)


def seq_arrow(c: Canvas, x1: float, y: float, x2: float, text: str, dashed: bool = False) -> None:
    c.line(x1, y, x2, y, arrow=True, dashed=dashed)
    c.text(text, (x1 + x2) / 2, y - 10, font_size=16, weight="600")


def fig2_1() -> str:
    c = Canvas(1700, 980)
    layer_x = 110
    width = 1480
    c.rect(layer_x, 150, width, 125, cls="box")
    c.rect(layer_x, 300, width, 150, cls="box")
    c.rect(layer_x, 480, width, 155, cls="box")
    c.rect(layer_x, 665, width, 160, cls="box")

    c.text("接入层", 160, 185, anchor="start", font_size=22, weight="700")
    c.text("前端实现层", 160, 335, anchor="start", font_size=22, weight="700")
    c.text("后端服务层", 160, 515, anchor="start", font_size=22, weight="700")
    c.text("数据与智能层", 160, 700, anchor="start", font_size=22, weight="700")

    c.rect(260, 185, 240, 60, "Web 端", cls="subbox", font_size=20, wrap=8)
    c.rect(545, 185, 240, 60, "Electron 桌面端", cls="subbox", font_size=20, wrap=8)
    c.rect(830, 185, 240, 60, "通知 / 托盘能力", cls="subbox", font_size=20, wrap=9)

    c.card(220, 345, 250, "界面与路由", ["Vue 3", "Vue Router", "Vite"])
    c.card(520, 345, 250, "状态与交互", ["Pinia", "Axios", "Socket.IO Client"])
    c.card(820, 345, 250, "核心页面", ["ChatView", "Content", "ChatRoom", "Favorites"])
    c.card(1120, 345, 250, "桌面适配", ["Electron Main", "Preload", "系统通知"])

    c.card(180, 525, 260, "业务接口", ["Express API", "用户 / 聊天 / 房间", "收藏 / 上传 / 链接预览"])
    c.card(490, 525, 260, "实时通信", ["Socket.IO", "私聊事件", "群聊 / 聊天室广播"])
    c.card(800, 525, 260, "智能服务", ["AIController", "ChatRoomAIController", "AgentController"])
    c.card(1110, 525, 260, "安全能力", ["JWT", "Passport", "邮件验证码 / OAuth"])

    c.card(180, 720, 260, "核心存储", ["MongoDB", "Users", "Messages / GroupMessage"])
    c.card(490, 720, 260, "知识沉淀", ["Favorite", "Summary", "AIConversation"])
    c.card(800, 720, 260, "文件存储", ["Uploads 目录", "fileInfo 快照"])
    c.card(1110, 720, 260, "AI 与检索", ["DeepSeek API", "VectorSearchTool", "MessageIndexer / RAG"])

    for x in [380, 665, 950]:
        c.line(x, 245, x, 300, arrow=True)
    for x in [310, 620, 930, 1240]:
        c.line(x, 450, x, 480, arrow=True)
    for x in [310, 620, 930, 1240]:
        c.line(x, 635, x, 665, arrow=True)
    return c.render()


def fig3_1() -> str:
    c = Canvas(1600, 900)
    c.actor(90, 290, "技术交流用户")
    c.rect(170, 255, 190, 72, "进入系统", wrap=8)
    c.rect(410, 255, 220, 72, "选择群聊或专题聊天室", wrap=10)
    c.rect(690, 245, 240, 92, "提交问题上下文\n文本 / 代码 / 日志 / 文件", wrap=12)
    c.rect(980, 245, 240, 92, "协同讨论\n引用回复 / 标记问题", wrap=12)
    c.diamond(1320, 290, 170, 120, "是否获得\n可行方案", wrap=6)
    c.rect(1240, 520, 220, 82, "收藏关键消息", wrap=8)
    c.rect(960, 520, 220, 82, "生成阶段总结", wrap=8)
    c.rect(680, 520, 220, 82, "搜索与再次复用", wrap=8)
    c.rect(980, 400, 240, 82, "AI 补充分析\nRAG 检索 / 代码分析", wrap=12)
    c.line(110, 312, 170, 291, arrow=True)
    c.line(360, 291, 410, 291, arrow=True)
    c.line(630, 291, 690, 291, arrow=True)
    c.line(930, 291, 980, 291, arrow=True)
    c.line(1220, 291, 1235, 291, arrow=True)
    c.polyline([(1320, 350), (1320, 440), (1220, 440)], arrow=True)
    c.text("否", 1270, 432, font_size=16, weight="700")
    c.text("是", 1370, 270, font_size=16, weight="700")
    c.polyline([(980, 440), (930, 440), (930, 337), (980, 337)], arrow=True)
    c.polyline([(1350, 350), (1350, 480), (1350, 520)], arrow=True)
    c.line(1240, 561, 1180, 561, arrow=True)
    c.line(960, 561, 900, 561, arrow=True)
    return c.render()


def fig3_2() -> str:
    c = Canvas(1800, 1080)
    lanes = [
        (20, 20, 250, 1020, "用户"),
        (270, 20, 360, 1020, "Web / Electron 客户端"),
        (630, 20, 520, 1020, "业务服务层"),
        (1150, 20, 630, 1020, "AI / RAG / 存储"),
    ]
    for lane in lanes:
        c.lane(*lane)

    c.rect(50, 110, 190, 70, "登录并进入交流空间", wrap=9)
    c.rect(320, 100, 260, 92, "加载会话列表\n历史消息与在线状态", wrap=12)
    c.rect(710, 100, 360, 92, "认证身份\n返回房间、成员与上下文数据", wrap=14)

    c.rect(50, 260, 190, 70, "发送消息", wrap=8)
    c.rect(320, 250, 260, 92, "提交文本 / 代码 / 文件\n并同步 Socket 事件", wrap=12)
    c.rect(710, 240, 360, 112, "校验消息内容\n持久化消息与附件信息\n广播给当前会话成员", wrap=14)
    c.rect(1240, 255, 300, 82, "写入 MongoDB\n更新索引队列", wrap=12)

    c.rect(320, 420, 260, 100, "渲染新消息\n支持引用、问题状态\n与最佳答案展示", wrap=12)
    c.diamond(920, 570, 170, 120, "人工回复是否\n已解决问题", wrap=7)
    c.rect(1240, 460, 300, 82, "检索相似问题\n与历史讨论", wrap=12)
    c.rect(1240, 610, 300, 102, "生成 AI 问答\n代码分析与阶段总结", wrap=12)
    c.rect(710, 760, 360, 92, "将 AI 结果写回消息流\n并广播给当前空间", wrap=14)

    c.rect(50, 900, 190, 72, "收藏关键内容", wrap=8)
    c.rect(320, 890, 260, 92, "查看收藏、总结\n与历史检索结果", wrap=12)
    c.rect(710, 890, 360, 92, "保存标签、备注、总结\n供后续检索与复用", wrap=14)

    c.line(240, 145, 320, 145, arrow=True)
    c.line(580, 145, 710, 145, arrow=True)
    c.line(240, 285, 320, 285, arrow=True)
    c.line(580, 285, 710, 285, arrow=True)
    c.line(240, 425, 320, 425, arrow=True)
    c.line(580, 425, 710, 425, arrow=True)
    c.line(1070, 425, 1240, 425, arrow=True)
    c.line(580, 470, 690, 470, arrow=True)
    c.polyline([(920, 630), (920, 730), (890, 730), (890, 760)], arrow=True)
    c.text("是", 960, 555, font_size=16, weight="700")
    c.text("否", 1010, 640, font_size=16, weight="700")
    c.polyline([(1005, 570), (1180, 570), (1180, 500), (1240, 500)], arrow=True)
    c.line(1390, 542, 1390, 610, arrow=True)
    c.polyline([(1240, 660), (1150, 660), (1150, 806), (1070, 806)], arrow=True)
    c.line(240, 936, 320, 936, arrow=True)
    c.line(580, 936, 710, 936, arrow=True)
    return c.render()


def fig3_3() -> str:
    c = Canvas(1760, 980)
    modules = [
        (70, "用户与认证", ["注册 / 登录", "验证码登录", "OAuth 登录", "联系人维护"]),
        (410, "即时通讯", ["私聊 / 群聊", "文本 / 代码 / 文件", "搜索与未读", "在线状态"]),
        (750, "技术聊天室", ["创建聊天室", "公开 / 邀请 / 密码加入", "问题标记", "房间生命周期"]),
        (1090, "AI 辅助", ["问答与解释", "RAG 检索", "代码分析", "阶段总结"]),
        (1430, "知识沉淀", ["收藏快照", "标签与备注", "来源回溯", "统计与复用"]),
    ]
    for x, title, items in modules:
        c.card(x, 220, 260, title, items)
        c.polyline([(880, 118), (880, 180), (x + 130, 180), (x + 130, 220)], arrow=True)

    return c.render()


def fig3_4() -> str:
    c = Canvas(1500, 920)
    c.actor(110, 300, "技术交流用户")
    c.actor(1360, 300, "AI 服务")
    c.boundary(280, 70, 980, 780, "智能聊天室系统")
    cases = {
        "ask": (540, 180, "发起技术求助"),
        "ctx": (920, 180, "发送代码 / 日志 / 文件"),
        "room": (540, 340, "创建专题聊天室"),
        "qa": (920, 340, "标记问题 / 最佳答案"),
        "search": (540, 510, "检索历史讨论"),
        "ai": (920, 510, "请求 AI 辅助"),
        "sum": (540, 680, "生成讨论总结"),
        "fav": (920, 680, "收藏关键结论"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 150, 46, label)
    for key in ["ask", "room", "search", "sum", "fav", "qa"]:
        cx, cy, _ = cases[key]
        c.line(140, 342, cx - 150, cy, arrow=False)
    c.line(1210, 510, 1330, 510)
    c.line(1210, 680, 1330, 332)
    c.polyline([(690, 180), (770, 180)], dashed=True, arrow=True)
    c.relation_label(770, 162, "<<include>>")
    c.polyline([(540, 556), (540, 634)], dashed=True, arrow=True)
    c.relation_label(540, 598, "<<extend>>")
    c.polyline([(920, 556), (920, 634)], dashed=True, arrow=True)
    c.relation_label(920, 598, "<<extend>>")
    return c.render()


def fig3_5() -> str:
    c = Canvas(1500, 920)
    c.actor(110, 300, "个人开发者")
    c.actor(1360, 280, "AI 服务")
    c.boundary(280, 70, 980, 780, "智能聊天室系统")
    cases = {
        "ask": (540, 180, "咨询代码问题"),
        "rag": (920, 180, "开启 RAG 问答"),
        "exp": (540, 360, "解释选中文本"),
        "ana": (920, 360, "请求代码分析"),
        "fav": (540, 560, "收藏关键消息"),
        "tag": (920, 560, "添加标签与备注"),
        "search": (730, 720, "检索收藏记录"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 150, 46, label)
    for key in ["ask", "exp", "fav", "search"]:
        cx, cy, _ = cases[key]
        c.line(140, 342, cx - 150, cy)
    c.line(1210, 180, 1330, 300)
    c.line(1210, 360, 1330, 300)
    c.line(690, 360, 1330, 300)
    c.polyline([(690, 180), (770, 180)], dashed=True, arrow=True)
    c.relation_label(770, 162, "<<include>>")
    c.polyline([(690, 560), (770, 560)], dashed=True, arrow=True)
    c.relation_label(770, 542, "<<include>>")
    c.polyline([(920, 226), (920, 314)], dashed=True, arrow=True)
    c.relation_label(920, 270, "<<extend>>")
    return c.render()


def fig3_6() -> str:
    c = Canvas(1500, 920)
    c.actor(110, 320, "普通交流用户")
    c.boundary(280, 70, 980, 780, "智能聊天室系统")
    cases = {
        "join": (540, 180, "加入聊天室 / 群聊"),
        "browse": (920, 180, "浏览公告与消息"),
        "send": (540, 360, "发送文本 / 附件"),
        "search": (920, 360, "搜索历史消息"),
        "download": (540, 560, "下载共享资料"),
        "summary": (920, 560, "查看阶段总结"),
        "fav": (730, 720, "收藏重要内容"),
    }
    for cx, cy, label in cases.values():
        c.ellipse(cx, cy, 150, 46, label)
    for cx, cy, _ in cases.values():
        c.line(140, 362, cx - 150, cy)
    c.polyline([(690, 180), (770, 180)], dashed=True, arrow=True)
    c.relation_label(770, 162, "<<include>>")
    c.polyline([(1070, 360), (1140, 360), (1140, 560), (1070, 560)], dashed=True, arrow=True)
    c.relation_label(1148, 462, "<<extend>>")
    c.polyline([(540, 606), (540, 666), (580, 720)], dashed=True, arrow=True)
    c.relation_label(540, 650, "<<extend>>")
    return c.render()


def fig4_1() -> str:
    c = Canvas(1800, 1100)
    c.card(70, 180, 250, "接入端", ["Web 客户端", "Electron 桌面端", "系统通知与托盘"])
    c.card(390, 180, 280, "前端应用层", ["ChatView / Content", "ChatRoom / Favorites", "Pinia / Router / Axios"])
    c.card(740, 180, 280, "接入协议层", ["RESTful API", "Socket.IO 事件", "JWT 鉴权"])
    c.card(1090, 180, 280, "业务服务层", ["用户 / 房间 / 消息", "收藏 / 上传 / 链接预览", "AI / Agent 控制器"])
    c.card(1440, 180, 280, "数据与智能层", ["MongoDB", "Uploads", "VectorSearch / DeepSeek"])
    c.card(250, 510, 280, "普通请求链路", ["登录", "资料查询", "收藏管理", "文件上传"])
    c.card(610, 510, 280, "实时通信链路", ["私聊推送", "群聊广播", "在线状态与房间成员"])
    c.card(970, 510, 280, "智能服务链路", ["问答", "代码分析", "聊天总结"])
    c.card(1330, 510, 280, "知识沉淀链路", ["消息索引", "收藏快照", "总结记录"])
    c.polyline([(195, 320), (530, 320), (530, 510)], arrow=True)
    c.polyline([(530, 320), (750, 320)], arrow=True)
    c.polyline([(750, 320), (1110, 320)], arrow=True)
    c.polyline([(1110, 320), (1580, 320)], arrow=True)
    c.polyline([(880, 320), (750, 320), (750, 510)], arrow=True)
    c.polyline([(1230, 320), (1110, 320), (1110, 510)], arrow=True)
    c.polyline([(1580, 320), (1470, 320), (1470, 510)], arrow=True)
    c.line(530, 656, 610, 656, arrow=True)
    c.line(890, 656, 970, 656, arrow=True)
    c.line(1250, 656, 1330, 656, arrow=True)
    return c.render()


def fig4_2() -> str:
    c = Canvas(1800, 1100)
    for lane in [
        (20, 20, 260, 1040, "用户"),
        (280, 20, 350, 1040, "前端界面"),
        (630, 20, 420, 1040, "业务服务"),
        (1050, 20, 360, 1040, "存储与索引"),
        (1410, 20, 370, 1040, "AI 服务"),
    ]:
        c.lane(*lane)
    c.rect(55, 110, 190, 70, "登录系统", wrap=8)
    c.rect(335, 100, 240, 90, "校验令牌\n初始化页面与会话上下文", wrap=12)
    c.rect(705, 100, 270, 90, "返回用户信息\n会话列表与房间数据", wrap=12)
    c.rect(55, 250, 190, 70, "进入聊天空间", wrap=8)
    c.rect(335, 240, 240, 90, "加载消息历史\n建立 Socket 连接", wrap=12)
    c.rect(705, 240, 270, 90, "订阅私聊 / 群聊 / 聊天室事件", wrap=12)
    c.rect(55, 390, 190, 70, "发送消息", wrap=8)
    c.rect(335, 380, 240, 90, "提交文本 / 代码 / 文件\n并刷新消息区", wrap=12)
    c.rect(705, 370, 270, 110, "校验权限与消息类型\n写入消息记录\n广播实时事件", wrap=12)
    c.rect(1100, 390, 260, 70, "持久化消息\n加入索引队列", wrap=10)
    c.diamond(1500, 565, 160, 120, "是否触发\nAI 辅助", wrap=6)
    c.rect(55, 700, 190, 70, "查看 AI 结果", wrap=8)
    c.rect(335, 690, 240, 90, "渲染流式回复\n或总结结果", wrap=12)
    c.rect(705, 680, 270, 110, "调用控制器\n组织上下文并写回消息流", wrap=12)
    c.rect(1100, 700, 260, 70, "读取历史消息\n与收藏快照", wrap=10)
    c.rect(1470, 700, 240, 90, "问答 / 代码分析\n总结生成", wrap=12)
    c.rect(55, 880, 190, 70, "收藏或回看结果", wrap=8)
    c.rect(335, 870, 240, 90, "进入收藏页\n搜索与再次复用", wrap=12)
    c.rect(705, 870, 270, 90, "保存收藏快照\n写入标签、备注与总结", wrap=12)
    c.line(245, 145, 335, 145, arrow=True)
    c.line(575, 145, 705, 145, arrow=True)
    c.line(245, 285, 335, 285, arrow=True)
    c.line(575, 285, 705, 285, arrow=True)
    c.line(245, 425, 335, 425, arrow=True)
    c.line(575, 425, 705, 425, arrow=True)
    c.line(975, 425, 1100, 425, arrow=True)
    c.polyline([(1360, 425), (1500, 425), (1500, 505)], arrow=True)
    c.text("是", 1538, 544, font_size=16, weight="700")
    c.text("否", 1565, 625, font_size=16, weight="700")
    c.polyline([(1500, 625), (1500, 745), (1470, 745)], arrow=True)
    c.polyline([(1490, 565), (1410, 565), (1410, 745)], arrow=True)
    c.line(245, 915, 335, 915, arrow=True)
    c.line(575, 915, 705, 915, arrow=True)
    return c.render()


def fig4_3() -> str:
    c = Canvas(1800, 1000)
    c.rect(760, 140, 280, 72, "智能聊天室系统", cls="header", font_size=24, wrap=12)
    groups = [
        (120, 320, "用户管理模块", ["注册与登录", "验证码登录", "OAuth 登录", "好友与资料管理"]),
        (470, 320, "即时通讯模块", ["私聊 / 群聊", "消息检索", "在线状态", "多类型消息"]),
        (820, 320, "聊天室模块", ["聊天室创建", "加入策略", "房间成员", "问题状态"]),
        (1170, 320, "AI 助手模块", ["问答", "代码分析", "RAG 检索", "阶段总结"]),
        (1520, 320, "收藏模块", ["收藏快照", "标签备注", "来源回溯", "统计分析"]),
    ]
    for x, y, title, items in groups:
        c.card(x - 110, y, 220, title, items)
        c.polyline([(900, 212), (900, 260), (x, 260), (x, y)], arrow=True)
    return c.render()


def fig4_4() -> str:
    c = Canvas(1700, 920)
    c.rect(90, 380, 150, 60, "开始", cls="header", font_size=20, wrap=8)
    c.rect(300, 360, 190, 100, "选择认证方式\n邮箱密码 / 验证码 / OAuth", wrap=12)
    c.diamond(590, 410, 170, 120, "是否为\n本地认证", wrap=6)
    c.rect(760, 260, 220, 80, "校验邮箱与密码\n或验证码", wrap=11)
    c.rect(760, 520, 220, 80, "跳转 OAuth 平台\n并接收回调", wrap=11)
    c.rect(1070, 390, 240, 80, "统一生成 JWT\n写入用户身份信息", wrap=11)
    c.rect(1400, 390, 190, 80, "访问受保护资源", wrap=10)
    c.line(240, 410, 300, 410, arrow=True)
    c.line(490, 410, 505, 410, arrow=True)
    c.text("是", 665, 340, font_size=16, weight="700")
    c.text("否", 665, 500, font_size=16, weight="700")
    c.polyline([(675, 410), (720, 410), (720, 300), (760, 300)], arrow=True)
    c.polyline([(675, 410), (720, 410), (720, 560), (760, 560)], arrow=True)
    c.polyline([(980, 300), (1030, 300), (1030, 430), (1070, 430)], arrow=True)
    c.polyline([(980, 560), (1030, 560), (1030, 430), (1070, 430)], arrow=True)
    c.line(1310, 430, 1400, 430, arrow=True)
    return c.render()


def fig4_5() -> str:
    c = Canvas(1700, 920)
    c.rect(100, 380, 160, 60, "开始发送", cls="header", font_size=20, wrap=8)
    c.rect(320, 360, 220, 100, "前端组织消息体\n文本 / 文件 / 代码", wrap=12)
    c.rect(610, 360, 220, 100, "服务端校验权限\n解析消息类型", wrap=12)
    c.rect(900, 360, 220, 100, "实时广播\nSocket.IO 推送", wrap=12)
    c.rect(1190, 360, 220, 100, "持久化到消息集合\n并更新房间状态", wrap=12)
    c.rect(610, 560, 220, 80, "加入索引队列\n供 AI 检索使用", wrap=11)
    c.rect(320, 560, 220, 80, "客户端刷新消息区\n更新未读与已读状态", wrap=12)
    c.line(260, 410, 320, 410, arrow=True)
    c.line(540, 410, 610, 410, arrow=True)
    c.line(830, 410, 900, 410, arrow=True)
    c.line(1120, 410, 1190, 410, arrow=True)
    c.polyline([(1300, 460), (1300, 600), (830, 600)], arrow=True)
    c.polyline([(900, 410), (870, 410), (870, 600), (830, 600)], arrow=True)
    c.polyline([(610, 600), (540, 600)], arrow=True)
    return c.render()


def fig4_6() -> str:
    c = Canvas(1700, 940)
    c.rect(90, 390, 150, 60, "创建聊天室", cls="header", font_size=20, wrap=8)
    c.rect(300, 360, 220, 120, "填写房间名称\n技术方向\n加入方式与有效时长", wrap=12)
    c.rect(590, 360, 220, 120, "生成 RoomID\n初始化成员与系统消息", wrap=12)
    c.diamond(910, 420, 170, 120, "加入方式", wrap=6)
    c.rect(1110, 210, 220, 80, "公开加入\n自动进入房间", wrap=10)
    c.rect(1110, 390, 220, 80, "邀请码加入\n校验 inviteCode", wrap=10)
    c.rect(1110, 570, 220, 80, "密码加入\n校验 password", wrap=10)
    c.rect(1410, 390, 190, 80, "广播消息\n同步成员状态", wrap=10)
    c.rect(1410, 630, 190, 80, "到期清理\n自动失效", wrap=10)
    c.line(240, 420, 300, 420, arrow=True)
    c.line(520, 420, 590, 420, arrow=True)
    c.line(810, 420, 825, 420, arrow=True)
    c.text("公开", 1010, 250, font_size=16, weight="700")
    c.text("邀请码", 1018, 420, font_size=16, weight="700")
    c.text("密码", 1010, 600, font_size=16, weight="700")
    c.polyline([(995, 420), (1060, 420), (1060, 250), (1110, 250)], arrow=True)
    c.polyline([(995, 420), (1110, 430)], arrow=True)
    c.polyline([(995, 420), (1060, 420), (1060, 610), (1110, 610)], arrow=True)
    c.polyline([(1330, 250), (1370, 250), (1370, 430), (1410, 430)], arrow=True)
    c.line(1330, 430, 1410, 430, arrow=True)
    c.polyline([(1330, 610), (1370, 610), (1370, 430), (1410, 430)], arrow=True)
    c.polyline([(1505, 470), (1505, 630)], arrow=True)
    return c.render()


def fig4_7() -> str:
    c = Canvas(1800, 1000)
    xs = [120, 420, 760, 1080, 1380, 1640]
    labels = ["用户", "前端页面", "ChatRoomAIController", "VectorSearchTool", "大模型接口", "消息存储"]
    for x, label in zip(xs, labels):
        lifeline(c, x, 140, 900, label)
    seq_arrow(c, 120, 220, 420, "1. 提交问题")
    seq_arrow(c, 420, 280, 760, "2. 调用 askAI / askAIStream")
    seq_arrow(c, 760, 340, 1080, "3. 检索历史消息")
    seq_arrow(c, 1080, 400, 760, "4. 返回相似上下文", dashed=True)
    seq_arrow(c, 760, 470, 1380, "5. 组织提示词并调用模型")
    seq_arrow(c, 1380, 540, 760, "6. 返回回答内容", dashed=True)
    seq_arrow(c, 760, 610, 1640, "7. 写入 AI 消息 / 总结记录")
    seq_arrow(c, 760, 700, 420, "8. 返回流式或完整响应", dashed=True)
    seq_arrow(c, 420, 780, 120, "9. 渲染回复并更新聊天界面", dashed=True)
    return c.render()


def fig4_8() -> str:
    c = Canvas(1700, 920)
    c.rect(100, 380, 150, 60, "发起收藏", cls="header", font_size=20, wrap=8)
    c.rect(320, 360, 220, 100, "读取原始消息\n与发送者信息", wrap=12)
    c.rect(610, 360, 220, 100, "构造收藏快照\n内容 / 附件 / 代码信息", wrap=12)
    c.rect(900, 360, 220, 100, "补充标签与备注", wrap=12)
    c.rect(1190, 360, 220, 100, "保存 Favorite 记录", wrap=12)
    c.rect(610, 560, 220, 80, "按关键词 / 标签查询", wrap=12)
    c.rect(900, 560, 220, 80, "打开收藏详情\n并回溯消息来源", wrap=12)
    c.line(250, 410, 320, 410, arrow=True)
    c.line(540, 410, 610, 410, arrow=True)
    c.line(830, 410, 900, 410, arrow=True)
    c.line(1120, 410, 1190, 410, arrow=True)
    c.polyline([(1300, 460), (1300, 600), (830, 600)], arrow=True)
    c.line(830, 600, 900, 600, arrow=True)
    return c.render()


def fig4_9() -> str:
    c = Canvas(1700, 980)
    c.rect(120, 150, 1080, 720, cls="box")
    c.rect(150, 190, 120, 640, "导航区\n首页\n联系人\n聊天室\n收藏", cls="subbox", font_size=20, wrap=6)
    c.rect(300, 190, 240, 640, "会话区\n最近聊天\n群聊列表\n聊天室列表\n搜索入口", cls="subbox", font_size=20, wrap=7)
    c.rect(570, 190, 440, 120, "消息头部\n当前会话信息 / 成员 / 房间详情按钮", cls="subbox", font_size=20, wrap=16)
    c.rect(570, 340, 440, 360, "消息区\n文本、代码、文件、引用消息\n问题标记、最佳答案、表情反馈", cls="subbox", font_size=20, wrap=18)
    c.rect(570, 730, 440, 100, "输入区\n文本输入、文件上传、代码发送、AI 入口", cls="subbox", font_size=20, wrap=18)
    c.rect(1040, 190, 130, 640, "右侧扩展区\nAI 面板\n收藏详情\n聊天总结", cls="subbox", font_size=20, wrap=6)
    c.rect(1290, 250, 280, 520, cls="box")
    c.rect(1320, 290, 220, 90, "移动端消息头", cls="subbox", font_size=18, wrap=12)
    c.rect(1320, 410, 220, 210, "消息区", cls="subbox", font_size=18, wrap=10)
    c.rect(1320, 650, 220, 60, "底部输入栏", cls="subbox", font_size=18, wrap=10)
    c.rect(1320, 730, 220, 30, "底部导航：聊天 / 聊天室 / 收藏", cls="subbox", font_size=14, wrap=16)
    return c.render()


def fig4_10() -> str:
    c = Canvas(1800, 1100)
    c.card(80, 180, 240, "Users", ["uID", "uName", "uEmail", "Friends", "provider"])
    c.card(440, 150, 250, "Room", ["RoomID", "RoomName", "type", "joinType", "Members"])
    c.card(780, 150, 260, "Messages", ["from", "to", "content", "messageType", "isRead"])
    c.card(1130, 150, 280, "GroupMessage", ["roomId", "fromName", "content", "questionStatus", "reactions"])
    c.card(1480, 180, 220, "Favorite", ["userId", "messageId", "chatId", "tags", "note"])
    c.card(260, 620, 260, "AIConversation", ["userId", "role", "messages", "updatedAt"])
    c.card(880, 620, 260, "Summary", ["userId", "chatType", "targetId", "summary"])
    c.line(320, 250, 440, 250)
    c.text("1 : N\n创建 / 加入", 380, 230, font_size=16, weight="600")
    c.line(320, 310, 260, 620)
    c.text("1 : N\n发起 AI 对话", 250, 470, font_size=16, weight="600")
    c.line(520, 620, 880, 620)
    c.text("1 : N\n生成总结", 700, 600, font_size=16, weight="600")
    c.line(690, 250, 780, 250)
    c.text("1 : N\n私聊消息", 735, 230, font_size=16, weight="600")
    c.line(690, 310, 1130, 310)
    c.text("1 : N\n群聊 / 聊天室消息", 910, 290, font_size=16, weight="600")
    c.line(1410, 250, 1480, 250)
    c.text("1 : N\n收藏快照", 1445, 230, font_size=16, weight="600")
    c.line(1260, 390, 1560, 390)
    c.text("消息来源回溯", 1410, 375, font_size=16, weight="600")
    c.line(320, 350, 1480, 350)
    c.text("Users 与 Favorite 通过 userId 关联", 920, 338, font_size=15, weight="600")
    return c.render()


FIGURES: dict[str, tuple[str, callable]] = {
    "figure2-1.svg": ("2_1figure.png", fig2_1),
    "figure3-1.svg": ("3_1figure.png", fig3_1),
    "figure3-2.svg": ("3_2figure.png", fig3_2),
    "figure3-3.svg": ("3_3figure.png", fig3_3),
    "figure3-4.svg": ("3_4figure.png", fig3_4),
    "figure3-5.svg": ("3_5figure.png", fig3_5),
    "figure3-6.svg": ("3_6figure.png", fig3_6),
    "figure4-1.svg": ("4_1figure.png", fig4_1),
    "figure4-2.svg": ("4_2figure.png", fig4_2),
    "figure4-3.svg": ("4_3figure.png", fig4_3),
    "figure4-4.svg": ("4_4figure.png", fig4_4),
    "figure4-5.svg": ("4_5figure.png", fig4_5),
    "figure4-6.svg": ("4_6figure.png", fig4_6),
    "figure4-7.svg": ("4_7figure.png", fig4_7),
    "figure4-8.svg": ("4_8figure.png", fig4_8),
    "figure4-9.svg": ("4_9figure.png", fig4_9),
    "figure4-10.svg": ("4_10figure.png", fig4_10),
}


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for svg_name, (_, builder) in FIGURES.items():
        path = FIG_DIR / svg_name
        path.write_text(builder(), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
