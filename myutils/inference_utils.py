import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import linspace
from metrics import reward_function
from .kwargs_utils import _make_dict

def inference(env, policy, num=10, save=True, Max=False,more=False, **kwargs):
    """
    주어진 환경과 정책을 사용하여 추론을 수행하는 함수입니다.

    Parameters:
    - env: 추론에 사용할 환경 객체
    - policy: 추론에 사용할 정책 객체
    - num: 추론할 에피소드 수 (기본값: 10)
    - save: 추론 결과를 저장할지 여부 (기본값: True)
    - Max: 최대 보상을 갖는 에피소드의 결과만 반환할지 여부 (기본값: False)

    Returns:
    - 추론 결과로 얻은 위치와 속도 정보를 담은 numpy 배열
    - Max가 True인 경우 최대 보상을 갖는 에피소드의 결과만 반환됩니다.
    """
    re_list = []
    total_pos = np.zeros((num, 1000, 3))  # 에피소드 *걸음수*(x,y,z)
    total_vel = np.zeros((num, 1000, 3))  # 에피소드 *걸음수*(x,y,z) for velocity
    more_reward =_make_dict(**kwargs) if more else None

    for ep in range(num):
        ep_steps = 0
        ep_tot_reward = 0
        ep_com = np.zeros((1000, 3))
        ep_vel = np.zeros((1000, 3))  # for velocity
        
        state = env.reset()
        if save:
            env.store_next_episode()
        while True:
            # 현재 상태의 com 저장
            ep_com[ep_steps] = env.model.com_pos().array()
            # 현재 상태의 velocity 저장
            ep_vel[ep_steps] = env.model.com_vel().array()  # assuming com_vel() method exists
            # samples random action
            action = policy(state)
            # applies action and advances environment by one step
            state, reward, done, info = env.step(action)
            if more:
                temp = reward_function(env.model, env.head_body, **kwargs)
                for key in more_reward:
                    more_reward[key] += temp[key]
            ep_steps += 1
            ep_tot_reward += reward

            # check if done
            if done or (ep_steps >= 1000):
                Epis = f"Episode {ep}: "
                print(
                     f"{Epis}steps={ep_steps}; reward={ep_tot_reward:0.3f}, com={env.model.com_pos()}"
                )
                if more:
                    string = ' '*len(Epis)
                    for key in more_reward:
                        string += f'{key}:{round(more_reward[key],2)}; '
                    print(string)

                if save:
                    env.write_now()
                env.reset()
                re_list.append(ep_tot_reward)
                total_pos[ep] = ep_com
                total_vel[ep] = ep_vel  # add velocity to total_vel
                break

    maxs = np.where(re_list == max(re_list))[0][0]
    print(f'Epis: {maxs + 1},Max_Re:{re_list[maxs]}')
    return (total_pos[maxs] if Max else total_pos, total_vel[maxs] if Max else total_vel)

def plot_3d(com_pos:np.ndarray, com_vel:np.ndarray, Max=False, vector=False, vector_scale=0.1, scatter_size=20):
    """
    3D 그래프로 COM 위치와 속도를 플롯하는 함수입니다.

    Parameters:
    - com_pos: COM 위치 정보를 담은 numpy 배열
    - com_vel: COM 속도 정보를 담은 numpy 배열
    - Max: 최대 보상을 갖는 에피소드의 결과만 플롯할지 여부 (기본값: False)
    - vector: 속도 벡터를 플롯할지 여부 (기본값: False)
    - vector_scale: 속도 벡터의 크기 조정 비율 (기본값: 0.1)
    - scatter_size: scatter plot의 크기 (기본값: 20)
    """
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')

    title = "Max Reward's COM" if Max else "All of COM"
    if Max:
        points = com_pos
        velocities = com_vel[::20]
        ax.scatter(points[:,0], points[:,2], points[:,1], color='b', s=scatter_size)
        if vector:
            ax.quiver(points[::20,0], points[::20,2], points[::20,1], velocities[:,0], velocities[:,2], velocities[:,1], color='r', length=vector_scale)
    else:
        colors = cm.rainbow(linspace(0, 1, len(com_pos)))
        for points, velocities, color in zip(com_pos, com_vel[::20], colors):
            ax.scatter(points[:,0], points[:,2], points[:,1], color=color, s=scatter_size)
            if vector:
                ax.quiver(points[::20,0], points[::20,2], points[::20,1], velocities[:,0], velocities[:,2], velocities[:,1], color=color, length=vector_scale)

    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')
    plt.show()

def plot_2d(com_pos:np.ndarray, com_vel:np.ndarray, Max=False, vector=False, headlength=10, headwidth=3, headaxislength=4.5, scatter_size=20, vector_step=20):
    """
    2D 그래프로 COM 위치와 속도를 플롯하는 함수입니다.

    Parameters:
    - com_pos: COM 위치 정보를 담은 numpy 배열
    - com_vel: COM 속도 정보를 담은 numpy 배열
    - Max: 최대 보상을 갖는 에피소드의 결과만 플롯할지 여부 (기본값: False)
    - vector: 속도 벡터를 플롯할지 여부 (기본값: False)
    - headlength: 화살표 머리의 길이 (기본값: 10)
    - headwidth: 화살표 머리의 너비 (기본값: 3)
    - headaxislength: 화살표 머리의 축 길이 (기본값: 4.5)
    - scatter_size: scatter plot의 크기 (기본값: 20)
    - vector_step: 속도 벡터를 플롯할 때 사용할 간격 (기본값: 20)
    """
    fig, ax = plt.subplots(figsize=(10,10))

    title = "Max Reward's COM" if Max else "All of COM"
    if Max:
        points = com_pos
        velocities = com_vel[::vector_step]
        ax.scatter(points[:,0], points[:,2], color='b', s=scatter_size)
        if vector:
            ax.quiver(points[::vector_step,0], points[::vector_step,2], velocities[:,0], velocities[:,2], color='r', headlength=headlength, headwidth=headwidth, headaxislength=headaxislength)
    else:
        colors = cm.rainbow(linspace(0, 1, len(com_pos)))
        for points, velocities, color in zip(com_pos, com_vel[::vector_step], colors):
            ax.scatter(points[:,0], points[:,2], color=color, s=scatter_size)
            if vector:
                ax.quiver(points[::vector_step,0], points[::vector_step,2], velocities[:,0], velocities[:,2], color=color, headlength=headlength, headwidth=headwidth, headaxislength=headaxislength)

    ax.set_xlabel('X')
    ax.set_ylabel('Z')

    plt.title(title)
    plt.show()

if __name__ =="__main__":
    print("test")
    com_pos, com_vel = np.random.rand(10,1000,3), np.random.rand(10,1000,3)
    plot_3d(com_pos[0], com_vel[0],Max=True)
    plot_2d(com_pos[0], com_vel[0],Max=True, vector=True, vector_scale=30, scatter_size=30, vector_step=50)
