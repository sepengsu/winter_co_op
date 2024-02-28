# DEP-RL based Gait Simulation
![image](https://github.com/sepengsu/winter_co_op/assets/111292354/7864afd8-b14c-470e-b016-cc7f80bbc4ba)

![image](https://github.com/sepengsu/winter_co_op/assets/111292354/cb4b03a8-f517-4304-ac8b-23f5c64770ee)
## 주제: 강화학습 기반 정상인 보행 데이터 생성 
기간: 2023.12.18 - 2024.02.19

<details>
<summary>1. 연구 배경</summary>

Gait Simulation의 방법론은 크게 CMA-ES(Covariance matrix adaptation evolution strategy)와 RL(Reinforcement Learning)이 있다. 이중 환자 보행 simulation과 다양한 환경에도 적용가능한 RL를 사용하고자 하였다. 이와 관련하여 SCONE 제작 연구소에서 발표한 DEP-RL(Differential Extrinsic Plasticity-RL)을 사용하고자 하였다. 하지만 여러 가지 문제점이 있어 이를 해결하는 것을 목표로 연구를 진행하였다.

</details>

<details>
<summary>2. DEP-RL의 baseline 문제점</summary>

DEP-RL은 Musculoskeletal system에서 좋은 성능을 보이고 gait simulation에서 좋은 성능을 보인다. 하지만 크게 3가지 문제점이 있었다.

1. 느린 학습 속도
2. Unstability of trunk: 몸이 좌우로 흔들며 걷는 문제
3. Peak GRF(Ground React Force on foot) 문제

</details>

<details>
<summary>3. 해결 방안</summary>

1. **Customization of body model**  
   H1622 모델에 대하여 Trunk의 좌우 움직임을 제한하기 위하여 2가지 구성요소를 통하여 구현  
   1.1. Joint motor: trunk muscle 보조 torque로 3축 torque 구현  
   1.2. Harness: trunk translation limit를 구현  
   
2. **Customization reward function**  
   Reward function은 두 가지 목적에 대한 수식을 각각 구현하여 목표를 설정하였다.  
   2.1. Balance  
   COM, trunk(상반신의 COM)의 z축 cost 도입  
   좌우 방향으로 몸을 기울이지 않고 걷도록 학습  
   2.2. GRFDelta  
   물리적 의미: Impact  
   Peak GRF 줄이는 역할

</details>

<details>
<summary>4. 연구 결과</summary>

#### 4.1. Custom body model  
![image](https://github.com/sepengsu/winter_co_op/assets/111292354/c9efa7e5-0c36-4274-b486-7e879a6473f6)  

#### 4.2. Combined Model
![image](https://github.com/sepengsu/winter_co_op/assets/111292354/e866ae8b-5343-4737-a7f5-c93ddc87d0f7)  

#### 4.3. 비교
Body model 수정 --> Balance 문제와 Peak GRF 문제 해결  
Custom reward function을 도입--> pelvis tilt의 불안정성 문제 일부 해결  
기존 연구보다 빠른 학습 속도   
![image](https://github.com/sepengsu/winter_co_op/assets/111292354/44a4cdb5-d788-4331-88d6-825f4374a5f6)

</details>
## 사용 라이브러리

- DEP_RL: https://github.com/martius-lab/depRL
- Sconegym: https://github.com/tgeijten/sconegym
