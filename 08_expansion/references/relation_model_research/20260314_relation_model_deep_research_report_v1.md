Role: 어휘탐색 UX 리서치 아키텍트

# 한국어 학습자용 어휘 탐색 서비스의 Relation Model 재설계를 위한 비교 연구

## Executive summary

학습자용 사전/서비스에서 “related words”는 분류(카테고리) 중심 목록이 아니라, 동일 장면에서 학습자가 수행해야 하는 과업(이해·선택·대체·생산)을 직접 단축시키는 “동시 제시 묶음”으로 운영되는 경향이 강하다. citeturn18view4turn0search19turn21view1turn0search3  
영어 learner’s dictionary 계열의 thesaurus는 유의어를 “대체 가능”으로만 묶지 않고, 근접 유의어 간 차이를 설명과 예문으로 분해해 “비교/선택” 과업을 전면에 둔다. citeturn18view4  
collocation 계열 기능은 “무엇이 함께 쓰이는가(결합)”를 클릭·탐색으로 전개해, 번역이나 정의만으로는 해결되지 않는 “자연스러운 생산(말하기/쓰기)”을 목표로 설계된다. citeturn0search19turn35view0turn0search24  
“cross-link / jump / see also”는 현재 단어에서 다음 학습 단계로 이동시키는 내비게이션 장치로서, see/see also/compare/more at 같은 링크 타입으로 의미 분화·관용구 위치 이동·비교 구도 전환을 수행한다. citeturn25view0  
entity["organization","국립국어원","south korea language institute"]의 entity["book","한국어기초사전","nikl web learner dict"]/entity["book","한국어-영어 학습사전","nikl bilingualised web"]은 “관련어”, “문법·표현”, “활용형”, “관용구·속담”을 포함하고, “주제 및 상황 범주별 찾기”로 생활 장면(시간·날짜·요일·날씨/계절·약속 등) 기반 탐색을 공식 기능으로 제공한다. citeturn21view1turn21view3turn9search11turn12search1turn23view0turn0search3  
시간/요일/계절/시점 같은 구조 어휘는 “calendar-like anchor(주·월·연, 요일)”와 “temporal grammar anchor(부터/까지, -ㄴ/은 지, 무렵 등)”가 결합될 때 실제 장면(일정 잡기, 마감, 영업시간, 날씨 계획)으로 전이되며, 테마/상황 허브는 그 전이를 단축하는 UX 패턴이다. citeturn9search11turn15search3turn13search4turn10search1turn13search6turn9search9  
이중언어 학습자에게 번역은 decoding(읽기·듣기 해독)에는 유용하지만 encoding(말하기·쓰기 생산)에서는 문법·결합·용례 차이를 가리면서 오류를 유발할 수 있고, 연구는 bilingualised(정의+예문+번역) 형식의 상대적 효율성과 동시에 “정보 오해/번역 유사구조의 함정”을 보고한다. citeturn33view0turn34view0turn30view0  
따라서 relation 모델은 (a) related=“같은 장면에서 같이 보여줄 이유(동시 제시 계약)”와 (b) cross-link=“다음 이동이 학습 효율을 높이는 이유(이동 계약)”를 분리하고, edge에 과업(role)·scope(lemma/sense)·제약(constraints)·근거(evidence)를 명시하는 최소 스키마가 핵심이다. citeturn25view0turn28view0turn30view0turn23view0  

## Source table

| source name | url | type | relevant feature | direct implication for our service |
|---|---|---|---|
| 한국어기초사전 안내 소책자(국문) | `https://www.korean.go.kr/common/download.do?...pdf` | official help (pdf) | 5만 어휘, 쉬운 뜻풀이·생활 예문, 멀티미디어, “관련어 정보”, “문법·표현/활용형/관용구·속담” 포함을 명시. citeturn21view1turn21view3turn21view2 | relation의 1차 목적을 “학습 정보 연결”로 정의하고, 관련어/문법/표현/활용형을 동일 그래프에서 연결 가능한 노드로 취급해야 함. related/cross-link 모두 “학습 정보 연결”이라는 상위 계약 하에 설계 가능. citeturn21view1turn21view3 |
| “외국어 학습사전 편찬 경과와 의의” | `https://www.korean.go.kr/nkview/nklife/2016_4/26_0408.pdf` | research / official paper (pdf) | 한-외 학습사전이 기초사전의 “예문, 관련어, 문형, 멀티미디어”를 공유한다고 명시. citeturn23view0turn23view1turn23view2 | relation edge는 “언어별 번역”과 독립적으로 재사용되도록 분리 저장(언어별 share)하는 것이 정합적. “문형(패턴)”을 relation의 핵심 타입으로 포함해야 함. citeturn23view0turn23view2 |
| 한국어-영어 학습사전 Help | `https://krdict.korean.go.kr/m/eng/help` | official help | bilingualised dictionary(기초사전 번역), “connection among all information” 및 theme/situation 분류 제공을 명시. citeturn12search1 | cross-link는 “all information connection”을 전제로, sense·예문·관용구·상황 허브·번역을 모두 점프 대상으로 설계 가능. citeturn12search1 |
| 국립국어원 사업 소개 영상(외국어 학습사전 사용 설명) | `https://korean.go.kr/front/board/boardMovieView.do?...` | official help (video page) | “반대말, 높임말, 낮춤말, 참고어” 등 관계 정보를 함께 본다고 설명. citeturn0search3 | 한국어 학습 맥락에서 related words의 핵심 축에 “존대/낮춤(사회언어학적 변이)”를 포함해야 함. citeturn0search3 |
| 한국어기초사전 ‘주제 및 상황 범주별 찾기’ 화면 | `https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=83940` | official dictionary feature | “시간 표현하기/날짜 표현하기/요일 표현하기/날씨와 계절/약속하기” 등 장면 허브 탐색을 제공. citeturn9search11 | 시간·요일·계절은 개별 표제어 related 목록만으로는 불충분하고, “상황 허브→필수 문법/표현→핵심 어휘”의 다단 점프가 학습 효율이 큼. citeturn9search11 |
| 한국어기초사전 OpenAPI(주제·상황 코드 노출) | `https://krdict.korean.go.kr/spa/openApi/openApiInfo` | official help / API | “시간/날짜/요일/날씨·계절” 등 주제·상황 코드가 명시적으로 정의됨. citeturn9search15 | 서비스 relation 데이터에 “scene/topic id”를 1급 필드로 두면, 사전·API 기반 확장과 정합성이 높음. citeturn9search15 |
| 누리-세종학당 Vocabulary Dictionary | `https://nuri.iksi.or.kr/front/cms/contents/layout2/learningdictionary/contentsList.do` | official service | “Korean Basic Vocabulary Learning Dictionary(English Edition)” 등 학습자용 어휘 사전 콘텐츠를 운영. citeturn1search0 | 한국어 학습자 사전(특히 KR-EN)에서도 “주제별/학습용” 패키지 사전이 별도 운영됨. 서비스에서 topic hub(장면)을 relation의 상위 단위로 두는 근거. citeturn1search0 |
| 한국어 기초어휘 학습사전(영어판) 서지 | `https://nuri.iksi.or.kr/library/search/detail/CATEKZ000000002423?...` | official service / library record | 발행정보(2020), 영어판, KSIF 교재로 등록. citeturn1search22 | “학습용 어휘 사전”은 표제어 관계를 ‘수업/주제 묶음’ 단위로 편성하는 경우가 많으므로, word→topic, topic→word의 양방향 relation이 필요. citeturn1search22 |
| Cambridge Dictionary(홈) | `https://dictionary.cambridge.org/` | official dictionary/service | learner’s dictionary + grammar + thesaurus를 동일 플랫폼에서 제공. citeturn0search2 | “definition 중심(해독)”과 “thesaurus/grammar 중심(생산·정확성)”을 한 entry에서 분기시키는 cross-link 설계가 표준 패턴. citeturn0search2 |
| Cambridge Thesaurus(설명 페이지) | `https://dictionary.cambridge.org/thesaurus/` | official dictionary feature | near-synonym 차이를 “설명+예문”으로 제공, corpus 기반을 명시. citeturn18view4 | related words를 “유의어 리스트”가 아니라 “선택 과업을 완결시키는 비교 카드(차이/문체/용례)”로 설계해야 함. citeturn18view4 |
| Cambridge Collocations(예시 페이지) | `https://dictionary.cambridge.org/collocation/english/screen` | official dictionary feature | collocation 목록에서 “클릭→추가 예문” 탐색을 유도. citeturn0search24 | collocation은 related(동시 제시)와 cross-link(예문 탐색 점프)가 결합된 복합 위젯이 효과적. citeturn0search24 |
| Oxford Learner’s Dictionaries(홈) | `https://www.oxfordlearnersdictionaries.com/` | official dictionary/service | learner 대상 정의·예문·synonyms 등을 제공하는 학습 사전 플랫폼임을 명시. citeturn16search32 | “entry 기본(정의/예문)” 위에 relation 위젯을 층형으로 얹는 정보 구조가 정합적. citeturn16search32 |
| Oxford Collocations Dictionary 소개 | `https://www.oxfordlearnersdictionaries.com/about/collocations/introduction.html` | official help | collocations dictionary가 ‘need-to-know basis’로 collocational competence를 키운다고 설명. citeturn0search19 | related words의 핵심 역할에 “결합(생산)”을 포함하고, UI는 “이미 아는 단어→필요한 결합만 확장” 흐름을 지원해야 함. citeturn0search19 |
| Oxford 표식/라벨 가이드(크로스레퍼런스 표식) | `https://www.oxfordlearnersdictionaries.com/about/english/labels` | official help | cross reference 화살표 표식이 관련 entry로 이동함을 설명. citeturn17search1 | “jump type”을 UI 라벨/아이콘으로 구분하면 학습자가 ‘왜 이동하는지’를 즉시 이해. jump taxonomy를 데이터로 먼저 정의해야 함. citeturn17search1 |
| OALD cross-reference 형태 분석(학술) | `https://globalex.link/wp-content/uploads/2019/08/Lexicon-31_001.pdf` | research (pdf) | see/see also/compare/more at 및 [SYN]/[OPP] 등 다양한 cross reference 형식을 보고. citeturn25view0 | cross-link를 단일 타입(see also)으로 뭉개면 “이동 목적”이 불명확해진다. 데이터에서 jump 목적을 분리 인코딩해야 함. citeturn25view0 |
| British Council: Dictionaries, Lexicography and Language Learning | `https://www.teachingenglish.org.uk/sites/teacheng/files/pub_F044%20ELT-32%20...pdf` | research / institutional (pdf) | learner dictionaries가 sentence pattern 목록과 그것으로의 cross reference를 제공해 문법-어휘 경계에서 학습을 돕는다고 서술. citeturn28view0 | 한국어에서 “문법 anchor”를 cross-link 1급 시민으로 취급해야 함(품사/활용/문형/조사). citeturn28view0 |
| Euralex 1994 controlled study(사전 유형 비교) | `https://euralex.org/elx_proceedings/Euralex1994/...pdf` | research (pdf) | bilingualised(정의+예문+번역) 사용 시 점수 우세 경향, 숙련도별로 활용 방식이 다름. citeturn33view0turn32view0 | 번역만 제공하는 relation(단순 대응)으로는 생산 과업에서 부족해지며, 정의/예문/제약을 함께 엮는 relation이 필요. 동시에 UI는 숙련도별로 “번역 의존”을 흡수하도록 단계적 노출이 필요. citeturn33view0 |
| Lexikos 2017: bilingualized dictionary의 함정(문법) | `https://www.scielo.org.za/scielo.php?pid=S2224-00392017000100008&script=sci_arttext` | research (journal) | 번역이 encoding 오류의 원인이 될 수 있고, 사용자들이 사전 정보를 오해해 부적절 구조를 모방한다고 보고. citeturn34view0 | bilingual learner에게는 “번역 관계” 외에 “문법 제약/구조 차이/사용 문맥”을 relation로 명시해야 함. citeturn34view0 |
| Collocation tool 연구(OUP IJL) | `https://academic.oup.com/ijl/article/30/4/454/2555491` | research (journal) | 온라인 collocation 도구가 정확한 collocation 생산에 기여, “탐색이 쉬움”이 선호 요인으로 보고. citeturn35view0 | cross-link 설계에서 “다음 클릭이 정답 결합을 찾기 쉬운가”를 핵심 KPI로 둘 수 있음(탐색 비용 최소화). citeturn35view0 |
| LMF(다언어 관계·제약·라벨) | `https://aclanthology.org/W06-1001.pdf` | research / standardization (pdf) | sense axis relation 등이 label/variation/comment 같은 속성으로 관계 의미를 부여하고, 번역에 조건/제약을 표현해야 함을 서술. citeturn30view0turn30view1 | relation edge에 “라벨(관계 의미) + 변이(언어/레지스터/조건) + 제약”을 필드로 두는 것이 표준화 흐름과 정합. citeturn30view0turn30view1 |

## Related words model synthesis

### Role taxonomy

“related words”를 “같은 화면에서 같이 보여줄 이유”로 재정의하면, 분류 기준이 아니라 학습 과업(role) 기준의 taxonomy가 안정적으로 나온다. Cambridge Thesaurus가 near-synonym의 차이를 설명·예문으로 제공하는 구조는 “비교/선택(role)”을 전면에 둔 전형이다. citeturn18view4  

| role(학습 과업) | related words가 해결하는 문제 | relation types(예시) | learner-facing 운영 방식(근거) | design implication |
|---|---|---|---|---|
| 비교·선택·대체 | “비슷한데 뭐가 다른가/어떤 게 맞는가” | near-synonym set, confusables, paraphrase | thesaurus가 차이를 설명하고 예문을 제공해 “선택 과업”을 완결. citeturn18view4 | related 위젯은 “리스트”가 아니라 “비교 카드(차이 축)”가 되어야 함(의미·문체·결합·빈도·제약). |
| 대조·경계 설정 | 의미 경계가 흐릿해 오용 | antonym, contrast pair, scalar set | 사전/학습사전이 [OPP]/반대말 관계를 cross reference로 운영. citeturn25view0turn0search3 | antonym은 단순 반대가 아니라 “대조 축(형용사 스케일, 시간 범위 시작/끝)”로 묶어야 학습 전이 증가. |
| 결합·생산 | 번역은 아는데 “어떻게 붙이나” | collocation set, subcat frame, particle pairing | collocations 사전은 ‘need-to-know’ 기반으로 결합 능력을 구축. citeturn0search19 | related 위젯에 결합을 넣되, 상위는 “자주 쓰는 결합 5~10개”로 절제하고 나머지는 점프로 확장. |
| 문법-어휘 경계 | 단어 의미는 이해했는데 문형이 틀림 | sentence pattern set, grammar anchor list | learner dictionaries는 sentence pattern 목록과 그에 대한 cross reference를 제공. citeturn28view0 | 한국어는 조사/어미/문형이 생산 오류의 핵심이므로, related 안에 “대표 문형 1~3개”를 기본 포함. |
| 장면 확장 | 단어가 장면에서 고립됨 | topic cluster, scene lexicon | 한국어기초사전은 ‘시간/요일/약속/날씨·계절’ 등 주제·상황 허브로 제공. citeturn9search11turn9search15 | word page에 “이 단어가 자주 등장하는 장면 카드”를 related로 둬야 함(예: ‘약속하기’). |
| 사회언어학적 변이 | 같은 뜻인데 높임/낮춤/문체가 다름 | honorific pair, speech level variants | 학습사전 기능 설명에서 높임말/낮춤말 등 관계 제공을 명시. citeturn0search3 | 한국어 서비스에서 related의 1급 축: 높임/낮춤, 구어/문어, 공손도(상황별). |

### Good examples

한국어 학습사전 계열은 표제어 안에 관련어·문법·표현·활용형을 포함시키는 것을 “학습용”의 차별점으로 공표한다. citeturn21view1turn21view3turn23view1  
한국어기초사전이 “주제 및 상황 범주별 찾기”로 시간·날짜·요일·날씨/계절을 분리해 제공하는 구조는 “구조 어휘를 장면 허브로 묶는 related 접근”의 공식 사례다. citeturn9search11turn9search15  
영어 학습자 thesaurus는 near-synonym을 한 덩어리로 묶되 “차이 설명+예문”을 통해 비교·대체 과업을 완결시키므로, 같은 방식으로 한국어에서도 ‘비슷한 말’은 “대체 가능 여부/제약”을 같이 제공해야 한다. citeturn18view4turn34view0  
collocation 지원은 “결합을 first-class로 보여주고, 클릭으로 예문/세부를 확장”하는 패턴이 학습자 생산에 기여한다(탐색이 쉬울수록 선호). citeturn0search24turn35view0  

### Design cautions

유의어/관련어를 sense를 가리지 않고 lemma 단위로만 노출하면, “다의어의 다른 의미”가 섞여 비교 과업이 실패한다는 위험이 크고, learner dictionary 전통은 이를 cross reference(see/compare 등)로 분리 운영해 왔다. citeturn25view0turn34view0  
번역 대응어를 related로 전면 배치하면 decoding에는 도움이나 encoding에서 “번역 유사구조를 그대로 모방”하는 오류가 강화될 수 있다. citeturn34view0turn33view0turn30view0  
related는 “같은 장면에서 같이 보여줘야 하는가”를 통과한 소수만 남기고, 나머지는 cross-link로 넘기는 분리가 정보 과밀을 줄인다(‘need-to-know’ 원칙). citeturn0search19turn35view0  

## Cross-link model synthesis

### Jump taxonomy

cross-link를 “현재 단어를 본 뒤 다음에 어디로 이동해야 학습 효율이 커지는가”로 정의하면, 링크의 목적이 곧 taxonomy가 된다. OALD 분석은 see/see also/compare/more at, [SYN]/[OPP] 같은 다양한 cross reference 형식이 존재함을 보여주며, 이는 “이동 목적을 텍스트로 인코딩”해 온 역사적 증거다. citeturn25view0  

| jump 목적(Next best move) | 학습자 다음 과업 | 대표 표현 | 근거가 되는 운영 사례 | cross-link 설계 규칙(서비스 적용) |
|---|---|---|---|---|
| sense disambiguation | “지금 의미가 맞는가” 확인 | compare, which word, see also(sense) | 다양한 cross reference(see/compare 등)로 항목 간 연결. citeturn25view0 | edge에 `scope=sense`와 `disambiguation hint`를 필수로 둬야 함. 번역 링크도 sense-gated. citeturn30view0turn34view0 |
| idiom/phrase relocation | “관용구/연어로 확장” | more at, idioms tab | 학습사전이 관용구·속담을 검색/탭으로 분리 제공. citeturn12search1turn21view3 | 단어→관용구는 related(요약) + jump(전체 목록) 이원화. |
| collocation expansion | “자연스러운 결합 찾기” | collocations → examples | collocation 페이지에서 클릭해 예문 확장. citeturn0search24turn35view0 | jump는 “정답 결합에 도달하는 클릭 수” 최소화. 결합 직후 예문까지 한 번에 노출. citeturn35view0 |
| grammar/pattern anchoring | “어떤 문형/조사/어미와 쓰나” | pattern ref, grammar note | sentence patterns와 cross reference 제공이 learner dictionary의 핵심 기능으로 서술. citeturn28view0 | word→pattern 점프를 1급으로 모델링. pattern 노드에 예문·제약·대체 패턴을 포함. citeturn30view1 |
| scene/topic move | “같은 장면에서 필요한 어휘 확장” | topic index, situation hub | 시간/요일/날씨·계절/약속 등 상황 범주 탐색 제공. citeturn9search11turn9search15 | word→scene hub, scene hub→(필수 문법/필수 어휘) 점프를 표준화. |
| sociopragmatic move | “공손/문체 맞추기” | honorific variant link | 높임말/낮춤말/참고어 등 관계 정보를 함께 제공. citeturn0search3 | ‘상황(대상·관계)’을 조건으로 갖는 conditional jump 필요(예: 손윗사람/공식). |

### Good examples

한국어-영어 학습사전 help는 “all information connection”을 명시하며, 이는 cross-link를 단순 ‘see also’가 아니라 “탭/분기(예문·뜻풀이·관용구·용례)”까지 포함하는 통합 내비게이션으로 운영할 수 있음을 시사한다. citeturn12search1  
한국어기초사전은 “주제 및 상황 범주별 찾기”에서 시간·요일·날씨·계절 같은 구조 영역을 독립 허브로 제공하므로, word→hub 점프가 이미 공식 UX로 검증된 형태다. citeturn9search11turn9search15  
영어 쪽에서 collocation tool 연구는 “탐색이 쉬울수록 올바른 collocation을 찾는다”는 결과를 보고하므로, 한국어에서도 “결합/문형” 점프는 설명보다 탐색 비용을 먼저 최적화해야 한다. citeturn35view0  

### Design cautions

cross-link가 “이동 목적”을 UI/라벨로 드러내지 않으면, 학습자는 링크를 연쇄 클릭하다가 현재 과업(예: ‘약속 잡기 문장 만들기’)을 잃는다. Oxford는 cross reference 표식을 라벨로 암시하는 구조를 운영한다. citeturn17search1turn25view0  
관용구를 “more at” 형태로 숨기는 방식은 user-friendly를 저해할 수 있다는 지적이 있으며, 이는 “어디로 이동해야 하는가”가 명시되지 않을 때 발생하는 탐색 실패의 구체 사례다. citeturn25view0  
bilingualised 정보는 유익하지만 학습자가 사전 정보를 오해하거나 번역을 구조 모델로 삼아 오류를 고착시킬 수 있으므로, cross-link는 “번역→(문형/제약/예문)”으로 강제 분기되는 안전장치가 필요하다. citeturn34view0turn33view0  

## Time anchor와 Grammar anchor

### What learners need

시간/요일/계절/시점 어휘는 개별 표제어의 뜻풀이보다 “시간을 문장에 붙이는 장치(조사·문형)”와 “장면(약속/마감/영업/수업)”이 동시에 있어야 학습이 완료된다. 한국어기초사전이 시간·날짜·요일·날씨·계절을 별도 상황 범주로 제공하는 것은 이 요구를 전제로 한 설계다. citeturn9search11turn9search15  
temporal grammar anchor는 (a) 범위(시작/끝), (b) 경과/기간, (c) 대략, (d) 캘린더 경계(월말/연말)처럼 기능이 명확히 나뉘며, 학습사전은 이를 조사·의존명사·표현 표제어로 수록한다(예: ‘까지’, ‘부터’, ‘-ㄴ/은 지’, ‘무렵’, ‘월말’). citeturn13search4turn15search3turn10search1turn13search6turn9search9  
한국어 학습사전이 “문법·표현/관용구·속담/활용형”까지 표제어로 포함한다는 공식 설명은, time/grammar anchor를 ‘부가 정보’가 아니라 ‘탐색 노드’로 취급해야 함을 뒷받침한다. citeturn21view2turn23view1  
영어 학습 사전 전통에서도 lexis가 grammar로 이어지는 경계에서 sentence patterns와 cross reference가 핵심이라는 서술이 존재하며, 같은 논리로 한국어에서도 조사/문형 앵커 점프가 학습 효율의 중심이 된다. citeturn28view0  

### Recommended jump patterns

다음 패턴은 “현재 단어→다음 이동”을 시간/문법 앵커에 맞춰 정렬한 것이다. 근거 표제어/허브는 한국어기초사전의 범주(시간·요일·날씨·계절·약속)와 학습사전 표제어(조사/의존명사/표현)에서 직접 확인된다. citeturn9search11turn15search3turn13search4turn10search1turn13search6turn9search9  

1) **요일(월요일 등) → ‘약속하기’ 허브 → (부터/까지) 범위 문장 패턴 → 빈출 동사 결합(만나다/있다/열다/쉬다)**  
요일은 캘린더 anchor라서 단독 의미보다 “일정 장면”으로 점프가 먼저 필요하고, 범위 조사(부터/까지)가 ‘시간표 문장’을 완성한다. citeturn9search11turn15search3turn13search4  

2) **주/기간(주일) → (주중/주말/다음 주 같은 캘린더 확장) → ‘-ㄴ/은 지’ 경과 표현(기간 감각) → 예문**  
‘주일’은 월요일~일요일 단위로 정의되어 주간 개념의 허브가 되며, 경과 표현 ‘-ㄴ/은 지’는 “지금까지 얼마나”로 장면(오랜만, 근황)을 확장한다. citeturn9search12turn10search1  

3) **범위 조사(부터/까지) → (전에/후에/무렵) 시점 정밀화 → ‘마감/약속/영업시간’ 장면 허브**  
‘부터/까지’는 범위 뼈대를 만들고, ‘무렵’ 같은 대략 시점 표현은 실제 대화에서 필수다. ‘월말’처럼 캘린더 경계 표제어는 마감/업무 장면으로 곧장 연결된다. citeturn15search3turn13search4turn13search6turn9search9  

4) **계절(봄 등) → ‘날씨와 계절’ 허브 → (원인/결과·체감 표현) 결합 → 문화/생활 단어(황사/방학/옷차림)**  
계절은 장면(날씨, 생활, 행사) 중심의 토픽 확장이 핵심이며, 한국어기초사전이 날씨·계절을 상황 범주로 제공한다. citeturn9search11turn9search15  

5) **대략 시점(무렵) → 동의 표지(-쯤/-경) → 숫자 시각(시/분, 자정 등) → 예문 탐색 점프**  
‘무렵’ entry는 동의 관계를 제공하므로, related(동의 표지)와 jump(예문·시간 숫자)로 분리하는 것이 탐색 비용을 줄인다. citeturn13search6turn35view0  

### Anti-patterns

시간/요일/계절을 related_vocab로만 “같은 범주”로 나열하면, 학습자는 문장을 완성할 수 없고(조사/문형 부재), 다음 이동이 불명확해진다. citeturn28view0turn9search11  
범위/경과/대략 같은 시간 기능을 한 덩어리로 섞으면(예: ‘부터/무렵/월말’ 혼합 리스트), 시간 문장 구성이 실패하고 의미 혼동이 커진다(각 표제어가 다른 기능을 정의). citeturn15search3turn13search6turn9search9  
번역 링크만 제공하면 encoding에서 번역 유사 구조를 그대로 모방하는 오류가 발생할 수 있으므로, time/grammar anchor에는 제약/예문을 동반한 점프가 필요하다. citeturn34view0turn33view0turn30view0  

## Proposed minimum schema

relation 데이터를 “edge(관계)”로 통일하면, related words(동시 제시)와 cross-link(점프)를 동일 데이터 모델로 관리하면서 UI 계약만 분리할 수 있다. 다언어 관계를 다루는 LMF 논의는 relation에 label/variation/condition 및 example 근거를 두는 것이 합리적임을 보여준다. citeturn30view0turn30view1  

### Must-have fields

| field | type | meaning | required 이유(근거) |
|---|---|---|---|
| edge_id | string | 관계 고유 ID | 동일 pair에 복수 관계(role/조건)가 생기므로 필요. citeturn30view1 |
| source_node_id | string | 현재(출발) 노드 | “현재 단어→다음 이동”을 명시하려면 필수. citeturn25view0 |
| target_node_id | string | 도착 노드 | cross reference의 본질. citeturn25view0 |
| node_type_pair | enum | (word/sense/grammar/scene/idiom/etc) | 한국어기초사전이 문법·표현/관용구·속담까지 표제어로 포함. citeturn21view2turn23view1 |
| relation_role | enum | compare / contrast / collocate / pattern / topic / pragmatics 등 | learner task 중심 운영을 위해 1차 분류 필요. citeturn18view4turn0search19turn28view0 |
| relation_type | enum | synonym / antonym / reference / pattern_link / topic_member / example_link 등 | 사전은 see/compare/[SYN]/[OPP]처럼 타입을 분리해 운영. citeturn25view0turn0search3 |
| scope | enum | lemma / sense | sense 혼합이 비교 과업을 깨뜨림. citeturn25view0turn34view0 |
| display_intent | enum | related_widget / jump_link | “같은 화면에서 같이 보여줄 것” vs “이동” 계약 분리. citeturn0search24turn25view0 |
| label_localized | object | UI 라벨(예: ‘비슷한 말’, ‘비교’, ‘문형’) | Oxford가 cross reference 표식을 라벨로 암시. citeturn17search1 |
| constraints | object | 조건(품사, 결합 제약, 시간 기능, 공손도, 레지스터 등) | 번역만으로는 조건 차이가 가려져 encoding 오류가 발생. citeturn34view0turn30view0 |
| evidence | object | 예문/출처/코퍼스 근거(최소 1개) | collocation·pattern은 예문 기반이 학습 효과를 좌우. citeturn35view0turn28view0 |
| provenance | object | 출처(사전명, 편찬/자동생성, 버전) | 한국어-외국어 학습사전이 기초사전 내용을 공유·재사용함을 명시. citeturn23view0turn12search1 |

### Nice-to-have fields

| field | type | meaning | value |
|---|---|---|---|
| priority_score | number | 노출 우선순위 | ‘need-to-know’로 상위 결합만 노출하고 나머지는 점프로 넘김. citeturn0search19turn35view0 |
| proficiency_band | enum | 초/중/고급 등 | 한국어기초사전이 어휘 등급 정보를 제공. citeturn21view3 |
| scene_id | string | 주제·상황 코드 | 주제·상황 분류가 공식 코드로 존재. citeturn9search15 |
| ui_template | enum | compare_card / collocation_strip / timeline / topic_hub 등 | 같은 relation이라도 역할에 따라 위젯이 달라짐. citeturn0search24turn18view4 |
| navigation_cost_hint | object | 클릭 수/예문 바로보기 여부 | “탐색이 쉬움”이 학습자 선호·성과에 영향을 줌. citeturn35view0 |
| bidirectional | boolean | 역방향 자동 생성 여부 | see/see also/compare는 대체로 왕복 탐색을 전제. citeturn25view0 |
| variation | object | 방언/언어권/문체 변이 | 다언어/변이 표현이 relation 속성으로 필요. citeturn30view0turn23view0 |
| safety_notes | object | 번역 함정/오해 가능성 경고 | bilingualized 사용에서 오해·모방 오류가 보고됨. citeturn34view0turn33view0 |

## Decision memo for PM

### Recommend

related words와 cross-link를 하나의 relation graph(edge)로 통합 저장하되, `display_intent`로 “동시 제시(related 위젯)”와 “점프(내비게이션 링크)”를 분리 운영. citeturn25view0turn30view0turn12search1  
relation의 1차 분류를 “학습 과업(role)”로 두고(compare/contrast/collocate/pattern/topic/pragmatics), sense 단위 scope와 constraints/evidence를 의무화. citeturn18view4turn28view0turn34view0  
시간/요일/계절/시점은 word-to-word related를 최소화하고, “상황 허브(시간 표현/요일 표현/약속하기/날씨·계절) → 문법 앵커(부터/까지, -ㄴ/은 지, 무렵 등) → 예문”의 점프 체인으로 기본 UX를 고정. citeturn9search11turn15search3turn13search4turn10search1turn13search6  

### Why

한국어기초사전/한국어-외국어 학습사전은 관련어·문형·멀티미디어 등 “학습 정보 연결”을 공식 기능으로 제시하며, 이는 relation을 그래프 형태로 확장·재사용하는 설계와 정합성이 높다. citeturn21view1turn23view0turn12search1  
영어 learner’s dictionary 전통은 see/compare/[SYN]/[OPP] 등 링크 목적을 다르게 인코딩해 “현재→다음 이동”의 이유를 남겨 왔고, 이는 jump taxonomy를 데이터로 먼저 정의해야 함을 의미한다. citeturn25view0turn17search1  
이중언어 학습에서 번역 단독 제공은 encoding에서 오류를 만들 수 있으며, bilingualised(정의+예문+번역) 결합이 더 나은 성과를 보이기도 하지만 사용자 숙련도·오해 가능성이 함께 보고되므로, constraints/evidence가 붙은 relation이 필요하다. citeturn33view0turn34view0turn30view0  
collocation/pattern 탐색은 “찾기 쉬움”이 성과를 좌우하는 것으로 보고되어, relation edge 자체보다 “탐색 비용”을 줄이는 UI 템플릿·우선순위가 제품 경쟁력으로 연결된다. citeturn35view0turn0search24  

### Risks

sense-scope 없는 related/translation 연결은 다의어 간 혼합을 만들어 비교·대체 과업을 붕괴시킬 수 있다. citeturn25view0turn34view0  
번역 중심 cross-link는 학습자가 번역 구조를 생산 모델로 삼는 오류를 강화할 수 있고, dictionary 정보 오해가 오류 고착으로 이어질 수 있다. citeturn34view0turn33view0  
링크 타입이 “왜 이동하는가”를 드러내지 않으면(라벨/아이콘 부재) 연쇄 점프가 학습 과업을 끊고, 관용구/문형의 위치 탐색이 user-unfriendly가 될 수 있다. citeturn25view0turn17search1  
주제·상황 허브를 도입해도 문법 앵커(조사/문형) 점프가 약하면 시간/요일/계절은 “단어 지식”에서 “문장 생산”으로 전이되지 않는다. citeturn28view0turn9search11turn13search4turn10search1