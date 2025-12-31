import wikipediaapi
import re

# 干支のリスト
ZODIACS = ["申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未"]

def get_zodiac(year):
    """西暦から干支を算出する"""
    remainder = year % 12
    return ZODIACS[remainder]

def get_birth_year(name):
    """Wikipediaから誕生年を推測する"""
    # 日本語のWikipediaを指定
    wiki = wikipediaapi.Wikipedia(
        user_agent='CelebrityZodiacFinder/1.0 (your_email@example.com)',
        language='ja'
    )
    
    page = wiki.page(name)

    if not page.exists():
        return None

    # 概要テキストから「1xxx年」または「2xxx年」というパターンを検索（簡易的）
    # 生年月日などの記載がある最初の部分を探す
    text = page.summary[0:200] 
    match = re.search(r'([1-2][0-9]{3})年', text)
    
    if match:
        return int(match.group(1))
    return None

def main():
    print("=== 有名人干支チェッカー ===")
    name = input("干支が知りたい有名人の名前を入れてください: ")

    year = get_birth_year(name)

    if year:
        zodiac = get_zodiac(year)
        print(f"-----------------------------")
        print(f"{name} さんの生まれ年は {year}年 です")
        print(f"{name} さんは  {zodiac}  年です！")
        print(f"-----------------------------")
    else:
        print("ごめん、分からへん。その人有名ちゃうやろ？")

if __name__ == "__main__":
    main()