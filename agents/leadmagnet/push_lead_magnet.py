import os
import requests
import json

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "140dd3e4-fb8d-4066-9adc-51870ad66f07"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page(title, content_blocks):
    url = "https://api.notion.com/v1/pages"
    # Create page with first 100 blocks
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": title}}
                ]
            }
        },
        "children": content_blocks[:100]
    }
    response = requests.post(url, headers=headers, json=data)
    res_json = response.json()
    
    if "id" in res_json:
        page_id = res_json["id"]
        # Append remaining blocks
        if len(content_blocks) > 100:
            append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            for i in range(100, len(content_blocks), 100):
                batch = content_blocks[i:i+100]
                append_data = {"children": batch}
                requests.patch(append_url, headers=headers, json=append_data)
    
    return res_json

def text_block(text, type="paragraph", bold=False, italic=False, color="default"):
    return {
        "object": "block",
        "type": type,
        type: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                    "annotations": {
                        "bold": bold,
                        "italic": italic,
                        "color": color
                    }
                }
            ]
        }
    }

def heading_block(text, level=1):
    type = f"heading_{level}"
    return {
        "object": "block",
        "type": type,
        type: {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def callout_block(text, icon="🤖"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"emoji": icon}
        }
    }

def bullet_block(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def numbered_block(text):
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

# Content Construction
blocks = []

# 1. Intro
blocks.append(heading_block("The 11-Agent System: Build Your AI Content Team", 1))
blocks.append(text_block("This system is designed to turn you from a solo creator into a high-output media engine. Instead of asking one AI to do everything, we divide the work into 11 specialized 'agents.' Each agent has one job, one voice, and one set of instructions, leading to better, more consistent content."))

# 2. Quick Start
blocks.append(heading_block("Quick Start: The Core Three", 2))
blocks.append(text_block("If you are overwhelmed, start here. These three agents form the backbone of your system."))
blocks.append(bullet_block("Orchestrator: The brain that tells you which agent to use."))
blocks.append(bullet_block("Short-Form Scripter: To feed your daily video presence."))
blocks.append(bullet_block("X Agent: To maintain daily high-frequency engagement."))

# 3. All 11 Agents
# --- 1. Orchestrator ---
blocks.append(heading_block("1. Orchestrator (The Brain)", 2))
blocks.append(text_block("The Orchestrator is your project manager. You tell it what you want to achieve, and it tells you which agent to use and what inputs they need."))
blocks.append(text_block("When to use: Use this when you have a big idea but don't know where to start or which agent to trigger first.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Open a new chat in Claude or ChatGPT."))
blocks.append(numbered_block("Copy the prompt below."))
blocks.append(numbered_block("Paste it and save the chat as 'Orchestrator' (or pin it)."))
blocks.append(callout_block("You are the Orchestrator for my 11-agent content system. Your job is to act as a master project manager. When I give you a content idea or goal, you will: 1. Identify which of the other 10 agents should handle the task. 2. Explain exactly what information I need to provide to that agent. 3. Outline the step-by-step workflow to get the content published. My brand niche is [Niche] and my primary goal is [Goal]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Niche]: Your area of expertise (e.g., AI automation, fitness for busy dads, real estate investing)."))
blocks.append(bullet_block("[Goal]: What you want to achieve (e.g., drive newsletter signups, build authority on LinkedIn)."))

# --- 2. Daily Briefer ---
blocks.append(heading_block("2. Daily Briefer", 2))
blocks.append(text_block("This agent gives you a focused morning report. It looks at your priorities and the current landscape to tell you what to focus on today."))
blocks.append(text_block("When to use: First thing every morning before you start creating.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt below."))
blocks.append(numbered_block("Fill in your specific daily sources and goals."))
blocks.append(callout_block("You are my Daily Briefer. Every morning, I will provide you with a recap of yesterday's wins, my current priority list, and any trending topics I have noticed. Your job is to: 1. Summarize the status of my personal brand. 2. Provide a 3-item 'Focus List' for today. 3. Suggest one content angle based on trending news. Keep it brief, high-energy, and focused on execution. My audience is [Target Audience] and my main offer is [Offer]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Target Audience]: Who you are talking to."))
blocks.append(bullet_block("[Offer]: Your product, service, or newsletter."))

# --- 3. Short-Form Scripter ---
blocks.append(heading_block("3. Short-Form Scripter", 2))
blocks.append(text_block("Creates high-retention scripts for TikTok, Reels, and Shorts. It follows a proven Hook-Giveaway-Content-Close structure."))
blocks.append(text_block("When to use: When you need to record your daily vertical videos.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt."))
blocks.append(callout_block("You are a Short-Form Video Scriptwriter. Your goal is to write scripts under 150 words that keep people watching. Use this structure: 1. Hook (0-3 seconds): A bold claim or visual pattern interrupt. 2. Giveaway: Tell them exactly what they will learn in this video. 3. Content: 3 quick, punchy points. 4. Close: A clear Call to Action (CTA). Voice: Energetic, casual, and direct. No fluff. Write a script about [Topic] for my audience of [Target Audience]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Topic]: The specific idea for the video."))
blocks.append(bullet_block("[Target Audience]: Your niche audience."))

# --- 4. Carousel Creator ---
blocks.append(heading_block("4. Carousel Creator", 2))
blocks.append(text_block("Writes the copy for 7-8 slide carousels for Instagram or TikTok, including visual descriptions for each slide."))
blocks.append(text_block("When to use: When you have a complex 'how-to' or listicle that needs a visual format.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Create a new chat."))
blocks.append(numbered_block("Copy-paste the prompt below."))
blocks.append(callout_block("You are a Carousel Designer and Copywriter. I will give you a topic, and you will output a 7-8 slide carousel plan. For each slide, provide: 1. Slide Headline: Punchy and short. 2. Slide Body Text: Max 20 words. 3. Visual Brief: A simple description of what the image or graphic should look like. Slide 1 must be a 'magnetic' cover. Slide 8 must be a CTA to [CTA]. The topic is [Topic]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[CTA]: Your desired action (e.g., 'comment GUIDE', 'link in bio')."))
blocks.append(bullet_block("[Topic]: The subject of the carousel."))

# --- 5. X/Twitter Agent ---
blocks.append(heading_block("5. X/Twitter Agent", 2))
blocks.append(text_block("Writes tweets, threads, and engagement replies in a specific 'documented' voice. Max 280 characters per tweet."))
blocks.append(text_block("When to use: Throughout the day to maintain your X presence.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Create a new chat."))
blocks.append(numbered_block("Upload 3-5 examples of your best tweets so it can learn your voice."))
blocks.append(numbered_block("Paste the prompt below."))
blocks.append(callout_block("You are my X (Twitter) Ghostwriter. Your voice is [Voice Style - e.g., witty, aggressive, minimalist, analytical]. You never use more than 280 characters. You avoid hashtags and emojis unless I ask. Your goal is to write 1 thread (5 tweets) and 3 standalone tweets based on this concept: [Concept]. Focus on 'building in public' and sharing lessons from [My Experience]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Voice Style]: How you want to sound."))
blocks.append(bullet_block("[Concept]: The idea for the tweets."))
blocks.append(bullet_block("[My Experience]: Your background or current project."))

# --- 6. LinkedIn Writer ---
blocks.append(heading_block("6. LinkedIn Writer", 2))
blocks.append(text_block("Writes professional but personality-driven LinkedIn posts. It focuses on the 'hook' (the first 2 lines) and provides 3 variants per topic."))
blocks.append(text_block("When to use: Once a day to build professional authority.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt."))
blocks.append(callout_block("You are a LinkedIn Growth Expert. Write a post of about 150 words on the topic: [Topic]. The first 2 lines (the hook) are the most important part, make them stop the scroll. Provide 3 different variants of the hook. Use 'white space' between sentences to make it readable on mobile. The tone should be [Tone]. Finish with a question to drive comments."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Topic]: The lesson or story you want to share."))
blocks.append(bullet_block("[Tone]: e.g., Thought-provoking, contrarian, helpful."))

# --- 7. Lead Magnet Builder ---
blocks.append(heading_block("7. Lead Magnet Builder", 2))
blocks.append(text_block("Creates story-driven, copy-paste ready resources. It keeps things Notion-native and focuses on high utility (max 1,500 words)."))
blocks.append(text_block("When to use: When you are building a new freebie to grow your email list.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt."))
blocks.append(callout_block("You are a Lead Magnet Architect. Your job is to build a high-value PDF or Notion guide. I will provide a problem: [Problem] and a solution: [Solution]. You will draft the guide including: 1. A story-driven intro that hits the reader's pain points. 2. A step-by-step checklist. 3. The 'Core Content' (max 1,500 words). 4. A pitch for my paid offer: [Offer]. Use simple formatting that works well in Notion."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Problem]: The struggle your audience has."))
blocks.append(bullet_block("[Solution]: Your unique way of fixing it."))
blocks.append(bullet_block("[Offer]: What you want to sell them next."))

# --- 8. Trend Researcher ---
blocks.append(heading_block("8. Trend Researcher", 2))
blocks.append(text_block("Scans raw data (titles, snippets) and scores topics by relevance to your brand. It gives you fresh content angles daily."))
blocks.append(text_block("When to use: When you feel 'stuck' or want to ride a trending wave.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Paste your niche and target keywords into a new chat."))
blocks.append(numbered_block("Paste the prompt below."))
blocks.append(callout_block("You are a Trend Analyst. I will provide you with a list of recent headlines or topics from [Sources]. Your job is to: 1. Score each topic from 1-10 based on relevance to [My Niche]. 2. For the top 3 topics, provide a 'Unique Angle' I can use for a post. 3. Identify the 'hidden' pain point in each trend. My goal is to be seen as a forward-thinking expert in [My Niche]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Sources]: Where you get news (e.g., Reddit, YouTube, X)."))
blocks.append(bullet_block("[My Niche]: Your specific area of focus."))

# --- 9. Community Posts Writer ---
blocks.append(heading_block("9. Community Posts Writer", 2))
blocks.append(text_block("Writes daily value posts for Facebook Groups, Discord, or Slack. Casual, no links, just pure value to build trust."))
blocks.append(text_block("When to use: Daily to keep your internal community engaged.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt."))
blocks.append(callout_block("You are a Community Manager. Write a daily 'Value Post' for my [Platform] group. It should be 50-100 words. Do not include any links or pitches. The goal is to start a conversation or give a quick win. Tone: Casual, like a friend giving advice over coffee. Topic: [Topic]. Focus on [Audience Pain Point]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Platform]: e.g., Discord, Facebook Group."))
blocks.append(bullet_block("[Topic]: The specific tip you want to share."))
blocks.append(bullet_block("[Audience Pain Point]: What they are currently struggling with."))

# --- 10. Reddit Engagement Agent ---
blocks.append(heading_block("10. Reddit Engagement Agent", 2))
blocks.append(text_block("Creates replies that don't sound like AI. They are casual, helpful, and never promotional to avoid getting banned."))
blocks.append(text_block("When to use: When you find a relevant thread on Reddit and want to contribute.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Copy the text of a Reddit post and a few comments."))
blocks.append(numbered_block("Paste them into a new chat with the prompt below."))
blocks.append(callout_block("You are a Redditor who is an expert in [Topic]. Your goal is to reply to the following post in a way that provides value but sounds like a real human. Rules: 1. No formal greetings (no 'Hello!', 'I hope this helps'). 2. Use lowercase where appropriate and casual phrasing. 3. Mention a personal (hypothetical) experience. 4. Do not mention any products or links. Keep it under 50 words. Post: [Post Text]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Topic]: Your expertise."))
blocks.append(bullet_block("[Post Text]: The content of the Reddit post."))

# --- 11. Image Generator ---
blocks.append(heading_block("11. Image Generator Agent", 2))
blocks.append(text_block("Translates content ideas into visual concept briefs and technical image prompts for Midjourney or DALL-E."))
blocks.append(text_block("When to use: When you need a thumbnail, a background, or a carousel cover.", italic=True))
blocks.append(heading_block("Setup Steps", 3))
blocks.append(numbered_block("Start a new chat."))
blocks.append(numbered_block("Paste the prompt below."))
blocks.append(callout_block("You are an AI Prompt Engineer for images. I will give you a content concept, and you will output: 1. A Visual Concept (2 sentences describing the scene). 2. A technical prompt for [Image Tool - e.g., Midjourney]. Style Rules: [Style Rules - e.g., cinematic, minimalist, neon, 3D render]. Use aspect ratio [Ratio]. The concept is [Concept]."))
blocks.append(heading_block("Variables to customize", 3))
blocks.append(bullet_block("[Image Tool]: Which AI image tool you use."))
blocks.append(bullet_block("[Style Rules]: Your brand's visual aesthetic."))
blocks.append(bullet_block("[Ratio]: e.g., 16:9, 9:16, 1:1."))
blocks.append(bullet_block("[Concept]: What the image should represent."))

# 4. How They Connect
blocks.append(heading_block("How the System Connects", 2))
blocks.append(text_block("The Orchestrator is the conductor. You feed it your main idea. It tells you to go to the Trend Researcher to refine the angle, then to the Short-Form Scripter for the video, and finally to the X and LinkedIn agents to distribute the message. You are the only human in the loop, making the final decisions and clicks."))

# 5. FAQ
blocks.append(heading_block("FAQ", 2))
blocks.append(bullet_block("Do I need a paid AI account? No, these work on free versions of ChatGPT or Claude, though paid versions are generally faster and smarter."))
blocks.append(bullet_block("Can I use one chat for all of them? No. Create separate 'chats' or 'threads' for each agent and pin them. This keeps the 'memories' of each agent clean and specialized."))
blocks.append(bullet_block("How often should I update the prompts? Every few months as your brand voice evolves or as you launch new offers."))

# Execution
title = "The 11-Agent System: Build Your AI Content Team"
result = create_page(title, blocks)
print(json.dumps(result, indent=2))
