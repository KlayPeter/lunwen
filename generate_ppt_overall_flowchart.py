from __future__ import annotations

import subprocess
from pathlib import Path

from generate_chapter234_figures import Canvas


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
IMG_DIR = ROOT / "img"
IMG2_DIR = ROOT / "img 2"

SVG_PATH = FIG_DIR / "ppt_adoption_front_backend_overall_flow.svg"
SVG_COPY_PATH = IMG2_DIR / "PPT_系统前后端总体流程图.svg"
PNG_PATH = IMG_DIR / "PPT_系统前后端总体流程图.png"

CANVAS_WIDTH = 1900
CANVAS_HEIGHT = 1360

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def rect(
    canvas: Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    cls: str = "box",
    font_size: int = 22,
    wrap: int = 12,
) -> tuple[float, float, float, float]:
    canvas.rect(x, y, w, h, text, cls=cls, font_size=font_size, wrap=wrap)
    return x, y, w, h


def top_center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, w, _ = box
    return x + w / 2, y


def bottom_center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, w, h = box
    return x + w / 2, y + h


def left_center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, _, h = box
    return x, y + h / 2


def right_center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, w, h = box
    return x + w, y + h / 2


def build_svg() -> str:
    c = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    c.boundary(70, 60, 1760, 600, "前端业务流程（管理端 Vue / 用户端 UniApp）")
    c.boundary(70, 720, 1760, 560, "后端处理流程（Spring Boot）")

    c.header_rect(760, 110, 380, 72, "访问系统")
    c.diamond(950, 255, 240, 120, "角色选择", wrap=6)

    c.boundary(140, 320, 760, 225, "宠物领养用户端")
    c.boundary(1000, 320, 760, 225, "管理员端")

    user_login = rect(c, 185, 390, 170, 66, "登录 / 注册")
    user_browse = rect(c, 395, 390, 190, 66, "浏览宠物信息\n社区内容")
    user_submit = rect(c, 625, 390, 220, 66, "AI识图上报\n提交领养申请")
    user_center = rect(c, 365, 485, 300, 66, "个人中心查看状态\n与反馈回复")

    admin_login = rect(c, 1045, 390, 170, 66, "管理员登录")
    admin_clue = rect(c, 1255, 390, 205, 66, "查看线索\n添加进展记录")
    admin_pet = rect(c, 1495, 390, 220, 66, "发布 / 编辑\n流浪宠物信息")
    admin_audit = rect(c, 1230, 485, 330, 66, "审核领养申请\n社区内容与评论")

    request = rect(c, 640, 570, 620, 68, "统一接口：前端封装请求并发起 HTTP 调用", cls="header", font_size=24, wrap=22)
    page_update = rect(c, 1320, 570, 360, 68, "页面渲染 / 列表刷新 / 状态回显", cls="subbox", font_size=22, wrap=18)

    controller = rect(c, 760, 790, 380, 70, "Controller 接收请求", cls="header", font_size=24, wrap=18)
    service = rect(c, 705, 885, 490, 78, "Service 业务层校验\n身份、参数与业务规则", font_size=23, wrap=20)
    error_box = rect(c, 1380, 885, 270, 78, "返回错误信息", cls="subbox", font_size=23, wrap=12)

    c.diamond(950, 1035, 240, 120, "业务类型", wrap=8)

    mysql_box = rect(c, 160, 955, 250, 64, "MySQL 数据操作", font_size=22, wrap=16)
    redis_box = rect(c, 160, 1050, 250, 64, "Redis 缓存处理", font_size=22, wrap=16)
    baidu_ai = rect(c, 1490, 955, 250, 64, "百度 AI 识图接口", font_size=22, wrap=16)
    deepseek = rect(c, 1490, 1050, 250, 64, "DeepSeek 大模型接口", font_size=22, wrap=16)

    assemble = rect(c, 770, 1135, 360, 68, "组装业务结果", cls="header", font_size=24, wrap=16)
    response = rect(c, 705, 1225, 490, 68, "封装 JSON 结果并返回前端", cls="header", font_size=24, wrap=20)

    request_top = top_center(request)
    request_bottom = bottom_center(request)
    page_update_bottom = bottom_center(page_update)
    page_update_left = left_center(page_update)
    page_update_center = (page_update[0] + page_update[2] / 2, page_update[1] + page_update[3] / 2)

    user_role_target = top_center(user_login)
    admin_role_target = top_center(admin_login)
    c.line(950, 182, 950, 195, arrow=True)
    c.polyline([(830, 255), (user_role_target[0], 255), user_role_target], arrow=True)
    c.polyline([(1070, 255), (admin_role_target[0], 255), admin_role_target], arrow=True)

    c.line(*right_center(user_login), *left_center(user_browse), arrow=True)
    c.line(*right_center(user_browse), *left_center(user_submit), arrow=True)
    c.polyline([right_center(user_submit), (735, 520), (515, 520), top_center(user_center)], arrow=True)

    c.line(*right_center(admin_login), *left_center(admin_clue), arrow=True)
    c.line(*right_center(admin_clue), *left_center(admin_pet), arrow=True)
    c.polyline([right_center(admin_pet), (1605, 520), (1395, 520), top_center(admin_audit)], arrow=True)

    c.polyline([bottom_center(user_center), (515, 605), (790, 605), (790, 570)], arrow=True)
    c.polyline([bottom_center(admin_audit), (1395, 605), (1110, 605), (1110, 570)], arrow=True)

    c.line(request_bottom[0], request_bottom[1], 950, 790, arrow=True)
    c.text("HTTP 请求", 1040, 720, font_size=16, weight="700")

    c.line(*bottom_center(controller), *top_center(service), arrow=True)
    c.line(*right_center(service), *left_center(error_box), arrow=True)
    c.text("校验失败", 1288, 914, font_size=16, weight="700")
    c.line(950, 963, 950, 975, arrow=True)
    c.text("校验通过", 1010, 977, font_size=16, weight="700")

    c.polyline([(830, 1035), (620, 1035), (620, 987), right_center(mysql_box)], arrow=True)
    c.polyline([(830, 1035), (620, 1035), (620, 1082), right_center(redis_box)], arrow=True)
    c.polyline([(1070, 1035), (1280, 1035), (1280, 987), left_center(baidu_ai)], arrow=True)
    c.polyline([(1070, 1035), (1280, 1035), (1280, 1082), left_center(deepseek)], arrow=True)

    c.polyline([bottom_center(mysql_box), (285, 1090), (860, 1090), (860, 1135)], arrow=True)
    c.polyline([bottom_center(redis_box), (285, 1160), (900, 1160), (900, 1135)], arrow=True)
    c.polyline([bottom_center(baidu_ai), (1615, 1090), (1040, 1090), (1040, 1135)], arrow=True)
    c.polyline([bottom_center(deepseek), (1615, 1160), (1000, 1160), (1000, 1135)], arrow=True)

    c.line(*bottom_center(assemble), *top_center(response), arrow=True)

    c.polyline([right_center(response), (1285, 1259), (1285, 604), page_update_left], arrow=True, dashed=True)
    c.polyline([top_center(error_box), (1515, 830), (1515, 638), page_update_bottom], arrow=True, dashed=True)
    c.text("JSON / 状态结果", 1365, 690, font_size=16, weight="700")

    c.polyline([page_update_center, (1240, 510), (515, 510)], dashed=True)
    c.polyline([page_update_center, (1660, 520), (1395, 520)], dashed=True)

    return c.render()


def render_png(svg_path: Path, png_path: Path) -> bool:
    browser = next((path for path in CHROME_CANDIDATES if path.exists()), None)
    if browser is None:
        return False

    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={CANVAS_WIDTH},{CANVAS_HEIGHT}",
        f"--screenshot={png_path.resolve()}",
        svg_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True)
    return png_path.exists()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    IMG2_DIR.mkdir(parents=True, exist_ok=True)

    svg = build_svg()
    SVG_PATH.write_text(svg, encoding="utf-8")
    SVG_COPY_PATH.write_text(svg, encoding="utf-8")

    if render_png(SVG_PATH, PNG_PATH):
        print(PNG_PATH)
    print(SVG_PATH)
    print(SVG_COPY_PATH)


if __name__ == "__main__":
    main()
