‏#!/usr/bin/env python3
‏# -*- coding: utf-8 -*-

"""
ئیبن ڕەشید - ئامرازی فێرکاری (نوێکراوە بە instagrapi 2.3.0)
تەنها بۆ مەبەستی فێرکاری - بەکارهێنانی نایاسایی قەدەغەیە
"""

‏import os
‏import sys
‏import json
‏import time
‏import random
‏import logging
‏from datetime import datetime
‏from typing import List, Dict, Optional

# دڵنیابوون لە دامەزراندنی instagrapi
‏try:
‏    from instagrapi import Client
‏    from instagrapi.exceptions import LoginRequired, ClientError
‏except ImportError:
‏    print("📦 دامەزراندنی instagrapi...")
‏    os.system('pip install instagrapi')
‏    from instagrapi import Client
‏    from instagrapi.exceptions import LoginRequired, ClientError

# ============================================
# بەشی 1: ڕێکخستنی لۆگ کردن
# ============================================

‏def setup_logging():
    """ڕێکخستنی لۆگ کردن بۆ بینینی هەڵەکان"""
‏    logging.basicConfig(
‏        level=logging.INFO,
‏        format='%(asctime)s - %(levelname)s - %(message)s',
‏        handlers=[
‏            logging.FileHandler("insta_tool.log"),
‏            logging.StreamHandler()
        ]
    )
‏    return logging.getLogger(__name__)

‏logger = setup_logging()

# ============================================
# بەشی 2: دروستکردنی ژمارە موبایلەکانی عێراق
# ============================================

‏class IraqiPhoneNumberGenerator:
    """
    پۆلێک بۆ دروستکردنی ژمارە موبایلەکانی عێراق
‏    https://github.com/subzeroid/instagrapi
    """
    
‏    COUNTRY_CODE = "964"
    
    # پێشگرە ڕاستەکانی کۆمپانیاکانی عێراق (بەپێی ڕاستکردنەوەکانی تۆ)
‏    PROVIDER_PREFIXES = {
‏        "asiacell": ["0770", "0771", "0772", "0773", "0774", "0775", "0776", "0777", "0778", "0779"],
‏        "korek": ["0750", "0751"],
‏        "zain": ["0780", "0781", "0782", "0783", "0784", "0785", "0786", "0787", "0788", "0789",
                 "0790", "0791", "0792", "0793", "0794", "0795", "0796", "0797", "0798", "0799"],
‏        "itishaluna": ["0740", "0741", "0742", "0743", "0744"],
‏        "kalemat": ["0745", "0746", "0747", "0748", "0749"],
‏        "mobitel": ["0760", "0761"],
‏        "moutiny": ["0762", "0763", "0764", "0765", "0766", "0767", "0768", "0769"]
    }
    
‏    @staticmethod
‏    def generate_phone_number(provider: Optional[str] = None) -> Dict:
        """
        دروستکردنی ژمارەیەکی هەڕەمەکی بۆ عێراق
        
‏        Args:
‏            provider: ناوی کۆمپانیا (ئەگەر دیاری نەکرابێت، هەڕەمەکی هەڵدەبژێردرێت)
        
‏        Returns:
‏            Dictionaryێک لەگەڵ وردەکاری ژمارەکە
        """
‏        if provider is None:
‏            provider = random.choice(list(IraqiPhoneNumberGenerator.PROVIDER_PREFIXES.keys()))
        
‏        if provider not in IraqiPhoneNumberGenerator.PROVIDER_PREFIXES:
‏            raise ValueError(f"کۆمپانیای {provider} نەناسراوە")
        
‏        prefix = random.choice(IraqiPhoneNumberGenerator.PROVIDER_PREFIXES[provider])
        
        # دروستکردنی 6 یان 7 ژمارەی پاشکۆ
‏        if len(prefix) == 4:  # پێشگرەکانی وەک 0770
‏            remaining = ''.join([str(random.randint(0, 9)) for _ in range(6)])
‏            full_number = prefix + remaining  # 4+6=10
‏        else:  # پێشگرەکانی وەک 078 (3 ژمارە)
‏            remaining = ''.join([str(random.randint(0, 9)) for _ in range(7)])
‏            full_number = prefix + remaining  # 3+7=10
        
‏        international = IraqiPhoneNumberGenerator.COUNTRY_CODE + full_number[1:]
        
‏        return {
‏            "id": random.randint(1000, 9999),
‏            "provider": provider,
‏            "prefix": prefix,
‏            "local_format": full_number,
‏            "international_format": international,
‏            "full_number": full_number,
‏            "created_at": datetime.now().isoformat()
        }
    
‏    @staticmethod
‏    def generate_multiple_numbers(count: int = 10, provider: Optional[str] = None) -> List[Dict]:
        """دروستکردنی چەندین ژمارە"""
‏        numbers = []
‏        for i in range(count):
‏            number = IraqiPhoneNumberGenerator.generate_phone_number(provider)
‏            number["id"] = i + 1
‏            numbers.append(number)
            # زیادکردنی درەو بۆ ڕێگری لە ناسینەوە
‏            time.sleep(random.uniform(0.1, 0.3))
‏        return numbers

# ============================================
# بەشی 3: ناردنی پەیام بۆ تیلیگرام
# ============================================

‏class TelegramBotSender:
    """
    پۆلێک بۆ ناردنی پەیام بۆ بۆتی تیلیگرام
‏    https://core.telegram.org/bots/api
    """
    
‏    def __init__(self, bot_token: str, chat_id: str):
‏        self.bot_token = bot_token
‏        self.chat_id = chat_id
‏        self.api_url = f"https://api.telegram.org/bot{bot_token}"
‏        self.session = requests.Session()
    
‏    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """ناردنی پەیام بۆ تیلیگرام"""
‏        try:
‏            import requests
‏            url = f"{self.api_url}/sendMessage"
‏            data = {
‏                "chat_id": self.chat_id,
‏                "text": text,
‏                "parse_mode": parse_mode
            }
‏            response = self.session.post(url, data=data, timeout=15)
‏            return response.status_code == 200
‏        except Exception as e:
‏            logger.error(f"هەڵە لە ناردنی پەیام: {e}")
‏            return False
    
‏    def send_formatted_numbers(self, numbers: List[Dict]) -> None:
        """ناردنی ژمارەکان بە شێوازی جوان بۆ تیلیگرام"""
‏        if not numbers:
‏            self.send_message("❌ هیچ ژمارەیەک دروست نەکرا")
‏            return
        
        # ناردنی کورتی
‏        summary = f"<b>📊 کورتی ژمارە دروستکراوەکان</b>\n"
‏        summary += f"• کۆی گشتی: {len(numbers)}\n"
‏        summary += f"• کاتی دروستکردن: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
‏        self.send_message(summary)
        
        # ناردنی وردەکاری هەر 5 ژمارە
‏        for i in range(0, len(numbers), 5):
‏            batch = numbers[i:i+5]
‏            message = "<b>📱 وردەکاری ژمارەکان</b>\n\n"
            
‏            for item in batch:
‏                message += f"<b>{item['id']}. {item['provider'].upper()}</b>\n"
‏                message += f"   📞 {item['local_format']}\n"
‏                message += f"   🌍 +{item['international_format']}\n"
‏                message += "────────────────\n"
            
‏            self.send_message(message)
‏            time.sleep(1)  # چاوەڕوانی کەم بۆ ڕێگری لە ڕەیت لیمیت

# ============================================
# بەشی 4: بەکارهێنانی instagrapi بۆ فێرکاری
# ============================================

‏class InstagramDemo:
    """
    پۆلێک بۆ پیشاندانی بەکارهێنانی instagrapi
    تەنها بۆ مەبەستی فێرکاری - نابێت بۆ هێرش بەکاربهێنرێت
    """
    
‏    def __init__(self, username: str = None, password: str = None):
‏        self.username = username
‏        self.password = password
‏        self.client = None
‏        self.session_file = "instagram_session.json"
    
‏    def login_with_session(self) -> bool:
        """
        چوونەژوورەوە بە بەکارهێنانی فایلی سێشن (ئەگەر هەبێت)
‏        https://github.com/subzeroid/instagrapi#session-with-persistence
        """
‏        try:
‏            self.client = Client()
            
            # ئەگەر فایلی سێشن هەبێت، باریدەکەین
‏            if os.path.exists(self.session_file):
‏                logger.info("بارکردنی سێشنی پێشوو...")
‏                self.client.load_settings(self.session_file)
                
                # هەوڵی چوونەژوورەوە بە سێشنی بارکراو
‏                try:
‏                    self.client.login(self.username, self.password)
‏                    self.client.get_timeline_feed()
‏                    logger.info("✅ سێشن سەرکەوتوو بوو")
‏                    return True
‏                except LoginRequired:
‏                    logger.warning("سێشنی پێشوو بەسەرنەچوو، دەستپێکردنەوە...")
‏                    os.remove(self.session_file)
‏                    return self.fresh_login()
‏            else:
‏                return self.fresh_login()
                
‏        except Exception as e:
‏            logger.error(f"هەڵە لە چوونەژوورەوە: {e}")
‏            return False
    
‏    def fresh_login(self) -> bool:
        """چوونەژوورەوەی نوێ و پاشەکەوتکردنی سێشن"""
‏        try:
‏            if not self.username or not self.password:
‏                logger.warning("ناوی بەکارهێنەر و پاسوۆرد دیاری نەکراوە")
‏                return False
            
‏            logger.info(f"هەوڵی چوونەژوورەوە بۆ @{self.username}...")
            
            # ڕێکخستنی درەو بۆ ڕێگری لە ناسینەوە
‏            self.client.delay_range = [1, 3]
            
            # چوونەژوورەوە
‏            self.client.login(self.username, self.password)
            
            # پاشەکەوتکردنی سێشن
‏            self.client.dump_settings(self.session_file)
‏            logger.info(f"✅ سێشن پاشەکەوت کرا بۆ {self.session_file}")
            
‏            return True
            
‏        except Exception as e:
‏            logger.error(f"هەڵە لە چوونەژوورەوە: {e}")
‏            return False
    
‏    def get_user_info_demo(self, target_username: str) -> Optional[Dict]:
        """
        پیشاندانی وەرگرتنی زانیاری بەکارهێنەر
        تەنها بۆ مەبەستی فێرکاری
        """
‏        try:
‏            if not self.client:
‏                logger.error("سەرەتا دەبێت بچیتە ژوورەوە")
‏                return None
            
‏            logger.info(f"وەرگرتنی زانیاری بۆ @{target_username}...")
            
            # وەرگرتنی ئایدی بەکارهێنەر
‏            user_id = self.client.user_id_from_username(target_username)
            
            # وەرگرتنی زانیاری تەواو
‏            user_info = self.client.user_info(user_id)
            
            # پیشاندانی زانیاری
‏            info = {
‏                "username": user_info.username,
‏                "full_name": user_info.full_name,
‏                "followers": user_info.follower_count,
‏                "following": user_info.following_count,
‏                "posts": user_info.media_count,
‏                "is_private": user_info.is_private,
‏                "is_verified": user_info.is_verified
            }
            
‏            logger.info(f"✅ زانیاری بۆ @{target_username} وەرگیرا")
‏            return info
            
‏        except Exception as e:
‏            logger.error(f"هەڵە لە وەرگرتنی زانیاری: {e}")
‏            return None

# ============================================
# بەشی 5: فەرمونی سەرەکی
# ============================================

‏def main():
    """فەرمونی سەرەکی"""
    
‏    print("="*70)
‏    print("ئیبن ڕەشید - ئامرازی فێرکاری (نوێکراوە بە instagrapi 2.3.0)")
‏    print("="*70)
‏    print("\n⚠️ ئاگادارباش:")
‏    print("   ئەم ئامرازە تەنها بۆ مەبەستی فێرکاری و ڕوونکردنەوەیە")
‏    print("   بەکارهێنانی بۆ تاقیکردنەوەی ژمارەی کەسانی تر نایاساییە")
‏    print("   سەردانی بکە بۆ زانیاری زیاتر: https://github.com/subzeroid/instagrapi\n")
    
    # پشکنینی نوسخەی instagrapi
‏    try:
‏        import instagrapi
‏        logger.info(f"✅ نوسخەی instagrapi: {instagrapi.__version__}")
‏    except:
‏        logger.info("⚠️ نوسخەی instagrapi نەدۆزرایەوە")
    
    # وەرگرتنی زانیاری تیلیگرام
‏    try:
‏        import requests
‏    except ImportError:
‏        os.system('pip install requests')
‏        import requests
    
‏    print("📱 بۆ ناردنی ئەنجام بۆ تیلیگرام:")
‏    bot_token = input("🔑 تۆکنی بۆتی تیلیگرام بنووسە: ").strip()
‏    chat_id = input("👤 ئایدی چاتی خۆت بنووسە: ").strip()
    
‏    if not bot_token or not chat_id:
‏        print("❌ تۆکن و چات ئایدی پێویستە")
‏        return
    
    # وەرگرتنی ژمارەی پێویست
‏    try:
‏        count = int(input("\n📊 ژمارەی ئەو ژمارانە بنووسە کە دەتەوێت دروست بکەیت (1-100): "))
‏        if count < 1 or count > 100:
‏            count = 10
‏            print("📌 10 وەرگیرا (پێویستە 1-100)")
‏    except:
‏        count = 10
‏        print("📌 10 وەرگیرا")
    
    # هەڵبژاردنی کۆمپانیا
‏    print("\n🏢 کۆمپانیاکان:")
‏    providers = list(IraqiPhoneNumberGenerator.PROVIDER_PREFIXES.keys())
‏    for i, provider in enumerate(providers, 1):
‏        print(f"   {i}. {provider}")
‏    print(f"   {len(providers)+1}. هەموویان (هەڕەمەکی)")
    
‏    try:
‏        choice = int(input("هەڵبژاردن (ژمارەکە بنووسە): "))
‏        if 1 <= choice <= len(providers):
‏            provider = providers[choice - 1]
‏        else:
‏            provider = None
‏    except:
‏        provider = None
‏        print("📌 هەڕەمەکی هەڵبژێردرا")
    
    # دروستکردنی ژمارەکان
‏    print(f"\n🔄 دروستکردنی {count} ژمارە...")
‏    generator = IraqiPhoneNumberGenerator()
‏    numbers = generator.generate_multiple_numbers(count, provider)
    
    # پێشاندانی ژمارەکان
‏    print("\n📱 ژمارە دروستکراوەکان:")
‏    for num in numbers[:10]:  # تەنها 10 یەکەم پیشان بدە
‏        print(f"   {num['id']}. {num['provider']}: {num['local_format']}")
    
‏    if count > 10:
‏        print(f"   ... و {count - 10} دانەی تر")
    
    # ناردنی بۆ تیلیگرام
‏    print("\n📤 ناردنی ئەنجام بۆ تیلیگرام...")
‏    telegram = TelegramBotSender(bot_token, chat_id)
    
    # ناردنی پەیامی سەرەتا
‏    start_msg = f"<b>✅ ئامرازەکە بە سەرکەوتوویی کاردەکات</b>\n"
‏    start_msg += f"📊 {count} ژمارە دروستکرا\n"
‏    start_msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
‏    start_msg += f"<i>ئەم ژمارانە تەنها بۆ مەبەستی فێرکاری دروست کراون</i>"
    
‏    if telegram.send_message(start_msg):
‏        print("✅ پەیامی سەرەتا نێردرا")
        
        # ناردنی وردەکاری ژمارەکان
‏        telegram.send_formatted_numbers(numbers)
‏        print("✅ وردەکاری ژمارەکان نێردرا")
‏    else:
‏        print("❌ نەتوانرا پەیام بنێردرێت")
    
    # پاشەکەوتکردن لە فایل
‏    filename = f"iraq_numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
‏    with open(filename, 'w', encoding='utf-8') as f:
‏        json.dump(numbers, f, ensure_ascii=False, indent=2)
    
‏    print(f"\n📁 ژمارەکان پاشەکەوت کراون لە: {filename}")
    
    # بەشی پیشاندانی instagrapi (ئەگەر بەکارهێنەر ویستی)
‏    print("\n" + "="*70)
‏    print("🔧 بەشی پیشاندانی instagrapi (ئارەزوومەندانە)")
‏    print("="*70)
‏    print("ئەم بەشە تەنها بۆ پیشاندانی تواناییەکانی instagrapiە")
‏    print("و پێویستی بە ناوی بەکارهێنەر و پاسوۆردی ڕاستەقینەی ئینستاگرام هەیە\n")
    
‏    demo_choice = input("ئایا دەتەوێت instagrapi تاقی بکەیتەوە؟ (n) بۆ نەخێر: ").lower()
    
‏    if demo_choice == 'y' or demo_choice == 'yes':
‏        insta_user = input("ناوی بەکارهێنەری ئینستاگرام (تەنها بۆ فێرکاری): ").strip()
‏        insta_pass = input("پاسوۆردی ئینستاگرام (تەنها بۆ فێرکاری): ").strip()
        
‏        if insta_user and insta_pass:
‏            demo = InstagramDemo(insta_user, insta_pass)
‏            if demo.login_with_session():
                # وەرگرتنی زانیاری بۆ ئەکاونتی خۆی یان ئەکاونتێکی گشتی
‏                target = input("ناوی بەکارهێنەری ئامانج (بۆ نموونە instagram): ").strip() or "instagram"
                
‏                info = demo.get_user_info_demo(target)
‏                if info:
‏                    print(f"\n📊 زانیاری بۆ @{target}:")
‏                    print(f"   ناوی تەواو: {info['full_name']}")
‏                    print(f"   شوێنکەوتوو: {info['followers']:,}")
‏                    print(f"   بەشدار: {info['following']:,}")
‏                    print(f"   پۆست: {info['posts']}")
‏                    print(f"   تایبەت: {info['is_private']}")
‏                    print(f"   پشتڕاستکراوە: {info['is_verified']}")
    
‏    print("\n👋 سوپاس بۆ بەکارهێنانی ئەم ئامرازە. تکایە بە ڕەوشتی و یاسایی مامەڵە بکە.")
‏    print("📚 سەرچاوەی فێربوون: https://github.com/subzeroid/instagrapi")

‏if __name__ == "__main__":
‏    main()
