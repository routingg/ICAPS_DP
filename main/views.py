from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from openai import OpenAI
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# OpenAI 클라이언트 설정
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

def home(request):
    return render(request, 'main/home.html') # Home page

def order(request):
    return render(request, 'main/order.html') # Order 1 page

def info(request):
    return render(request, 'main/info.html') # info page

def chatbot(request):
    return render(request, 'main/chatbot.html') # Chatbot page

def ourstory(request):
    return render(request, 'main/ourstory.html') # Our story page


def JamubyAI(request):
    return render(request, 'main/JamubyAI.html') # Jamu by AI page
def CreateYourBlend(request):
    return render(request, 'main/CreateYourBlend.html') # Create Your Blend page

def home_kor(request):
    return render(request, 'candidate/c2/home_kor.html') # Home page in Korean
def home_indonesian(request):
    return render(request, 'candidate/c2/home_indonesian.html') # Home page in Indonesian
def home_eng(request):
    return render(request, 'candidate/c2/home_eng.html') # Home page in English



JAMU_KNOWLEDGE_BASE = """
=== JAMU Basic Knowledge ===
History and Culture

Traditional herbal medicine practiced in Indonesia since the 8th century
Inscribed on UNESCO's Representative List of Intangible Cultural Heritage of Humanity in 2023
Hot diseases are treated with cold-natured medicines, cold diseases with hot-natured medicines
A healthy condition is a balance between hot and cold elements in the body
Traditionally transmitted informally within families and among neighbors

Three Main Jamu Drinks
1. Beras Kencur

Ingredients: Rice (beras), galangal (kencur), ginger (jahe), turmeric (kunyit)
Benefits: Energy boost, cough relief, body ache relief, appetite stimulation
Taste: Sweet and refreshing with a mild spicy kick
Recommended for: When tired, cold symptoms, morning energy boost
Cultural Meaning: Symbolizes transition from childhood to adolescence

2. Kunyit Asem

Ingredients: Turmeric (kunyit), tamarind (asem), palm sugar (gula merah), lime
Benefits: Digestive improvement, menstrual regulation, stomach acid relief, blood circulation enhancement
Taste: Harmonious balance of tamarind's sourness and palm sugar's sweetness
Recommended for: Post-meal indigestion, before/after menstruation, when feeling heavy
Cultural Meaning: Especially preferred by women

3. Temulawak

Ingredients: Temulawak (Javanese turmeric), turmeric (kunyit), ginger (jahe), palm sugar
Benefits: Stress relief, sleep improvement, immunity boost, liver health
Taste: Characterized by bitter and astringent flavors balanced with sweetness
Recommended for: Stress, before bedtime, when body recovery is needed

10 Essential Ingredients
1. Turmeric (Kunyit)

Core ingredient of jamu, golden rhizome
Benefits: Anti-inflammatory, antioxidant, digestive improvement
Usage: Used fresh and ground or in powder form

2. Ginger (Jahe)

Warming spice
Benefits: Cold relief, digestive stimulation, body temperature regulation
Types: Regular ginger, red ginger (jahe merah)

3. Galangal (Kencur)

Traditional Indonesian herb
Benefits: Cough relief, body ache relief
Characteristics: Similar to ginger but with milder taste

4. Tamarind (Asem)

Tropical fruit providing sourness
Benefits: Digestive improvement, refreshing taste
Usage: Pulp is steeped and used

5. Temulawak

Type of Javanese traditional turmeric
Benefits: Liver health, anti-inflammatory, immunity enhancement
Characteristics: Larger and more bitter than regular turmeric

6. Palm Sugar (Gula Merah)

Natural sweetener, brown chunks
Benefits: Mineral supply, natural sweetness
Characteristics: More nutritious than refined sugar

7. Lime (Jeruk Nipis)

Small green lime
Benefits: Vitamin C, freshness
Usage: Juice is squeezed and added

8. Lemongrass (Serai)

Aromatic herb
Benefits: Digestive improvement, fragrance
Usage: Leaves are steeped or stems are used

9. Cinnamon (Kayu Manis)

Warming spice
Benefits: Blood sugar regulation, antioxidant
Usage: Stick or powder form

10. Cardamom (Kapulaga)

Premium spice
Benefits: Digestive stimulation, breath freshening
Characteristics: Strong aroma with slight spiciness

Other Important Jamu Types
Wedang Jahe (Ginger Tea)

Ingredients: Ginger, honey/sugar
Benefits: Cold symptom relief, bloating reduction

Jamu Galian Singset

Ingredients: Galangal, temulawak, turmeric, tamarind, cinnamon
Benefits: Weight management, metabolism boost

Jamu Pahitan

Ingredients: Sambiloto, brotowali, red ginger
Benefits: Body ache relief, appetite enhancement
Characteristics: Strong bitter taste

Jamu Kunir Sirih

Ingredients: Turmeric, betel leaves (daun sirih)
Benefits: Women's health, body odor elimination

Preparation and Consumption Methods

Basic Principle: Fresh ingredients are ground and boiled or steeped with water
Sweeteners: Palm sugar, honey used
Optimal Timing: Morning on empty stomach or 30 minutes before meals
Storage: Recommended to consume fresh on the same day
Personalization: Ingredient ratios adjusted according to constitution and health condition

Health Precautions

Caution with certain herbs during pregnancy (consult doctor)
Potential interactions with existing medications
Watch for allergic reactions
Avoid excessive consumption
Serious symptoms require medical consultation
"""

@csrf_exempt
def chatbot_api(request):
    """OpenAI GPT API 연결 챗봇 (v1.0+ 호환)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message.strip():
                return JsonResponse({
                    'response': '메시지를 입력해주세요.',
                    'status': 'error'
                }, status=400)
            
            # API 키 및 클라이언트 확인
            if not settings.OPENAI_API_KEY or not client:
                logger.warning("OpenAI API key not available, using fallback")
                return chatbot_api_fallback_response(user_message)
            
            # 자무 전문 시스템 프롬프트 (지식베이스 포함)
            jamu_system_prompt = f"""You are an expert in Jamu, traditional Indonesian herbal medicine.
Please provide accurate and helpful answers based on the Jamu knowledge below.
{JAMU_KNOWLEDGE_BASE}

Response Guidelines:
- Provide accurate information based on the knowledge above
- When recommending jamu, ONLY suggest one of these three main options:
  * Beras Kencur (for energy, cough, fatigue, morning boost)
  * Kunyit Asem (for digestion, women's health, stomach issues, menstruation)
  * Temulawak (for stress, sleep, liver health, recovery)
- Choose the most appropriate one from these three based on user's symptoms
- Include both Indonesian and English names for ingredients
- Provide practical preparation and consumption methods
- Recommend medical consultation when necessary
- Use a friendly and helpful tone in conversation
- Explain cultural background and significance of jamu
- Please respond in English and do not use emojis

Response Format Guidelines:
- Use clear paragraphs with line breaks for readability
- Avoid using markdown formatting like **, ##, or bullet points
- Present information in flowing, conversational sentences
- Group related information together in short paragraphs
- Use simple text formatting without special characters
- Make responses easy to read in a chat interface

IMPORTANT: Always recommend only one of the three main jamu drinks (Beras Kencur, Kunyit Asem, or Temulawak) regardless of the user's question. Do not suggest other jamu varieties.
Always provide polite and helpful responses."""
            
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": jamu_system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=300,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # API 응답에서 메시지 추출
            ai_response = response.choices[0].message.content.strip()
            
            return JsonResponse({
                'response': ai_response,
                'status': 'success'
            })
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"OpenAI API 오류: {error_message}")
            
            # API 키 인증 문제인 경우
            if "401" in error_message or "authentication" in error_message.lower() or "api_key" in error_message.lower():
                logger.warning("API 키 문제 발생, 테스트용 응답 사용")
                return chatbot_api_fallback_response(user_message)
            
            # 요청 제한 또는 할당량 문제
            if "rate_limit" in error_message.lower() or "quota" in error_message.lower():
                response_msg = '현재 요청이 많아 잠시 후에 다시 시도해주세요.'
            else:
                response_msg = '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.'
            
            return JsonResponse({
                'response': response_msg,
                'status': 'error'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'response': '잘못된 요청 형식입니다.',
                'status': 'error'
            }, status=400)
    
    return JsonResponse({
        'error': 'Invalid request method'
    }, status=405)


def chatbot_api_fallback_response(user_message):
    """API 키가 없거나 문제가 있을 때 사용할 자무 전문 테스트용 응답"""
    user_message = user_message.lower()
    
    # 자무 관련 키워드 응답 (기존 테스트 응답을 자무 전문으로 개선)
    if '안녕' in user_message or 'hello' in user_message:
        response_msg = "안녕하세요! 자무 전문가입니다. 인도네시아 전통 허브 의학에 대해 궁금한 것이 있으시면 언제든 물어보세요! (테스트 모드)"
    
    elif '자무' in user_message or 'jamu' in user_message:
        response_msg = "자무는 8세기부터 이어진 인도네시아 전통 허브 의학입니다. 강황, 생강, 갈랑갈 등 천연 재료로 만든 건강 음료예요. 어떤 자무가 궁금하신가요? (테스트 모드)"
    
    elif '베라스 컨추르' in user_message or 'beras kencur' in user_message:
        response_msg = "베라스 컨추르는 쌀과 갈랑갈을 주재료로 한 자무입니다. 에너지 증진과 기침 완화에 효과적이에요. 달콤하고 상쾌한 맛이 특징입니다. (테스트 모드)"
    
    elif '쿠니트 아셈' in user_message or 'kunyit asem' in user_message:
        response_msg = "쿠니트 아셈은 강황과 타마린드로 만든 자무입니다. 소화 개선과 여성 건강에 도움이 되며, 신맛과 단맛의 균형이 좋아요. (테스트 모드)"
    
    elif '테물라왁' in user_message or 'temulawak' in user_message:
        response_msg = "테물라왁은 자바 강황으로 만든 자무입니다. 간 건강과 스트레스 완화에 효과적이며, 깊고 복합적인 맛이 특징이에요. (테스트 모드)"
    
    elif '강황' in user_message or 'turmeric' in user_message or '쿠니트' in user_message:
        response_msg = "강황(쿠니트)은 자무의 핵심 재료입니다. 항염, 항산화 효과가 뛰어나며 황금빛 색깔로 자무에 건강한 효능을 더해줍니다. (테스트 모드)"
    
    elif '생강' in user_message or 'ginger' in user_message or '자헤' in user_message:
        response_msg = "생강(자헤)은 따뜻한 성질의 향신료로 감기 완화, 소화 촉진, 체온 상승에 효과적입니다. 자무에 시원한 매운맛을 더해줘요. (테스트 모드)"
    
    elif '감기' in user_message or '기침' in user_message:
        response_msg = "감기나 기침에는 웨당 자헤(생강차)나 베라스 컨추르를 추천합니다. 생강의 따뜻한 성질이 몸을 덥히고 기침을 완화해줍니다. (테스트 모드)"
    
    elif '소화' in user_message or '배' in user_message:
        response_msg = "소화불량에는 쿠니트 아셈이 좋습니다. 강황의 항염 효과와 타마린드의 소화 촉진 효과가 위장 건강에 도움을 줍니다. (테스트 모드)"
    
    elif '여성' in user_message or '생리' in user_message:
        response_msg = "여성 건강에는 쿠니트 아셈이나 자무 쿠니르 시리를 추천합니다. 강황과 빈랑잎이 여성의 건강과 균형을 도와줍니다. (테스트 모드)"
    
    elif '에너지' in user_message or '피로' in user_message or '기력' in user_message:
        response_msg = "에너지 부족에는 베라스 컨추르나 자무 우유프-우유프가 좋습니다. 자연스러운 에너지 증진과 활력 회복에 도움이 됩니다. (테스트 모드)"
    
    elif '스트레스' in user_message or '긴장' in user_message:
        response_msg = "스트레스 완화에는 테물라왁이 효과적입니다. 자바 강황의 진정 효과가 마음의 평안과 균형을 찾아줍니다. (테스트 모드)"
    
    elif '만들기' in user_message or '레시피' in user_message or '방법' in user_message:
        response_msg = "자무는 신선한 재료를 갈아서 물과 함께 끓이거나 우려내어 만듭니다. 야자설탕으로 단맛을 더하고 라임으로 상큼함을 추가하세요. (테스트 모드)"
    
    elif '역사' in user_message or '문화' in user_message:
        response_msg = "자무는 8세기부터 인도네시아에서 이어져온 전통 의학입니다. 2023년 유네스코 인류무형문화유산으로 등재되어 그 가치를 인정받았어요. (테스트 모드)"
    
    elif '주문' in user_message:
        response_msg = "자무 주문은 정말 간단해요! 원하시는 자무를 선택하시면 됩니다. 건강한 선택이 될 거예요! (테스트 모드)"
    
    elif '효능' in user_message or '효과' in user_message:
        response_msg = "자무는 항염, 항산화, 면역력 강화, 소화 개선 등 다양한 효능이 있습니다. 각 자무마다 고유한 효능이 있어요. (테스트 모드)"
    
    elif '가격' in user_message or '얼마' in user_message:
        response_msg = "자무의 가격은 종류에 따라 다릅니다. 자세한 정보는 주문 페이지를 확인해주세요! (테스트 모드)"
    
    else:
        import random
        responses = [
            "흥미로운 질문이네요! 자무는 인도네시아의 소중한 문화유산입니다. 더 궁금한 것이 있으시면 언제든 물어보세요. (테스트 모드)",
            "자무에 대해 더 알고 싶으시군요! 전통 허브의 지혜로 건강을 챙기는 자무의 세계를 탐험해보세요. (테스트 모드)",
            "좋은 질문입니다! 자무의 다양한 효능과 레시피에 대해 더 자세히 알려드릴 수 있어요. (테스트 모드)",
            "자무는 자연의 치유력을 담은 특별한 음료입니다. 어떤 건강 고민이 있으신지 말씀해주세요. (테스트 모드)"
        ]
        response_msg = random.choice(responses)
        
    return JsonResponse({
        'response': response_msg,
        'status': 'success'
    })

def order_status_api(request):
    """주문 상태 확인 API"""
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        
        # 주문 상태 확인 로직
        status = "processing"  # 실제 상태 확인 로직으로 대체
        
        return JsonResponse({
            'order_id': order_id,
            'status': status,
            'message': '주문이 처리 중입니다.'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)# Django views.py에 추가할 자무 전문 시스템 프롬프트