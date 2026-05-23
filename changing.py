import streamlit as st
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="내신 등급 변환 계산기", page_icon="📊", layout="centered")

# 데이터 정의 (각 등급별 상위 누적 비율 %)
# 9등급제 누적 비율: 1등(4), 2등(11), 3등(23), 4등(40), 5등(60), 6등(77), 7등(89), 8등(96), 9등(100)
grades_9 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
cum_pct_9 = np.array([4.0, 11.0, 23.0, 40.0, 60.0, 77.0, 89.0, 96.0, 100.0])

# 5등급제 누적 비율: 1등(10), 2등(34), 3등(66), 4등(90), 5등(100)
grades_5 = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
cum_pct_5 = np.array([10.0, 34.0, 66.0, 90.0, 100.0])

# --- 앱 타이틀 ---
st.title("📊 내신 등급 변환 계산기")
st.markdown("##### 간편한 (9등급제 ↔ 5등급제) 누적 비율 + 등급 변환")
st.write("---")

# --- 모드 선택 위젯 ---
mode = st.radio(
    "변환 방식을 선택하세요",
    ["9등급제 ➡️ 5등급제", "5등급제 ➡️ 9등급제"],
    index=0,
    horizontal=True
)

st.write("")

# --- 변환 로직 및 UI ---
if mode == "9등급제 ➡️ 5등급제":
    st.subheader("9등급제를 5등급제로 변환")

    # 1.0 ~ 9.0 입력 (소수점 첫째자리까지 정밀 조절 가능)
    input_grade = st.number_input(
        "9등급제 등급 입력 (1.0 ~ 9.0)",
        min_value=1.0,
        max_value=9.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    if st.button("변환하기", type="primary"):
        # 1. 입력된 9등급이 상위 몇 %에 해당하는지 보간(Interpolation)
        # 등급이 낮아질수록(숫자가 커질수록) 누적 %가 커지므로 interp 함수 사용 시 주의
        pct = np.interp(input_grade, grades_9, cum_pct_9)

        # 2. 해당 누적 %가 5등급제 기준 몇 등급에 해당하는지 역산
        converted_grade = np.interp(pct, cum_pct_5, grades_5)

        # 결과 출력
        st.success(f"🎉 변환 완료!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="입력 (9등급제)", value=f"{input_grade} 등급")
        with col2:
            st.metric(label="출력 (5등급제)", value=f"{converted_grade:.2f} 등급")

        st.info(f"💡 해당 등급의 예상 상위 누적 비율은 약 **{pct:.1f}%** 입니다.")

else:
    st.subheader("5등급제를 9등급제로 변환")

    # 1.0 ~ 5.0 입력
    input_grade = st.number_input(
        "5등급제 등급 입력 (1.0 ~ 5.0)",
        min_value=1.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    if st.button("변환하기", type="primary"):
        # 1. 입력된 5등급이 상위 몇 %에 해당하는지 보간
        pct = np.interp(input_grade, grades_5, cum_pct_5)

        # 2. 해당 누적 %가 9등급제 기준 몇 등급에 해당하는지 역산
        converted_grade = np.interp(pct, cum_pct_9, grades_9)

        # 결과 출력
        st.success(f"🎉 변환 완료!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="입력 (5등급제)", value=f"{input_grade} 등급")
        with col2:
            st.metric(label="출력 (9등급제 예상)", value=f"{converted_grade:.2f} 등급")

        st.info(f"💡 해당 등급의 예상 상위 누적 비율은 약 **{pct:.1f}%** 입니다.")

# --- 하단 안내 메세지 ---
st.write("---")
with st.expander("📌 등급 변환 기준표 확인하기"):
    st.markdown("""
    | 등급 | 9등급제 비율 (누적) | 5등급제 비율 (누적) |
    | :---: | :---: | :---: |
    | **1등급** | 4% (4%) | 10% (10%) |
    | **2등급** | 7% (11%) | 24% (34%) |
    | **3등급** | 12% (23%) | 32% (66%) |
    | **4등급** | 17% (40%) | 24% (90%) |
    | **5등급** | 20% (60%) | 10% (100%) |
    | **6등급** | 17% (77%) | - |
    | **7등급** | 12% (89%) | - |
    | **8등급** | 7% (96%) | - |
    | **9등급** | 4% (100%) | - |
    """)