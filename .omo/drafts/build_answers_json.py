#!/usr/bin/env python3
"""
Build docs/speaking/data/answers.json — skeleton with all 71 topics from the
May-Aug 2026 IELTS Speaking PDF (new question bank).

Schema: see .omo/drafts/answers-schema.md

Topic count = 71 (PDF truth) — see schema Note A. Plan/questionnaire/task
claim 73 due to a counting error (3+14+7+3=27, not 29).
"""

import json
from pathlib import Path

OUTPUT = Path("/home/ljh2923/opencode-project/IELTS/docs/speaking/data/answers.json")


def q(qid, question_en):
    """Make an empty-skeleton Question."""
    return {
        "id": qid,
        "question_en": question_en,
        "question_zh": "",
        "answer_en": "",
        "answer_hint_zh": "",
        "ai_supplemented": False,
    }


def topic(tid, title_zh, title_en, part, category, is_required,
          is_ai_supplemented, pdf_pages, questions, cue_card=None):
    """Make a Topic entry."""
    out = {
        "id": tid,
        "slug": tid,
        "title_zh": title_zh,
        "title_en": title_en,
        "part": part,
        "category": category,
        "is_required": is_required,
        "is_ai_supplemented": is_ai_supplemented,
        "pdf_pages": pdf_pages,
        "questions": questions,
    }
    if cue_card is not None:
        out["cue_card"] = cue_card
    return out


def p23_questions(title_en, title_zh, part3_qs):
    """Build questions array for a Part 2&3 topic. First question is the cue card prompt."""
    out = [
        {
            "id": "cue",
            "question_en": title_en,
            "question_zh": title_zh,
            "answer_en": "",
            "answer_hint_zh": "",
            "ai_supplemented": False,
        }
    ]
    for i, question in enumerate(part3_qs, 1):
        out.append(q(f"p3-{i}", question))
    return out


def p23_cue(bullets_en, bullets_zh):
    return {
        "bullets_en": bullets_en,
        "bullets_zh": bullets_zh,
    }


# ---------------------------------------------------------------------------
# Part 1 Required (5)
# ---------------------------------------------------------------------------

p1_required = [
    topic(
        "p1-hometown", "家乡", "Hometown", "p1-required", "place", True, False,
        [5, 6, 7],
        [
            q("q1", "Where is your hometown?"),
            q("q2", "Is that a big city or a small place?"),
            q("q3", "Please describe your hometown a little."),
            q("q4", "How long have you been living there?"),
            q("q5", "Do you think you will continue living there for a long time?"),
            q("q6", "Do you like your hometown?"),
            q("q7", "Do you like living there?"),
            q("q8", "What do you like (most) about your hometown?"),
            q("q9", "Is there anything you dislike about it?"),
            q("q10", "What's your hometown famous for?"),
            q("q11", "Did you learn about the history of your hometown at school?"),
            q("q12", "Are there many young people in your hometown?"),
            q("q13", "Is your hometown a good place for young people to pursue their careers?"),
            q("q14", "Have you learned anything about the history of your hometown?"),
            q("q15", "Did you learn about the culture of your hometown in your childhood?"),
        ],
    ),
    topic(
        "p1-work", "工作或学习", "Work or Studies", "p1-required", "object", True, False,
        [5, 6],
        [
            # Work branch
            q("q1", "What work do you do?"),
            q("q2", "Why did you choose to do that type of work (or that job)?"),
            q("q3", "Do you like your job?"),
            q("q4", "What requirements did you need to meet to get your current job?"),
            q("q5", "Do you have any plans for your work in the next five years?"),
            q("q6", "What do you think is the most important at the moment?"),
            q("q7", "Do you want to change to another job?"),
            q("q8", "Do you miss being a student?"),
            q("q9", "What technology do you use at work?"),
            q("q10", "Who helps you the most? And how?"),
            # Study branch
            q("q11", "What subjects are you studying?"),
            q("q12", "Do you like your subject?"),
            q("q13", "Why did you choose to study that subject?"),
            q("q14", "Do you think that your subject is popular in your country?"),
            q("q15", "Do you have any plans for your studies in the next five years?"),
            q("q16", "What are the benefits of being your age?"),
            q("q17", "Do you want to change your major?"),
            q("q18", "Do you prefer to study in the mornings or in the afternoons?"),
            q("q19", "How much time do you spend on your studies each week?"),
            q("q20", "Are you looking forward to working?"),
            q("q21", "What technology do you use when you study?"),
            q("q22", "What changes would you like to see in your school?"),
        ],
    ),
    topic(
        "p1-home", "家 / 住所", "Home/Accommodation", "p1-required", "object", True, False,
        [6, 7],
        [
            q("q1", "What kind of house or apartment do you want to live in in the future?"),
            q("q2", "Are the transport facilities to your home very good?"),
            q("q3", "Do you prefer living in a house or an apartment?"),
            q("q4", "Please describe the room you live in."),
            q("q5", "What part of your home do you like the most?"),
            q("q6", "How long have you lived there?"),
            q("q7", "Do you plan to live there for a long time?"),
            q("q8", "What's the difference between where you are living now and where you have lived in the past?"),
            q("q9", "Can you describe the place where you live?"),
            q("q10", "What room does your family spend most of the time in?"),
            q("q11", "What's your favorite room in your apartment/house?"),
            q("q12", "What makes you feel pleasant in your home?"),
            q("q13", "Do you think it is important to live in a comfortable environment?"),
            q("q14", "Do you live in an apartment or a house?"),
            q("q15", "Who do you live with?"),
            q("q16", "What do you usually do in your apartment?"),
            q("q17", "What kinds of accommodation do you live in?"),
        ],
    ),
    topic(
        "p1-area", "你居住的地区", "The area you live in", "p1-required", "place", True, False,
        [7],
        [
            q("q1", "Do you like the area that you live in?"),
            q("q2", "Where do you like to go in that area?"),
            q("q3", "Do you know any famous people in your area?"),
            q("q4", "What are some changes in the area recently?"),
            q("q5", "Do you know any of your neighbors?"),
            q("q6", "Are the people in your neighborhood nice and friendly?"),
            q("q7", "Do you live in a noisy or a quiet area?"),
        ],
    ),
    topic(
        "p1-city", "你居住的城市", "The city you live in", "p1-required", "place", True, False,
        [7],
        [
            q("q1", "What city do you live in?"),
            q("q2", "Do you like this city? Why?"),
            q("q3", "How long have you lived in this city?"),
            q("q4", "Are there big changes in this city?"),
            q("q5", "Is this city your permanent residence?"),
            q("q6", "Are there people of different ages living in this city?"),
            q("q7", "Are the people friendly in this city?"),
            q("q8", "Is the city friendly to children and old people?"),
            q("q9", "Do you often see your neighbors?"),
            q("q10", "What's the weather like where you live?"),
            q("q11", "Would you recommend your city to others?"),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Part 1 High-frequency (27)
# ---------------------------------------------------------------------------

p1_high_freq = [
    # PLACE (3)
    topic("p1f-parks", "公园", "Parks", "p1-high-freq", "place", False, False, [8],
          [
              q("q1", "Did you like going to parks as a child?"),
              q("q2", "Do you still like going to parks now?"),
              q("q3", "Would you like to see more parks in your city?"),
              q("q4", "Are there any parks you want to go to in the future?"),
          ]),
    topic("p1f-outer-space", "太空与星星", "Outer space and stars", "p1-high-freq", "place", False, False, [8],
          [
              q("q1", "Have you ever learned about outer space and stars?"),
              q("q2", "Do you like science fiction movies? Why?"),
              q("q3", "Do you want to know more about outer space?"),
              q("q4", "Do you want to go into outer space in the future?"),
          ]),
    topic("p1f-building", "建筑", "Building", "p1-high-freq", "place", False, False, [8],
          [
              q("q1", "Are there tall buildings near your home?"),
              q("q2", "Do you take photos of buildings?"),
              q("q3", "Is there a building that you would like to visit?"),
              q("q4", "Do you want to live in a tall building?"),
          ]),
    # OBJECT (14)
    topic("p1f-science", "科学", "Science", "p1-high-freq", "object", False, False, [9],
          [
              q("q1", "Do you like science?"),
              q("q2", "When did you start to learn about science?"),
              q("q3", "Which science subject is interesting to you?"),
              q("q4", "What kinds of interesting things have you done with science?"),
              q("q5", "Do you like watching science TV programs?"),
              q("q6", "Do Chinese people often visit science museums?"),
          ]),
    topic("p1f-cars", "汽车", "Cars", "p1-high-freq", "object", False, False, [9],
          [
              q("q1", "Did you enjoy traveling by car when you were a kid?"),
              q("q2", "What types of cars do you like?"),
              q("q3", "Do you prefer to be a driver or a passenger?"),
              q("q4", "What do you usually do when there is a traffic jam?"),
              q("q5", "Do you think car colors are important?"),
          ]),
    topic("p1f-teachers", "老师", "Teachers", "p1-high-freq", "object", False, False, [9],
          [
              q("q1", "Do you have a favorite teacher?"),
              q("q2", "Do you want to be a teacher in the future?"),
              q("q3", "Do you have a teacher from your past that you still remember?"),
              q("q4", "Are you still in touch with your primary school teachers?"),
              q("q5", "In what way has your favourite teacher helped you?"),
          ]),
    topic("p1f-social-media", "社交媒体", "Social media", "p1-high-freq", "object", False, False, [9, 10],
          [
              q("q1", "Have you ever posted anything on social media?"),
              q("q2", "When did you start using social media?"),
              q("q3", "Do you think you spend too much time on social media?"),
              q("q4", "Do your friends use social media?"),
              q("q5", "What do people often do on social media?"),
          ]),
    topic("p1f-watch", "手表", "Watch", "p1-high-freq", "object", False, False, [10],
          [
              q("q1", "Do you wear a watch?"),
              q("q2", "Have you ever got a watch as a gift?"),
              q("q3", "Why do some people wear expensive watches?"),
              q("q4", "Do you think it is important to wear a watch? Why?"),
          ]),
    topic("p1f-websites", "网站", "Websites", "p1-high-freq", "object", False, False, [10],
          [
              q("q1", "What kinds of websites do you often visit?"),
              q("q2", "What is your favourite website?"),
              q("q3", "Are there any changes to the websites you often visit?"),
              q("q4", "What kinds of websites are popular in your country?"),
          ]),
    topic("p1f-mirrors", "镜子", "Mirrors", "p1-high-freq", "object", False, False, [10],
          [
              q("q1", "Do you like looking at yourself in the mirror? How often?"),
              q("q2", "Have you ever bought mirrors?"),
              q("q3", "Do you usually take a mirror with you?"),
              q("q4", "Would you use mirrors to decorate your room?"),
          ]),
    topic("p1f-gifts", "礼物", "Gifts", "p1-high-freq", "object", False, False, [10, 11],
          [
              q("q1", "Have you ever sent handmade gifts to others?"),
              q("q2", "Have you ever received a great gift?"),
              q("q3", "What do you consider when choosing a gift?"),
              q("q4", "Do you think you are good at choosing gifts?"),
              q("q5", "What gift have you received recently?"),
          ]),
    topic("p1f-pets", "宠物与动物", "Pets and Animals", "p1-high-freq", "object", False, False, [11],
          [
              q("q1", "What's your favourite animal? Why?"),
              q("q2", "Where do you prefer to keep your pet, indoors or outdoors?"),
              q("q3", "Have you ever had a pet before?"),
              q("q4", "What is the most popular animal in China?"),
          ]),
    topic("p1f-food", "食物", "Food", "p1-high-freq", "object", False, False, [11],
          [
              q("q1", "What is your favourite food?"),
              q("q2", "What kind of food did you like when you were young?"),
              q("q3", "Do you eat different foods at different times of the year?"),
              q("q4", "Has your favourite food changed since you were a child?"),
          ]),
    topic("p1f-sports-team", "运动队 / 团队运动", "Sports team", "p1-high-freq", "object", False, False, [11],
          [
              q("q1", "Have you ever been part of a sports team?"),
              q("q2", "Is team sports popular in your culture?"),
              q("q3", "Do you like watching team games? Why?"),
              q("q4", "What are the differences between team sports and individual sports?"),
          ]),
    topic("p1f-scenery", "风景", "Scenery", "p1-high-freq", "object", False, False, [11],
          [
              q("q1", "Do you look out the window at the scenery when travelling by bus or car?"),
              q("q2", "Do you prefer the mountains or the sea?"),
              q("q3", "Do you like to take scenery pictures?"),
              q("q4", "What are the most beautiful sights you have seen while travelling?"),
          ]),
    topic("p1f-views", "景色", "Views", "p1-high-freq", "object", False, False, [12],
          [
              q("q1", "Do you like taking pictures of different views?"),
              q("q2", "Do you prefer views in urban areas or rural areas?"),
              q("q3", "Do you prefer views in your own country or in other countries?"),
              q("q4", "Have you seen an unforgettable and beautiful view or scenery?"),
          ]),
    topic("p1f-childhood", "童年活动", "Childhood activities", "p1-high-freq", "object", False, False, [12],
          [
              q("q1", "What were your favourite activities?"),
              q("q2", "What were your favourite activities when you were a child?"),
              q("q3", "Did you prefer to do activities alone or with a group of people when you were a child?"),
              q("q4", "Are there any differences between the activities you liked when you were a child and those you like now?"),
          ]),
    # EVENT (7)
    topic("p1f-shopping", "购物", "Shopping", "p1-high-freq", "event", False, False, [13],
          [
              q("q1", "Do you like shopping?"),
              q("q2", "How often do you go shopping?"),
              q("q3", "Do you prefer online shopping or in-store shopping?"),
              q("q4", "Have you ever returned anything you bought online?"),
          ]),
    topic("p1f-singing", "唱歌", "Singing", "p1-high-freq", "event", False, False, [13],
          [
              q("q1", "Do you like singing? Why?"),
              q("q2", "Have you ever learned how to sing?"),
              q("q3", "Who do you want to sing for?"),
              q("q4", "Do you think singing can bring happiness to people?"),
          ]),
    topic("p1f-life-stages", "人生阶段", "Life stages", "p1-high-freq", "event", False, False, [13],
          [
              q("q1", "What did you often do with your friends in your childhood?"),
              q("q2", "What do you think is the most important at the moment?"),
              q("q3", "Do you have any plans for the next five years?"),
              q("q4", "How do people remember each stage of their lives?"),
              q("q5", "Do you enjoy being the age you are now?"),
              q("q6", "At what age do you think people are the happiest?"),
          ]),
    topic("p1f-morning", "早晨", "Morning time", "p1-high-freq", "event", False, False, [13, 14],
          [
              q("q1", "Do you like getting up early in the morning?"),
              q("q2", "What do you usually do in the morning?"),
              q("q3", "What did you do in the morning when you were little? Why?"),
              q("q4", "Are there any differences between what you do in the morning now and what you did in the past?"),
              q("q5", "Do you spend your mornings doing the same things on both weekends and weekdays? Why?"),
          ]),
    topic("p1f-reading", "阅读", "Reading", "p1-high-freq", "event", False, False, [14],
          [
              q("q1", "Do you like reading?"),
              q("q2", "Do you prefer to read on paper or on a screen?"),
              q("q3", "When do you need to read carefully, and when not?"),
              q("q4", "Do you prefer scanning or detailed reading?"),
          ]),
    topic("p1f-walking", "散步 / 走路", "Walking", "p1-high-freq", "event", False, False, [14],
          [
              q("q1", "Do you walk a lot?"),
              q("q2", "Did you often go outside to have a walk when you were a child?"),
              q("q3", "Why do people like to walk in parks?"),
              q("q4", "Where would you like to take a long walk if you had the chance?"),
              q("q5", "Where did you go for a walk lately?"),
          ]),
    topic("p1f-typing", "打字", "Typing", "p1-high-freq", "event", False, False, [14],
          [
              q("q1", "Do you prefer typing or handwriting?"),
              q("q2", "Do you type on a desktop or laptop keyboard every day?"),
              q("q3", "When did you learn how to type on a keyboard?"),
              q("q4", "How do you improve your typing?"),
          ]),
    # ABSTRACT (3)
    topic("p1f-tidiness", "整洁", "Tidiness", "p1-high-freq", "abstract", False, False, [15],
          [
              q("q1", "Do you like to keep things tidy?"),
              q("q2", "Did you use to keep your room tidy as a child?"),
              q("q3", "待补充"),
          ]),
    topic("p1f-music", "音乐", "Music", "p1-high-freq", "abstract", False, False, [15],
          [
              q("q1", "Do you prefer sad or happy music?"),
              q("q2", "Does happy music make you feel more excited?"),
              q("q3", "待补充"),
          ]),
    topic("p1f-hobby", "爱好", "Hobby", "p1-high-freq", "abstract", False, False, [15],
          [
              q("q1", "Do you have any hobbies?"),
              q("q2", "Did you have any hobbies when you were a child?"),
              q("q3", "Do you have a hobby that you've had since childhood?"),
              q("q4", "Do you have the same hobbies as your family members?"),
          ]),
]


# ---------------------------------------------------------------------------
# Part 2&3 (39)
# ---------------------------------------------------------------------------

p23 = [
    # PLACE (6)
    topic("p23-fav-city", "描述你最喜欢的一座城市", "Describe your favorite city that you have visited",
          "p23", "place-p23", False, False, [16],
          p23_questions(
              "Describe your favorite city that you have visited",
              "描述你去过的最喜欢的一座城市。",
              [
                  "Which is more suitable for young people, urban life or rural life, and which is more suitable for old people?",
                  "How do people choose a city to travel to?",
                  "Do you think a tourist city is also a good place to live? Why?",
                  "Do most people prefer to travel in a modern city or a historical city?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "How you knew it", "When you visited it", "And explain why it is your favourite city"],
              ["它在哪里", "你怎么知道它的", "你什么时候去的", "并解释为什么它是你最喜欢的城市"],
          )),
    topic("p23-boring", "描述一个无聊的地方", "Describe a boring place",
          "p23", "place-p23", False, True, [17],  # AI-supplemented
          p23_questions(
              "Describe a boring place",
              "描述一个无聊的地方。",
              [
                  "Why do most children think education is boring?",
                  "Why aren't young people willing to listen to the experiences of older people?",
                  "What can people do when they feel bored?",
                  "Why are some teachers' classes boring? Are there any solutions?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "Who you went there with", "What you did there", "And explain why you think it is a boring place"],
              ["它在哪里", "你和谁一起去的", "你在那里做了什么", "并解释为什么你觉得它很无聊"],
          )),
    topic("p23-tall", "描述一座你喜欢或不喜欢的高楼", "Describe a tall building you like or dislike",
          "p23", "place-p23", False, False, [17],
          p23_questions(
              "Describe a tall building you like or dislike",
              "描述一座你喜欢或不喜欢的高楼。",
              [
                  "Are there many tall buildings in your country?",
                  "What are the differences between those tall buildings in your country?",
                  "Why are different places laid out and designed differently?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["What it is used for", "Where it is", "What it looks like", "And explain why you like/dislike it"],
              ["它的用途是什么", "它在哪里", "它看起来什么样", "并解释为什么你喜欢/不喜欢它"],
          )),
    topic("p23-interest-bldg", "描述一座有趣的建筑", "Describe an interesting building",
          "p23", "place-p23", False, False, [18],
          p23_questions(
              "Describe an interesting building",
              "描述一座有趣的建筑。",
              [
                  "What types of buildings are popular in your country?",
                  "Is it worth spending a lot of money on the exterior appearance of a building?",
                  "Is it more important for a building to look good on the outside or on the inside?",
                  "Why do people like to visit historical sites?",
                  "Do you think it's reasonable to charge an entry fee for visiting interesting buildings?",
                  "Is it better to live in a new building or an old one?",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "What it looks like", "What function it has", "And explain why you think it is interesting"],
              ["它在哪里", "它看起来什么样", "它有什么功能", "并解释为什么你觉得它有趣"],
          )),
    topic("p23-famous-city", "描述一个你觉得非常有趣/出名的城市", "Describe a city that you think is very interesting/famous",
          "p23", "place-p23", False, False, [18],
          p23_questions(
              "Describe a city that you think is very interesting/famous",
              "描述一个你觉得非常有趣/出名的城市。",
              [
                  "What advantages can tourism bring to a city?",
                  "Why do some young people like to live in cities?",
                  "Do most elderly people live in the city or in the countryside?",
                  "Do you think well-developed tourism will have negative effects on local people?",
                  "What are the benefits of urbanization?",
                  "Do you think the big cities in China today will become even larger in the future?",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "What it is famous for", "How you knew this city", "And explain why you think it is very interesting/famous"],
              ["它在哪里", "它因什么出名", "你是怎么知道这座城市的", "并解释为什么你觉得它非常有趣/出名"],
          )),
    topic("p23-nanning", "描述一个你游览得很开心的城市", "Describe a city you enjoyed visiting",
          "p23", "place-p23", False, False, [19],
          p23_questions(
              "Describe a city you enjoyed visiting",
              "描述一个你游览得很开心的城市。",
              [
                  "What kinds of facilities do big cities have?",
                  "Do you think modern cities are suitable for young people or old people?",
                  "Before you travel to a city, what factors would you consider?",
                  "What are the disadvantages of living in a very famous city?",
                  "Do you prefer to visit well-developed cities or cities with a long history?",
                  "For those who live in cities, is it because they want to or have to?",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "When you visited it", "How long you stayed there", "What you did there", "And explain why you enjoyed visiting it"],
              ["它在哪里", "你什么时候去的", "你在那里待了多久", "你在那里做了什么", "并解释为什么你喜欢游览这座城市"],
          )),
    # PEOPLE (11)
    topic("p23-child-friend", "描述你童年时期的一个朋友", "Describe a friend from your childhood",
          "p23", "people", False, False, [21],
          p23_questions(
              "Describe a friend from your childhood",
              "描述你童年时期的一个朋友。",
              [
                  "Do you still keep in touch with your friends from childhood? Why or why not?",
                  "How important is childhood friendship to children?",
                  "What do you think of communicating via social media?",
                  "Do you think online communication through social media will replace face-to-face communication?",
                  "What's the difference between having younger friends and older friends?",
                  "Has technology changed people's friendships? How?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he/she is", "Where and how you met each other", "What you often did together", "And explain what made you like him/her"],
              ["他/她是谁", "你们在哪里以及怎么认识的", "你们经常一起做什么", "并解释是什么让你喜欢他/她"],
          )),
    topic("p23-business", "描述你认识的一个做生意成功的人", "Describe a person you know who has a successful business",
          "p23", "people", False, False, [21],
          p23_questions(
              "Describe a person you know who has a successful business",
              "描述你认识的一个做生意成功的人。",
              [
                  "Why do some people start their own business?",
                  "Should governments provide financial support to start-ups?",
                  "Do most people prefer shopping at big stores or small stores?",
                  "What makes a business successful?",
                  "What makes a business fail?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["Who this person is", "How you got to know him/her", "Why and how he/she started the business", "What business he/she does", "And explain why you think the business is successful"],
              ["这个人是谁", "你是怎么认识他/她的", "他/她为什么以及如何开始做这个生意", "他/她做的是什么生意", "并解释为什么你觉得这个生意是成功的"],
          )),
    topic("p23-plants", "描述一个喜欢在家里或花园种植物的人", "Describe a person who loves to grow plants",
          "p23", "people", False, True, [22],  # AI-supplemented
          p23_questions(
              "Describe a person who loves to grow plants (e.g. vegetables, flowers) at home or in the garden",
              "描述一个喜欢在家里或花园种植物(蔬菜、花等)的人。",
              [
                  "What are the advantages of growing vegetables or flowers at home?",
                  "Do many people grow vegetables or flowers at home in your country?",
                  "Is it easy to grow plants at home?",
                  "Why do people like to grow plants?",
                  "Why do some people prefer to grow their own fruits and vegetables instead of buying them from the market?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["Who this person is", "What plants he/she grows", "How he/she grows the plants", "And explain why he/she loves growing plants"],
              ["这个人是谁", "他/她种什么植物", "他/她怎么种", "并解释为什么他/她喜欢种植物"],
          )),
    topic("p23-medical", "描述一个你认识的想从事医疗行业的人", "Describe a person you know who would like to choose a career in the medical field",
          "p23", "people", False, False, [22],
          p23_questions(
              "Describe a person you know who would like to choose a career in the medical field (e.g. a doctor, a nurse)",
              "描述一个你认识的想从事医疗行业(医生、护士等)的人。",
              [
                  "Do you think being a doctor is easy or difficult?",
                  "Do you think learning biology is interesting for children?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["When you knew him/her", "When he/she started to think about that", "What he/she would like to do", "And explain why he/she would like to choose this career"],
              ["你什么时候认识他/她", "他/她什么时候开始这样想", "他/她想做什么", "并解释为什么他/她想选择这个职业"],
          )),
    topic("p23-planning", "描述一个总做计划且擅长规划的人", "Describe a person who makes plans a lot and is good at planning",
          "p23", "people", False, False, [23],
          p23_questions(
              "Describe a person who makes plans a lot and is good at planning",
              "描述一个总做计划且擅长规划的人。",
              [
                  "Do you think it's important to plan ahead?",
                  "What activities do we need to plan ahead?",
                  "Do you think children should plan their future careers?",
                  "Should children ask their teachers or parents for advice when making plans?",
                  "Is making study plans popular among young people?",
                  "Do you think choosing a college major is closely related to a future career?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he/she is", "How you knew him/her", "What plans he/she makes", "And explain how you feel about this person"],
              ["他/她是谁", "你是怎么认识他/她的", "他/她做什么计划", "并解释你对这个人的感受"],
          )),
    topic("p23-child-art", "描述一个喜欢画画的小孩", "Describe a child who loves drawing/painting",
          "p23", "people", False, True, [23],  # AI-supplemented
          p23_questions(
              "Describe a child who loves drawing/painting",
              "描述一个喜欢画画/绘画的小孩。",
              [
                  "What is the right age for a child to learn drawing?",
                  "Why do most children draw more often than adults do?",
                  "Why do some people visit galleries or museums instead of viewing artworks online?",
                  "Do you think galleries and museums should be free of charge?",
                  "How do artworks inspire people?",
                  "What are the differences between reading a book and visiting a museum?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he/she is", "How/when you knew him/her", "How often he/she draws/paints", "And explain why you think he/she loves drawing/painting"],
              ["他/她是谁", "你什么时候/怎么认识他/她", "他/她多久画一次", "并解释为什么你觉得他/她喜欢画画"],
          )),
    topic("p23-self-learn", "描述一个没老师自学的朋友", "Describe one of your friends who learned something without a teacher",
          "p23", "people", False, True, [24],  # AI-supplemented
          p23_questions(
              "Describe one of your friends who learned something without a teacher",
              "描述一个没老师自学的朋友。",
              [
                  "Is it necessary to keep learning after graduating from school?",
                  "Should teachers make learning in their classes fun?",
                  "Do you think there are too many subjects for students to learn?",
                  "Is it better to focus on a few subjects or to learn many subjects?",
                  "Do you think enterprises should provide training for their employees?",
                  "Do you think it is good for older adults to continue learning?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he/she is", "What he/she learned", "Why he/she learned this", "And explain whether it would be easier to learn from a teacher"],
              ["他/她是谁", "他/她学的是什么", "他/她为什么自学这个", "并解释有老师教会不会更轻松"],
          )),
    topic("p23-famous", "描述一个你想见面的名人", "Describe a famous person you would like to meet",
          "p23", "people", False, True, [24],  # AI-supplemented
          p23_questions(
              "Describe a famous person you would like to meet",
              "描述一个你想见面的名人。",
              [
                  "What are the advantages and disadvantages of being a famous child?",
                  "What can today's children do to become famous?",
                  "What can children do with their fame?",
                  "Do people become famous because of their talent?",
                  "Is it easy to become famous in your country?",
                  "Do you want to be a famous person?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he/she is", "How you knew him/her", "How/where you would like to meet him/her", "And explain why you would like to meet him/her"],
              ["他/她是谁", "你是怎么知道他/她的", "你希望如何/在哪里见到他/她", "并解释为什么你想见他/她"],
          )),
    topic("p23-helper", "描述一个经常帮助他人的人", "Describe a person who often helps others",
          "p23", "people", False, True, [25],  # AI-supplemented
          p23_questions(
              "Describe a person who often helps others",
              "描述一个经常帮助他人的人。",
              [
                  "What can children do to help their parents?",
                  "Should children help their parents with household chores?",
                  "What kind of help do people need when looking for a new job?",
                  "Who should people ask for help, colleagues or family members?",
                  "Do you think schools should teach children to do household chores?",
                  "Why are employees reluctant to ask their managers for help?",
              ],
          ),
          cue_card=p23_cue(
              ["Who this person is", "How often he/she helps others", "How/why he/she helps others", "And how you feel about this person"],
              ["这个人是谁", "他/她多久帮一次他人", "他/她如何/为什么帮助他人", "并谈谈你对这个人的感受"],
          )),
    topic("p23-smart", "描述一个用聪明方式解决问题的人", "Describe a person who solved a problem in a smart way",
          "p23", "people", False, True, [25],  # AI-supplemented
          p23_questions(
              "Describe a person who solved a problem in a smart way",
              "描述一个用聪明方式解决问题的人。",
              [
                  "Do you think children are born smart or they learn to become smart?",
                  "How do children become smart at school?",
                  "Why are some people well-rounded and others only good at one thing?",
                  "Why does modern society need talents of all kinds?",
                  "Do you think smart children are happier than other children?",
                  "Is it important for schools to identify and develop each student's talents?",
              ],
          ),
          cue_card=p23_cue(
              ["Who this person is", "What the problem was", "How he/she solved it", "And explain why you think he/she did it in a smart way"],
              ["这个人是谁", "问题是什么", "他/她如何解决", "并解释为什么你觉得他/她的方式很聪明"],
          )),
    topic("p23-nature", "描述一个喜欢保护自然的人", "Describe a person who likes to look after the natural world",
          "p23", "people", False, True, [26],  # AI-supplemented
          p23_questions(
              "Describe a person who likes to look after the natural world",
              "描述一个喜欢保护自然的人。",
              [
                  "Do you think parents should teach their children how to protect the environment?",
                  "What laws about the environment are effective in your country?",
                  "Which do you think people prefer, rewards or punishment, when it comes to government intervention in environmental protection?",
                  "Is it easy for children in cities to get close to the natural world?",
                  "What can people do to protect the natural world?",
                  "Is it important to teach students environmental protection at school?",
              ],
          ),
          cue_card=p23_cue(
              ["Who this person is", "What he or she does", "How he or she does it", "How often he or she does it", "And explain how you feel about this person"],
              ["这个人是谁", "他/她做什么", "他/她怎么做", "他/她多久做一次", "并谈谈你对这个人的感受"],
          )),
    # OBJECTS (10)
    topic("p23-law", "描述一项你想在国内推行的新法律", "Describe a new law you would like to introduce in your country",
          "p23", "object-p23", False, False, [28],
          p23_questions(
              "Describe a new law you would like to introduce in your country",
              "描述一项你想在国内推行的新法律。",
              [
                  "What rules should students follow at school?",
                  "Do people in your country usually obey the law?",
                  "What kinds of behavior are considered as good behavior?",
                  "Do you think children can learn about the law outside of school?",
                  "What are the benefits for people to obey rules?",
                  "How can parents teach children to obey rules?",
              ],
          ),
          cue_card=p23_cue(
              ["What law it is", "What changes this law brings", "Whether this new law will be popular", "How you came up with the new law", "And explain how you feel about this new law"],
              ["是什么法律", "这项法律带来什么变化", "这项新法会不会受欢迎", "你是怎么想出这项新法的", "并解释你对这项新法的感受"],
          )),
    topic("p23-changed-plan", "描述你最近不得不改变的一个计划", "Describe a plan that you had to change recently",
          "p23", "object-p23", False, False, [28],
          p23_questions(
              "Describe a plan that you had to change recently",
              "描述你最近不得不改变的一个计划。",
              [
                  "Do people often change their plans?",
                  "Would you tell others if you change your plan?",
                  "Why do you think parents still make plans for their children nowadays?",
                  "How does technology help people make plans?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["When this happened", "What made you change the plan", "What the new plan was", "And how you felt about the change"],
              ["这件事发生在什么时候", "是什么让你改变计划", "新计划是什么", "并谈谈你对这次变化的感受"],
          )),
    topic("p23-video", "描述一个有趣的视频", "Describe an interesting video",
          "p23", "object-p23", False, False, [29],
          p23_questions(
              "Describe an interesting video",
              "描述一个有趣的视频。",
              [
                  "What kind of videos do people in your country like to watch?",
                  "Which is more helpful, watching videos or reading books?",
                  "What skills can people learn from watching videos?",
                  "Are there any differences between the videos that young people and old people like to watch?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["When and where you watched it", "What it is about", "Why you watched it", "And explain how you feel about it"],
              ["你什么时候在哪里看的", "它讲的是什么", "你为什么看它", "并谈谈你对它的感受"],
          )),
    topic("p23-movie", "描述一部你最近看并喜欢的电影", "Describe a movie you watched and enjoyed recently",
          "p23", "object-p23", False, False, [29],
          p23_questions(
              "Describe a movie you watched and enjoyed recently",
              "描述一部你最近看并喜欢的电影。",
              [
                  "What kinds of movies do you think are successful in your country?",
                  "What are the factors that make a successful movie?",
                  "Do Chinese people prefer to watch domestic movies or foreign movies?",
                  "Do you think only well-known directors can create the best movies?",
                  "Do you think successful movies should have well-known actors or actresses in leading roles?",
                  "Why do people prefer to watch movies in the cinema?",
              ],
          ),
          cue_card=p23_cue(
              ["When and where you watched it", "Who you watched it with", "What it was about", "And explain why you watched this movie"],
              ["你什么时候在哪里看的", "你和谁一起看的", "它讲的是什么", "并解释你为什么看这部电影"],
          )),
    topic("p23-tech", "描述一件你想拥有的科技产品(非手机)", "Describe a piece of technology (not a phone) that you would like to own",
          "p23", "object-p23", False, False, [30],
          p23_questions(
              "Describe a piece of technology (not a phone) that you would like to own",
              "描述一件你想拥有的科技产品(非手机)。",
              [
                  "What are the differences between the technology of the past and that of today?",
                  "What technology do young people like to use?",
                  "What are the differences between online and face-to-face communication?",
                  "Do you think technology has changed the way people communicate?",
                  "What negative effects does technology have on people's relationships?",
                  "What are the differences between making friends in real life and online?",
              ],
          ),
          cue_card=p23_cue(
              ["What it is", "How much it costs", "How you knew it", "And explain why you would like to own it"],
              ["它是什么", "它多少钱", "你是怎么知道它的", "并解释为什么你想拥有它"],
          )),
    topic("p23-heirloom", "描述一件家里长期保存的重要物品", "Describe something important that has been kept in your family for a long time",
          "p23", "object-p23", False, False, [30],
          p23_questions(
              "Describe something important that has been kept in your family for a long time",
              "描述一件家里长期保存的重要物品。",
              [
                  "What things do families keep for a long time?",
                  "What's the difference between things valued by people in the past and today?",
                  "What kinds of things are kept in museums?",
                  "What's the influence of technology on museums?",
                  "What are the benefits of technology for learning history?",
                  "Why do people visit museums?",
              ],
          ),
          cue_card=p23_cue(
              ["What it is", "When your family had it", "How your family got it", "And explain why it is important to your family"],
              ["它是什么", "你们家什么时候有的", "你们家是怎么得到的", "并解释为什么它对你们家很重要"],
          )),
    topic("p23-perfect-job", "描述一个未来你想做的完美工作", "Describe a perfect job you would like to have in the future",
          "p23", "object-p23", False, False, [31],
          p23_questions(
              "Describe a perfect job you would like to have in the future",
              "描述一个未来你想做的完美工作。",
              [
                  "What kind of job can be called a 'dream job'?",
                  "What jobs do children want to do when they grow up?",
                  "Do people's ideal jobs change as they grow up?",
                  "What should people consider when choosing jobs?",
                  "Is salary the main reason why people choose a certain job?",
                  "What kind of jobs are the most popular in your country?",
              ],
          ),
          cue_card=p23_cue(
              ["What it is", "How you knew it", "What you need to learn to get the job", "And explain why you think it is your perfect job"],
              ["它是什么", "你是怎么知道它的", "要得到这份工作你需要学什么", "并解释为什么你觉得它是你理想的工作"],
          )),
    topic("p23-foreign-job", "描述一个你想在国外做的短期工作", "Describe a short-term job you want to have in a foreign country",
          "p23", "object-p23", False, False, [31],
          p23_questions(
              "Describe a short-term job you want to have in a foreign country",
              "描述一个你想在国外做的短期工作。",
              [
                  "What short-term jobs do young people do in other countries?",
                  "What challenges do young people face when working abroad?",
                  "What are the benefits of working for an international company?",
                  "What personal skills are required to work in an international company?",
                  "What kind of work can young people do in foreign countries?",
                  "Why are some people unwilling to work in other countries?",
              ],
          ),
          cue_card=p23_cue(
              ["Where it is", "How you know of it", "What the job is", "And explain why you want to do it"],
              ["它在哪里", "你是怎么知道它的", "这份工作是什么", "并解释你为什么想做它"],
          )),
    topic("p23-app", "描述你电脑或手机上的一个程序或APP", "Describe a program or app on your computer or phone",
          "p23", "object-p23", False, False, [32],
          p23_questions(
              "Describe a program or app on your computer or phone",
              "描述你电脑或手机上的一个程序或APP。",
              [
                  "What are the differences between old and young people when using apps?",
                  "Why do some people not like using apps?",
                  "What apps are popular in your country? Why?",
                  "Should parents limit their children's use of computer programs and computer games? Why and how?",
                  "Do you think young people are more and more reliant on these programs?",
                  "What do you think about some countries banning children from using social media?",
              ],
          ),
          cue_card=p23_cue(
              ["What it is", "How often you use it", "When/how you use it", "When/how you found it", "And explain how you feel about it"],
              ["它是什么", "你多久用一次", "你什么时候/怎么用", "你什么时候/怎么发现它的", "并谈谈你对它的感受"],
          )),
    topic("p23-overspent", "描述一件你花钱超过预期的物品", "Describe an item on which you spent more than expected",
          "p23", "object-p23", False, True, [32, 33],  # AI-supplemented
          p23_questions(
              "Describe an item on which you spent more than expected",
              "描述一件你花钱超过预期的物品。",
              [
                  "Do you often buy more than you expected?",
                  "What do you think young people spend most of their money on?",
                  "Do you think it is important to save money? Why?",
                  "Do people buy things they don't need?",
                  "Do you think it is the rich people's responsibility to donate money to people in need?",
                  "What kind of things are people happy to pay a high price for?",
              ],
          ),
          cue_card=p23_cue(
              ["What it is", "How much you spent on it", "Why you bought it", "And explain why you think you spent more than expected"],
              ["它是什么", "你花了多少钱", "你为什么买它", "并解释为什么你觉得你花超了预期"],
          )),
    # EVENTS (12)
    topic("p23-decision", "描述你做过的一个重大决定", "Describe an important decision that you made",
          "p23", "event-p23", False, True, [35],  # AI-supplemented
          p23_questions(
              "Describe an important decision that you made",
              "描述你做过的一个重大决定。",
              [
                  "Do you think children sometimes have to make important decisions?",
                  "What important decisions do teenagers need to make after graduation?",
                  "Who can children turn to for help when making a decision?",
                  "Do you think advertisements can influence our decisions when shopping?",
                  "Do you think the influence of advertising is good?",
                  "How do people usually make important decisions?",
              ],
          ),
          cue_card=p23_cue(
              ["What the decision was", "How you made your decision", "What the results of the decision were", "And explain why it was important"],
              ["这个决定是什么", "你是怎么做这个决定的", "这个决定的结果是什么", "并解释为什么它很重要"],
          )),
    topic("p23-early", "描述一次你很早就起床的经历", "Describe a time when you got up early",
          "p23", "event-p23", False, False, [35],
          p23_questions(
              "Describe a time when you got up early",
              "描述一次你很早就起床的经历。",
              [
                  "Do you know anyone who likes to get up early?",
                  "Why do people get up early?",
                  "What kinds of occasions need people to arrive early?",
                  "Why do some people like to stay up late?",
                  "Is it good to arrive early in any situation?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["When it was", "What you did", "Why you got up early", "And how you felt about it"],
              ["是什么时候", "你做了什么", "你为什么早起", "并谈谈你当时的感受"],
          )),
    topic("p23-group", "描述一次你团队合作的经验", "Describe a time when you worked in a group",
          "p23", "event-p23", False, False, [36],
          p23_questions(
              "Describe a time when you worked in a group",
              "描述一次你团队合作的经验。",
              [
                  "Why do some people prefer to work by themselves?",
                  "What should a leader do to make team members want to follow him or her?",
                  "Should students learn to do group work?",
                  "What group tasks are there in schools?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["What you did", "Who you worked with", "What problems you faced", "And explain why you worked in the group"],
              ["你做了什么", "你与谁一起合作", "你遇到了什么问题", "并解释你为什么团队合作"],
          )),
    topic("p23-sports", "描述一个你看过并喜欢的现场体育赛事", "Describe a live sports event you watched and liked",
          "p23", "event-p23", False, False, [36],
          p23_questions(
              "Describe a live sports event you watched and liked",
              "描述一个你看过并喜欢的现场体育赛事。",
              [
                  "Why do some people like to watch sports events?",
                  "Where do people normally watch sports events?",
                  "What are the advantages of watching sports events online?",
                  "What sports matches are suitable for children to attend?",
                  "待补充",
              ],
          ),
          cue_card=p23_cue(
              ["What it was", "When and where you watched it", "Who you watched it with", "And explain why you liked it"],
              ["是什么赛事", "你什么时候在哪里看的", "你和谁一起看的", "并解释你为什么喜欢它"],
          )),
    topic("p23-proud", "描述一次你为家人感到骄傲的时刻", "Describe a time when you felt proud of a family member",
          "p23", "event-p23", False, False, [37],
          p23_questions(
              "Describe a time when you felt proud of a family member",
              "描述一次你为家人感到骄傲的时刻。",
              [
                  "When would parents feel proud of their children?",
                  "Should parents reward children? Why and how?",
                  "Is it good to reward children too often? Why?",
                  "On what occasions would adults be proud of themselves?",
                  "Do rewards help a child become better?",
                  "What do you think about children working hard just for grades?",
              ],
          ),
          cue_card=p23_cue(
              ["When it happened", "Who the person is", "What the person did", "And explain why you felt proud of him/her"],
              ["这件事发生在什么时候", "这个人是谁", "这个人做了什么", "并解释为什么你为他/她感到骄傲"],
          )),
    topic("p23-imagination", "描述一次你需要发挥想象力的时刻", "Describe a time you needed to use your imagination",
          "p23", "event-p23", False, False, [37],
          p23_questions(
              "Describe a time you needed to use your imagination",
              "描述一次你需要发挥想象力的时刻。",
              [
                  "Do you think adults can have lots of imagination?",
                  "Do you think imagination is essential for scientists?",
                  "What kinds of jobs need imagination?",
                  "What subjects are helpful for children's imagination?",
                  "What games help develop children's imagination?",
                  "How important is imagination to children?",
              ],
          ),
          cue_card=p23_cue(
              ["When it was", "Why you needed to use imagination", "How difficult or easy it was", "And explain how you felt about it"],
              ["是什么时候", "你为什么需要发挥想象力", "是难还是容易", "并谈谈你当时的感受"],
          )),
    topic("p23-smiling", "描述一个很多人都微笑的场合", "Describe an occasion when many people were smiling",
          "p23", "event-p23", False, False, [38],
          p23_questions(
              "Describe an occasion when many people were smiling",
              "描述一个很多人都微笑的场合。",
              [
                  "Do you think people who like to smile are more friendly?",
                  "Why do most people smile in photographs?",
                  "Do women smile more than men? Why?",
                  "Do people smile more when they are younger or older?",
                  "Is smiling important in your culture?",
                  "Are there any occasions when people need to pretend to smile?",
              ],
          ),
          cue_card=p23_cue(
              ["When it happened", "Who you were with", "What happened", "And explain why most people were smiling"],
              ["这件事发生在什么时候", "你和谁在一起", "发生了什么", "并解释为什么大多数人都在微笑"],
          )),
    topic("p23-no-phone", "描述一次你不被允许使用手机的场合", "Describe an occasion when you were not allowed to use your mobile phone",
          "p23", "event-p23", False, False, [38],
          p23_questions(
              "Describe an occasion when you were not allowed to use your mobile phone",
              "描述一次你不被允许使用手机的场合。",
              [
                  "How do young and old people use mobile phones differently?",
                  "What positive and negative impact do mobile phones have on friendship?",
                  "Is it a waste of time to take pictures with mobile phones?",
                  "Do you think it is necessary to have laws on the use of mobile phones?",
                  "What are examples of good and poor phone manners?",
                  "How does the internet benefit people?",
              ],
          ),
          cue_card=p23_cue(
              ["When it was", "Where it was", "Why you were not allowed to use your mobile phone", "And how you felt about it"],
              ["是什么时候", "在哪里", "为什么不允许使用手机", "并谈谈你当时的感受"],
          )),
    topic("p23-advice", "描述一次你给别人建议的经历", "Describe a time when you gave advice to others",
          "p23", "event-p23", False, True, [39],  # AI-supplemented
          p23_questions(
              "Describe a time when you gave advice to others",
              "描述一次你给别人建议的经历。",
              [
                  "Should people prepare before giving advice?",
                  "Is it good to ask advice from strangers online?",
                  "What are the personalities of people whose job is to give advice to others?",
                  "What are the problems if you ask too many people for advice?",
                  "Why do some people think it is better to ask for advice from friends than from parents?",
                  "When would old people ask young people for advice?",
              ],
          ),
          cue_card=p23_cue(
              ["When it was", "To whom you gave the advice", "What the advice was", "And explain why you gave the advice"],
              ["是什么时候", "你给谁建议", "你给的是什么建议", "并解释你为什么给建议"],
          )),
    topic("p23-bad-music", "描述一个你参加过的、你不喜欢所放音乐的活动", "Describe an event you attended in which you didn't enjoy the music played",
          "p23", "event-p23", False, True, [39, 40],  # AI-supplemented
          p23_questions(
              "Describe an event you attended in which you didn't enjoy the music played",
              "描述一个你参加过的、你不喜欢所放音乐的活动。",
              [
                  "What kind of music events do people like today?",
                  "Do you think children should receive some musical education?",
                  "What are the differences between old and young people's music preferences?",
                  "What kind of music events are there in your country?",
                  "Why do many people like listening to music while doing sports?",
                  "What are the differences between listening to music at home and at a live concert?",
              ],
          ),
          cue_card=p23_cue(
              ["What it was", "Who you went with", "Why you decided to go there", "And explain why you didn't enjoy it"],
              ["是什么活动", "你和谁一起去的", "你为什么决定去", "并解释你为什么不喜欢它"],
          )),
    topic("p23-encourage", "描述一次你鼓励别人做他/她不想做的事", "Describe a time when you encouraged someone to do something that he/she didn't want to do",
          "p23", "event-p23", False, False, [40],
          p23_questions(
              "Describe a time when you encouraged someone to do something that he/she didn't want to do",
              "描述一次你鼓励别人做他/她不想做的事。",
              [
                  "How can leaders encourage their employees?",
                  "When should parents encourage their children?",
                  "What kind of encouragement should parents give?",
                  "Do you think some people are better than others at persuading?",
                  "Should children do everything their parents ask them to do?",
                  "How can employers encourage their staff?",
              ],
          ),
          cue_card=p23_cue(
              ["Who he or she is", "What you encouraged him/her to do", "How he/she reacted", "And explain why you encouraged him/her to do it"],
              ["他/她是谁", "你鼓励他/她做什么", "他/她反应如何", "并解释你为什么鼓励他/她做这件事"],
          )),
    topic("p23-vehicle", "描述一次你想骑自行车/摩托车/开车去的小旅行", "Describe a bicycle/motorcycle/car trip you would like to go",
          "p23", "event-p23", False, False, [40, 41],
          p23_questions(
              "Describe a bicycle/motorcycle/car trip you would like to go",
              "描述一次你想骑自行车/摩托车/开车去的小旅行。",
              [
                  "Which form of vehicle is more popular in your country, bikes, cars or motorcycles?",
                  "Do you think air pollution comes mostly from mobile vehicles?",
                  "Do you think people need to change the way of transportation drastically to protect the environment?",
                  "How are the transportation systems in urban areas and rural areas different?",
                  "Why do more people own and drive private vehicles now?",
                  "What do you think of the future of electric cars?",
              ],
          ),
          cue_card=p23_cue(
              ["Who you would like to go with", "Where you would like to go", "When you would like to go", "And explain why you would like to go by bicycle/motorcycle/car"],
              ["你想和谁一起去", "你想去哪里", "你想什么时候去", "并解释你为什么想骑自行车/摩托车/开车去"],
          )),
]


# ---------------------------------------------------------------------------
# Assemble + write
# ---------------------------------------------------------------------------

all_topics = p1_required + p1_high_freq + p23
assert len(all_topics) == 71, f"Expected 71 topics, got {len(all_topics)}"

# Per-topic validation
required_topic_fields = {"id", "slug", "title_zh", "title_en", "part", "category",
                         "is_required", "is_ai_supplemented", "pdf_pages", "questions"}
required_q_fields = {"id", "question_en", "question_zh", "answer_en",
                     "answer_hint_zh", "ai_supplemented"}

ids = set()
for t in all_topics:
    missing = required_topic_fields - set(t.keys())
    assert not missing, f"Topic {t.get('id')} missing fields: {missing}"
    assert t["id"] == t["slug"], f"id != slug for {t['id']}"
    assert t["id"] not in ids, f"Duplicate id: {t['id']}"
    ids.add(t["id"])
    assert t["part"] in ("p1-required", "p1-high-freq", "p23")
    if t["part"] != "p23":
        assert "cue_card" not in t, f"{t['id']} should not have cue_card"
    else:
        assert "cue_card" in t, f"{t['id']} must have cue_card"
        cc = t["cue_card"]
        assert 3 <= len(cc["bullets_en"]) <= 5, f"{t['id']} cue_card bullet count"
    q_ids = set()
    for qu in t["questions"]:
        missing_q = required_q_fields - set(qu.keys())
        assert not missing_q, f"Question {qu.get('id')} in {t['id']} missing: {missing_q}"
        assert qu["id"] not in q_ids, f"Duplicate q id {qu['id']} in {t['id']}"
        q_ids.add(qu["id"])

import datetime as _dt
data = {
    "meta": {
        "source_pdf": "抢鲜版-2026年5-8月雅思口语新题库0508.pdf",
        "source_pages": 41,
        "bank_period": "2026 May-Aug",
        "extracted_on": _dt.date.today().isoformat(),
        "topic_count": len(all_topics),
        "schema_version": "1.0.0",
        "notes": [
            "Topic count = 71 (PDF truth). Plan/questionnaire/task claim 73 due to a counting error (3+14+7+3=27, not 29). See .omo/drafts/answers-schema.md Note A.",
            "All answer fields are empty skeletons — Wave 2-7 workers fill them.",
            "PDF has placeholder questions marked '待补充' across 11 Part 3 sections + 2 Part 1 abstract topics (Tidiness q3, Music q3); preserved verbatim so Wave 8 can detect when they're still empty. Locations: p1f-tidiness q3, p1f-music q3, p23-fav-city p3-5, p23-boring p3-5, p23-tall p3-4, p23-business p3-6, p23-plants p3-6, p23-medical p3-3, p23-changed-plan p3-5, p23-video p3-5, p23-early p3-6, p23-group p3-5, p23-sports p3-5.",
            "AI-supplemented topics (per experience-questionnaire.md '没有' items): plant-grower, child-artist, self-learner, famous-person, helper, smart-solver, nature-lover, boring-place, overspent-item, important-decision, gave-advice, bad-music-event.",
        ],
    },
    "topics": all_topics,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT} — {len(all_topics)} topics")