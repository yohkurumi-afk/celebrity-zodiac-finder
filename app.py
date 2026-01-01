import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def get_birth_year(name):
    """
    指定された有名人の名前からWikipediaを解析し、誕生年と「自信の有無」を返す。
    戻り値: (year, is_confident)
    """
    url = f"https://ja.wikipedia.org/wiki/{name}"
    
    # ブラウザのふりをするためのヘッダー
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"エラー: アクセスできませんでした (Status: {response.status_code})")
            return None, False

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- 戦略1: Infobox（基本情報テーブル）から探す ---
        infobox = soup.find('table', class_='infobox')

        # class='infobox'がない場合のフォールバック
        if not infobox:
            tables = soup.find_all('table')
            for table in tables:
                text = table.get_text()
                if '生誕' in text or '生年月日' in text or '出生' in text or '生まれ' in text or '誕生' in text:
                    infobox = table
                    break
        
        if infobox:
            for row in infobox.find_all('tr'):
                header = row.find('th')
                data = row.find('td')
                
                if header and data:
                    header_text = header.get_text().strip()
                    if "生誕" in header_text or "生年月日" in header_text or "出生" in header_text or "生まれ" in header_text or "誕生" in header_text:
                        data_text = data.get_text()
                        matches = re.findall(r'([0-9]{1,4})年', data_text)
                        
                        if matches:
                            years = [int(y) for y in matches]
                            valid_years = [y for y in years if y < 2100]
                            if valid_years:
                                # 表から見つかった -> 自信あり (True)
                                return max(valid_years), True

        # --- 戦略2: 本文（段落）から探す ---
        paragraphs = soup.find_all('p')
        
        for p in paragraphs[:3]:
            text = p.get_text()
            matches = re.findall(r'([0-9]{1,4})年', text)
            
            if matches:
                for match in matches:
                    year = int(match)
                    if 100 < year < 2100:
                        # 本文から推測 -> 自信なし (False)
                        return year, False

        print("エラー: 表からも本文からも『年』が見つかりませんでした")

    except Exception as e:
        print(f"予期せぬエラー: {e}")
        pass
        
    return None, False

def get_zodiac(year):
    """
    西暦から干支（文字）を計算して返す。
    """
    eto_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    eto_icon = ["🐹チュ〜", "🐮モ〜", "🐯ガオ〜", "🐰ウサ〜", "🐲リュ〜", "🐍シャ〜", "🐴ヒヒ〜ン", "🐏メェ〜", "🐵キ〜", "🐔コケコッコ〜", "🐶ワンッ", "🐗シシ〜"]
    
    index = (year - 4) % 12
    return eto_list[index], eto_icon[index]

def main():
    st.title("あの人の干支が知りたい")

    name = st.text_input("干支が知りたい有名人の名前を入れてください: ")

    if st.button("調べる"):
        if not name:
            st.warning("名前を入力してください")
        else:
            with st.spinner("検索中..."):
                # ここで年と自信フラグの2つを受け取る
                year, is_confident = get_birth_year(name)

            if year:
                zodiac_name, zodiac_icon = get_zodiac(year)
                
                if is_confident:
                    # 自信ありの場合の出力
                    output_text = f"""
                    {name} さんの生まれ年は {year}年 です
                    {name} さんは  {zodiac_name}  年です！  {zodiac_icon}
                    """
                else:
                    # 自信なしの場合の出力
                    output_text = f"""
                    ちょっと自信ないけど...
                    {name} さんの生まれ年は {year}年 です
                    {name} さんは  {zodiac_name}  年です！  {zodiac_icon}
                    ちゃんと調べてね
                    """
                
                st.text(output_text)
                
            else:
                st.error("ごめん、分からへん。その人有名ちゃうやろ？")

if __name__ == "__main__":
    main()