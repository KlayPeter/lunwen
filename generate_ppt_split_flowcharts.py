from __future__ import annotations

from pathlib import Path

from generate_chapter234_figures import Canvas


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
IMG2_DIR = ROOT / "img 2"


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


def build_frontend_svg() -> str:
    c = Canvas(1850, 1120)
    c.boundary(60, 40, 1730, 1040, "前端总体流程（管理端 Vue / 用户端 UniApp）")

    c.header_rect(760, 90, 330, 70, "访问系统")
    c.diamond(925, 230, 240, 120, "角色选择", wrap=6)
    c.boundary(110, 320, 820, 620, "宠物领养用户端")
    c.boundary(960, 320, 780, 620, "管理员端")

    user_login = rect(c, 380, 380, 210, 66, "登录 / 注册")
    c.diamond(485, 505, 220, 110, "选择功能", wrap=6)

    pet_list = rect(c, 150, 600, 180, 60, "浏览宠物列表", wrap=10)
    pet_detail = rect(c, 150, 680, 180, 60, "查看宠物详情", wrap=10)
    adoption_apply = rect(c, 150, 760, 180, 60, "提交领养申请", wrap=10)

    upload_photo = rect(c, 390, 600, 190, 60, "上传图片", wrap=10)
    ai_fill = rect(c, 390, 680, 190, 60, "AI识别自动回填", wrap=10)
    clue_submit = rect(c, 390, 760, 190, 60, "填写信息并提交", wrap=10)

    post_community = rect(c, 640, 620, 190, 60, "发布社区内容", wrap=10)
    comment_box = rect(c, 640, 720, 190, 60, "评论互动", wrap=10)

    user_center = rect(c, 360, 860, 320, 66, "个人中心查看状态\n与反馈回复", cls="header", font_size=24, wrap=18)

    admin_login = rect(c, 1260, 380, 210, 66, "管理员登录")
    c.diamond(1365, 505, 260, 110, "选择管理功能", wrap=8)

    clue_list = rect(c, 995, 600, 170, 60, "查看线索列表", wrap=10)
    progress_record = rect(c, 995, 700, 170, 60, "添加进展记录", wrap=10)

    edit_pet = rect(c, 1185, 600, 175, 60, "添加 / 编辑宠物", wrap=10)
    publish_pet = rect(c, 1185, 700, 175, 60, "发布宠物信息", wrap=10)

    apply_list = rect(c, 1380, 600, 170, 60, "查看申请列表", wrap=10)
    apply_audit = rect(c, 1380, 700, 170, 60, "申请审核", wrap=10)

    community_audit = rect(c, 1570, 635, 145, 100, "审核社区内容\n与评论", wrap=8)

    request_box = rect(
        c,
        650,
        945,
        560,
        70,
        "与后端交互：发起请求并接收返回结果",
        cls="header",
        font_size=24,
        wrap=24,
    )

    c.line(925, 160, 925, 170, arrow=True)
    c.polyline([(805, 230), (485, 230), top_center(user_login)], arrow=True)
    c.polyline([(1045, 230), (1365, 230), top_center(admin_login)], arrow=True)

    c.line(*bottom_center(user_login), 485, 450, arrow=True)
    c.polyline([(375, 505), (240, 505), top_center(pet_list)], arrow=True)
    c.polyline([(485, 560), (485, 600)], arrow=True)
    c.polyline([(595, 505), (735, 505), top_center(post_community)], arrow=True)

    c.line(*bottom_center(pet_list), *top_center(pet_detail), arrow=True)
    c.line(*bottom_center(pet_detail), *top_center(adoption_apply), arrow=True)
    c.line(*bottom_center(upload_photo), *top_center(ai_fill), arrow=True)
    c.line(*bottom_center(ai_fill), *top_center(clue_submit), arrow=True)
    c.line(*bottom_center(post_community), *top_center(comment_box), arrow=True)

    c.polyline([bottom_center(adoption_apply), (240, 850), (520, 850), top_center(user_center)], arrow=True)
    c.polyline([bottom_center(clue_submit), (485, 850), top_center(user_center)], arrow=True)
    c.polyline([bottom_center(comment_box), (735, 850), (520, 850), top_center(user_center)], arrow=True)

    c.line(*bottom_center(admin_login), 1365, 450, arrow=True)
    c.polyline([(1235, 505), (1080, 505), top_center(clue_list)], arrow=True)
    c.polyline([(1325, 560), (1275, 560), (1275, 600), top_center(edit_pet)], arrow=True)
    c.polyline([(1405, 560), (1465, 560), (1465, 600), top_center(apply_list)], arrow=True)
    c.polyline([(1495, 505), (1640, 505), (1640, 635)], arrow=True)

    c.line(*bottom_center(clue_list), *top_center(progress_record), arrow=True)
    c.line(*bottom_center(edit_pet), *top_center(publish_pet), arrow=True)
    c.line(*bottom_center(apply_list), *top_center(apply_audit), arrow=True)

    c.polyline([bottom_center(progress_record), (1080, 910), (930, 910), (930, 945)], arrow=True)
    c.polyline([bottom_center(publish_pet), (1272, 910), (1030, 910), (1030, 945)], arrow=True)
    c.polyline([bottom_center(apply_audit), (1465, 910), (1110, 910), (1110, 945)], arrow=True)
    c.polyline([bottom_center(community_audit), (1642, 910), (1110, 910), (1110, 945)], arrow=True)
    c.polyline([bottom_center(user_center), (520, 925), (770, 925), (770, 945)], arrow=True)

    return c.render()


def build_backend_svg() -> str:
    c = Canvas(1650, 1120)
    c.boundary(60, 40, 1530, 1040, "后端总体流程（Spring Boot / MySQL / Redis / AI 服务）")

    request_box = rect(c, 620, 90, 410, 70, "前端发起 HTTP 请求", cls="header", font_size=24, wrap=18)
    controller = rect(c, 620, 200, 410, 70, "Controller 接收请求", cls="header", font_size=24, wrap=18)
    service = rect(c, 560, 310, 530, 78, "Service 业务层校验\n身份、参数与业务规则", font_size=24, wrap=22)

    c.diamond(825, 485, 260, 120, "校验是否通过", wrap=8)
    error_box = rect(c, 1190, 450, 240, 70, "返回错误信息", cls="subbox", font_size=24, wrap=14)

    c.diamond(825, 650, 260, 120, "业务类型", wrap=8)
    mysql_box = rect(c, 150, 620, 220, 65, "MySQL 数据操作", wrap=16)
    redis_box = rect(c, 150, 715, 220, 65, "Redis 缓存处理", wrap=16)
    baidu_ai = rect(c, 1280, 620, 220, 65, "百度 AI 识图接口", wrap=16)
    deepseek = rect(c, 1280, 715, 220, 65, "DeepSeek 大模型接口", wrap=16)

    assemble = rect(c, 645, 775, 360, 68, "组装业务结果", cls="header", font_size=24, wrap=16)
    json_box = rect(c, 620, 860, 410, 68, "封装 JSON 结果", cls="header", font_size=24, wrap=16)
    render_box = rect(c, 650, 945, 350, 68, "返回前端渲染", cls="header", font_size=24, wrap=16)

    c.line(*bottom_center(request_box), *top_center(controller), arrow=True)
    c.line(*bottom_center(controller), *top_center(service), arrow=True)
    c.line(*bottom_center(service), 825, 425, arrow=True)

    c.polyline([(955, 485), (1070, 485), left_center(error_box)], arrow=True)
    c.text("否", 1015, 470, font_size=16, weight="700")
    c.line(825, 545, 825, 590, arrow=True)
    c.text("是", 845, 570, font_size=16, weight="700")

    c.polyline([(695, 650), (480, 650), (480, 652), right_center(mysql_box)], arrow=True)
    c.polyline([(695, 650), (480, 650), (480, 747), right_center(redis_box)], arrow=True)
    c.polyline([(955, 650), (1170, 650), (1170, 652), left_center(baidu_ai)], arrow=True)
    c.polyline([(955, 650), (1170, 650), (1170, 747), left_center(deepseek)], arrow=True)

    c.polyline([bottom_center(mysql_box), (260, 745), (735, 745), (735, 775)], arrow=True)
    c.polyline([bottom_center(redis_box), (260, 775), (785, 775), (785, 775)], arrow=True)
    c.polyline([bottom_center(baidu_ai), (1390, 745), (915, 745), (915, 775)], arrow=True)
    c.polyline([bottom_center(deepseek), (1390, 775), (865, 775), (865, 775)], arrow=True)

    c.line(*bottom_center(assemble), *top_center(json_box), arrow=True)
    c.line(*bottom_center(json_box), *top_center(render_box), arrow=True)
    c.polyline([bottom_center(error_box), (1310, 860), (930, 860), (930, 945)], arrow=True, dashed=True)

    return c.render()


def write_outputs() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    IMG2_DIR.mkdir(parents=True, exist_ok=True)

    frontend_svg = build_frontend_svg()
    backend_svg = build_backend_svg()

    outputs = {
        FIG_DIR / "ppt_frontend_overall_flow.svg": frontend_svg,
        FIG_DIR / "ppt_backend_overall_flow.svg": backend_svg,
        IMG2_DIR / "PPT_前端总体流程图.svg": frontend_svg,
        IMG2_DIR / "PPT_后端总体流程图.svg": backend_svg,
    }

    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    write_outputs()
