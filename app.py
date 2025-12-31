import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def get_birth_year(name):
    """
    指定された有名人の名前からWikipediaのInfoboxを解析し、誕生年を返す。
    """
    url = f"https://ja.wikipedia.org/wiki/{name}"
    
    # 【重要】ブラウザのふりをするためのヘッダー
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # headersを指定してアクセス
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            # サーバーログ用にprintは残しつつ、Noneを返す
            print(f"エラー: アクセスできませんでした (Status: {response.status_code})")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Infobox（基本情報テーブル）を探す
        infobox = soup.find('table', class_='infobox')

        # class='infobox'がない場合のフォールバック（一般的な表から探す）
        if not infobox:
            tables = soup.find_all('table')
            for table in tables:
                # 表全体のテキストを取得して判定
                text = table.get_text()
                # main.pyと同じキーワード条件
                if '生誕' in text or '生年月日' in text or '出生' in text or '生まれ' in text or '誕生' in text:
                    infobox = table
                    break
        
        if not infobox:
            print("エラー: 基本情報（Infobox）が見つかりませんでした")
            return None

        # Infobox内の行を走査してキーワードを探す
        for row in infobox.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            
            if header and data:
                header_text = header.get_text().strip()
                
                # main.pyと同じキーワード条件
                if "生誕" in header_text or "生年月日" in header_text or "出生" in header_text or "生まれ" in header_text or "誕生" in header_text:
                    data_text = data.get_text()
                    
                    # main.pyと同じ正規表現: 1桁～4桁の数字＋年
                    matches = re.findall(r'([0-9]{1,4})年', data_text)
                    
                    if matches:
                        # 文字列を数値に変換
                        years = [int(y) for y in matches]
                        valid_years = [y for y in years if y < 2100]
                        
                        if valid_years:
                            # 最も大きい数字を西暦とみなす
                            return max(valid_years)

        print("エラー: 表の中に『年』が見つかりませんでした")

    except Exception as e:
        print(f"予期せぬエラー: {e}")
        pass
        
    return None

def get_zodiac(year):
    """
    西暦から干支（文字）を計算して返す。
    """
    eto_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 紀元後4年が「子年」の基準
    index = (year - 4) % 12
    return eto_list[index]

# --- ここからがStreamlit用の画面処理 ---

def main():
    # タイトル表示 (print "===..." に対応)
    st.title("あの人の干支が知りたい")

    # 入力フォーム (input() に対応)
    name = st.text_input("干支が知りたい有名人の名前を入れてください: ")

    # ボタンが押されたら実行
    if st.button("調べる"):
        # 空欄チェック
        if not name:
            st.warning("名前を入力してください")
        else:
            # 処理中表示（任意ですが、UXのため追加）
            with st.spinner("検索中..."):
                year = get_birth_year(name)

            if year:
                zodiac = get_zodiac(year)
                
                # main.pyの出力形式（点線など）を再現して表示
                # st.text は等幅フォントでそのまま表示するため再現性が高いです
                output_text = f"""
-----------------------------
{name} さんの生まれ年は {year}年 です
{name} さんは  {zodiac}  年です！
-----------------------------
                """
                st.text(output_text)
                
                # （参考）Streamlitらしいリッチな表示もあわせて出すならこちら
                # st.success(f"{name} さんの生まれ年は {year}年 です")
                # st.info(f"{name} さんは {zodiac} 年です！")
                
            else:
                # エラーメッセージ (print "ごめん..." に対応)
                st.error("ごめん、分からへん。その人有名ちゃうやろ？")

if __name__ == "__main__":
    main()