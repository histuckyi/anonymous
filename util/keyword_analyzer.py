from pynori.korean_analyzer import KoreanAnalyzer


class KeywordAnalyzer:
    none_tag = ["NNG", "NNP", "NNB", "NR", "NP"]
    stop_tags = ["MM", "MAG", "MAJ",
                 "IC", "JKS", "JKC", "JKG", "JKO", "JKB", "JKB", "JKQ", "JX", "JC",
                 "EP", "EF", "EC", "ETN", "ETM",
                 "XPN", "XSN", "XSV", "XSA",
                 "XR",
                 "VV", "VCP", "VX",
                 "SF", "SE", "SS", "SP", "SO", "SW"]
    analyzer = KoreanAnalyzer(
           decompound_mode='MIXED', # DISCARD(서브단어) or MIXED(원형과 서브단어) or NONE어(원형)  복합명사
           infl_decompound_mode='MIXED', # DISCARD or MIXED or NONE  굴절
           discard_punctuation=True,
           output_unknown_unigrams=False,  # 언논 단어를 음절 단위로 쪼갬 여부
           pos_filter=True, stop_tags=stop_tags,
           synonym_filter=False, mode_synonym='NORM' # NORM or EXTENSION, 동의어 필터링 실행 여부
       )

    def extract_keyword(self, text):
        return self.analyzer.do_analysis(text)
