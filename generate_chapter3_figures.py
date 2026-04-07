# -*- coding: utf-8 -*-
from __future__ import annotations

from html import escape
from pathlib import Path


WIDTH = 1600
HEIGHT = 1100
OUT_DIR = Path(r"F:\personal\poject\Mini-Chat-Bar-main\docs\latex\figures")
FONT_STACK = "Microsoft YaHei, SimSun, Arial, sans-serif"


def svg_header(width: int = WIDTH, height: int = HEIGHT) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">',
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#000000"/>',
        "</marker>",
        "</defs>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<g stroke="#000000" fill="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" font-family="{FONT_STACK}">',
    ]


def svg_footer() -> list[str]:
    return ["</g>", "</svg>"]


def text_block(
    x: float,
    y: float,
    text: str,
    *,
    size: int = 26,
    weight: str = "normal",
    anchor: str = "middle",
) -> str:
    lines = text.split("\n")
    line_gap = size * 1.35
    start_y = y - ((len(lines) - 1) * line_gap) / 2
    tspans = []
    for idx, line in enumerate(lines):
        dy = "0" if idx == 0 else f"{line_gap}"
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{start_y}" fill="#000000" stroke="none" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
        + "".join(tspans)
        + "</text>"
    )


def rect_box(
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    size: int = 25,
    rx: int = 14,
    weight: str = "normal",
    dashed: bool = False,
) -> list[str]:
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}"{dash}/>',
        text_block(x + w / 2, y + h / 2, text, size=size, weight=weight),
    ]


def ellipse_usecase(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    text: str,
    *,
    size: int = 23,
) -> list[str]:
    return [
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>',
        text_block(cx, cy, text, size=size),
    ]


def diamond_box(
    cx: float,
    cy: float,
    w: float,
    h: float,
    text: str,
    *,
    size: int = 24,
) -> list[str]:
    x1 = cx
    y1 = cy - h / 2
    x2 = cx + w / 2
    y2 = cy
    x3 = cx
    y3 = cy + h / 2
    x4 = cx - w / 2
    y4 = cy
    return [
        f'<polygon points="{x1},{y1} {x2},{y2} {x3},{y3} {x4},{y4}"/>',
        text_block(cx, cy, text, size=size, weight="bold"),
    ]


def line_arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    dashed: bool = False,
) -> str:
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#arrow)"{dash}/>'


def poly_arrow(points: list[tuple[float, float]], *, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" marker-end="url(#arrow)"{dash}/>'


def actor(x: float, y: float, label: str) -> list[str]:
    head_y = y
    body_y = y + 34
    return [
        f'<circle cx="{x}" cy="{head_y}" r="20"/>',
        f'<line x1="{x}" y1="{head_y + 20}" x2="{x}" y2="{body_y + 70}"/>',
        f'<line x1="{x - 34}" y1="{body_y}" x2="{x + 34}" y2="{body_y}"/>',
        f'<line x1="{x}" y1="{body_y + 70}" x2="{x - 30}" y2="{body_y + 120}"/>',
        f'<line x1="{x}" y1="{body_y + 70}" x2="{x + 30}" y2="{body_y + 120}"/>',
        text_block(x, body_y + 165, label, size=26, weight="bold"),
    ]


def boundary(x: float, y: float, w: float, h: float, title: str) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10"/>',
        text_block(x + 24, y + 30, title, size=24, weight="bold", anchor="start"),
    ]


def write_svg(name: str, parts: list[str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    content = "\n".join(svg_header() + parts + svg_footer()) + "\n"
    (OUT_DIR / name).write_text(content, encoding="utf-8")


def figure_3_1() -> None:
    parts: list[str] = []
    parts += actor(90, 325, "技术交流人群")
    boxes = [
        (210, 230, 180, 96, "进入系统\n登录并进入主界面"),
        (460, 230, 180, 96, "选择交流空间"),
        (710, 230, 200, 96, "发起技术问题\n文本 / 代码 / 文件"),
        (980, 230, 210, 96, "获得反馈\n成员回复 / 引用补充\nAI辅助 / 总结建议"),
        (1260, 230, 190, 96, "沉淀关键结果\n收藏 / 标签 / 备注"),
        (1490, 230, 90, 96, "检索\n复用"),
    ]
    for box in boxes:
        parts += rect_box(*box, size=24, weight="bold" if box[0] == 460 else "normal")

    parts += rect_box(400, 420, 90, 56, "私聊", size=22)
    parts += rect_box(515, 420, 90, 56, "群聊", size=22)
    parts += rect_box(630, 420, 120, 56, "技术聊天室", size=20)
    parts.append(line_arrow(124, 278, 210, 278))
    parts.append(line_arrow(390, 278, 460, 278))
    parts.append(line_arrow(640, 278, 710, 278))
    parts.append(line_arrow(910, 278, 980, 278))
    parts.append(line_arrow(1190, 278, 1260, 278))
    parts.append(line_arrow(1450, 278, 1490, 278))
    parts.append(poly_arrow([(550, 326), (550, 380), (445, 380), (445, 420)]))
    parts.append(poly_arrow([(550, 326), (550, 390), (560, 390), (560, 420)]))
    parts.append(poly_arrow([(550, 326), (550, 380), (690, 380), (690, 420)]))
    parts += rect_box(
        330,
        630,
        940,
        110,
        "覆盖实时沟通、AI辅助分析、关键内容沉淀与后续复用",
        size=27,
        dashed=True,
        weight="bold",
    )
    parts.append(
        poly_arrow(
            [(1535, 326), (1535, 560), (810, 560), (810, 326)],
        )
    )
    parts.append(text_block(1170, 530, "再次调用既有结论", size=22, anchor="start"))
    write_svg("3_1figure.svg", parts)


def figure_3_2() -> None:
    parts: list[str] = []
    parts += rect_box(620, 70, 250, 86, "登录认证\n邮箱 / 验证码 / OAuth", weight="bold")
    parts += rect_box(620, 200, 250, 86, "选择会话空间\n私聊 / 群聊 / 聊天室")
    parts += rect_box(620, 330, 250, 86, "加载上下文\n历史消息 / 在线状态 / 公告资料")
    parts += rect_box(620, 460, 250, 86, "发送消息\n文本 / 代码 / 图片 / 文件")
    parts += rect_box(1110, 460, 280, 86, "后端校验与权限检查\nJWT / 参数 / 会话边界")
    parts += rect_box(1110, 610, 280, 86, "持久化与服务处理\nMongoDB / 附件 / 业务路由")
    parts += rect_box(620, 610, 250, 86, "实时推送与界面更新\nSocket.IO / REST 返回")
    parts += rect_box(620, 760, 250, 86, "成员回复与补充\n引用回复 / 方案比较 / 继续追问")
    parts += diamond_box(745, 930, 260, 120, "问题\n是否解决", size=25)
    parts += rect_box(1110, 880, 280, 96, "调用AI问答与总结\nRAG 检索 / 流式回答 / 讨论摘要")
    parts += rect_box(620, 1010, 250, 86, "结果沉淀\n收藏 / 标签 / 备注")
    parts += rect_box(1020, 1010, 280, 86, "再次复用\n关键词搜索 / 收藏回看 / 历史检索")

    for y1, y2 in [(156, 200), (286, 330), (416, 460)]:
        parts.append(line_arrow(745, y1, 745, y2))
    parts.append(line_arrow(870, 503, 1110, 503))
    parts.append(line_arrow(1250, 546, 1250, 610))
    parts.append(line_arrow(1110, 653, 870, 653))
    parts.append(line_arrow(745, 696, 745, 760))
    parts.append(line_arrow(745, 846, 745, 870))
    parts.append(poly_arrow([(875, 930), (980, 930), (980, 928), (1110, 928)]))
    parts.append(poly_arrow([(1250, 976), (1250, 980), (1250, 803), (870, 803)]))
    parts.append(text_block(1135, 790, "未解决", size=22))
    parts.append(text_block(690, 986, "已解决", size=22))
    parts.append(line_arrow(745, 990, 745, 1010))
    parts.append(line_arrow(870, 1053, 1020, 1053))
    parts += rect_box(
        350,
        875,
        170,
        120,
        "业务闭环\n进入空间\n→ 讨论协作\n→ 结果沉淀\n→ 再次复用",
        size=22,
        dashed=True,
    )
    write_svg("3_2figure.svg", parts)


def figure_3_3() -> None:
    parts: list[str] = []
    parts += rect_box(620, 70, 360, 90, "智能聊天室系统", size=30, weight="bold")
    parts += rect_box(
        110,
        250,
        360,
        210,
        "用户管理模块\n· 邮箱 / 验证码登录\n· OAuth 第三方登录\n· 资料维护与联系人\n· 在线状态与权限校验",
        size=24,
    )
    parts += rect_box(
        620,
        250,
        360,
        210,
        "即时通讯模块\n· 私聊与群聊消息\n· 文本 / 代码 / 文件传输\n· 引用转发与消息搜索\n· 已读状态与实时同步",
        size=24,
    )
    parts += rect_box(
        1130,
        250,
        360,
        210,
        "聊天室模块\n· 聊天室创建与加入\n· 公开 / 密码 / 邀请码策略\n· 公告、成员与在线统计\n· 时长控制与自动过期",
        size=24,
    )
    parts += rect_box(
        365,
        620,
        360,
        210,
        "AI助手智能问答模块\n· 技术问答与流式回答\n· RAG 历史检索\n· 代码解释与错误分析\n· 聊天总结与上下文对话",
        size=24,
    )
    parts += rect_box(
        875,
        620,
        360,
        210,
        "收藏模块\n· 消息收藏与来源回溯\n· 标签、备注与分类\n· 关键字筛选检索\n· 个人知识沉淀复用",
        size=24,
    )

    parts.append(line_arrow(800, 160, 290, 250))
    parts.append(line_arrow(800, 160, 800, 250))
    parts.append(line_arrow(800, 160, 1310, 250))
    parts.append(line_arrow(800, 460, 545, 620))
    parts.append(line_arrow(980, 460, 1055, 620))
    parts.append(line_arrow(1310, 460, 545, 620))
    parts.append(line_arrow(1310, 460, 1055, 620))
    parts.append(poly_arrow([(725, 725), (800, 725), (875, 725)]))
    parts.append(text_block(800, 695, "知识沉淀与智能辅助联动", size=22))
    write_svg("3_3figure.svg", parts)


def figure_3_4() -> None:
    parts: list[str] = []
    parts += actor(110, 360, "技术交流人群")
    parts += boundary(300, 90, 1230, 870, "智能聊天室系统")
    parts += ellipse_usecase(620, 220, 170, 56, "发起技术问题求助")
    parts += ellipse_usecase(980, 220, 170, 56, "发送代码 / 日志 / 文件")
    parts += ellipse_usecase(1330, 220, 150, 56, "调用AI辅助分析")
    parts += ellipse_usecase(620, 470, 170, 56, "创建专题聊天室")
    parts += ellipse_usecase(980, 470, 170, 56, "组织多人集中讨论")
    parts += ellipse_usecase(620, 720, 170, 56, "收藏关键结论")
    parts += ellipse_usecase(980, 720, 210, 56, "搜索历史消息 / 回看总结")

    for cy in [220, 470, 720]:
        parts.append(line_arrow(170, cy, 450, cy))
    parts.append(line_arrow(170, 785, 770, 785))
    parts.append(line_arrow(170, 650, 770, 650))
    parts.append(line_arrow(790, 220, 810, 220))
    parts.append(line_arrow(1150, 220, 1180, 220))
    parts.append(line_arrow(790, 470, 810, 470))
    parts.append(poly_arrow([(620, 276), (620, 330), (980, 330), (980, 414)]))
    parts.append(poly_arrow([(980, 526), (980, 600), (620, 600), (620, 664)]))
    parts.append(poly_arrow([(620, 276), (620, 340), (1330, 340), (1330, 164)], dashed=True))
    parts.append(text_block(910, 320, "<<include>>", size=18))
    parts.append(poly_arrow([(620, 526), (620, 570), (980, 570), (980, 664)], dashed=True))
    parts.append(text_block(905, 560, "<<include>>", size=18))
    write_svg("3_4figure.svg", parts)


def figure_3_5() -> None:
    parts: list[str] = []
    parts += actor(120, 360, "个人开发者")
    parts += boundary(300, 100, 1230, 860, "智能聊天室系统")
    parts += ellipse_usecase(670, 220, 180, 56, "向AI助手提问")
    parts += ellipse_usecase(1080, 220, 170, 56, "继续追问代码细节")
    parts += ellipse_usecase(670, 460, 180, 56, "创建临时技术聊天室")
    parts += ellipse_usecase(1080, 460, 190, 56, "收藏AI回复 / 关键消息")
    parts += ellipse_usecase(670, 720, 170, 56, "添加标签与备注")
    parts += ellipse_usecase(1080, 720, 210, 56, "检索收藏并回看原会话")

    parts.append(line_arrow(180, 220, 490, 220))
    parts.append(line_arrow(180, 460, 490, 460))
    parts.append(line_arrow(180, 720, 490, 720))
    parts.append(line_arrow(180, 600, 900, 600))
    parts.append(line_arrow(850, 220, 910, 220))
    parts.append(line_arrow(860, 460, 890, 460))
    parts.append(line_arrow(840, 720, 870, 720))
    parts.append(poly_arrow([(670, 276), (670, 330), (1080, 330), (1080, 164)], dashed=True))
    parts.append(text_block(935, 320, "<<include>>", size=18))
    parts.append(poly_arrow([(1080, 516), (1080, 590), (670, 590), (670, 664)], dashed=True))
    parts.append(text_block(890, 575, "<<include>>", size=18))
    parts.append(poly_arrow([(1080, 516), (1080, 600), (1080, 664)]))
    write_svg("3_5figure.svg", parts)


def figure_3_6() -> None:
    parts: list[str] = []
    parts += actor(120, 360, "普通交流用户")
    parts += boundary(300, 100, 1230, 860, "智能聊天室系统")
    parts += ellipse_usecase(680, 220, 160, 56, "加入聊天室")
    parts += ellipse_usecase(1080, 220, 220, 56, "浏览公告 / 成员 / 历史消息")
    parts += ellipse_usecase(680, 460, 190, 56, "发送文本或共享资料")
    parts += ellipse_usecase(1080, 460, 170, 56, "检索历史消息")
    parts += ellipse_usecase(680, 720, 150, 56, "下载共享文件")
    parts += ellipse_usecase(1080, 720, 160, 56, "收藏高频结论")

    parts.append(line_arrow(180, 220, 520, 220))
    parts.append(line_arrow(180, 460, 490, 460))
    parts.append(line_arrow(180, 720, 530, 720))
    parts.append(line_arrow(180, 590, 910, 590))
    parts.append(line_arrow(840, 220, 860, 220))
    parts.append(line_arrow(870, 460, 910, 460))
    parts.append(line_arrow(830, 720, 920, 720))
    parts.append(poly_arrow([(680, 276), (680, 330), (1080, 330), (1080, 164)], dashed=True))
    parts.append(text_block(920, 320, "<<include>>", size=18))
    parts.append(poly_arrow([(1080, 516), (1080, 590), (680, 590), (680, 664)], dashed=True))
    parts.append(text_block(900, 575, "<<include>>", size=18))
    write_svg("3_6figure.svg", parts)


def main() -> None:
    figure_3_1()
    figure_3_2()
    figure_3_3()
    figure_3_4()
    figure_3_5()
    figure_3_6()
    print("chapter3 figures generated")


if __name__ == "__main__":
    main()
