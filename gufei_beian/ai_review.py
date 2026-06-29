import json
import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


def get_ai_client():
    """获取 AI 客户端"""
    if not settings.AI_API_KEY or not settings.AI_ENABLED:
        return None
    return OpenAI(api_key=settings.AI_API_KEY, base_url=settings.AI_API_BASE)


def run_ai_review(application):
    """
    对备案申请进行 AI 预审。
    分析申请表单数据，返回审核结果。
    """
    if not settings.AI_ENABLED:
        logger.info('AI 预审未启用，跳过')
        return None

    from .models import AIReview

    ai_review, _ = AIReview.objects.get_or_create(application=application)

    client = get_ai_client()
    if client is None:
        ai_review.status = 'error'
        ai_review.summary = 'AI 预审未配置 API Key'
        ai_review.save()
        return ai_review

    # 构建 prompt
    prompt = _build_review_prompt(application)

    try:
        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        '你是一位专业的环境保护审核专家，负责审核"一般工业固体废物跨省转移备案"的申请材料。'
                        '请仔细审查申请内容，检查信息完整性、合规性和合理性。'
                        '你必须以 JSON 格式返回审核结果，不要包含任何其他内容。'
                    )
                },
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3,
        )

        raw = response.choices[0].message.content
        ai_review.raw_response = raw

        # 解析 JSON
        result = _parse_ai_response(raw)
        ai_review.status = result.get('status', 'passed')
        ai_review.summary = result.get('summary', '')
        ai_review.score = result.get('score', 80)
        ai_review.issues = result.get('issues', [])
        ai_review.suggestions = result.get('suggestions', [])
        ai_review.save()

        logger.info(f'AI 预审完成: {application.application_no} -> {ai_review.status}')
        return ai_review

    except Exception as e:
        logger.error(f'AI 预审异常: {e}')
        ai_review.status = 'error'
        ai_review.summary = f'AI 预审调用异常: {str(e)}'
        ai_review.save()
        return ai_review


def _build_review_prompt(application):
    """构建审核 prompt"""
    return f"""
请审核以下"一般工业固体废物跨省转移备案"申请，并返回 JSON 格式的审核结果。

【申请编号】{application.application_no}

【转移单位信息】
- 单位名称：{application.transfer_unit}
- 单位地址：{application.transfer_address}
- 联系人：{application.transfer_contact}
- 联系电话：{application.transfer_phone}

【接收单位信息】
- 单位名称：{application.receive_unit}
- 所在省份：{application.receive_province}
- 单位地址：{application.receive_address}
- 联系人：{application.receive_contact}
- 联系电话：{application.receive_phone}
- 处置方式：{application.disposal_method}

【固体废物信息】
- 废物名称：{application.waste_name}
- 废物类别：{application.waste_category}
- 废物代码：{application.waste_code}
- 转移数量（吨）：{application.transfer_amount}
- 形态：{application.waste_form}
- 包装方式：{application.packaging}
- 主要成分：{application.main_components or '未填写'}
- 危险特性：{application.hazardous or '未填写'}

【运输信息】
- 运输单位：{application.transport_unit}
- 运输方式：{application.transport_method}
- 转移期限：{application.transfer_start} 至 {application.transfer_end}

请返回以下 JSON 格式（严格按此格式，不要包含 markdown 代码块标记）：
{{
    "status": "passed" 或 "failed",
    "score": 0-100 的整数评分,
    "summary": "审核摘要，100字以内",
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}

审核要点：
1. 转移单位与接收单位信息是否完整、合理
2. 废物类别与代码是否匹配
3. 废物名称、形态、包装方式是否合理
4. 处置方式是否适合该废物类别
5. 运输方式是否合理
6. 转移期限是否合理（不应超过1年）
7. 联系电话格式是否正确
"""


def _parse_ai_response(raw):
    """解析 AI 返回的 JSON"""
    # 尝试直接解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 尝试提取 JSON 代码块
    import re
    match = re.search(r'\{[\s\S]*\}', raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # 返回默认值
    return {
        'status': 'error',
        'score': 0,
        'summary': 'AI 返回格式解析失败',
        'issues': [],
        'suggestions': [],
    }